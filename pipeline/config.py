from pathlib import Path

PLAY_APP_ID = "ai.perplexity.app.android"
APPSTORE_ID = "1668000334"
PLAY_LANGS = (
    "en", "es", "pt", "fr", "ar", "id", "ru", "de", "ko", "it", "th", "vi", "tr", "ja", "hi",
    "nl", "pl", "sv", "da", "nb", "fi", "cs", "el", "hu", "ro", "uk", "bg", "hr", "sk", "sr",
    "iw", "fa", "ur", "bn", "ta", "te", "mr", "ms", "fil", "zh-TW", "zh-CN", "ca",
)
PLAY_COUNTRY = "us"
APPSTORE_COUNTRIES = (
    "us", "gb", "in", "ca", "au", "de", "fr", "es", "br", "mx",
    "jp", "kr", "id", "sg", "ae",
)
# The published corpus (data/) is the 90-day run of 2026-10-09 plus an Android-only append
# through 2026-10-25T23:59:59Z (pipeline/append_gap.py), so it spans 2026-07-11T06:03:20Z to
# 2026-10-25T23:59:59Z: 106.75 days. Both values are raised so they describe that corpus;
# neither run hit the cap, and no review has ever been sampled out. Runs 1 and 2 used 90 / 20,000.
WINDOW_DAYS = 107
MAX_ROWS = 30_000
SEED = 42
PAGE_SIZE = 200
PAGE_DELAY = 0.5
RETRIES = 3
HTTP_TIMEOUT = (10, 45)
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
COLUMNS = (
    "review_id", "platform", "country", "store_lang", "timestamp", "date_utc", "rating",
    "title", "review_text", "app_version", "thumbs_up", "has_dev_reply",
)

ANNOTATION_MODEL = "claude-haiku-5-5"
ANNOTATION_BATCH_SIZE = 25
ANNOTATION_OUTPUT_TOKENS_PER_REVIEW = 180
ANNOTATION_PRICE_READ_DATE = "2026-10-09"
ANNOTATION_PRICING_URL = "https://platform.claude.com/docs/en/about-claude/pricing"
# USD per million tokens, used by dry runs and explicit --offline-prices runs.
ANNOTATION_ESTIMATE_PRICES = {
    "short": {"input": 0.10, "output": 0.50, "cache_write": 0.125, "cache_read": 0.01},
    "long": {"input": 0.50, "output": 2.50, "cache_write": 0.625, "cache_read": 0.05},
}
ANNOTATION_LONG_PROMPT_THRESHOLD = 100_000
