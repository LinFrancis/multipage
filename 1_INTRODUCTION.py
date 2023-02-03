import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import plotly.express as px
from PIL import Image

st.set_page_config(page_title="R2R DATA EXPLORER", page_icon="🌱", layout="wide", initial_sidebar_state="expanded")

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

##logo
def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://raw.githubusercontent.com/LinFrancis/datatest/main/R2R_RGB_PINK.png);
                background-repeat: no-repeat;
                background-size: 300px 119px;
                padding-top: 1px;
                background-position: 2px 2px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
add_logo()

##MAIN SIDE

#st.title("R2R METRICS DASHBOARD")
st.title("DATA EXPLORER")
#col_x.caption("Information from R2R Surveys until 2022/10/20")
st.markdown('<div style="text-align: justify;"></div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: justify;">R2R is a worldwide Campaign launched in 2021 by the High-Level Champions (HLT). It aims to increase resilience for four billion people living in vulnerable communities in collaboration with partner organizations from around the world while developing tools to support them in their work. The Campaign has developed a people-centred resilience Metrics Framework for non-state actors to report climate resilience actions and to quantify and validate their impact under a common framework. This framework will be opened to public consultation at COP27.</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: justify;"></div>', unsafe_allow_html=True) ##Espacio Texto
st.markdown('<div style="text-align: justify;">The Metrics Framework pursues several objectives at once, playing an essential function for both the Campaign and the global climate action and resilience communities. The Framework is the cornerstone of the R2R Campaign, serving as a guide for partners in taking action and for the HLC Team on how to manage and foster their work. It is composed of two complementary sets of metrics: Quantitative or Magnitude Metrics help estimate the effect size of the impact, fundamentally through the number of beneficiaries reached, and Qualitative or Depth Metrics, which help understand how the partners and their members are contributing to increasing resilience of people vulnerable to climate change, by observing on which key conditions (Resilience Attributes) are they making a change.</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: justify;"></div>', unsafe_allow_html=True) ##Espacio Texto

with st.expander("Summarised view of the Metrics Framework"):
    st.image("Summary_Metrics_R2R_Framework.png")
