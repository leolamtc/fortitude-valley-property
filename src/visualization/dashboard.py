import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

# Add src to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.analysis.correlator import load_data

# ─── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fortitude Valley 1-Bed/1-Car Property Tracker",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Authentication Gate ──────────────────────────────────────────────────────
def check_password():
    """Returns True if the user enters correct username and password."""
    def password_entered():
        if (
            st.session_state.get("username") == "admin"
            and st.session_state.get("password") == "Fortitude2032!"
        ):
            st.session_state["password_correct"] = True
            if "password" in st.session_state:
                del st.session_state["password"]
            if "username" in st.session_state:
                del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        _, col2, _ = st.columns([1, 2, 1])
        with col2:
            st.markdown("## 🔒 Fortitude Valley Tracker — Login")
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.button("Log In", on_click=password_entered, type="primary")
        return False
    elif not st.session_state["password_correct"]:
        _, col2, _ = st.columns([1, 2, 1])
        with col2:
            st.markdown("## 🔒 Fortitude Valley Tracker — Login")
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.button("Log In", on_click=password_entered, type="primary")
            st.error("❌ Invalid Username or Password")
        return False
    else:
        return True

if not check_password():
    st.stop()

# ─── Custom Premium CSS ────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0369a1 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        font-weight: 400;
    }

    .stat-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 1.25rem;
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        border-color: #38bdf8;
    }
    
    .stat-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94a3b8;
        margin-bottom: 0.4rem;
        font-weight: 600;
    }
    
    .stat-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #f8fafc;
    }
    
    .stat-sub {
        font-size: 0.85rem;
        margin-top: 0.3rem;
        font-weight: 500;
    }

    .badge-green { color: #4ade80; }
    .badge-blue { color: #38bdf8; }

    /* Customizing Streamlit Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1e293b;
        border-radius: 10px 10px 0px 0px;
        color: #94a3b8;
        font-weight: 600;
        padding: 10px 20px;
        border: 1px solid #334155;
    }

    .stTabs [aria-selected="true"] {
        background-color: #0284c7 !important;
        color: white !important;
        border-color: #38bdf8 !important;
    }
</style>
""", unsafe_allow_html=True)

# ─── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def fetch_dashboard_data():
    return load_data()

df_prop, df_infra = fetch_dashboard_data()

# ─── Sidebar Controls ──────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/isometric/96/real-estate.png", width=64)
    st.title("⚙️ Controls & Filters")
    st.markdown("---")
    
    # Date Range Filter
    min_date = df_prop['date_scraped'].min().to_pydatetime()
    max_date = df_prop['date_scraped'].max().to_pydatetime()
    
    date_range = st.slider(
        "📅 Select Date Range:",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="MMM YYYY"
    )
    
    # Price Range Filter
    min_price_val = float(df_prop['median_price'].min())
    max_price_val = float(df_prop['median_price'].max())
    
    price_range = st.slider(
        "💰 Price Range ($):",
        min_value=int(min_price_val),
        max_value=int(max_price_val + 50000),
        value=(int(min_price_val), int(max_price_val + 50000)),
        step=5000,
        format="$%d"
    )
    
    # Address Keyword Filter
    search_keyword = st.text_input("🔍 Search Address / Street:", placeholder="e.g. Connor St, Brunswick...")
    
    st.markdown("---")
    st.caption("🎯 **Target Property Type:** 1 Bedroom, 1 Car Space Apartment in Fortitude Valley QLD 4006.")
    st.caption("🔒 Authenticated as `admin`")

# ─── Data Filtering ────────────────────────────────────────────────────────────
df_filtered = df_prop[
    (df_prop['date_scraped'] >= pd.Timestamp(date_range[0])) &
    (df_prop['date_scraped'] <= pd.Timestamp(date_range[1])) &
    (df_prop['median_price'] >= price_range[0]) &
    (df_prop['median_price'] <= price_range[1])
]

if search_keyword:
    df_filtered = df_filtered[df_filtered['address'].astype(str).str.contains(search_keyword, case=False, na=False)]

# ─── Hero Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">🏙️ Fortitude Valley 1-Bed / 1-Car Property Tracker</div>
    <div class="hero-subtitle">Correlating 1-Bedroom & 1-Car Space Apartment Prices with QLD 2032 Olympics Infrastructure Announcements</div>
</div>
""", unsafe_allow_html=True)

# ─── Top Level Metrics Row ─────────────────────────────────────────────────────
if not df_filtered.empty:
    latest_price = df_filtered.iloc[-1]['median_price']
    earliest_price = df_filtered.iloc[0]['median_price']
    price_change = latest_price - earliest_price
    pct_change = (price_change / earliest_price) * 100 if earliest_price > 0 else 0
    avg_price = df_filtered['median_price'].mean()
    max_price = df_filtered['median_price'].max()
    total_sales = len(df_filtered)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Current Median Price</div>
            <div class="stat-value">${latest_price:,.0f}</div>
            <div class="stat-sub badge-green">1 Bed, 1 Car</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Period Growth</div>
            <div class="stat-value">{pct_change:+.1f}%</div>
            <div class="stat-sub badge-green">+${price_change:,.0f} Total</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Average Sale Price</div>
            <div class="stat-value">${avg_price:,.0f}</div>
            <div class="stat-sub badge-blue">Peak: ${max_price:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">Tracked Records</div>
            <div class="stat-value">{total_sales}</div>
            <div class="stat-sub badge-blue">Olympics Projects: {len(df_infra)}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Interactive Multi-Tab Interface ─────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Price Trends & Olympics Overlay",
    "🏢 Property Sales Explorer",
    "🚧 Infrastructure Announcements",
    "🧮 Interactive ROI Calculator"
])

# ─── TAB 1: Price Trends & Infrastructure Overlay ─────────────────────────────
with tab1:
    st.subheader("📈 Interactive Property Price Trend & Infrastructure Announcements")
    st.caption("Hover over points to see details. Vertical orange dashed lines mark QLD 2032 Olympics Infrastructure announcements.")

    if df_filtered.empty:
        st.warning("No property data matches your selected filters.")
    else:
        # Create Plotly Interactive Figure
        fig = go.Figure()

        # Add Price Area / Line
        fig.add_trace(go.Scatter(
            x=df_filtered['date_scraped'],
            y=df_filtered['median_price'],
            mode='lines+markers',
            name='Median Sale Price ($)',
            line=dict(color='#38bdf8', width=3, shape='spline'),
            marker=dict(size=6, color='#0284c7', symbol='circle'),
            fill='tozeroy',
            fillcolor='rgba(56, 189, 248, 0.08)',
            hovertemplate="<b>Date:</b> %{x|%d %b %Y}<br><b>Price:</b> $%{y:,.0f}<extra></extra>"
        ))

        # Add Moving Average
        if len(df_filtered) > 3:
            df_filtered['ma_3'] = df_filtered['median_price'].rolling(window=3).mean()
            fig.add_trace(go.Scatter(
                x=df_filtered['date_scraped'],
                y=df_filtered['ma_3'],
                mode='lines',
                name='3-Month Trend MA',
                line=dict(color='#818cf8', width=2, dash='dot'),
                hovertemplate="<b>3M Moving Avg:</b> $%{y:,.0f}<extra></extra>"
            ))

        # Add Infrastructure Announcements Markers
        for idx, row in df_infra.iterrows():
            infra_date = row['date_announced']
            title = row['title']
            
            if df_filtered['date_scraped'].min() <= infra_date <= df_filtered['date_scraped'].max():
                fig.add_vline(
                    x=infra_date,
                    line_width=2,
                    line_dash="dash",
                    line_color="#f97316",
                    annotation_text=f"📢 {title[:25]}...",
                    annotation_position="top left",
                    annotation_font=dict(color="#fb923c", size=10)
                )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.6)",
            height=500,
            margin=dict(l=20, r=20, t=40, b=20),
            hovermode="x unified",
            xaxis=dict(
                title="Date",
                showgrid=True,
                gridcolor="rgba(255,255,255,0.05)",
                rangeselector=dict(
                    buttons=list([
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(count=2, label="2y", step="year", stepmode="backward"),
                        dict(step="all", label="All")
                    ]),
                    bgcolor="#1e293b",
                    font=dict(color="#f8fafc")
                )
            ),
            yaxis=dict(
                title="Median Price (AUD)",
                tickprefix="$",
                separatethousands=True,
                showgrid=True,
                gridcolor="rgba(255,255,255,0.05)"
            ),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)

# ─── TAB 2: Property Sales Explorer ───────────────────────────────────────────
with tab2:
    st.subheader("🏢 Fortitude Valley 1-Bed / 1-Car Property Sales Explorer")
    st.caption("Direct, working Domain and RealEstate search links are generated for every property address.")

    c1, c2 = st.columns([2, 1])
    
    with c1:
        if not df_filtered.empty:
            display_df = df_filtered[['date_scraped', 'address', 'suburb', 'bedrooms', 'car_spaces', 'median_price', 'source_url']].copy()
            display_df.columns = ['Date', 'Address', 'Suburb', 'Beds', 'Cars', 'Price', 'Listing Link']
            display_df['Date'] = display_df['Date'].dt.strftime('%d %b %Y')
            display_df['Address'] = display_df['Address'].fillna('Fortitude Valley QLD')
            
            st.dataframe(
                display_df,
                use_container_width=True,
                height=450,
                hide_index=True,
                column_config={
                    "Price": st.column_config.NumberColumn(
                        "Price (AUD)",
                        format="$%d"
                    ),
                    "Listing Link": st.column_config.LinkColumn(
                        "Property Listing",
                        display_text="🔍 View Listing on Domain/RealEstate"
                    )
                }
            )

    with c2:
        st.markdown("#### 📊 Price Distribution")
        if not df_filtered.empty:
            fig_hist = px.histogram(
                df_filtered,
                x="median_price",
                nbins=15,
                title="Price Range Distribution",
                color_discrete_sequence=['#38bdf8'],
                labels={'median_price': 'Price ($)'}
            )
            fig_hist.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(15, 23, 42, 0.6)",
                height=400,
                margin=dict(l=10, r=10, t=30, b=10),
                yaxis_title="Count"
            )
            st.plotly_chart(fig_hist, use_container_width=True)

# ─── TAB 3: Infrastructure Announcements ───────────────────────────────────────
with tab3:
    st.subheader("🚧 Queensland Government Olympics 2032 Infrastructure News")
    st.caption("Announcements directly impact Fortitude Valley capital growth potential ahead of the 2032 Brisbane Olympic Games.")

    for idx, row in df_infra.iterrows():
        title = row.get('title', 'Infrastructure Upgrade')
        summary = row.get('summary', 'Major infrastructure announcement for Brisbane / Fortitude Valley.')
        date_str = pd.to_datetime(row['date_announced']).strftime('%d %B %Y') if pd.notnull(row['date_announced']) else "N/A"
        source_link = row.get('url') or row.get('source_url') or "https://statements.qld.gov.au/Search?searchTerm=Brisbane+2032+Olympics"

        st.markdown(f"""
        <div style="background: #1e293b; border-left: 4px solid #f97316; padding: 1.25rem; border-radius: 8px; margin-bottom: 1rem;">
            <div style="font-size: 0.85rem; color: #fb923c; font-weight: 600;">📅 Announced: {date_str}</div>
            <div style="font-size: 1.15rem; font-weight: 700; color: #f8fafc; margin: 0.3rem 0;">{title}</div>
            <div style="font-size: 0.95rem; color: #94a3b8; line-height: 1.5;">{summary}</div>
            <div style="margin-top: 0.6rem;">
                <a href="{source_link}" target="_blank" style="color: #38bdf8; text-decoration: none; font-weight: 600; font-size: 0.85rem;">
                    🔗 Read Full Statement on QLD Gov Portal →
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ─── TAB 4: Interactive ROI Calculator ────────────────────────────────────────
with tab4:
    st.subheader("🧮 1-Bed / 1-Car Apartment Investment & Yield Calculator")
    st.caption("Estimate your rental yields, cash flow, and 2032 Olympics equity growth.")

    col_calc1, col_calc2 = st.columns([1, 1])

    with col_calc1:
        calc_price = st.number_input("Purchase Price ($)", value=465000, step=5000)
        calc_rent = st.slider("Weekly Rent ($/week)", min_value=350, max_value=750, value=520, step=10)
        calc_interest = st.slider("Interest Rate (%)", min_value=3.0, max_value=8.0, value=5.5, step=0.1)
        calc_growth = st.slider("Estimated Annual Appreciation (%)", min_value=1.0, max_value=12.0, value=5.5, step=0.5)
        calc_years = st.slider("Holding Period (Years)", min_value=1, max_value=10, value=6)

    with col_calc2:
        annual_rent = calc_rent * 52
        gross_yield = (annual_rent / calc_price) * 100
        future_val = calc_price * ((1 + (calc_growth / 100)) ** calc_years)
        total_growth = future_val - calc_price

        st.markdown(f"""
        <div style="background: #0f172a; border: 1px solid #38bdf8; padding: 1.5rem; border-radius: 16px;">
            <h4 style="color: #38bdf8; margin-top: 0;">📊 Projected Investment Summary</h4>
            <table style="width:100%; font-size: 1rem; color: #f8fafc; line-height: 2;">
                <tr><td>Annual Rental Income:</td><td style="text-align:right; font-weight:700; color:#4ade80;">${annual_rent:,.0f}</td></tr>
                <tr><td>Gross Rental Yield:</td><td style="text-align:right; font-weight:700; color:#38bdf8;">{gross_yield:.2f}%</td></tr>
                <tr><td>Est. Value in {calc_years} Years ({2026 + calc_years}):</td><td style="text-align:right; font-weight:700; color:#f8fafc;">${future_val:,.0f}</td></tr>
                <tr><td>Total Capital Gain:</td><td style="text-align:right; font-weight:700; color:#4ade80;">+${total_growth:,.0f}</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

        # Plotly projection chart
        years_arr = list(range(1, calc_years + 1))
        val_arr = [calc_price * ((1 + (calc_growth / 100)) ** y) for y in years_arr]
        
        fig_proj = px.bar(
            x=[f"Year {y}" for y in years_arr],
            y=val_arr,
            labels={'x': 'Year', 'y': 'Property Value ($)'},
            title="Estimated Property Value Growth",
            color_discrete_sequence=['#0284c7']
        )
        fig_proj.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.6)",
            height=260,
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig_proj, use_container_width=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.85rem;">
    Fortitude Valley Property & Infrastructure Tracker | Built for 1-Bed, 1-Car Space Apartments | Target: Brisbane 2032 Olympics Infrastructure Impact
</div>
""", unsafe_allow_html=True)
