import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nassau Candy Analytics",
    page_icon="🍬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Main App Background ── */
    .stApp { background: linear-gradient(135deg, #1a0533 0%, #2d1054 100%); }

    /* ── Metric Cards ── */
    .metric-card {
        background: linear-gradient(135deg, #6B21A8, #7C3AED);
        padding: 20px; border-radius: 15px; text-align: center;
        box-shadow: 0 4px 15px rgba(107,33,168,0.4); margin: 5px;
    }
    .metric-value { font-size: 2rem; font-weight: bold; color: #FFD700; }
    .metric-label { font-size: 0.9rem; color: #E9D5FF; margin-top: 5px; }

    /* ── Titles ── */
    .page-title {
        text-align: center; color: #FF69B4; font-size: 2.5rem;
        font-weight: bold; padding: 10px;
        text-shadow: 0 0 20px rgba(255,105,180,0.5);
    }
    .subtitle { text-align: center; color: #C084FC; font-size: 1.1rem; margin-bottom: 20px; }
    .section-header {
        color: #FF69B4; font-size: 1.3rem; font-weight: bold;
        border-bottom: 2px solid #6B21A8; padding-bottom: 5px; margin: 20px 0 10px 0;
    }

    /* ══════════════════════════════════
       SIDEBAR — FORCE ALL TEXT BRIGHT
    ══════════════════════════════════ */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0220 0%, #1a0533 60%, #2d1054 100%) !important;
        border-right: 2px solid #7C3AED !important;
    }

    /* Force EVERY text element in sidebar to be bright */
    section[data-testid="stSidebar"] * {
        color: #F0ABFC !important;
        font-weight: 600 !important;
    }

    /* Sidebar headings — extra bright pink */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #FF69B4 !important;
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        text-shadow: 0 0 8px rgba(255,105,180,0.6) !important;
    }

    /* Sidebar bold text — gold */
    section[data-testid="stSidebar"] strong,
    section[data-testid="stSidebar"] b {
        color: #FFD700 !important;
        font-weight: 800 !important;
    }

    /* Radio button labels */
    section[data-testid="stSidebar"] .stRadio > label,
    section[data-testid="stSidebar"] .stRadio span,
    section[data-testid="stSidebar"] .stRadio p {
        color: #FFFFFF !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
    }

    /* Multiselect filter labels */
    section[data-testid="stSidebar"] .stMultiSelect > label,
    section[data-testid="stSidebar"] .stMultiSelect label {
        color: #FFD700 !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }

    /* Multiselect tags */
    section[data-testid="stSidebar"] [data-baseweb="tag"] {
        background-color: #7C3AED !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="tag"] span {
        color: #FFD700 !important;
        font-weight: bold !important;
    }

    /* Slider label */
    section[data-testid="stSidebar"] .stSlider > label {
        color: #FFD700 !important;
        font-weight: 700 !important;
    }

    /* Paragraph text */
    section[data-testid="stSidebar"] p {
        color: #E9D5FF !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
    }

    /* Divider */
    section[data-testid="stSidebar"] hr {
        border: 1px solid #7C3AED !important;
        margin: 8px 0 !important;
    }

    /* Navigation label */
    section[data-testid="stSidebar"] .stMarkdown {
        color: #F0ABFC !important;
    }

    /* Record count and built by text */
    section[data-testid="stSidebar"] .element-container p {
        color: #C084FC !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Load Data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/awatharesaroj-cmd/Nassau-Candy-Final_Project-Analytics/main/Nassau_Candy_Distributor.csv"
    df = pd.read_csv(url)
    df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
    df['Year'] = df['Order Date'].dt.year
    df['Month Num'] = df['Order Date'].dt.month
    df['Month Name'] = df['Order Date'].dt.strftime('%B')

    lead_time_map = {'Same Day': 1, 'First Class': 2, 'Second Class': 4, 'Standard Class': 7}
    df['Lead Time (Days)'] = df['Ship Mode'].map(lead_time_map)

    df['Shipping Speed'] = df['Lead Time (Days)'].apply(
        lambda x: 'Fast' if x <= 2 else ('Standard' if x <= 4 else 'Slow'))

    factory_map = {
        'Wonka Bar - Nutty Crunch Surprise': "Lot's O' Nuts",
        'Wonka Bar - Fudge Mallows': "Lot's O' Nuts",
        'Wonka Bar - Scrumdiddlyumptious': "Lot's O' Nuts",
        'Wonka Bar -Scrumdiddlyumptious': "Lot's O' Nuts",
        'Wonka Bar - Milk Chocolate': "Wicked Choccy's",
        'Wonka Bar - Triple Dazzle Caramel': "Wicked Choccy's",
        'Laffy Taffy': 'Sugar Shack', 'SweeTARTS': 'Sugar Shack',
        'Nerds': 'Sugar Shack', 'Fun Dip': 'Sugar Shack',
        'Fizzy Lifting Drinks': 'Sugar Shack',
        'Everlasting Gobstopper': 'Secret Factory',
        'Hair Toffee': 'The Other Factory',
        'Lickable Wallpaper': 'Secret Factory',
        'Wonka Gum': 'Secret Factory',
        'Kazookles': 'The Other Factory'
    }
    df['Factory'] = df['Product Name'].map(factory_map).fillna('Unknown')
    df['Profit Margin %'] = (df['Gross Profit'] / df['Sales'] * 100).round(1)
    return df

df = load_data()

MONTH_ORDER = ['January','February','March','April','May','June',
               'July','August','September','October','November','December']
COLORS = ['#7C3AED','#EC4899','#F59E0B','#10B981','#3B82F6','#EF4444','#8B5CF6']

# ── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.markdown("## 🍬 Nassau Candy")
st.sidebar.markdown("### 📄 Navigation")
page = st.sidebar.radio("", [
    "🏠 Executive Summary",
    "🏭 Factory Performance",
    "🚚 Shipping Analysis",
    "📦 Product Analytics",
    "🎯 What-If Analysis"
])
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔽 Filters")
divisions  = st.sidebar.multiselect("Division",  sorted(df['Division'].dropna().unique()),  default=list(df['Division'].dropna().unique()))
regions    = st.sidebar.multiselect("Region",    sorted(df['Region'].dropna().unique()),    default=list(df['Region'].dropna().unique()))
ship_modes = st.sidebar.multiselect("Ship Mode", sorted(df['Ship Mode'].dropna().unique()), default=list(df['Ship Mode'].dropna().unique()))
years      = st.sidebar.multiselect("Year",      sorted(df['Year'].unique()),               default=list(df['Year'].unique()))

dff = df[df['Division'].isin(divisions) & df['Region'].isin(regions) &
         df['Ship Mode'].isin(ship_modes) & df['Year'].isin(years)]

st.sidebar.markdown("---")
st.sidebar.markdown(f"📊 **Records:** {len(dff):,}")
st.sidebar.markdown("👤 **Built by:** Saroj")
st.sidebar.markdown("🎓 **Unified Mentor | July 2026**")

# ── Helper ───────────────────────────────────────────────────────────────────
def kpi(col, val, label):
    with col:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-value">{val}</div>
            <div class="metric-label">{label}</div>
        </div>""", unsafe_allow_html=True)

def chart_layout(fig, h=400):
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.2)',
                      font_color='white', height=h)
    return fig

# ════════════════════════════════════════════════════════════════════════════
# PAGE 1 — EXECUTIVE SUMMARY
# ════════════════════════════════════════════════════════════════════════════
if page == "🏠 Executive Summary":
    st.markdown('<p class="page-title">🍬 Nassau Candy Distributor</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Factory Reallocation & Shipping Optimization Analytics</p>', unsafe_allow_html=True)

    tot_sales  = dff['Sales'].sum()
    tot_orders = dff['Order ID'].nunique()
    margin     = dff['Gross Profit'].sum() / tot_sales * 100 if tot_sales else 0
    avg_lt     = dff['Lead Time (Days)'].mean()

    c1,c2,c3,c4 = st.columns(4)
    kpi(c1, f"${tot_sales/1000:.0f}K", "💰 Total Sales")
    kpi(c2, f"{tot_orders/1000:.0f}K",  "📦 Total Orders")
    kpi(c3, f"{margin:.1f}%",           "📈 Profit Margin %")
    kpi(c4, f"{avg_lt:.2f}",            "🚚 Avg Lead Time (days)")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown('<p class="section-header">📊 Total Sales & Profit by Month</p>', unsafe_allow_html=True)
        monthly = dff.groupby(['Month Num','Month Name']).agg(
            Sales=('Sales','sum'), Profit=('Gross Profit','sum')).reset_index().sort_values('Month Num')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=monthly['Month Name'], y=monthly['Sales'],
                                 name='Total Sales', line=dict(color='#7C3AED', width=3), mode='lines+markers'))
        fig.add_trace(go.Scatter(x=monthly['Month Name'], y=monthly['Profit'],
                                 name='Total Profit', line=dict(color='#EC4899', width=3), mode='lines+markers'))
        fig.update_xaxes(
            categoryorder='array', categoryarray=MONTH_ORDER,
            title_text='Month', title_font=dict(color='#F0ABFC', size=13),
            tickfont=dict(color='#E9D5FF', size=11)
        )
        fig.update_yaxes(
            title_text='Amount ($)', title_font=dict(color='#F0ABFC', size=13),
            tickfont=dict(color='#E9D5FF', size=11),
            tickprefix='$'
        )
        fig.update_layout(legend=dict(
            font=dict(color='#E9D5FF'), bgcolor='rgba(0,0,0,0.3)',
            bordercolor='#7C3AED', borderwidth=1
        ))
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    with col2:
        st.markdown('<p class="section-header">🍩 Sales by Division</p>', unsafe_allow_html=True)
        div_s = dff.groupby('Division')['Sales'].sum().reset_index()
        fig2 = px.pie(div_s, values='Sales', names='Division',
                      color_discrete_sequence=COLORS, hole=0.5, template='plotly_dark')
        st.plotly_chart(chart_layout(fig2), use_container_width=True)

    st.markdown('<p class="section-header">📊 Total Orders by Ship Mode</p>', unsafe_allow_html=True)
    sm = dff.groupby('Ship Mode')['Order ID'].nunique().reset_index()
    sm.columns = ['Ship Mode','Orders']
    fig3 = px.bar(sm, x='Orders', y='Ship Mode', orientation='h',
                  color='Ship Mode', color_discrete_sequence=COLORS, template='plotly_dark', text='Orders')
    fig3.update_traces(textposition='outside')
    fig3.update_layout(showlegend=False)
    fig3.update_xaxes(title_text='Number of Orders',
        title_font=dict(color='#F0ABFC',size=13), tickfont=dict(color='#E9D5FF',size=11))
    fig3.update_yaxes(title_text='Ship Mode',
        title_font=dict(color='#F0ABFC',size=13), tickfont=dict(color='#E9D5FF',size=11))
    st.plotly_chart(chart_layout(fig3, 300), use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 2 — FACTORY PERFORMANCE
# ════════════════════════════════════════════════════════════════════════════
elif page == "🏭 Factory Performance":
    st.markdown('<p class="page-title">🏭 Factory Performance Analysis</p>', unsafe_allow_html=True)

    coords = pd.DataFrame({
        'Factory':   ["Lot's O' Nuts","Wicked Choccy's",'Sugar Shack','Secret Factory','The Other Factory'],
        'Latitude':  [32.881893, 32.076176, 48.11914, 41.446333, 35.1175],
        'Longitude': [-111.768036,-81.088371,-96.18115,-90.565487,-89.971107]
    })
    fs = dff.groupby('Factory').agg(
        Total_Sales=('Sales','sum'), Avg_LT=('Lead Time (Days)','mean'),
        Orders=('Order ID','nunique')).reset_index()
    fd = coords.merge(fs, on='Factory', how='left').fillna(0)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="section-header">🗺️ Factory Locations across USA</p>', unsafe_allow_html=True)
        fig_map = px.scatter_mapbox(fd, lat='Latitude', lon='Longitude',
            size='Total_Sales', color='Factory', hover_name='Factory',
            hover_data={'Total_Sales':':.0f','Avg_LT':':.2f'},
            size_max=40, zoom=3, mapbox_style='carto-darkmatter',
            color_discrete_sequence=COLORS)
        fig_map.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white',
                              height=350, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig_map, use_container_width=True)

    with col2:
        st.markdown('<p class="section-header">💰 Total Sales by Factory</p>', unsafe_allow_html=True)
        fig_s = px.bar(fs.sort_values('Total_Sales'), x='Total_Sales', y='Factory',
                       orientation='h', color='Factory', color_discrete_sequence=COLORS,
                       template='plotly_dark', text='Total_Sales')
        fig_s.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
        fig_s.update_layout(showlegend=False)
        fig_s.update_xaxes(title_text='Total Sales ($)',
            title_font=dict(color='#F0ABFC',size=13), tickfont=dict(color='#E9D5FF',size=11))
        fig_s.update_yaxes(title_text='Factory',
            title_font=dict(color='#F0ABFC',size=13), tickfont=dict(color='#E9D5FF',size=11))
        st.plotly_chart(chart_layout(fig_s, 350), use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<p class="section-header">⏱️ Avg Lead Time by Factory</p>', unsafe_allow_html=True)
        fig_lt = px.bar(fs.sort_values('Avg_LT'), x='Avg_LT', y='Factory',
                        orientation='h', color='Factory', color_discrete_sequence=COLORS,
                        template='plotly_dark', text='Avg_LT')
        fig_lt.update_traces(texttemplate='%{text:.1f} days', textposition='outside')
        fig_lt.update_layout(showlegend=False)
        fig_lt.update_xaxes(title_text='Avg Lead Time (Days)',
            title_font=dict(color='#F0ABFC',size=13), tickfont=dict(color='#E9D5FF',size=11))
        fig_lt.update_yaxes(title_text='Factory',
            title_font=dict(color='#F0ABFC',size=13), tickfont=dict(color='#E9D5FF',size=11))
        st.plotly_chart(chart_layout(fig_lt), use_container_width=True)

    with col4:
        st.markdown('<p class="section-header">📋 Product Performance by Factory</p>', unsafe_allow_html=True)
        matrix = dff.groupby(['Product Name','Factory'])['Sales'].sum().reset_index()
        pivot  = matrix.pivot(index='Product Name', columns='Factory', values='Sales').fillna(0)
        pivot['Total'] = pivot.sum(axis=1)
        st.dataframe(pivot.sort_values('Total',ascending=False)
                     .style.format('${:,.0f}'),
                     use_container_width=True, height=350)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 3 — SHIPPING ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
elif page == "🚚 Shipping Analysis":
    st.markdown('<p class="page-title">🚚 Shipping Analysis</p>', unsafe_allow_html=True)

    avg_lt    = dff['Lead Time (Days)'].mean()
    tot_ord   = dff['Order ID'].nunique()
    slow      = dff[dff['Shipping Speed']=='Slow']['Order ID'].nunique()
    slow_pct  = slow / tot_ord * 100 if tot_ord else 0

    c1,c2,c3,c4 = st.columns(4)
    kpi(c1, f"{avg_lt:.2f}",      "⏱️ Avg Lead Time")
    kpi(c2, f"{slow:,}",          "🐌 Slow Shipments")
    kpi(c3, f"{slow_pct:.1f}%",   "📊 Slow Shipment %")
    kpi(c4, f"{tot_ord/1000:.0f}K","📦 Total Orders")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="section-header">📊 Avg Lead Time by Ship Mode</p>', unsafe_allow_html=True)
        lt_sm = dff.groupby('Ship Mode')['Lead Time (Days)'].mean().reset_index()
        fig = px.bar(lt_sm, x='Lead Time (Days)', y='Ship Mode', orientation='h',
                     color='Ship Mode', color_discrete_sequence=COLORS,
                     template='plotly_dark', text='Lead Time (Days)')
        fig.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig.update_layout(showlegend=False)
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    with col2:
        st.markdown('<p class="section-header">🍩 Orders by Shipping Speed</p>', unsafe_allow_html=True)
        spd = dff.groupby('Shipping Speed')['Order ID'].nunique().reset_index()
        fig2 = px.pie(spd, values='Order ID', names='Shipping Speed',
                      color_discrete_sequence=COLORS, hole=0.5, template='plotly_dark')
        st.plotly_chart(chart_layout(fig2), use_container_width=True)

    st.markdown('<p class="section-header">🗺️ Regional Shipping Performance by Ship Mode</p>', unsafe_allow_html=True)
    reg_sm = dff.groupby(['Region','Ship Mode'])['Lead Time (Days)'].mean().reset_index()
    fig3 = px.bar(reg_sm, x='Region', y='Lead Time (Days)', color='Ship Mode',
                  barmode='group', color_discrete_sequence=COLORS, template='plotly_dark',
                  labels={'Lead Time (Days)':'Avg Lead Time (Days)','Region':'Region'})
    fig3.update_xaxes(title_text='Region',
        title_font=dict(color='#F0ABFC',size=13), tickfont=dict(color='#E9D5FF',size=11))
    fig3.update_yaxes(title_text='Avg Lead Time (Days)',
        title_font=dict(color='#F0ABFC',size=13), tickfont=dict(color='#E9D5FF',size=11))
    fig3.update_layout(legend=dict(font=dict(color='#E9D5FF'),
        bgcolor='rgba(0,0,0,0.3)',bordercolor='#7C3AED',borderwidth=1))
    st.plotly_chart(chart_layout(fig3, 350), use_container_width=True)

    st.markdown('<p class="section-header">📊 Total Sales by Region and Ship Mode</p>', unsafe_allow_html=True)
    reg_sales = dff.groupby(['Region','Ship Mode'])['Sales'].sum().reset_index()
    fig4 = px.bar(reg_sales, x='Sales', y='Region', color='Ship Mode',
                  orientation='h', barmode='stack',
                  color_discrete_sequence=COLORS, template='plotly_dark')
    fig4.update_xaxes(title_text='Total Sales ($)',
        title_font=dict(color='#F0ABFC',size=13), tickfont=dict(color='#E9D5FF',size=11))
    fig4.update_yaxes(title_text='Region',
        title_font=dict(color='#F0ABFC',size=13), tickfont=dict(color='#E9D5FF',size=11))
    fig4.update_layout(legend=dict(font=dict(color='#E9D5FF'),
        bgcolor='rgba(0,0,0,0.3)',bordercolor='#7C3AED',borderwidth=1))
    st.plotly_chart(chart_layout(fig4, 350), use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 4 — PRODUCT ANALYTICS
# ════════════════════════════════════════════════════════════════════════════
elif page == "📦 Product Analytics":
    st.markdown('<p class="page-title">📦 Product Analytics</p>', unsafe_allow_html=True)

    tot_s = dff['Sales'].sum()
    tot_p = dff['Gross Profit'].sum()
    mgn   = tot_p / tot_s * 100 if tot_s else 0
    tot_u = dff['Units'].sum()

    c1,c2,c3,c4 = st.columns(4)
    kpi(c1, f"${tot_s/1000:.0f}K", "💰 Total Sales")
    kpi(c2, f"${tot_p/1000:.1f}K", "💵 Total Profit")
    kpi(c3, f"{mgn:.1f}%",         "📈 Profit Margin %")
    kpi(c4, f"{tot_u/1000:.0f}K",  "📦 Total Units")
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="section-header">🏆 Top 10 Products by Sales</p>', unsafe_allow_html=True)
        top10 = dff.groupby('Product Name')['Sales'].sum().nlargest(10).reset_index()
        fig = px.bar(top10, x='Sales', y='Product Name', orientation='h',
                     color='Sales', color_continuous_scale='Purples',
                     template='plotly_dark', text='Sales')
        fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
        fig.update_layout(yaxis=dict(categoryorder='total ascending'), showlegend=False)
        fig.update_xaxes(title_text='Total Sales ($)',
            title_font=dict(color='#F0ABFC',size=13), tickfont=dict(color='#E9D5FF',size=11))
        fig.update_yaxes(title_text='Product Name',
            title_font=dict(color='#F0ABFC',size=13), tickfont=dict(color='#E9D5FF',size=11))
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    with col2:
        st.markdown('<p class="section-header">🌳 Sales by Division</p>', unsafe_allow_html=True)
        tree = dff.groupby(['Division','Product Name'])['Sales'].sum().reset_index()
        fig2 = px.treemap(tree, path=['Division','Product Name'], values='Sales',
                          color='Sales', color_continuous_scale='Purples',
                          template='plotly_dark')
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white', height=400)
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<p class="section-header">📊 Profit Margin % by Product</p>', unsafe_allow_html=True)
        pm = dff.groupby('Product Name').agg(S=('Sales','sum'),P=('Gross Profit','sum')).reset_index()
        pm['Margin %'] = (pm['P']/pm['S']*100).round(1)
        fig3 = px.bar(pm.sort_values('Margin %'), x='Margin %', y='Product Name',
                      orientation='h', color='Margin %',
                      color_continuous_scale='RdYlGn', template='plotly_dark', text='Margin %')
        fig3.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig3.update_layout(showlegend=False)
        fig3.update_xaxes(title_text='Profit Margin (%)',
            title_font=dict(color='#F0ABFC',size=13), tickfont=dict(color='#E9D5FF',size=11))
        fig3.update_yaxes(title_text='Product Name',
            title_font=dict(color='#F0ABFC',size=13), tickfont=dict(color='#E9D5FF',size=11))
        st.plotly_chart(chart_layout(fig3), use_container_width=True)

    with col4:
        st.markdown('<p class="section-header">📋 Product Performance Matrix</p>', unsafe_allow_html=True)
        perf = dff.groupby('Product Name').agg(
            Total_Cost=('Cost','sum'), Total_Sales=('Sales','sum'),
            Gross_Profit=('Gross Profit','sum')).reset_index()
        perf['Margin %'] = (perf['Gross_Profit']/perf['Total_Sales']*100).round(1)
        perf = perf.sort_values('Total_Sales', ascending=False)
        st.dataframe(
            perf.style.format({'Total_Cost':'${:,.2f}','Total_Sales':'${:,.0f}','Gross_Profit':'${:,.2f}','Margin %':'{:.1f}%'}),
            use_container_width=True, height=400)

# ════════════════════════════════════════════════════════════════════════════
# PAGE 5 — WHAT-IF ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
elif page == "🎯 What-If Analysis":
    st.markdown('<p class="page-title">🎯 What-If Scenario Analysis</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Simulate the impact of lead time reduction on profit</p>', unsafe_allow_html=True)

    reduction = st.slider("🎚️ Lead Time Reduction (%)", 0, 50, 0, 5, format="%d%%")
    rf = reduction / 100

    avg_lt   = dff['Lead Time (Days)'].mean()
    tot_prof = dff['Gross Profit'].sum()
    sim_lt   = avg_lt * (1 - rf)
    sim_prof = tot_prof * (1 + rf * 0.3)
    gain     = sim_prof - tot_prof
    days_saved = avg_lt - sim_lt

    c1,c2,c3,c4 = st.columns(4)
    kpi(c1, f"{avg_lt:.2f}",           "⏱️ Current Lead Time")
    kpi(c2, f"{sim_lt:.2f}",           "⚡ Simulated Lead Time")
    kpi(c3, f"${tot_prof/1000:.1f}K",  "💰 Current Profit")
    kpi(c4, f"${sim_prof/1000:.1f}K",  "🚀 Simulated Profit")
    st.markdown("<br>", unsafe_allow_html=True)

    col5, col6 = st.columns(2)
    with col5:
        st.success(f"⏱️ **Days Saved:** {days_saved:.2f} days per order")
    with col6:
        st.success(f"💵 **Extra Profit:** ${gain:,.0f}  (+{reduction*0.3:.1f}% increase)")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="section-header">📊 Lead Time: Current vs Simulated by Factory</p>', unsafe_allow_html=True)
        flt = dff.groupby('Factory')['Lead Time (Days)'].mean().reset_index()
        flt['Simulated'] = flt['Lead Time (Days)'] * (1 - rf)
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Current', x=flt['Lead Time (Days)'], y=flt['Factory'],
                             orientation='h', marker_color='#7C3AED'))
        fig.add_trace(go.Bar(name='Simulated', x=flt['Simulated'], y=flt['Factory'],
                             orientation='h', marker_color='#EC4899'))
        fig.update_layout(
            barmode='group', template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.2)',
            font_color='white',
            legend=dict(
                title='Lead Time', font=dict(color='#E9D5FF'),
                bgcolor='rgba(0,0,0,0.3)', bordercolor='#7C3AED', borderwidth=1
            )
        )
        fig.update_xaxes(
            title_text='Lead Time (Days)',
            title_font=dict(color='#F0ABFC', size=13),
            tickfont=dict(color='#E9D5FF', size=11)
        )
        fig.update_yaxes(
            title_text='Factory',
            title_font=dict(color='#F0ABFC', size=13),
            tickfont=dict(color='#E9D5FF', size=11)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<p class="section-header">💰 Profit Impact by Reduction Scenario</p>', unsafe_allow_html=True)
        sc = pd.DataFrame({'Reduction %': [0,10,20,30,40,50],
                           'Simulated Profit': [tot_prof*(1+r/100*0.3) for r in [0,10,20,30,40,50]]})
        fig2 = px.line(sc, x='Reduction %', y='Simulated Profit', markers=True,
                       color_discrete_sequence=['#EC4899'], template='plotly_dark')
        fig2.add_hline(y=tot_prof, line_dash='dash', line_color='#7C3AED',
                       annotation_text='Current Profit')
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.2)',
                           font_color='white')
        fig2.update_xaxes(title_text='Lead Time Reduction (%)',
            title_font=dict(color='#F0ABFC',size=13), tickfont=dict(color='#E9D5FF',size=11))
        fig2.update_yaxes(title_text='Simulated Profit ($)',
            title_font=dict(color='#F0ABFC',size=13), tickfont=dict(color='#E9D5FF',size=11),
            tickprefix='$')
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<p class="section-header">📋 Recommendation Table</p>', unsafe_allow_html=True)
    rec = dff.groupby('Product Name').agg(
        Total_Sales=('Sales','sum'), Margin=('Profit Margin %','mean'),
        Lead_Time=('Lead Time (Days)','mean'), Factory=('Factory','first')).reset_index()
    rec['Simulated LT']     = (rec['Lead_Time'] * (1-rf)).round(2)
    rec['Recommendation']   = rec['Margin'].apply(
        lambda x: '✅ Keep' if x > 60 else ('⚠️ Review' if x > 30 else '❌ Reallocate'))
    rec = rec.sort_values('Total_Sales', ascending=False)
    st.dataframe(
        rec[['Product Name','Factory','Lead_Time','Simulated LT','Margin','Total_Sales','Recommendation']]
        .rename(columns={'Lead_Time':'Lead Time','Margin':'Margin %','Total_Sales':'Sales'})
        .style.format({'Lead Time':'{:.1f}','Simulated LT':'{:.2f}','Margin %':'{:.1f}%','Sales':'${:,.0f}'}),
        use_container_width=True, height=400)

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""<p style='text-align:center;color:#C084FC;font-size:0.9rem;'>
🍬 Nassau Candy Distributor Analytics | Built by Saroj | Unified Mentor Program | July 2026
</p>""", unsafe_allow_html=True)
