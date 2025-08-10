# app.py
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from dbp import db

# Page Config
st.set_page_config(page_title="Flight Analytics Dashboard", layout="wide")

# Initialize database
db1 = db()

# Sidebar
st.sidebar.title("✈️ Flight Analytics")
useroption = st.sidebar.selectbox('📌 Menu', ['Select One', 'Check Flights', 'Analytics'])

if useroption == 'Check Flights':
    st.title("🔍 Check Flights")
    st.markdown("Select **Source** and **Destination** to view available flights.")
    col1, col2 = st.columns(2)

    # Fetch city list
    city = db1.fetchcityname()

    with col1:
        source = st.selectbox("🌆 Source", sorted(city))
    with col2:
        dest = st.selectbox("🏙 Destination", sorted(city))

    if st.button("🚀 Search Flights", use_container_width=True):
        result = db1.fetchallflight(source, dest)
        st.dataframe(result, use_container_width=True)

elif useroption == 'Analytics':
    st.title("📊 Flight Data Analytics")
    st.markdown("A visual overview of flight trends, busiest airports, and pricing.")

    # --- Row 1: Pie Chart ---
    airline, freq = db1.fetchairlinefreq()
    fig_pie = px.pie(
        names=airline,
        values=freq,
        title="✈️ Flights by Airline",
        hole=0.35,
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig_pie.update_traces(textinfo='value+percent', pull=[0.05]*len(airline))
    st.plotly_chart(fig_pie, use_container_width=True)

    # --- Row 2: Two Charts Side by Side ---
    col1, col2 = st.columns(2)

    with col1:
        city, freq1 = db1.busyairport()
        fig_bar = px.bar(
            x=city,
            y=freq1,
            labels={'x': 'City', 'y': 'Frequency'},
            title="🏆 Busiest Airports",
            text=freq1,
            color=freq1,
            color_continuous_scale="Blues"
        )
        fig_bar.update_traces(marker_line_color='black', marker_line_width=1)
        st.plotly_chart(fig_bar, theme='streamlit', use_container_width=True)

    with col2:
        airline_avg, avg_price = db1.avgprice_per_airline()
        fig_avg_price = px.bar(
            x=airline_avg,
            y=avg_price,
            labels={'x': 'Airline', 'y': 'Average Price'},
            title="💰 Average Ticket Price per Airline",
            text=avg_price,
            color=avg_price,
            color_continuous_scale="Oranges"
        )
        fig_avg_price.update_traces(marker_line_color='black', marker_line_width=1)
        st.plotly_chart(fig_avg_price, theme='streamlit', use_container_width=True)

    # --- Row 3: Pie Chart Flights per Class ---
    st.markdown("---")
    classes, class_freq = db1.flights_per_class()
    fig_class = px.pie(
        names=classes,
        values=class_freq,
        title="🎟 Flights per Class",
        hole=0.3,
        color_discrete_sequence=px.colors.sequential.Aggrnyl
    )
    fig_class.update_traces(textinfo='value+percent', pull=[0.05]*len(classes))
    st.plotly_chart(fig_class, use_container_width=True)

else:
    st.title("ℹ️ About the Project")
    st.markdown("""
    This dashboard provides **interactive analytics** for flight data, including:
    - Most frequent airlines
    - Busiest airports
    - Average ticket prices
    - Class distribution

    Built with **Streamlit** and **Plotly** for interactive, real-time insights.
    """)

