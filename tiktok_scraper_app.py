import streamlit as st
import pandas as pd

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TT Scout",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

ACTOR_ID = "clockworks/tiktok-scraper"

# ── Indonesia cities list ─────────────────────────────────────────────────────
ID_CITIES = [
    "Jakarta", "Surabaya", "Bandung", "Medan", "Bekasi", "Tangerang",
    "Depok", "Semarang", "Palembang", "Makassar", "South Tangerang",
    "Batam", "Pekanbaru", "Bandar Lampung", "Padang", "Malang",
    "Bogor", "Pontianak", "Yogyakarta", "Denpasar (Bali)", "Balikpapan",
    "Samarinda", "Jambi", "Manado", "Mataram", "Kupang",
    "Ambon", "Jayapura", "Solo", "Cimahi", "Tasikmalaya",
]

# ── Custom CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600;700&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

*, html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif !important;
    background-color: #080808;
    color: #e8e8e8;
    box-sizing: border-box;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #0e0e0e !important;
    border-right: 1px solid #1c1c1c !important;
    min-width: 280px !important;
    max-width: 320px !important;
}
section[data-testid="stSidebar"] > div { padding: 1.2rem 1rem !important; }

/* ── Header ── */
.scout-logo {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.5rem; font-weight: 700;
    color: #fff; letter-spacing: -0.03em;
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 2px;
}
.scout-dot { color: #fe2c55; }
.scout-version {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.58rem; letter-spacing: 0.14em;
    color: #2a2a2a; text-transform: uppercase;
    margin-bottom: 1.2rem;
}
.section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem; letter-spacing: 0.14em;
    color: #333; text-transform: uppercase;
    margin: 14px 0 5px 0;
}

/* ── Range group ── */
.range-group {
    background: #111; border: 1px solid #1c1c1c;
    border-radius: 6px; padding: 10px 12px; margin-bottom: 8px;
}
.range-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem; letter-spacing: 0.12em;
    color: #444; text-transform: uppercase; margin-bottom: 8px;
}

