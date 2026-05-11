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

# ── Custom CSS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0a0a;
    color: #f0f0f0;
}
section[data-testid="stSidebar"] {
    background-color: #111111 !important;
    border-right: 1px solid #1e1e1e;
}
section[data-testid="stSidebar"] > div { padding: 1.5rem 1rem; }

.tt-title {
    font-family: 'Space Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.03em;
}
.tt-badge {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.12em;
    background: #fe2c55;
    color: #fff;
    padding: 3px 10px;
    border-radius: 2px;
    text-transform: uppercase;
    vertical-align: middle;
    margin-left: 10px;
}
.tt-sub { font-size: 0.82rem; color: #555; margin-bottom: 2rem; font-weight: 300; }
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.12em;
    color: #444;
    text-transform: uppercase;
    margin-bottom: 6px;
    margin-top: 18px;
}
.actor-pill {
    display: inline-block;
    background: #141414;
    border: 1px solid #222;
    color: #555;
    font-size: 0.65rem;
    padding: 3px 10px;
    border-radius: 20px;
    font-family: 'Space Mono', monospace;
    margin-bottom: 1.5rem;
}
.metric-row { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 1.5rem; }
.metric-card {
    flex: 1; min-width: 110px;
    background: #141414; border: 1px solid #1e1e1e;
    border-radius: 6px; padding: 12px 16px;
}
.metric-label {
    font-size: 0.62rem; font-family: 'Space Mono', monospace;
    letter-spacing: 0.08em; color: #444; text-transform: uppercase; margin-bottom: 4px;
}
.metric-value { font-size: 1.4rem; font-weight: 600; color: #f0f0f0; font-family: 'Space Mono', monospace; }
.metric-accent { color: #fe2c55; }

.profile-card {
    background: #111; border: 1px solid #1e1e1e;
    border-radius: 8px; padding: 16px 18px; margin-bottom: 10px;
    transition: border-color 0.15s;
}
.profile-card:hover { border-color: #fe2c55; }
.profile-handle { font-family: 'Space Mono', monospace; font-size: 0.88rem; color: #fe2c55; font-weight: 700; }
.profile-name   { font-size: 0.82rem; color: #888; margin-bottom: 6px; }
.profile-bio {
    font-size: 0.78rem; color: #666; line-height: 1.5;
    border-left: 2px solid #1e1e1e; padding-left: 10px;
    margin: 8px 0; font-style: italic;
}
.profile-stats {
    display: flex; gap: 16px; font-size: 0.75rem; color: #555;
    font-family: 'Space Mono', monospace; margin-top: 8px; flex-wrap: wrap;
}
.stat-item { display: flex; flex-direction: column; gap: 2px; }
.stat-val   { color: #ddd; font-size: 0.85rem; }
.kw-tag {
    display: inline-block; background: rgba(254,44,85,0.1);
    border: 1px solid rgba(254,44,85,0.25); color: #fe2c55;
    font-size: 0.67rem; padding: 2px 7px; border-radius: 2px;
    font-family: 'Space Mono', monospace; margin-right: 4px; margin-top: 6px;
}
.stButton > button {
    background: #fe2c55 !important; color: #fff !important; border: none !important;
    border-radius: 4px !important; font-family: 'Space Mono', monospace !important;
    font-size: 0.75rem !important; letter-spacing: 0.08em !important; width: 100%;
    transition: opacity 0.15s !important;
}
.stButton > button:hover { opacity: 0.82 !important; }
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea textarea {
    background: #141414 !important; border: 1px solid #222 !important;
    color: #f0f0f0 !important; border-radius: 4px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: #fe2c55 !important;
    box-shadow: 0 0 0 1px rgba(254,44,85,0.15) !important;
}
hr { border-color: #1a1a1a !important; }
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
    handle   = a.get("name") or a.get("uniqueId") or item.get("name") or item.get("uniqueId") or ""
    nickname = a.get("nickName") or a.get("nickname") or item.get("nickName") or ""
    bio      = a.get("signature") or a.get("description") or item.get("signature") or ""
    followers= int(a.get("fans") or a.get("followerCount") or item.get("fans") or 0)
    following= int(a.get("following") or a.get("followingCount") or item.get("following") or 0)
    likes    = int(a.get("heart") or a.get("heartCount") or item.get("heart") or 0)
    videos   = int(a.get("video") or a.get("videoCount") or item.get("video") or 0)
    verified = bool(a.get("verified") or item.get("verified") or False)
    caption  = item.get("text") or item.get("desc") or ""
    return {
        "handle":   handle,
        "nickname": nickname,
        "bio":      bio,
        "caption":  caption,
        "followers":followers,
        "following":following,
        "likes":    likes,
        "videos":   videos,
        "verified": verified,
        "url":      f"https://www.tiktok.com/@{handle}" if handle else "",
    }

def run_scraper(api_token: str, run_input: dict) -> list:
    try:
        from apify_client import ApifyClient
    except ImportError:
        st.error("`apify-client` not installed. Run: pip install apify-client")
        return []
    client = ApifyClient(api_token)
    run    = client.actor(ACTOR_ID).call(run_input=run_input)
    return list(client.dataset(run["defaultDatasetId"]).iterate_items())


# ── Sidebar ──────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="tt-title">TT Scout</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="actor-pill">⚙ {ACTOR_ID}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">Apify API Token</div>', unsafe_allow_html=True)
    api_token = st.text_input(
        "token", type="password",
        placeholder="apify_api_xxxx…",
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown('<div class="section-label">Search Mode</div>', unsafe_allow_html=True)
    mode = st.radio("mode",
                    ["Hashtag", "Profile usernames", "Search query"],
                    label_visibility="collapsed")

    st.markdown("---")
    num_videos = st.number_input("Videos to fetch per input",
                                 min_value=10, max_value=1000, value=100, step=10)

    if mode == "Hashtag":
        st.markdown('<div class="section-label">Hashtags (one per line)</div>', unsafe_allow_html=True)
        hashtags_raw = st.text_area("ht", placeholder="fyp\nbeauty\nskincare",
                                    height=100, label_visibility="collapsed")

    elif mode == "Profile usernames":
        st.markdown('<div class="section-label">Usernames (one per line)</div>', unsafe_allow_html=True)
        usernames_raw = st.text_area("un", placeholder="keishadayang\nandreazshow",
                                     height=100, label_visibility="collapsed")

    elif mode == "Search query":
        st.markdown('<div class="section-label">Search query</div>', unsafe_allow_html=True)
        search_query = st.text_input("sq", placeholder="beauty review indonesia",
                                     label_visibility="collapsed")

    st.markdown("---")
    st.markdown('<div class="section-label">Filters</div>', unsafe_allow_html=True)
    min_followers = st.number_input("Min followers",
                                    min_value=0, value=10_000, step=1_000, format="%d")
    kw_scope  = st.selectbox("Match keywords in", ["Bio", "Post caption", "Bio + caption"])
    keywords_raw = st.text_input("Keywords (comma-separated)",
                                 placeholder="beauty, skincare, review")

    st.markdown("---")
    run_btn = st.button("▶  Run Scraper")


# ── Main ─────────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:0.2rem">
  <span class="tt-title">TT Scout</span>
  <span class="tt-badge">Live</span>
</div>
<div class="tt-sub">Discover TikTok creators by follower count &amp; keyword</div>
""", unsafe_allow_html=True)

keywords = [k.strip() for k in keywords_raw.split(",") if k.strip()] if keywords_raw else []

if "profiles" not in st.session_state:
    st.session_state.profiles = []

# ── Run ──────────────────────────────────────────────────────────────────────────
if run_btn:
    if not api_token:
        st.error("Enter your Apify API token in the sidebar.")
    else:
        run_input = {"resultsPerPage": num_videos}

        if mode == "Hashtag":
            tags = [t.strip().lstrip("#") for t in hashtags_raw.splitlines() if t.strip()]
            if not tags: st.warning("Enter at least one hashtag."); st.stop()
            run_input["hashtags"] = tags

        elif mode == "Profile usernames":
            users = [u.strip().lstrip("@") for u in usernames_raw.splitlines() if u.strip()]
            if not users: st.warning("Enter at least one username."); st.stop()
            run_input["profiles"] = [f"https://www.tiktok.com/@{u}" for u in users]

        elif mode == "Search query":
            if not search_query.strip(): st.warning("Enter a search query."); st.stop()
            run_input["searchQueries"] = [search_query.strip()]

        with st.spinner(f"Running `{ACTOR_ID}` on Apify…"):
            raw_items = run_scraper(api_token, run_input)

        if not raw_items:
            st.warning("No results returned. Check your token or inputs.")
        else:
            parsed = [parse_profile(item) for item in raw_items]

            seen, unique = set(), []
            for p in parsed:
                if p["handle"] and p["handle"] not in seen:
                    seen.add(p["handle"])
                    unique.append(p)

            filtered = [p for p in unique if p["followers"] >= min_followers]

            if keywords:
                def passes(p):
                    txt = ""
                    if kw_scope in ("Bio", "Bio + caption"):        txt += " " + p["bio"]
                    if kw_scope in ("Post caption", "Bio + caption"): txt += " " + p["caption"]
                    return bool(kw_match(txt, keywords))
                filtered = [p for p in filtered if passes(p)]

            st.session_state.profiles = filtered
            st.success(f"**{len(filtered)}** profiles matched from **{len(unique)}** unique accounts.")


# ── Display ──────────────────────────────────────────────────────────────────────
profiles = st.session_state.profiles

if profiles:
    total_followers = sum(p["followers"] for p in profiles)
    avg_followers   = total_followers // len(profiles)
    verified_count  = sum(1 for p in profiles if p["verified"])

    st.markdown(f"""
    <div class="metric-row">
      <div class="metric-card"><div class="metric-label">Matched</div>
        <div class="metric-value metric-accent">{len(profiles)}</div></div>
      <div class="metric-card"><div class="metric-label">Total Followers</div>
        <div class="metric-value">{fmt(total_followers)}</div></div>
      <div class="metric-card"><div class="metric-label">Avg Followers</div>
        <div class="metric-value">{fmt(avg_followers)}</div></div>
      <div class="metric-card"><div class="metric-label">Verified</div>
        <div class="metric-value">{verified_count}</div></div>
      <div class="metric-card"><div class="metric-label">Min Filter</div>
        <div class="metric-value">{fmt(min_followers)}</div></div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2, 2, 2])
    with c1:
        sort_by = st.selectbox("Sort by", ["Followers ↓", "Followers ↑", "Likes ↓", "Videos ↓"])
    with c2:
        view_mode = st.radio("View", ["Cards", "Table"], horizontal=True)
    with c3:
        df_exp = pd.DataFrame([{k: p[k] for k in
            ["handle","nickname","bio","followers","following","likes","videos","verified","url"]}
            for p in profiles])
        st.download_button("⬇  Export CSV",
            data=df_exp.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"),
            file_name="tiktok_profiles.csv", mime="text/csv")

    sk, sr = {"Followers ↓":("followers",True),"Followers ↑":("followers",False),
               "Likes ↓":("likes",True),"Videos ↓":("videos",True)}[sort_by]
    sorted_p = sorted(profiles, key=lambda p: p[sk], reverse=sr)

    st.markdown("---")

    if view_mode == "Cards":
        for i in range(0, len(sorted_p), 2):
            row = sorted_p[i:i+2]
            cols = st.columns(2)
            for col, p in zip(cols, row):
                with col:
                    bio_txt  = p["bio"] or "<em style='color:#2a2a2a'>No bio</em>"
                    vbadge   = ' <span style="color:#25d4d0;font-size:0.68rem">✓</span>' if p["verified"] else ""
                    tags_str = "".join(f'<span class="kw-tag">{k}</span>'
                                      for k in kw_match(p["bio"]+" "+p["caption"], keywords))
                    st.markdown(f"""
                    <div class="profile-card">
                      <div class="profile-handle">@{p['handle']}{vbadge}</div>
                      <div class="profile-name">{p['nickname']}</div>
                      <div class="profile-bio">{bio_txt}</div>
                      <div>{tags_str}</div>
                      <div class="profile-stats">
                        <div class="stat-item">
                          <span style="font-size:0.6rem;color:#333">FOLLOWERS</span>
                          <span class="stat-val">{fmt(p['followers'])}</span>
                        </div>
                        <div class="stat-item">
                          <span style="font-size:0.6rem;color:#333">LIKES</span>
                          <span class="stat-val">{fmt(p['likes'])}</span>
                        </div>
                        <div class="stat-item">
                          <span style="font-size:0.6rem;color:#333">VIDEOS</span>
                          <span class="stat-val">{fmt(p['videos'])}</span>
                        </div>
                        <div class="stat-item">
                          <span style="font-size:0.6rem;color:#333">FOLLOWING</span>
                          <span class="stat-val">{fmt(p['following'])}</span>
                        </div>
                      </div>
                      <div style="margin-top:10px">
                        <a href="{p['url']}" target="_blank"
                           style="font-size:0.7rem;color:#333;text-decoration:none;
                                  font-family:'Space Mono',monospace;">
                          ↗ tiktok.com/@{p['handle']}
                        </a>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        df_view = pd.DataFrame([{
            "@handle":   "@"+p["handle"],
            "name":      p["nickname"],
            "followers": p["followers"],
            "likes":     p["likes"],
            "videos":    p["videos"],
            "✓":         "✓" if p["verified"] else "",
            "bio":       (p["bio"] or "")[:70]+("…" if len(p["bio"] or "")>70 else ""),
            "url":       p["url"],
        } for p in sorted_p])
        st.dataframe(df_view, use_container_width=True,
            column_config={
                "url":       st.column_config.LinkColumn("link"),
                "followers": st.column_config.NumberColumn(format="%d"),
                "likes":     st.column_config.NumberColumn(format="%d"),
                "videos":    st.column_config.NumberColumn(format="%d"),
            }, hide_index=True)

else:
    st.markdown("""
    <div style="text-align:center;padding:80px 0 60px">
      <div style="font-size:2.5rem;margin-bottom:14px">🎯</div>
      <div style="font-family:'Space Mono',monospace;font-size:0.85rem;color:#222;margin-bottom:10px">
        READY TO SCOUT
      </div>
      <div style="font-size:0.8rem;color:#333;line-height:1.8;max-width:360px;margin:0 auto">
        Pick a mode · Set follower filter · Add keywords<br>
        Then hit <strong style="color:#fe2c55">Run Scraper</strong>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div style="margin-top:3rem;padding-top:1rem;border-top:1px solid #111;
    font-size:0.65rem;color:#222;font-family:'Space Mono',monospace;
    display:flex;justify-content:space-between;">
  <span>TT SCOUT</span><span>actor · {ACTOR_ID}</span>
</div>
""", unsafe_allow_html=True)
