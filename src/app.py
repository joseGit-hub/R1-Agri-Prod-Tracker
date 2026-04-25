import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os

# Config
st.set_page_config(page_title="R1 Agri-Production", layout="wide")

st.markdown("""
    <style>
           .block-container {
                padding-top: 1rem;
                padding-bottom: 0rem;
                padding-left: 5rem;
                padding-right: 5rem;
            }
    </style>
    """, unsafe_allow_html=True)

def load_data():
    db_path = os.path.join("data-cleaned", "production.db")
    conn = sqlite3.connect(db_path)
    query = 'SELECT "Ecosystem/Croptype", "Geolocation", "Period", "Volume_Metric_Tons", "Year", "Quarter_Type" FROM crop_production'
    df = pd.read_sql(query, conn)
    conn.close()
    
    df = df.rename(columns={
        "Ecosystem/Croptype": "CropType",
        "Volume_Metric_Tons": "Volume",
        "Quarter_Type": "Quarter"
    })
    # Ensure Year is numeric for delta calculations
    df['Year'] = pd.to_numeric(df['Year'])
    return df

df = load_data()

# Sidebar
st.sidebar.header("Data Controls")

view_mode = st.sidebar.radio(
    "Select View Mode",
    ["Detailed Breakdown", "General Totals"],
    help="Detailed shows Irrigated/Rainfed/White/Yellow. General shows only the Palay/Corn totals."
)

if view_mode == "General Totals":
    df_filtered_logic = df[df['CropType'].isin(['Palay', 'Corn'])]
else:
    df_filtered_logic = df[~df['CropType'].isin(['Palay', 'Corn'])]

selected_crop = st.sidebar.multiselect("Specific Crops", options=df_filtered_logic['CropType'].unique(), default=df_filtered_logic['CropType'].unique())
selected_year = st.sidebar.multiselect("Years", options=sorted(df['Year'].unique()), default=df['Year'].unique())

final_df = df_filtered_logic[(df_filtered_logic['CropType'].isin(selected_crop)) & (df_filtered_logic['Year'].isin(selected_year))]

# Main
st.title("🌾 Region I Agri Production Tracker")

tab1, tab2, tab3 = st.tabs(["Executive Summary", "Production Breakdown", "Scenario Simulator"])

with tab1:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        latest_yr = sorted(final_df['Year'].unique())[-1] if not final_df.empty else 0
        prev_yr = latest_yr - 1
        
        current_vol = final_df[final_df['Year'] == latest_yr]['Volume'].sum()
        past_vol = final_df[final_df['Year'] == prev_yr]['Volume'].sum()
        
        if past_vol > 0:
            delta_val = ((current_vol - past_vol) / past_vol) * 100
            st.metric(f"Total Production ({latest_yr})", f"{current_vol:,.2f} MT", f"{delta_val:.2f}% vs {prev_yr}")
        else:
            st.metric(f"Total Production", f"{current_vol:,.2f} MT")
        
        fig_pie = px.pie(final_df, values='Volume', names='CropType', hole=0.4, 
                         title="Composition of Output", color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        yearly_trend = final_df.groupby('Year')['Volume'].sum().reset_index()
        fig_line = px.line(yearly_trend, x='Year', y='Volume', markers=True, title="Production Trend Over Time")
        fig_line.update_traces(line_color='#2E7D32', line_width=3)
        st.plotly_chart(fig_line, use_container_width=True)

with tab2:
    st.subheader("Quarterly & Seasonal Analysis")
    st.markdown("Understanding when the peak harvest periods occur for different crops.")

    col_t2a, col_t2b = st.columns([2, 1])

    with col_t2a:
        quarterly_df = final_df.groupby(['Year', 'Quarter'])['Volume'].sum().reset_index()
        
        fig_quarter = px.bar(
            quarterly_df, 
            x='Year', 
            y='Volume', 
            color='Quarter',
            barmode='group',
            title="Quarterly Performance Comparison",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_quarter, use_container_width=True)

    with col_t2b:
        st.info("""
        **Data Insight:** In Region I, Palay production typically peaks in **Quarter 4** (Main Harvest), while Corn may show different seasonal peaks. Use this chart to identify shifts in harvest timing over the 5-year period.
        """)
        
        st.write("**Volume Summary Table**")
        pivot_df = quarterly_df.pivot(index='Year', columns='Quarter', values='Volume')
        st.dataframe(pivot_df.style.format("{:,.0f}"))

with tab3:
    st.markdown("Use this tool to simulate how changes in farming efficiency would impact total regional output.")
    
    col_s1, col_s2 = st.columns(2)
    
    with col_s1:
        st.subheader("Simulation Parameters")
        yield_boost = st.slider("Projected Yield Improvement (%)", 0, 50, 10, help="Simulate better seeds or irrigation.")
        area_expansion = st.slider("Area Expansion (%)", -20, 20, 0, help="Simulate land conversion or loss.")
    
    # Calculation
    original_val = final_df[final_df['Year'] == latest_yr]['Volume'].sum()
    simulated_val = original_val * (1 + (yield_boost/100)) * (1 + (area_expansion/100))
    net_gain = simulated_val - original_val

    with col_s2:
        st.subheader("Projected Impact")
        st.write(f"Based on your parameters, the projected output for Region I would be:")
        st.title(f"{simulated_val:,.2f} MT")
        st.success(f"Potential Gain: +{net_gain:,.2f} Metric Tons")

    # Visualizing the Gap
    sim_data = pd.DataFrame({
        'Status': ['Current', 'Simulated'],
        'Volume': [original_val, simulated_val]
    })
    fig_sim = px.bar(sim_data, x='Status', y='Volume', color='Status', 
                     color_discrete_map={'Current': 'grey', 'Simulated': '#2E7D32'},
                     title="Current Output vs. Simulated Goal")
    st.plotly_chart(fig_sim, use_container_width=True)

# --- FOOTER ---
st.divider()
st.download_button(
    label="📥 Download Cleaned Data",
    data=final_df.to_csv(index=False),
    file_name=f"R1_Agri_Data_{latest_yr}.csv",
    mime="text/csv",
)