/* ── Metrics ── */
.metrics-strip {
    display: flex; gap: 8px; flex-wrap: wrap;
    margin-bottom: 1.2rem;
}
.m-card {
    flex: 1; min-width: 100px;
    background: #0e0e0e; border: 1px solid #1c1c1c;
    border-radius: 6px; padding: 10px 14px;
}
.m-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.58rem; letter-spacing: 0.1em;
    color: #333; text-transform: uppercase; margin-bottom: 4px;
}
.m-val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.25rem; font-weight: 600; color: #e8e8e8;
}
.m-val.red { color: #fe2c55; }

/* ── Profile cards ── */
.p-card {
    background: #0e0e0e; border: 1px solid #1a1a1a;
    border-radius: 8px; padding: 14px 16px; margin-bottom: 8px;
    transition: border-color 0.15s, transform 0.1s;
}
.p-card:hover { border-color: #fe2c55; transform: translateY(-1px); }
.p-handle {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.9rem; color: #fe2c55; font-weight: 700;
}
.p-name { font-size: 0.8rem; color: #555; margin-bottom: 5px; }
.p-bio {
    font-size: 0.77rem; color: #555; line-height: 1.55;
    border-left: 2px solid #1a1a1a; padding-left: 9px;
    margin: 7px 0; font-style: italic;
}
.p-stats {
    display: flex; gap: 14px; flex-wrap: wrap;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem; margin-top: 9px;
}
.p-stat-label { font-size: 0.56rem; color: #2e2e2e; letter-spacing: 0.1em; display: block; }
.p-stat-val   { color: #ccc; font-size: 0.82rem; }
.kw-chip {
    display: inline-block; background: rgba(254,44,85,0.08);
    border: 1px solid rgba(254,44,85,0.2); color: #fe2c55;
    font-size: 0.62rem; padding: 2px 6px; border-radius: 2px;
    font-family: 'IBM Plex Mono', monospace;
    margin-right: 3px; margin-top: 5px;
}
.verified-badge { color: #25d4d0; font-size: 0.65rem; margin-left: 5px; }

/* ── Empty state ── */
.empty-state {
    text-align: center; padding: 70px 0 50px;
}
.empty-icon { font-size: 2.8rem; margin-bottom: 12px; }
.empty-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem; color: #1e1e1e; margin-bottom: 8px;
    letter-spacing: 0.12em;
}
.empty-hint { font-size: 0.78rem; color: #2a2a2a; line-height: 1.8; }

/* ── Inputs ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea textarea,
.stSelectbox > div > div {
    background: #111 !important; border: 1px solid #1e1e1e !important;
    color: #e8e8e8 !important; border-radius: 4px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: #fe2c55 !important;
    box-shadow: 0 0 0 1px rgba(254,44,85,0.12) !important;
}
.stNumberInput button {
    background: #1a1a1a !important; border: 1px solid #222 !important;
    color: #888 !important;
}

/* ── Buttons ── */
.stButton > button {
    background: #fe2c55 !important; color: #fff !important;
    border: none !important; border-radius: 4px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.72rem !important; letter-spacing: 0.1em !important;
    width: 100%; padding: 0.55rem 1rem !important;
    transition: opacity 0.15s, transform 0.1s !important;
}
.stButton > button:hover { opacity: 0.85 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* ── Download button ── */
.stDownloadButton > button {
    background: #111 !important; color: #888 !important;
    border: 1px solid #1e1e1e !important; border-radius: 4px !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.68rem !important; letter-spacing: 0.08em !important;
    width: 100%; transition: border-color 0.15s !important;
}
.stDownloadButton > button:hover { border-color: #555 !important; color: #ccc !important; }

/* ── Radio ── */
.stRadio > div { gap: 6px !important; }
.stRadio > div > label {
    background: #111 !important; border: 1px solid #1e1e1e !important;
    border-radius: 4px !important; padding: 5px 12px !important;
    font-size: 0.76rem !important; cursor: pointer;
    transition: border-color 0.1s !important;
}
.stRadio > div > label:has(input:checked) {
    border-color: #fe2c55 !important; color: #fe2c55 !important;
}

/* ── Divider ── */
hr { border-color: #141414 !important; margin: 12px 0 !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important; gap: 4px;
    border-bottom: 1px solid #1a1a1a !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; color: #333 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.68rem !important; letter-spacing: 0.1em !important;
    border-radius: 4px 4px 0 0 !important;
    padding: 6px 14px !important;
}
.stTabs [aria-selected="true"] {
    color: #fe2c55 !important;
    border-bottom: 2px solid #fe2c55 !important;
}

/* ── Tooltip / info box ── */
.info-box {
    background: #0e0e0e; border: 1px solid #1c1c1c;
    border-left: 3px solid #fe2c55;
    border-radius: 4px; padding: 8px 12px;
    font-size: 0.74rem; color: #444; line-height: 1.6;
    margin: 8px 0;
}

/* ── Mobile tweaks ── */
@media (max-width: 640px) {
    .metrics-strip { gap: 6px; }
    .m-card { min-width: 80px; padding: 8px 10px; }
    .m-val { font-size: 1rem; }
    section[data-testid="stSidebar"] {
        min-width: 100% !important; max-width: 100% !important;
    }
    .p-stats { gap: 10px; }
}

/* ── Dataframe ── */
.stDataFrame { border: 1px solid #1a1a1a !important; border-radius: 6px !important; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────────────────────────────
def fmt(n):
    try:
        n = int(n or 0)
        if n >= 1_000_000: return f"{n/1_000_000:.1f}M"
        if n >= 1_000:     return f"{n/1_000:.1f}K"
        return str(n)
    except Exception:
        return "—"

def kw_match(text: str, keywords: list) -> list:
    if not keywords or not text:
        return []
    return [k for k in keywords if k.lower() in text.lower()]

def parse_profile(item: dict) -> dict:
    a = item.get("authorMeta") or item.get("author") or {}
    if not isinstance(a, dict):
        a = {}

    handle    = a.get("name") or a.get("uniqueId") or item.get("name") or item.get("uniqueId") or ""
    nickname  = a.get("nickName") or a.get("nickname") or item.get("nickName") or ""
    bio       = a.get("signature") or a.get("description") or item.get("signature") or ""
    followers = int(a.get("fans") or a.get("followerCount") or item.get("fans") or 0)
    following = int(a.get("following") or a.get("followingCount") or item.get("following") or 0)
    likes     = int(a.get("heart") or a.get("heartCount") or item.get("heart") or 0)
    videos    = int(a.get("video") or a.get("videoCount") or item.get("video") or 0)
    verified  = bool(a.get("verified") or item.get("verified") or False)
    caption   = item.get("text") or item.get("desc") or ""

    # Video-level stats (for min views filter)
    play_count    = int(item.get("playCount") or item.get("stats", {}).get("playCount") or 0)
    like_count    = int(item.get("diggCount") or item.get("stats", {}).get("diggCount") or 0)
    share_count   = int(item.get("shareCount") or item.get("stats", {}).get("shareCount") or 0)
    comment_count = int(item.get("commentCount") or item.get("stats", {}).get("commentCount") or 0)

    # Location — TikTok API exposes region/country code and sometimes city
    region = (
        a.get("region") or a.get("country") or
        item.get("authorRegion") or item.get("region") or
        item.get("locationCreated") or ""
    ).upper().strip()
    city = (
        a.get("city") or item.get("city") or item.get("authorCity") or ""
    ).strip().title()
    # Also try to detect Indonesia from bio keywords as fallback
    bio_lower = bio.lower()
    if not region:
        id_hints = ["indonesia", "jakarta", "bandung", "surabaya", "medan",
                    "bali", "yogyakarta", "semarang", "makassar", "depok",
                    "tangerang", "bekasi", "bogor", "palembang", "malang"]
        if any(h in bio_lower for h in id_hints):
            region = "ID"

    return {
        "handle":        handle,
        "nickname":      nickname,
        "bio":           bio,
        "caption":       caption,
        "followers":     followers,
        "following":     following,
        "likes":         likes,
        "videos":        videos,
        "verified":      verified,
        "play_count":    play_count,
        "like_count":    like_count,
        "share_count":   share_count,
        "comment_count": comment_count,
        "region":        region,
        "city":          city,
        "url":           f"https://www.tiktok.com/@{handle}" if handle else "",
    }

def run_scraper(api_token: str, run_input: dict) -> list:
    """
    Uses Apify REST API directly — avoids apify_client SDK Pydantic
    incompatibility with Python 3.14+.
    """
    import requests, time

    BASE = "https://api.apify.com/v2"
    HEADERS = {"Content-Type": "application/json"}
    AUTH = {"token": api_token}

    # 1. Start the actor run
    resp = requests.post(
        f"{BASE}/acts/{ACTOR_ID.replace('/', '~')}/runs",
        params=AUTH,
        headers=HEADERS,
        json=run_input,
        timeout=30,
    )
    if resp.status_code not in (200, 201):
        st.error(f"Apify error {resp.status_code}: {resp.text[:300]}")
        return []

    run_data   = resp.json().get("data", {})
    run_id     = run_data.get("id")
    dataset_id = run_data.get("defaultDatasetId")

    if not run_id:
        st.error("Could not start Apify run. Check your API token.")
        return []

    # 2. Poll until run finishes
    progress   = st.progress(0, text="Waiting for scraper to start…")
    poll_count = 0
    while True:
        time.sleep(5)
        poll_count += 1
        status_resp = requests.get(
            f"{BASE}/actor-runs/{run_id}",
            params=AUTH,
            timeout=15,
        )
        if status_resp.status_code != 200:
            break
        status = status_resp.json().get("data", {}).get("status", "")
        pct    = min(90, poll_count * 5)
        progress.progress(pct, text=f"Scraper running… ({status})")
        if status in ("SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"):
            break
        if poll_count > 120:          # 10-minute hard cap
            st.warning("Timeout waiting for Apify run.")
            break

    progress.progress(100, text="Fetching results…")

    if not dataset_id:
        # Re-fetch run data to get dataset id (sometimes missing on first response)
        run_info   = requests.get(f"{BASE}/actor-runs/{run_id}", params=AUTH, timeout=15)
        dataset_id = run_info.json().get("data", {}).get("defaultDatasetId", "")

    if not dataset_id:
        st.error("Could not retrieve dataset from Apify run.")
        return []

    # 3. Download all items (paginated, 1 000 per page)
    items, offset, limit = [], 0, 1000
    while True:
        items_resp = requests.get(
            f"{BASE}/datasets/{dataset_id}/items",
            params={**AUTH, "offset": offset, "limit": limit, "clean": "true"},
            timeout=60,
        )
        if items_resp.status_code != 200:
            break
        batch = items_resp.json()
        # Response is either a list or {"items": [...]}
        if isinstance(batch, list):
            page = batch
        else:
            page = batch.get("items", [])
        items.extend(page)
        if len(page) < limit:
            break
        offset += limit

    progress.empty()
    return items


# ── Session state defaults ────────────────────────────────────────────────────
if "profiles" not in st.session_state:
    st.session_state.profiles = []
if "raw_count" not in st.session_state:
    st.session_state.raw_count = 0


# ────────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ────────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="scout-logo">TT<span class="scout-dot">●</span>Scout</div>
    <div class="scout-version">TikTok Creator Discovery Tool</div>
    """, unsafe_allow_html=True)

    # ── API Token ────────────────────────────────────────────────────────────
    st.markdown('<div class="section-label">🔑 Apify API Token</div>', unsafe_allow_html=True)
    api_token = st.text_input(
        "token", type="password",
        placeholder="apify_api_xxxx…",
        label_visibility="collapsed",
    )

    st.markdown("---")

    # ── Search Mode ──────────────────────────────────────────────────────────
    st.markdown('<div class="section-label">🔍 Search Mode</div>', unsafe_allow_html=True)
    mode = st.radio("mode",
                    ["Hashtag", "Profile usernames", "Search query"],
                    label_visibility="collapsed")

    if mode == "Hashtag":
        st.markdown('<div class="section-label">Hashtags (one per line)</div>', unsafe_allow_html=True)
        hashtags_raw = st.text_area("ht", placeholder="#fyp\n#beauty\n#skincare",
                                    height=90, label_visibility="collapsed")
    elif mode == "Profile usernames":
        st.markdown('<div class="section-label">Usernames (one per line)</div>', unsafe_allow_html=True)
        usernames_raw = st.text_area("un", placeholder="@keishadayang\n@andreazshow",
                                     height=90, label_visibility="collapsed")
    else:
        st.markdown('<div class="section-label">Search Query</div>', unsafe_allow_html=True)
        search_query = st.text_input("sq", placeholder="beauty review indonesia",
                                     label_visibility="collapsed")

    st.markdown("---")

    # ── Fetch Limit (API cost control) ───────────────────────────────────────
    st.markdown('<div class="section-label">⚡ Fetch Limit (API Cost Control)</div>', unsafe_allow_html=True)
    st.markdown("""<div class="info-box">
    Fewer videos = lower Apify cost. Start small (50–100) to test, scale up when needed.
    </div>""", unsafe_allow_html=True)
    num_videos = st.number_input("Videos to fetch per input",
                                 min_value=10, max_value=2000, value=100, step=10,
                                 label_visibility="visible")

    st.markdown("---")

    # ── Follower Filter ───────────────────────────────────────────────────────
    st.markdown('<div class="section-label">👥 Follower Range</div>', unsafe_allow_html=True)
    col_min, col_max = st.columns(2)
    with col_min:
        st.caption("Min")
        min_followers = st.number_input("min_f", min_value=0, value=10_000,
                                        step=1_000, format="%d",
                                        label_visibility="collapsed")
    with col_max:
        st.caption("Max (0 = no limit)")
        max_followers = st.number_input("max_f", min_value=0, value=0,
                                        step=10_000, format="%d",
                                        label_visibility="collapsed")

    # ── Video Views Filter ────────────────────────────────────────────────────
    st.markdown('<div class="section-label">▶ Min Video Views (per post)</div>', unsafe_allow_html=True)
    min_views = st.number_input("min_views", min_value=0, value=0,
                                step=1_000, format="%d",
                                label_visibility="collapsed")

    # ── Verified Filter ────────────────────────────────────────────────────────
    only_verified = st.checkbox("✓ Verified accounts only", value=False)

    st.markdown("---")

    # ── Keyword Filters ───────────────────────────────────────────────────────
    st.markdown('<div class="section-label">🏷 Keyword Filters</div>', unsafe_allow_html=True)
    kw_scope = st.selectbox("Match keywords in",
                            ["Bio", "Post caption", "Bio + caption"],
                            label_visibility="visible")
    keywords_raw = st.text_input("Keywords (comma-separated)",
                                 placeholder="beauty, skincare, review",
                                 label_visibility="visible")
    keywords = [k.strip() for k in keywords_raw.split(",") if k.strip()] if keywords_raw else []

    st.markdown("---")

    # ── Location Filter ───────────────────────────────────────────────────────
    st.markdown('<div class="section-label">🇮🇩 Location Filter</div>', unsafe_allow_html=True)
    filter_indonesia = st.checkbox("Indonesia only (region = ID)", value=True)
    city_filter = st.multiselect(
        "City (match in bio — select 0 for any)",
        options=ID_CITIES,
        default=[],
        placeholder="All cities…",
    )

    st.markdown("---")
    run_btn = st.button("▶  Run Scraper")


# ────────────────────────────────────────────────────────────────────────────────
# MAIN
# ────────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:0.3rem;display:flex;align-items:center;gap:12px">
  <span style="font-family:'IBM Plex Mono',monospace;font-size:1.6rem;font-weight:700;color:#fff">
    TT<span style="color:#fe2c55">●</span>Scout
  </span>
  <span style="font-family:'IBM Plex Mono',monospace;font-size:0.58rem;letter-spacing:0.14em;
    background:#fe2c55;color:#fff;padding:3px 9px;border-radius:2px">LIVE</span>
</div>
<div style="font-size:0.8rem;color:#333;margin-bottom:1.5rem;font-weight:300">
  Discover TikTok creators — filter by followers, views &amp; keywords
</div>
""", unsafe_allow_html=True)


# ── Run ──────────────────────────────────────────────────────────────────────────
if run_btn:
    if not api_token:
        st.error("Enter your Apify API token in the sidebar.")
        st.stop()

    run_input = {"resultsPerPage": num_videos}

    if mode == "Hashtag":
        tags = [t.strip().lstrip("#") for t in hashtags_raw.splitlines() if t.strip()]
        if not tags:
            st.warning("Enter at least one hashtag.")
            st.stop()
        run_input["hashtags"] = tags

    elif mode == "Profile usernames":
        users = [u.strip().lstrip("@") for u in usernames_raw.splitlines() if u.strip()]
        if not users:
            st.warning("Enter at least one username.")
            st.stop()
        run_input["profiles"] = [f"https://www.tiktok.com/@{u}" for u in users]

    elif mode == "Search query":
        if not search_query.strip():
            st.warning("Enter a search query.")
            st.stop()
        run_input["searchQueries"] = [search_query.strip()]

    with st.spinner(f"Scraping TikTok via Apify… (fetching up to {num_videos} videos)"):
        raw_items = run_scraper(api_token, run_input)

    if not raw_items:
        st.warning("No results returned. Check your token or inputs.")
        st.stop()

    # Parse
    parsed = [parse_profile(item) for item in raw_items]

    # Deduplicate by handle
    seen, unique = set(), []
    for p in parsed:
        if p["handle"] and p["handle"] not in seen:
            seen.add(p["handle"])
            unique.append(p)

    # ── Apply filters ──────────────────────────────────────────────────────
    filtered = unique

    # Follower min
    filtered = [p for p in filtered if p["followers"] >= min_followers]

    # Follower max
    if max_followers > 0:
        filtered = [p for p in filtered if p["followers"] <= max_followers]

    # Min views (any video from the scrape)
    if min_views > 0:
        filtered = [p for p in filtered if p["play_count"] >= min_views]

    # Verified only
    if only_verified:
        filtered = [p for p in filtered if p["verified"]]

    # Keyword filter
    if keywords:
        def passes_kw(p):
            txt = ""
            if kw_scope in ("Bio", "Bio + caption"):          txt += " " + p["bio"]
            if kw_scope in ("Post caption", "Bio + caption"): txt += " " + p["caption"]
            return bool(kw_match(txt, keywords))
        filtered = [p for p in filtered if passes_kw(p)]

    # Indonesia country filter
    if filter_indonesia:
        filtered = [p for p in filtered if p["region"] in ("ID", "INDONESIA") or
                    p["region"] == "" and any(
                        c.lower() in p["bio"].lower()
                        for c in ["indonesia","jakarta","bandung","surabaya",
                                  "bali","yogyakarta","medan","semarang",
                                  "makassar","depok","tangerang","bekasi",
                                  "bogor","palembang","malang","batam",
                                  "pekanbaru","padang","pontianak","denpasar"]
                    )]

    # City filter — match city name in bio or city field
    if city_filter:
        def passes_city(p):
            haystack = (p["bio"] + " " + p["city"]).lower()
            return any(c.lower() in haystack for c in city_filter)
        filtered = [p for p in filtered if passes_city(p)]

    st.session_state.profiles  = filtered
    st.session_state.raw_count = len(unique)

    if filtered:
        st.success(f"✓ **{len(filtered)}** creators matched from **{len(unique)}** unique accounts ({len(raw_items)} posts fetched)")
    else:
        st.warning(f"No profiles matched your filters. ({len(unique)} unique accounts found — try loosening the filters.)")


# ── Display ──────────────────────────────────────────────────────────────────────
profiles   = st.session_state.profiles
raw_count  = st.session_state.raw_count

if profiles:
    total_followers = sum(p["followers"] for p in profiles)
    avg_followers   = total_followers // max(len(profiles), 1)
    verified_count  = sum(1 for p in profiles if p["verified"])
    total_views     = sum(p["play_count"] for p in profiles)

    st.markdown(f"""
    <div class="metrics-strip">
      <div class="m-card"><div class="m-label">Matched</div>
        <div class="m-val red">{len(profiles)}</div></div>
      <div class="m-card"><div class="m-label">Total Followers</div>
        <div class="m-val">{fmt(total_followers)}</div></div>
      <div class="m-card"><div class="m-label">Avg Followers</div>
        <div class="m-val">{fmt(avg_followers)}</div></div>
      <div class="m-card"><div class="m-label">Total Views</div>
        <div class="m-val">{fmt(total_views)}</div></div>
      <div class="m-card"><div class="m-label">Verified</div>
        <div class="m-val">{verified_count}</div></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Controls row ──────────────────────────────────────────────────────
    c1, c2, c3 = st.columns([2, 2, 2])
    with c1:
        sort_by = st.selectbox("Sort by", [
            "Followers ↓", "Followers ↑",
            "Likes ↓", "Videos ↓", "Views ↓"
        ])
    with c2:
        view_mode = st.radio("View", ["Cards", "Table"], horizontal=True)
    with c3:
        df_exp = pd.DataFrame([{
            "handle":        p["handle"],
            "nickname":      p["nickname"],
            "bio":           p["bio"],
            "followers":     p["followers"],
            "following":     p["following"],
            "likes":         p["likes"],
            "videos":        p["videos"],
            "post_views":    p["play_count"],
            "post_likes":    p["like_count"],
            "post_shares":   p["share_count"],
            "post_comments": p["comment_count"],
            "region":        p["region"],
            "city":          p["city"],
            "verified":      p["verified"],
            "url":           p["url"],
        } for p in profiles])
        st.download_button(
            "⬇  Export CSV",
            data=df_exp.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"),
            file_name="tiktok_profiles.csv",
            mime="text/csv",
        )

    sort_map = {
        "Followers ↓": ("followers",  True),
        "Followers ↑": ("followers",  False),
        "Likes ↓":     ("likes",      True),
        "Videos ↓":    ("videos",     True),
        "Views ↓":     ("play_count", True),
    }
    sk, sr   = sort_map[sort_by]
    sorted_p = sorted(profiles, key=lambda p: p[sk], reverse=sr)

    st.markdown("---")

    # ── Cards view ────────────────────────────────────────────────────────
    if view_mode == "Cards":
        for i in range(0, len(sorted_p), 2):
            row  = sorted_p[i:i+2]
            cols = st.columns(2)
            for col, p in zip(cols, row):
                with col:
                    bio_txt  = p["bio"] or "<em style='color:#1e1e1e'>No bio</em>"
                    vbadge   = '<span class="verified-badge">✓ verified</span>' if p["verified"] else ""
                    loc_parts = [x for x in [p["city"], p["region"]] if x]
                    loc_str   = " · ".join(loc_parts) if loc_parts else ""
                    loc_badge = (f'<span style="font-family:\'IBM Plex Mono\',monospace;'
                                 f'font-size:0.6rem;color:#2a6a3a;background:rgba(37,212,100,0.08);'
                                 f'border:1px solid rgba(37,212,100,0.2);padding:2px 6px;'
                                 f'border-radius:2px;margin-left:6px">📍 {loc_str}</span>'
                                 if loc_str else "")
                    tags_str = "".join(
                        f'<span class="kw-chip">{k}</span>'
                        for k in kw_match(p["bio"] + " " + p["caption"], keywords)
                    )
                    views_str = (
                        f'<div class="stat-item"><span class="p-stat-label">POST VIEWS</span>'
                        f'<span class="p-stat-val">{fmt(p["play_count"])}</span></div>'
                        if p["play_count"] else ""
                    )
                    st.markdown(f"""
                    <div class="p-card">
                      <div class="p-handle">@{p['handle']}{vbadge}{loc_badge}</div>
                      <div class="p-name">{p['nickname']}</div>
                      <div class="p-bio">{bio_txt}</div>
                      <div>{tags_str}</div>
                      <div class="p-stats">
                        <div class="stat-item">
                          <span class="p-stat-label">FOLLOWERS</span>
                          <span class="p-stat-val">{fmt(p['followers'])}</span>
                        </div>
                        <div class="stat-item">
                          <span class="p-stat-label">LIKES</span>
                          <span class="p-stat-val">{fmt(p['likes'])}</span>
                        </div>
                        <div class="stat-item">
                          <span class="p-stat-label">VIDEOS</span>
                          <span class="p-stat-val">{fmt(p['videos'])}</span>
                        </div>
                        <div class="stat-item">
                          <span class="p-stat-label">FOLLOWING</span>
                          <span class="p-stat-val">{fmt(p['following'])}</span>
                        </div>
                        {views_str}
                      </div>
                      <div style="margin-top:10px">
                        <a href="{p['url']}" target="_blank"
                           style="font-size:0.68rem;color:#2a2a2a;text-decoration:none;
                                  font-family:'IBM Plex Mono',monospace;">
                          ↗ tiktok.com/@{p['handle']}
                        </a>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

    # ── Table view ────────────────────────────────────────────────────────
    else:
        df_view = pd.DataFrame([{
            "@handle":   "@" + p["handle"],
            "name":      p["nickname"],
            "followers": p["followers"],
            "likes":     p["likes"],
            "videos":    p["videos"],
            "post views":p["play_count"],
            "region":    p["region"],
            "city":      p["city"],
            "✓":         "✓" if p["verified"] else "",
            "bio":       (p["bio"] or "")[:60] + ("…" if len(p["bio"] or "") > 60 else ""),
            "link":      p["url"],
        } for p in sorted_p])
        st.dataframe(
            df_view, use_container_width=True,
            column_config={
                "link":       st.column_config.LinkColumn("link"),
                "followers":  st.column_config.NumberColumn(format="%d"),
                "likes":      st.column_config.NumberColumn(format="%d"),
                "videos":     st.column_config.NumberColumn(format="%d"),
                "post views": st.column_config.NumberColumn(format="%d"),
            },
            hide_index=True,
        )

# ── Empty state ────────────────────────────────────────────────────────────────
else:
    st.markdown("""
    <div class="empty-state">
      <div class="empty-icon">🎯</div>
      <div class="empty-title">READY TO SCOUT</div>
      <div class="empty-hint">
        Pick a search mode on the left<br>
        Set follower range &amp; keyword filters<br>
        Hit <strong style="color:#fe2c55">Run Scraper</strong> to discover creators
      </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📖 Quick start guide"):
        st.markdown("""
**Search Modes**
- **Hashtag** — scrape posts from specific hashtags (e.g. `beauty`, `skincare`)
- **Profile usernames** — look up specific accounts directly
- **Search query** — keyword-based post search (e.g. `beauty review indonesia`)

**Filters**
- **Follower range** — set min and max to target micro or macro influencers
- **Min video views** — ensure the creator's posts actually get traction
- **Keywords** — match words in bio or post captions to find niche creators
- **Verified only** — toggle to show only verified accounts

**Cost control tips**
- Start with 50–100 videos per search to test results
- Combine hashtag + keyword filters to get precise matches without fetching thousands of posts
- Use the "Export CSV" button to save results for later
        """)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="margin-top:3rem;padding-top:1rem;border-top:1px solid #0e0e0e;
    font-size:0.6rem;color:#1e1e1e;font-family:'IBM Plex Mono',monospace;
    display:flex;justify-content:space-between;flex-wrap:wrap;gap:4px">
  <span>TT●SCOUT</span>
  <span>actor · {ACTOR_ID}</span>
</div>
""", unsafe_allow_html=True)
