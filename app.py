import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Config
st.set_page_config(page_title="BI Dashboard", layout="wide")

# 2. Baby Pink Custom Theme CSS
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #fce4ec; /* Light Baby Pink Background */
        color: #880e4f; /* Dark Pink Text */
    }
    /* Metrics/Cards */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 2px solid #f8bbd0;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
   /* Sab text ko Dark Maroon kar diya taake saaf nazar aaye */
    h1, h2, h3, p, label, .stMarkdown, span {
        color: #4a041c !important;
        font-weight: bold !important;
        
    /* Fix for Columns background */
    [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] {
        background-color: rgba(255, 255, 255, 0.3);
        padding: 10px;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🌸 Business Analytics")

uploaded_file = st.file_uploader("Upload File (Excel/CSV)", type=["xlsx", "csv"])

if uploaded_file:
    try:
        # Data Loading
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, header=1)
        
        df = df.dropna(how='all', axis=0)
        cols = df.columns.tolist()

        # 3. KPI Metrics
        st.subheader("📌 Quick Summary")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Records", len(df))
        m2.metric("Columns", len(cols))
        m3.metric("Status", "On")
        m4.metric("Live", "2026")

        st.divider()

        # 4. Multi-Graph Layout (Power BI style)
        # Row 1
        r1c1, r1c2 = st.columns(2)
        
        with r1c1:
            st.markdown("### 📈 Volume Trend")
            xt1 = st.selectbox("X-Axis (Trend):", cols, key="xt1")
            yt1 = st.selectbox("Y-Axis (Trend):", cols, key="yt1")
            fig1 = px.area(df, x=xt1, y=yt1, color_discrete_sequence=['#f06292'])
            fig1.update_xaxes(rangeslider_visible=False)
            fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig1, use_container_width=True)

        with r1c2:
            st.markdown("### 📊 Distribution Chart")
            xb = st.selectbox("Category (Bar):", cols, key="xb")
            yb = st.selectbox("Value (Bar):", cols, key="yb")
            fig2 = px.bar(df, x=xb, y=yb, color=xb, color_discrete_sequence=px.colors.qualitative.Pastel)
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig2, use_container_width=True)

        # Row 2
        r2c1, r2c2 = st.columns(2)

        with r2c1:
            st.markdown("### 🍩 Share Analysis")
            xp = st.selectbox("Labels (Pie):", cols, key="xp")
            yp = st.selectbox("Values (Pie):", cols, key="yp")
            fig3 = px.pie(df, names=xp, values=yp if pd.api.types.is_numeric_dtype(df[yp]) else None, hole=0.5)
            fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig3, use_container_width=True)

        with r2c2:
            st.markdown("### 🎯 Target Gauge")
            fig4 = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = len(df),
                gauge = {'bar': {'color': "#ad1457"}, 'axis': {'range': [None, len(df)*1.2]}}
            ))
            fig4.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color': "#880e4f"})
            st.plotly_chart(fig4, use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ Masla Aa Gaya: {e}")
else:
    st.info("Upload file to view dashboard")