import pytest

from pipeline import append_gap, scrape_play
from pipeline.common import ScrapeError

BASE_RUN = "2026-10-09T06:00:00Z"
GAP_RUN = "2026-10-25T23:59:59Z"
BASE_MANIFEST = {"run_time_utc": BASE_RUN, "settings": {"window_days": 90}}


def review(index, stamp, platform="android", text="useful answer"):
    from tests.test_pipeline import fixture
    row = scrape_play.parse_review(fixture("play")[0], "en")
    row.update(review_id=f"play_{index}", timestamp=stamp, date_utc=stamp[:10], review_text=text)
    if platform == "ios":
        row.update(review_id=f"ios_{index}", platform="ios", country="us", store_lang="")
    return row


BASE = [review(1, "2026-07-20T00:00:00Z"), review(2, "2026-10-08T06:00:00Z"), review(3, "2026-10-07T00:00:00Z", "ios")]
GAP = [
    review(2, "2026-10-08T06:00:00Z", text="edited text"),   # already in base: dropped, base row kept
    review(4, "2026-10-20T10:00:00Z"),                       # gap
    review(5, "2026-09-01T00:00:00Z"),                       # late-arriving, inside base coverage
    review(6, "2026-07-01T00:00:00Z"),                       # before base window start: dropped
    review(7, "2026-10-26T00:00:01Z"),                       # after later run time: dropped
    review(8, "2026-10-21T00:00:00Z", text="   "),           # empty body: dropped
    review(9, "2026-10-22T00:00:00Z", "ios"),                # iOS gap
    review(4, "2026-10-20T10:00:00Z"),                       # duplicate ID within the pull
]


def test_append_keeps_base_and_adds_only_gap_ids():
    result = append_gap.plan(BASE, BASE_MANIFEST, GAP, GAP_RUN)
    assert [r["review_id"] for r in result["added"]] == ["play_4", "ios_9"]
    assert [r["review_id"] for r in result["late"]] == ["play_5"]
    assert result["window_start"] == "2026-07-11T06:00:00Z"
    merged = result["merged"]
    assert len(merged) == 5 and merged == sorted(merged, key=lambda r: (r["timestamp"], r["review_id"]))
    assert next(r for r in merged if r["review_id"] == "play_2")["review_text"] == "useful answer"


def test_append_platform_subset_and_late_opt_in():
    result = append_gap.plan(BASE, BASE_MANIFEST, GAP, GAP_RUN, platforms=("android",), include_late=True)
    assert [r["review_id"] for r in result["added"]] == ["play_4", "play_5"]
    assert not any(r["review_id"] == "ios_9" for r in result["merged"])


def test_append_refuses_to_run_twice_or_backwards():
    with pytest.raises(ScrapeError, match="already appended"):
        append_gap.plan(BASE, BASE_MANIFEST | {"composition": [{"run_time_utc": GAP_RUN}]}, [], GAP_RUN)
    with pytest.raises(ScrapeError, match="after the base"):
        append_gap.plan(BASE, BASE_MANIFEST, [], BASE_RUN)
