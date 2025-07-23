# Packages 
import pandas as pd 
import numpy as np 
import streamlit as st 
import plotly.express as px 
from PIL import Image
import plotly.graph_objects as go 
import altair as alt 
import os

print("CWD:", os.getcwd())
print("Files:", os.listdir("."))
print("Archive files:", os.listdir("archive"))

# Streamlit config
st.set_page_config(
    page_title= "Energy Analysis Dashboard",
    page_icon="🔋", 
    layout= "wide",
    initial_sidebar_state= "expanded"
)

alt.themes.enable("dark")

# Custom CSS for background, font, and animation
st.markdown("""
    <style>
        body {
            background-color: #6a0dad;
            color: white;
        }
        .main {
            background-color: #6a0dad !important;
            color: white;
        }
        h1, h2, h3, h4 {
            color: #f7f7f7;
            font-family: 'Segoe UI', sans-serif;
            font-weight: bold;
        }
        .stApp {
            animation: fadeIn 1.5s ease-in-out;
        }
        @keyframes fadeIn {
            0% {opacity: 0;}
            100% {opacity: 1;}
        }
        .css-1rs6os.edgvbvh3 {
            background-color: #5e0aa3 !important;
        }
        .block-container {
            padding-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Load data and format date
try:
    data = pd.read_csv("archive/Panel_format.csv")
    if data.empty:
        st.error("The data file is empty.")
        st.stop()
    else:
        data["Year"] = pd.to_datetime(data["Year"], format="%Y")
except FileNotFoundError:
    st.error("The file 'archive/Panel_format.csv' was not found. Please check the file path.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while loading the data: {e}")
    st.stop()

# Sidebar
with st.sidebar:
    st.title("🌩️ Energy Dashboard")
    st.markdown("---")

    sidebar_image = Image.open("images/Energy1.jpeg")
    st.image(sidebar_image, use_container_width=True)

    country = st.selectbox("🌍 Select a country:", data["Country"].unique())
    st.markdown("---")
    st.write("This dashboard helps explore trends in energy production across different sources and years.")
    st.markdown("---") 

# Filter data
country_data = data[data["Country"] == country]

# Animated title
st.markdown(f"""
    <h1 style='text-align: center; animation: fadeInUp 2s;'>🔋 Energy Production Time Series Analysis for <span style="color:#FFD700">{country}</span></h1>
    <style>
        @keyframes fadeInUp {{
            0% {{opacity: 0; transform: translateY(20px);}}
            100% {{opacity: 1; transform: translateY(0);}}
        }}
    </style>
""", unsafe_allow_html=True)

st.markdown("""
This dashboard provides a detailed overview of various energy production trends in the selected country. Navigate using the sidebar to choose a different country.
""")

main_image = Image.open("images/Energy.jpg")
st.image(main_image, caption="⚡ Energy Sources", use_container_width=True)

# Charting function
def create_chart(data, y, title, yaxis_title):
    fig = px.line(
        data,
        x="Year",
        y=y,
        title=title,
        markers=True,
        line_shape="spline",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    fig.add_annotation(
        x=data['Year'].iloc[-1], 
        y=data[y].iloc[-1], 
        text="Latest Value", 
        showarrow=True, 
        arrowhead=2,
        font=dict(color="#FF5733", size=12)
    )
    
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title=yaxis_title,
        template='plotly_dark',
        font=dict(family="Arial", size=14, color="#ffffff"),
        title=dict(font=dict(size=20, color="#FFD700")),
        margin=dict(l=0, r=0, t=60, b=0),
        legend=dict(
            title="Legend",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode="x unified",
        xaxis=dict(
            rangeslider=dict(visible=True),
            showline=True,
            linecolor='white',
            mirror=True,
            gridcolor='gray'
        ),
        yaxis=dict(
            showline=True,
            linecolor='white',
            mirror=True,
            gridcolor='gray'
        )
    )

    fig.update_traces(
        hovertemplate='<b>Year</b>: %{x}<br><b>Value</b>: %{y}<extra></extra>'
    )

    st.plotly_chart(fig, use_container_width=True)

# Charts
st.subheader("📈 Population Over Time")
create_chart(country_data, 'pop', 'Population over Time', 'Population')

st.subheader("🌊 Hydro Energy Production Over Time")
create_chart(country_data, 'hydro_ej', 'Hydro Energy Production (Exajoules)', 'Exajoules')

st.subheader("⚛️ Nuclear Energy Production Over Time")
create_chart(country_data, 'nuclear_ej', 'Nuclear Energy Production (Exajoules)', 'Exajoules')

st.subheader("♻️ Renewable Energy Production Over Time")
create_chart(country_data, 'ren_power_ej', 'Renewable Energy Production (Exajoules)', 'Exajoules')

st.subheader("☀️ Solar Energy Production Over Time")
create_chart(country_data, 'solar_ej', 'Solar Energy Production (Exajoules)', 'Exajoules')
