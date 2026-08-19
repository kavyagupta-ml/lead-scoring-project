import streamlit as st
import pandas as pd
import numpy as np
import pickle
import json
import os
import plotly.graph_objects as go
from datetime import datetime
import io
import urllib.parse

# ============= PAGE CONFIG =============
st.set_page_config(
    page_title="LeadIntel Pro | Brandconn",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============= DESIGN TOKENS =============
pink = "#E63946"
pink_dark = "#D91E3D"
baby_pink = "#FADADD"
purple = "#8B5CF6"
cyan = "#06B6D4"
ink = "#1F2937"
gray_mid = "#4B5563"
gray_light = "#6B7280"
bg = "#F8F9FA"
card_bg = "#FFFFFF"
line = "#E5E7EB"
pink_tint = "#FCE7EA"
purple_tint = "#F3E8FF"
amber = "#F59E0B"
amber_tint = "#FFFAEB"
gray_tint = "#F3F4F6"

# ============= CUSTOM CSS =============
# Fix from last version: the old ".stButton > button { !important }" rule was
# beating the more specific column-scoped card style regardless of source order,
# because !important always wins on equal/lower specificity. Fixed by using
# Streamlit's real button "kind" attribute (primary vs secondary) as the hook
# instead of fighting specificity with more !important rules.
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
html, body, [class*="css"] {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', Roboto, Oxygen, Ubuntu, sans-serif;
}}
.stApp {{ background: linear-gradient(180deg, {bg} 0%, #F5F7FA 100%); }}
p, span, label {{ color: {ink}; }}

.hero {{
    background: linear-gradient(135deg, {pink} 0%, {purple} 100%);
    padding: 56px 44px;
    margin: -1rem -1rem 32px -1rem;
    box-shadow: 0 20px 60px rgba(230,57,70,0.15);
    position: relative;
    overflow: hidden;
}}
.hero::after {{
    content: '';
    position: absolute; top: -60px; right: -60px;
    width: 260px; height: 260px; border-radius: 50%;
    background: rgba(255,255,255,0.08);
}}
.hero-title {{ font-size: 42px; font-weight: 800; letter-spacing: -1px; color: #FFF; margin: 0; }}
.hero-sub {{ font-size: 16px; color: rgba(255,255,255,0.92); max-width: 640px; line-height: 1.6; margin-top: 10px; }}
.hero-byline {{ font-size: 12px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: rgba(255,255,255,0.75); margin-top: 16px; }}

h1, h2, h3, h4 {{ color: {ink} !important; font-weight: 700; }}
h3 {{ font-size: 22px !important; }}

/* SECONDARY buttons (filters, clear, small actions) — soft card style */
.stButton > button[kind="secondary"] {{
    background: linear-gradient(160deg, {card_bg} 0%, {bg} 100%);
    color: {ink};
    border: 1px solid {line};
    border-radius: 12px;
    font-weight: 600;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}}
.stButton > button[kind="secondary"]:hover {{
    border-color: {pink};
    box-shadow: 0 8px 20px rgba(230,57,70,0.12);
    transform: translateY(-3px);
}}

/* PRIMARY buttons (main CTAs — Score All Leads, Score This Lead) */
.stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, {pink} 0%, {pink_dark} 100%);
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    padding: 12px 30px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    box-shadow: 0 8px 20px rgba(230,57,70,0.25);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}
.stButton > button[kind="primary"]:hover {{
    transform: translateY(-3px);
    box-shadow: 0 12px 32px rgba(230,57,70,0.32);
}}

/* Metric filter cards — distinct tint per tier, muted when count is 0 */
.metric-card {{
    border-radius: 16px;
    padding: 22px 18px;
    text-align: center;
    border: 1px solid {line};
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    transition: all 0.3s ease;
}}
.metric-card:hover {{ transform: translateY(-4px); box-shadow: 0 10px 24px rgba(0,0,0,0.08); }}
.metric-card .num {{ font-size: 30px; font-weight: 800; letter-spacing: -1px; }}
.metric-card .lbl {{ font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: {gray_mid}; margin-top: 4px; }}
.metric-card.empty {{ opacity: 0.45; border-style: dashed; }}

[data-testid="stFileUploader"] section {{
    background-color: {card_bg} !important; border: 2px dashed {line} !important; border-radius: 10px !important;
}}
[data-testid="stFileUploader"] section:hover {{ border-color: {pink} !important; background-color: {pink_tint} !important; }}
[data-testid="stFileUploader"] section span, [data-testid="stFileUploader"] section small, [data-testid="stFileUploader"] section div {{ color: {ink} !important; }}
[data-testid="stFileUploader"] button {{ background-color: {card_bg} !important; color: {ink} !important; border: 1px solid {gray_light} !important; font-weight: 700 !important; box-shadow: none !important; }}
[data-testid="stFileUploader"] button:hover {{ background-color: {bg} !important; border-color: {pink} !important; }}

div[data-baseweb="input"], div[data-baseweb="select"] > div {{ border-radius: 10px !important; border: 2px solid {line} !important; background-color: {card_bg} !important; }}
div[data-baseweb="input"] input, div[data-baseweb="select"] > div, div[data-baseweb="base-input"] input {{ color: {ink} !important; background-color: {card_bg} !important; }}
div[data-baseweb="input"]:focus-within, div[data-baseweb="select"]:focus-within > div {{ border-color: {pink} !important; box-shadow: 0 0 0 4px rgba(230,57,70,0.1) !important; }}

/* Download buttons use a different wrapper (stDownloadButton) than stButton — style separately */
.stDownloadButton > button {{
    background: linear-gradient(160deg, {card_bg} 0%, {bg} 100%) !important;
    color: {ink} !important;
    border: 1px solid {line} !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
}}
.stDownloadButton > button:hover {{ border-color: {pink} !important; box-shadow: 0 8px 20px rgba(230,57,70,0.12) !important; }}
.stDownloadButton > button p {{ color: {ink} !important; }}

/* Popovers (Thresholds) render in their own container — force light styling explicitly */
[data-testid="stPopoverBody"] {{
    background-color: {card_bg} !important;
    color: {ink} !important;
    border-radius: 12px !important;
    border: 1px solid {line} !important;
    padding: 16px !important;
}}
[data-testid="stPopoverBody"] * {{ color: {ink} !important; }}

/* Uploaded-file chip inside the file uploader */
[data-testid="stFileUploaderFile"] {{ background-color: {bg} !important; border-radius: 8px !important; }}
[data-testid="stFileUploaderFile"] * {{ color: {ink} !important; }}

/* Belt-and-braces: force light backgrounds on any remaining native widget containers */
[data-testid="stExpander"], [data-testid="stExpander"] summary {{ background-color: {card_bg} !important; color: {ink} !important; }}
.stSlider [data-baseweb="slider"] {{ background: transparent !important; }}

.stTabs [data-baseweb="tab-list"] {{ gap: 8px; border-bottom: 2px solid {line}; }}
.stTabs [data-baseweb="tab"] {{ font-weight: 600; font-size: 14px; color: {gray_mid}; padding: 10px 20px; }}
.stTabs [aria-selected="true"] {{ color: {pink} !important; border-bottom: 3px solid {pink} !important; }}

.lead-card {{
    background: {card_bg}; border: 1px solid {line}; border-radius: 12px;
    padding: 16px 22px; margin-bottom: 12px; display: flex; align-items: center; gap: 18px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04); transition: all 0.3s ease;
}}
.lead-card:hover {{ transform: translateY(-3px); box-shadow: 0 12px 28px rgba(0,0,0,0.08); }}
.lead-name {{ flex: 1.4; font-weight: 700; color: {ink}; }}
.lead-meta {{ flex: 1.6; color: {gray_light}; font-size: 0.82rem; }}
.lead-bar-track {{ flex: 2; background: {gray_tint}; border-radius: 8px; height: 12px; overflow: hidden; }}
.lead-bar-fill {{ height: 100%; border-radius: 8px; transition: width 1s cubic-bezier(0.22, 1, 0.36, 1); }}
.lead-score {{ width: 58px; text-align: right; font-weight: 800; }}
.tier-badge {{ font-size: 0.72rem; font-weight: 700; padding: 6px 14px; border-radius: 10px; width: 90px; text-align: center; }}

div[data-testid="stAlert"] {{ border-radius: 12px; }}
[data-testid="stSidebar"] {{ background-color: {card_bg}; border-right: 1px solid {line}; }}
.sidebar-brand {{ background: linear-gradient(135deg, {pink} 0%, {purple} 100%); padding: 20px; border-radius: 16px; margin-bottom: 18px; box-shadow: 0 8px 24px rgba(230,57,70,0.15); }}
.sidebar-brand h2 {{ color: #FFF !important; margin: 0; font-size: 1.1rem; }}
.sidebar-brand p {{ color: rgba(255,255,255,0.85); margin: 4px 0 0 0; font-size: 0.8rem; }}

.grad-divider {{ height: 2px; border: none; margin: 28px 0; background: linear-gradient(90deg, transparent, {line}, transparent); }}

/* Top navbar row (replaces sidebar) */
.navbar-wrap {{
    display: flex; align-items: center; justify-content: space-between;
    padding: 10px 0; margin-bottom: 8px; border-bottom: 1px solid {line};
}}
.navbar-logo {{ font-weight: 800; font-size: 1.1rem; color: {pink}; text-transform: lowercase; letter-spacing: -0.4px; }}
[data-testid="stSidebar"] {{ display: none; }}

@media (max-width: 700px) {{
    .lead-card {{ flex-direction: column; align-items: flex-start; gap: 8px; }}
    .hero {{ padding: 36px 24px; }} .hero-title {{ font-size: 30px; }}
}}
</style>
""", unsafe_allow_html=True)

# ============= LOAD MODEL =============
@st.cache_resource
def load_model():
    with open('lead_scorer.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('model_columns.json', 'r') as f:
        model_columns = json.load(f)
    return model, model_columns

try:
    model, model_columns = load_model()
    model_loaded = True
except Exception as e:
    model_loaded = False
    load_error = str(e)

def score_new_lead(lead_dict):
    row = pd.DataFrame(0, index=[0], columns=model_columns)
    for key, value in lead_dict.items():
        if key in row.columns:
            row[key] = value
        else:
            onehot_col = f"{key}_{value}"
            if onehot_col in row.columns:
                row[onehot_col] = 1
    return model.predict_proba(row)[0][1] * 100, row

def score_dataframe(df):
    scores = []
    for _, r in df.iterrows():
        lead = {
            'TotalVisits': r.get('TotalVisits', 0),
            'Total Time Spent on Website': r.get('Total Time Spent on Website', 0),
            'Page Views Per Visit': r.get('Page Views Per Visit', 0),
            'Do Not Email': r.get('Do Not Email', 0),
            'Do Not Call': r.get('Do Not Call', 0),
            'Lead Source': r.get('Lead Source', 'Other'),
            'Lead Origin': r.get('Lead Origin', 'API'),
            'Last Activity': r.get('Last Activity', 'Email Opened'),
        }
        s, _ = score_new_lead(lead)
        scores.append(round(s, 1))
    return scores

def explain_lead(lead_dict, score):
    """Plain-language, rule-based explanation — 'This lead scored X because...'
    Separate from the feature-importance table: this translates raw values into
    the kind of sentence a salesperson would actually say."""
    bullets = []

    visits = lead_dict.get('TotalVisits', 0)
    if visits >= 15:
        bullets.append(f"{visits} visits (high engagement)")
    elif visits >= 5:
        bullets.append(f"{visits} visits (moderate engagement)")
    else:
        bullets.append(f"{visits} visits (low engagement)")

    time_spent = lead_dict.get('Total Time Spent on Website', 0)
    minutes = time_spent / 60
    if time_spent >= 600:
        bullets.append(f"{minutes:.0f} min on site (thorough review)")
    elif time_spent >= 120:
        bullets.append(f"{minutes:.0f} min on site (moderate review)")
    else:
        bullets.append(f"{minutes:.0f} min on site (quick visit)")

    activity = lead_dict.get('Last Activity', '')
    if activity in ['Converted to Lead', 'Email Opened']:
        bullets.append(f"{activity} (shows interest)")
    elif activity in ['SMS Sent', 'Olark Chat Conversation']:
        bullets.append(f"{activity} (active contact attempt)")
    else:
        bullets.append(f"{activity} (passive signal)")

    if lead_dict.get('Do Not Email', 0) == 1 or lead_dict.get('Do Not Call', 0) == 1:
        bullets.append("opted out of email or calls (limits follow-up channels)")

    source = lead_dict.get('Lead Source', '')
    if source in ['Google', 'Direct Traffic', 'Reference']:
        bullets.append(f"came via {source} (typically higher intent)")

    return bullets

# ============= CUSTOM THRESHOLDS (persisted to disk) =============
THRESH_FILE = 'thresholds.json'

def load_thresholds():
    if os.path.exists(THRESH_FILE):
        try:
            with open(THRESH_FILE) as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_thresholds(d):
    with open(THRESH_FILE, 'w') as f:
        json.dump(d, f)

if "thresholds" not in st.session_state:
    st.session_state.thresholds = load_thresholds()

def get_thresholds(client):
    return st.session_state.thresholds.get(client, {"a": 70, "b": 40})

def tier_for(score, thresholds):
    """Grade A/B/C — no hot/warm/cold wording. Boundaries are per-client and adjustable."""
    if score > thresholds["a"]:
        return "Grade A", pink, pink_tint
    elif score > thresholds["b"]:
        return "Grade B", amber, amber_tint
    else:
        return "Grade C", gray_light, gray_tint

def priority_col(df, thresholds):
    return df['Score'].apply(lambda x: tier_for(x, thresholds)[0])

def export_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Scored Leads', index=False)
    return output.getvalue()

def build_printable_report(df, client_name):
    """A styled HTML report — open it and use the browser's Print > Save as PDF
    to get a PDF, without needing a separate PDF-generation library installed."""
    rows_html = "".join(
        f"<tr><td>{r.get('Company','—')}</td><td>{r['Score']}%</td>"
        f"<td>{r['Priority']}</td><td>{r.get('Lead Source','—')}</td></tr>"
        for _, r in df.iterrows()
    )
    return f"""
    <html><head><meta charset="utf-8"><title>{client_name} — Lead Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; color: #1F2937; padding: 30px; }}
        h1 {{ color: #E63946; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th {{ background: #1F2937; color: white; padding: 8px; text-align: left; }}
        td {{ padding: 8px; border-bottom: 1px solid #E5E7EB; }}
        tr:nth-child(even) {{ background: #FAFBFC; }}
        .note {{ color: #6B7280; font-size: 12px; margin-top: 30px; }}
    </style></head>
    <body>
        <h1>Lead Report — {client_name}</h1>
        <p>Generated {datetime.now().strftime('%Y-%m-%d %H:%M')} · {len(df)} leads</p>
        <table><tr><th>Company</th><th>Score</th><th>Grade</th><th>Source</th></tr>{rows_html}</table>
        <p class="note">Open this file in a browser and use Print → Save as PDF to export as PDF.</p>
    </body></html>
    """

# ============= SAMPLE CLIENTS =============
CLIENTS = {
    "TechStartup AI": {"industry": "Software/SaaS"},
    "FinanceFlow": {"industry": "Financial Services"},
    "HealthTech Pro": {"industry": "Healthcare"},
    "E-Commerce Plus": {"industry": "Retail"},
}

# ============= HEADER =============
st.markdown(f"""
<div class="hero">
    <div class="hero-title">LeadIntel Pro</div>
    <div class="hero-sub">AI-powered lead qualification. Upload a batch of leads or score one at a time —
    the model ranks them by conversion probability so your team knows exactly who to contact first.</div>
    <div class="hero-byline">Internship Project · Brandconn Digital Group</div>
</div>
""", unsafe_allow_html=True)

if not model_loaded:
    st.error(f"Model file not found or failed to load: {load_error}")
    st.stop()

# ============= TOP CONTROL BAR (replaces sidebar) =============
nav1, nav2, nav3 = st.columns([2, 2, 1])
with nav1:
    st.markdown('<div class="navbar-logo">◆ leadintel pro</div>', unsafe_allow_html=True)
with nav2:
    selected_client = st.selectbox("Client", list(CLIENTS.keys()),
                                    format_func=lambda x: f"{x} ({CLIENTS[x]['industry']})",
                                    label_visibility="collapsed")
with nav3:
    with st.popover("⚙ Thresholds", use_container_width=True):
        th = get_thresholds(selected_client)
        st.caption(f"Grading cutoffs for {selected_client}")
        a_val = st.slider("Grade A cutoff (above)", 50, 95, th["a"], key=f"th_a_{selected_client}")
        b_val = st.slider("Grade B cutoff (above)", 10, a_val - 5, min(th["b"], a_val - 5), key=f"th_b_{selected_client}")
        if st.button("Save thresholds", key="save_th"):
            st.session_state.thresholds[selected_client] = {"a": a_val, "b": b_val}
            save_thresholds(st.session_state.thresholds)
            st.success("Saved.")

st.caption("Model: RandomForest · 91.9% cross-validated accuracy · Trained on 9,240 leads")
st.markdown('<div class="grad-divider" style="margin:12px 0 24px 0;"></div>', unsafe_allow_html=True)

if "client_data" not in st.session_state:
    st.session_state.client_data = {name: None for name in CLIENTS}
if "dash_filter" not in st.session_state:
    st.session_state.dash_filter = "All"
if "single_lead_history" not in st.session_state:
    st.session_state.single_lead_history = []

thresholds = get_thresholds(selected_client)

def render_lead_cards(df):
    name_col = None
    for candidate in ['Company', 'Name', 'Lead Name', 'Email']:
        if candidate in df.columns:
            name_col = candidate
            break
    for i, row in df.iterrows():
        score = row['Score']
        label, color, tint = tier_for(score, thresholds)
        display_name = row[name_col] if name_col else f"Lead #{i+1}"
        meta_bits = []
        if 'Lead ID' in df.columns:
            meta_bits.append(str(row['Lead ID']))
        if 'Lead Source' in df.columns:
            meta_bits.append(str(row['Lead Source']))
        if 'Last Activity' in df.columns:
            meta_bits.append(str(row['Last Activity']))
        meta = " · ".join(meta_bits)
        st.markdown(f"""
        <div class="lead-card" style="border-left: 4px solid {color};">
            <div class="lead-name">{display_name}</div>
            <div class="lead-meta">{meta}</div>
            <div class="tier-badge" style="background:{tint}; color:{color};">{label}</div>
            <div class="lead-bar-track"><div class="lead-bar-fill" style="width:{score}%; background:{color};"></div></div>
            <div class="lead-score" style="color:{color};">{score}%</div>
        </div>
        """, unsafe_allow_html=True)

def metric_card_button(count, label, color, key, filter_value):
    empty_class = "empty" if count == 0 else ""
    st.markdown(f"""
    <div class="metric-card {empty_class}" style="border-top: 4px solid {color};">
        <div class="num" style="color:{color};">{count}</div>
        <div class="lbl">{label}</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("View", key=key, use_container_width=True):
        st.session_state.dash_filter = filter_value
        st.rerun()

# ============= TABS =============
tab_dash, tab_batch, tab_single, tab_compare, tab_analytics, tab_performance = st.tabs(
    ["Dashboard", "Batch Score", "Single Lead", "Compare Leads", "Analytics", "Client Performance"]
)

# ============= DASHBOARD =============
with tab_dash:
    st.subheader(f"{selected_client}")
    df_active = st.session_state.client_data.get(selected_client)

    if df_active is None:
        st.info("No leads scored yet for this client. Go to **Batch Score** to upload a CSV.")
    else:
        a1 = int((df_active['Score'] > thresholds["a"]).sum())
        b1 = int(((df_active['Score'] > thresholds["b"]) & (df_active['Score'] <= thresholds["a"])).sum())
        c1 = int((df_active['Score'] <= thresholds["b"]).sum())

        c1_, c2_, c3_, c4_ = st.columns(4)
        with c1_:
            metric_card_button(len(df_active), "TOTAL LEADS", purple, "f_all", "All")
        with c2_:
            metric_card_button(a1, f"GRADE A (>{thresholds['a']}%)", pink, "f_a", "Grade A")
        with c3_:
            metric_card_button(b1, f"GRADE B (>{thresholds['b']}%)", amber, "f_b", "Grade B")
        with c4_:
            metric_card_button(c1, "GRADE C", gray_light, "f_c", "Grade C")

        st.write("")
        with st.expander("Advanced Filters"):
            fc1, fc2, fc3 = st.columns(3)
            with fc1:
                score_range = st.slider("Score range", 0, 100, (0, 100))
            with fc2:
                sources_avail = sorted(df_active['Lead Source'].unique()) if 'Lead Source' in df_active.columns else []
                source_filter = st.multiselect("Lead source", sources_avail, default=sources_avail)
            with fc3:
                activities_avail = sorted(df_active['Last Activity'].unique()) if 'Last Activity' in df_active.columns else []
                activity_filter = st.multiselect("Last activity", activities_avail, default=activities_avail)

        search_term = st.text_input("Search by company name or Lead ID", "")

        col_a, col_b = st.columns([2, 1])
        with col_a:
            current_filter = st.session_state.dash_filter
            if current_filter != "All":
                st.markdown(f"**Filtered: {current_filter}**")
                if st.button("Clear filter", key="clear_filter"):
                    st.session_state.dash_filter = "All"
                    st.rerun()
        with col_b:
            top_n_choice = st.selectbox("Show", ["All", "Top 5", "Top 10"], key="top_n_select")

        current_filter = st.session_state.dash_filter
        shown = df_active if current_filter == "All" else df_active[df_active['Priority'] == current_filter]
        shown = shown[(shown['Score'] >= score_range[0]) & (shown['Score'] <= score_range[1])]
        if 'Lead Source' in shown.columns and source_filter:
            shown = shown[shown['Lead Source'].isin(source_filter)]
        if 'Last Activity' in shown.columns and activity_filter:
            shown = shown[shown['Last Activity'].isin(activity_filter)]
        if search_term:
            mask = pd.Series(False, index=shown.index)
            if 'Company' in shown.columns:
                mask |= shown['Company'].astype(str).str.contains(search_term, case=False, na=False)
            if 'Lead ID' in shown.columns:
                mask |= shown['Lead ID'].astype(str).str.contains(search_term, case=False, na=False)
            shown = shown[mask]
        shown = shown.sort_values('Score', ascending=False).reset_index(drop=True)

        if top_n_choice == "Top 5":
            shown = shown.head(5)
        elif top_n_choice == "Top 10":
            shown = shown.head(10)

        st.markdown('<hr class="grad-divider">', unsafe_allow_html=True)

        if len(shown) == 0:
            st.info("No leads match the current filters — that's a real result, not an error.")
        else:
            render_lead_cards(shown)

        st.write("")
        st.markdown("**Export**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.download_button("CSV", shown.to_csv(index=False), f"{selected_client}_leads.csv", "text/csv")
        with col2:
            st.download_button("Excel", export_to_excel(shown), f"{selected_client}_leads.xlsx", "application/vnd.ms-excel")
        with col3:
            contact_list = shown[['Score', 'Priority'] + [c for c in ['Company', 'Lead ID', 'Lead Source'] if c in shown.columns]].sort_values('Score', ascending=False)
            st.download_button("Contact list", contact_list.to_csv(index=False), f"{selected_client}_contact_list.csv", "text/csv")
        with col4:
            html_report = build_printable_report(shown, selected_client)
            st.download_button("Printable report (HTML→PDF)", html_report, f"{selected_client}_report.html", "text/html")

        col5, col6 = st.columns(2)
        with col5:
            top10 = df_active.sort_values('Score', ascending=False).head(10)
            st.download_button("Top 10 leads to contact", top10.to_csv(index=False), f"{selected_client}_top10_contact.csv", "text/csv")
        with col6:
            top20 = df_active.sort_values('Score', ascending=False).head(20)
            st.download_button("Top 20 leads to follow up", top20.to_csv(index=False), f"{selected_client}_top20_followup.csv", "text/csv")

        st.markdown('<hr class="grad-divider">', unsafe_allow_html=True)
        with st.expander("Lead Quality Report — auto-generated insights"):
            a1 = int((df_active['Score'] > thresholds["a"]).sum())
            total = len(df_active)
            avg_score = df_active['Score'].mean()
            top_source = df_active['Lead Source'].mode()[0] if 'Lead Source' in df_active.columns and len(df_active) else "—"
            grade_a_df = df_active[df_active['Priority'] == 'Grade A']
            grade_a_top_source = grade_a_df['Lead Source'].mode()[0] if 'Lead Source' in grade_a_df.columns and len(grade_a_df) else None

            st.markdown(f"- **{a1} of {total} leads ({a1/total:.0%})** are Grade A — recommend the sales team contact these first, ideally within 24 hours.")
            st.markdown(f"- Average conversion probability across this batch is **{avg_score:.1f}%**.")
            st.markdown(f"- The most common lead source overall is **{top_source}**.")
            if grade_a_top_source:
                st.markdown(f"- Among Grade A leads specifically, **{grade_a_top_source}** is the most common source — worth investing more budget there.")
            if a1 == 0:
                st.markdown("- No leads currently reach Grade A. Consider lowering the Grade A threshold for this client, or treat the top few Grade B leads as this batch's priority list.")
            st.caption("These are simple rule-based summaries of the scored data, not model-generated natural language — presented here as a lightweight reporting layer on top of the scores.")

# ============= BATCH SCORE =============
with tab_batch:
    st.subheader(f"Batch Scoring — {selected_client}")
    st.caption("Expected columns: TotalVisits, Total Time Spent on Website, Page Views Per Visit, Do Not Email, Do Not Call, Lead Source, Lead Origin, Last Activity. A Company column is optional, for display.")

    if st.session_state.get("just_scored_message"):
        st.success(st.session_state.just_scored_message)
        st.session_state.just_scored_message = None

    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'], key=f"upload_{selected_client}")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(f"Loaded {len(df)} leads")
        with st.expander("Preview raw data"):
            st.dataframe(df.head(10), use_container_width=True)

        if st.button("Score All Leads", key="batch_score", type="primary"):
            with st.spinner("Scoring leads against the trained model..."):
                result_df = df.copy()
                result_df['Score'] = score_dataframe(df)
                result_df['Priority'] = priority_col(result_df, thresholds)
                result_df = result_df.sort_values('Score', ascending=False).reset_index(drop=True)
                prefix = "".join(w[0] for w in selected_client.split())[:4].upper()
                result_df['Lead ID'] = [f"{prefix}-{i+1:04d}" for i in range(len(result_df))]
                st.session_state.client_data[selected_client] = result_df
                st.session_state.dash_filter = "All"

                # Batch Scoring History — keep every upload, not just the latest
                if "batch_history" not in st.session_state:
                    st.session_state.batch_history = {c: [] for c in CLIENTS}
                st.session_state.batch_history.setdefault(selected_client, []).insert(0, {
                    "Time": datetime.now().strftime('%Y-%m-%d %H:%M'),
                    "Filename": uploaded_file.name,
                    "Leads": len(result_df),
                    "Avg Score": round(result_df['Score'].mean(), 1),
                    "raw_df": df,
                })
                st.session_state.batch_history[selected_client] = st.session_state.batch_history[selected_client][:10]

                st.session_state.just_scored_message = f"Scored {len(result_df)} leads — check the Dashboard tab to view and filter results."
            st.rerun()

    if "batch_history" not in st.session_state:
        st.session_state.batch_history = {c: [] for c in CLIENTS}
    history = st.session_state.batch_history.get(selected_client, [])
    if history:
        with st.expander(f"Batch Scoring History ({len(history)} saved upload{'s' if len(history) != 1 else ''})"):
            st.caption("Every upload for this client is kept here. Re-score applies the client's current thresholds to that batch again.")
            for idx, entry in enumerate(history):
                hc1, hc2, hc3, hc4 = st.columns([2, 1, 1, 1])
                hc1.write(f"**{entry['Filename']}** · {entry['Time']}")
                hc2.write(f"{entry['Leads']} leads")
                hc3.write(f"Avg {entry['Avg Score']}%")
                with hc4:
                    if st.button("Re-score & load", key=f"rescore_{idx}"):
                        raw = entry['raw_df']
                        rescored = raw.copy()
                        rescored['Score'] = score_dataframe(raw)
                        rescored['Priority'] = priority_col(rescored, thresholds)
                        rescored = rescored.sort_values('Score', ascending=False).reset_index(drop=True)
                        prefix = "".join(w[0] for w in selected_client.split())[:4].upper()
                        rescored['Lead ID'] = [f"{prefix}-{i+1:04d}" for i in range(len(rescored))]
                        st.session_state.client_data[selected_client] = rescored
                        st.session_state.just_scored_message = f"Re-scored {entry['Filename']} with current thresholds."
                        st.rerun()

    df_active = st.session_state.client_data.get(selected_client)
    if df_active is not None:
        st.markdown('<hr class="grad-divider">', unsafe_allow_html=True)
        render_lead_cards(df_active.sort_values('Score', ascending=False).reset_index(drop=True))

# ============= SINGLE LEAD =============
with tab_single:
    st.subheader(f"Score a Single Lead — {selected_client}")

    col1, col2 = st.columns(2)
    with col1:
        visits = st.number_input("Website Visits", 0, 100, 10)
        time_spent = st.number_input("Time on Site (seconds)", 0, 3000, 300)
        page_views = st.number_input("Page Views Per Visit", 0.0, 20.0, 3.5)
        lead_source = st.selectbox("Lead Source", ["Google", "Direct Traffic", "Olark Chat", "Organic Search", "Reference", "Other"])
    with col2:
        lead_origin = st.selectbox("Lead Origin", ["Landing Page Submission", "API", "Lead Add Form", "Lead Import"])
        last_activity = st.selectbox("Last Activity", ["Email Opened", "SMS Sent", "Olark Chat Conversation", "Page Visited on Website", "Converted to Lead"])
        do_not_email = st.checkbox("Opted out of email?")
        do_not_call = st.checkbox("Opted out of calls?")

    company_name = st.text_input("Company / Lead Name", "New Lead")

    if st.button("Score This Lead", key="single_score", type="primary"):
        lead = {
            'TotalVisits': visits, 'Total Time Spent on Website': time_spent, 'Page Views Per Visit': page_views,
            'Do Not Email': int(do_not_email), 'Do Not Call': int(do_not_call),
            'Lead Source': lead_source, 'Lead Origin': lead_origin, 'Last Activity': last_activity,
        }
        with st.spinner("Scoring..."):
            score, encoded_row = score_new_lead(lead)
        label, color, tint = tier_for(score, thresholds)
        st.success(f"{company_name} scored successfully")

        st.session_state.single_lead_history.insert(0, {
            "Time": datetime.now().strftime('%Y-%m-%d %H:%M'),
            "Company": company_name, "Score": round(score, 1), "Grade": label
        })
        st.session_state.single_lead_history = st.session_state.single_lead_history[:20]

        st.write("")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(160deg, {card_bg} 0%, {tint} 140%); border: 1px solid {line};
                        border-top: 4px solid {color}; padding: 28px; border-radius: 16px; text-align: center;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.06);">
                <h1 style="margin: 0; color: {color}; font-size: 48px; letter-spacing: -1px;">{score:.0f}%</h1>
                <p style="margin: 8px 0 0 0; color: {gray_mid}; font-size: 12px; text-transform: uppercase; letter-spacing: 1px;">Conversion Probability</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="padding: 22px 26px; background: {tint}; border-left: 4px solid {color}; border-radius: 12px;
                        height: 100%; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
                <span class="tier-badge" style="background:{card_bg}; color:{color};">{label}</span>
                <p style="margin: 14px 0 0 0; color: {ink}; font-weight: 700;">{company_name}</p>
                <p style="margin: 4px 0 0 0; color: {gray_light}; font-size: 0.85rem;">{lead_source} · {last_activity}</p>
            </div>
            """, unsafe_allow_html=True)

        # ── Lead Scoring Explanation (plain language) ──
        st.markdown("#### Lead Scoring Explanation")
        explanation_bullets = explain_lead(lead, score)
        st.markdown(f"**This lead scored {score:.0f}% because:**")
        for b in explanation_bullets:
            st.markdown(f"- {b}")

        # ── Feature contribution ("why this score") — more technical view ──
        with st.expander("Technical breakdown (model feature importances)"):
            st.caption("Approximate — based on the model's overall feature importances applied to this lead's specific values. Not a full per-lead explanation (e.g. SHAP), but a reasonable indicator of what mattered.")
            importances = pd.Series(model.feature_importances_, index=model_columns)
            active_cols = encoded_row.columns[(encoded_row.iloc[0] != 0)]
            contrib = importances[active_cols].sort_values(ascending=False).head(5)
            for feat, imp in contrib.items():
                st.markdown(f"- **{feat}** — relative importance {imp:.1%}")

        # ── Email to sales team (mailto, no backend needed) ──
        subject = urllib.parse.quote(f"Lead Score: {company_name} ({score:.0f}%)")
        body = urllib.parse.quote(
            f"Lead: {company_name}\nScore: {score:.0f}%\nGrade: {label}\n"
            f"Source: {lead_source}\nLast Activity: {last_activity}\n\nScored via LeadIntel Pro."
        )
        st.markdown(f'<a href="mailto:?subject={subject}&body={body}" style="text-decoration:none;"><button style="background:{card_bg};border:1px solid {line};border-radius:8px;padding:8px 16px;cursor:pointer;color:{ink};font-weight:600;">Email this lead to sales team</button></a>', unsafe_allow_html=True)

    if st.session_state.single_lead_history:
        st.markdown('<hr class="grad-divider">', unsafe_allow_html=True)
        st.markdown("#### Recent Scores (this session)")
        st.caption("Session-only history — resets when the app restarts, not a persistent database.")
        st.dataframe(pd.DataFrame(st.session_state.single_lead_history), use_container_width=True, hide_index=True)

# ============= COMPARE LEADS =============
with tab_compare:
    st.subheader(f"Compare Leads — {selected_client}")
    df_active = st.session_state.client_data.get(selected_client)

    if df_active is None:
        st.info("No scored leads yet for this client. Score some leads in **Batch Score** first.")
    else:
        name_col = 'Company' if 'Company' in df_active.columns else None
        options = df_active[name_col].tolist() if name_col else [f"Lead #{i+1}" for i in range(len(df_active))]
        picked = st.multiselect("Select 2-3 leads to compare", options, max_selections=3)

        if len(picked) >= 2:
            if name_col:
                compare_df = df_active[df_active[name_col].isin(picked)].drop_duplicates(subset=name_col)
            else:
                compare_df = df_active.iloc[[options.index(p) for p in picked]]

            cols = st.columns(len(compare_df))
            for col, (_, row) in zip(cols, compare_df.iterrows()):
                label, color, tint = tier_for(row['Score'], thresholds)
                with col:
                    display_name = row[name_col] if name_col else "Lead"
                    st.markdown(f"""
                    <div style="background:{card_bg}; border:1px solid {line}; border-top:4px solid {color};
                                border-radius:14px; padding:18px; text-align:center;">
                        <h4 style="margin:0;">{display_name}</h4>
                        <div style="font-size:32px; font-weight:800; color:{color}; margin:10px 0;">{row['Score']}%</div>
                        <span class="tier-badge" style="background:{tint}; color:{color};">{label}</span>
                        <hr style="margin:14px 0; border-color:{line};">
                        <p style="text-align:left; font-size:0.85rem; color:{gray_mid};">
                            Visits: {row.get('TotalVisits','—')}<br>
                            Time on site: {row.get('Total Time Spent on Website','—')}s<br>
                            Source: {row.get('Lead Source','—')}<br>
                            Last activity: {row.get('Last Activity','—')}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.caption("Pick at least 2 leads above to see them side by side.")

# ============= ANALYTICS =============
with tab_analytics:
    st.subheader(f"Analytics — {selected_client}")
    df_active = st.session_state.client_data.get(selected_client)

    if df_active is None:
        st.info("No scored leads yet for this client. Score some leads in **Batch Score** first.")
    else:
        col1, col2 = st.columns(2)
        with col1:
            fig_dist = go.Figure(data=[go.Histogram(x=df_active['Score'], nbinsx=20, marker=dict(color=pink))])
            fig_dist.update_layout(title="Score Distribution", xaxis_title="Score", yaxis_title="Count",
                                    template="plotly_white", paper_bgcolor=bg, plot_bgcolor=bg, font=dict(color=ink))
            st.plotly_chart(fig_dist, use_container_width=True)
        with col2:
            if 'Lead Source' in df_active.columns:
                sc = df_active['Lead Source'].value_counts()
                fig_source = go.Figure(data=[go.Bar(x=sc.index, y=sc.values, marker=dict(color=purple))])
                fig_source.update_layout(title="Leads by Source", xaxis_title="Source", yaxis_title="Count",
                                          template="plotly_white", paper_bgcolor=bg, plot_bgcolor=bg, font=dict(color=ink))
                st.plotly_chart(fig_source, use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            if 'Lead Origin' in df_active.columns:
                oc = df_active['Lead Origin'].value_counts()
                fig_origin = go.Figure(data=[go.Bar(x=oc.index, y=oc.values, marker=dict(color=cyan))])
                fig_origin.update_layout(title="Leads by Origin", xaxis_title="Origin", yaxis_title="Count",
                                          template="plotly_white", paper_bgcolor=bg, plot_bgcolor=bg, font=dict(color=ink))
                st.plotly_chart(fig_origin, use_container_width=True)
        with col4:
            a1 = int((df_active['Score'] > thresholds["a"]).sum())
            b1 = int(((df_active['Score'] > thresholds["b"]) & (df_active['Score'] <= thresholds["a"])).sum())
            c1 = int((df_active['Score'] <= thresholds["b"]).sum())
            fig_pie = go.Figure(data=[go.Pie(labels=['Grade A', 'Grade B', 'Grade C'], values=[a1, b1, c1],
                                              marker=dict(colors=[pink, amber, gray_light]))])
            fig_pie.update_layout(title="Grade Breakdown", template="plotly_white", paper_bgcolor=bg, plot_bgcolor=bg, font=dict(color=ink))
            st.plotly_chart(fig_pie, use_container_width=True)

        st.write("")
        m1, m2, m3 = st.columns(3)
        m1.metric("Average Score", f"{df_active['Score'].mean():.1f}%")
        m2.metric("Median Score", f"{df_active['Score'].median():.1f}%")
        m3.metric("Total Leads Scored", len(df_active))
        st.caption("Trend-over-time charts require timestamped historical data, which this dataset doesn't include — a natural next extension if leads are logged with dates.")

# ============= CLIENT PERFORMANCE =============
with tab_performance:
    st.subheader("Client Performance Metrics")
    st.caption("Compares clients that have at least one scored batch. Switch clients in the top bar and score some leads in Batch Score to populate more rows here.")

    rows = []
    for client_name in CLIENTS:
        cdf = st.session_state.client_data.get(client_name)
        if cdf is not None and len(cdf) > 0:
            cthresh = get_thresholds(client_name)
            a_count = int((cdf['Score'] > cthresh["a"]).sum())
            top_src = cdf['Lead Source'].mode()[0] if 'Lead Source' in cdf.columns and len(cdf) else "—"
            rows.append({
                "Client": client_name,
                "Total Leads": len(cdf),
                "Avg Score": round(cdf['Score'].mean(), 1),
                "Grade A %": round(a_count / len(cdf) * 100, 1),
                "Best Lead Source": top_src,
            })

    if not rows:
        st.info("No clients have scored data yet. Go to **Batch Score** for at least one client to populate this comparison.")
    else:
        perf_df = pd.DataFrame(rows).sort_values("Avg Score", ascending=False).reset_index(drop=True)
        st.dataframe(perf_df, use_container_width=True, hide_index=True)

        best_client = perf_df.iloc[0]['Client']
        st.markdown(f"**{best_client}** currently has the highest average conversion probability across its scored leads.")

        st.markdown('<hr class="grad-divider">', unsafe_allow_html=True)
        st.markdown("#### Estimated Value (illustrative)")
        st.caption("This dataset has no real revenue or deal-size figures, so true ROI per lead can't be calculated. As an illustration, enter an assumed value per converted lead below to see a rough expected-value estimate — not a substitute for real financial data.")
        assumed_value = st.number_input("Assumed value per converted lead ($)", 0, 100000, 500, step=50)
        if assumed_value > 0:
            perf_df['Est. Expected Value ($)'] = (perf_df['Avg Score'] / 100 * perf_df['Total Leads'] * assumed_value).round(0)
            st.dataframe(perf_df[['Client', 'Total Leads', 'Avg Score', 'Est. Expected Value ($)']], use_container_width=True, hide_index=True)

# ============= FOOTER =============
st.markdown('<hr class="grad-divider">', unsafe_allow_html=True)
st.markdown(f'<div style="text-align:center; color:{gray_light}; padding:16px; font-size:0.85rem;">LeadIntel Pro — an internship project for Brandconn Digital Group</div>', unsafe_allow_html=True)
