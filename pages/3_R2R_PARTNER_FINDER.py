import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns


#__________________________________________________________________________________________________________________________________________________________________
# Dashboard structure
#__________________________________________________________________________________________________________________________________________________________________
st.set_page_config(page_title="Explorer", page_icon="🌱", layout="wide", initial_sidebar_state="expanded")

CURRENT_THEME = "light"
IS_DARK_THEME = False

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

##R2R LOGO SIDE BAR
def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://raw.githubusercontent.com/LinFrancis/multiselection/main/R2R_RGB_PINK.png);
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

# Hide index when showing a table. CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

#__________________________________________________________________________________________________________________________________________________________________
# Export data
#__________________________________________________________________________________________________________________________________________________________________
from Data_cleaning import df, df_len

#st.write(df)  #GETTING DF CLEAN FORM Data_cleaning.py . It includes GI, PLEDGE;RA

#__________________________________________________________________________________________________________________________________________________________________
# MULTISELECTOR
#__________________________________________________________________________________________________________________________________________________________________
#
cats_defs = [
    ['Region',['Oceania & Pacific','East Asia','South Asia','East Europe & Central Asia','Northern & Western Europe','North Africa and the Middle East','Sub-Saharan Africa','South America','Central America and Caribbean','North America','']],
    ['Priority group',  ['Women and girls','LGBTQIA+ people','Elderly','Children & Youth','Indigenous and traditional communities','Ethnic or religious minorities','Refugees','Disabled People','Low income communities','']],
    ['Impact System',      ['Cross-cutting enablers: Planning and Finance','Food and Agriculture Systems','Coastal and Oceanic Systems','Water and Nature Systems','Human Settlement Systems','Infrastructure Systems','']],
    ['Engagement scope',['Individuals','Companies','Countries','Regions','Cities','Natural Systems','']],   #extend the tables cats_defs, cats, defs, poss if needed
    ['All Hazards',['Heat stress - lives & livelihoods combined','Heat stress - livelihoods (work)','Heat stress - lives','Extreme heat','Extreme cold','Snow and ice','Drought (agriculture focus)','Drought (other sectors)','Water stress (urban focus)','Water stress (rural focus)','Fire weather (risk of wildfires)','Urban flooding','Riverine flooding','Coastal flooding','Other coastal events','Oceanic events','Hurricanes/cyclones','Extreme wind','']] ]  #extend the tables cats_defs, cats, de

cats = [cats_defs[0][0], cats_defs[1][0]     , cats_defs[2][0]  ,cats_defs[3][0],cats_defs[4][0]       ]  #list of question categories
defs = [cats_defs[0][1], cats_defs[1][1]     , cats_defs[2][1]  ,cats_defs[3][1],cats_defs[4][1]      ]  #list of possible answers
poss = [df['Region']   , df['Priority group'], df['Impact System'] ,df['Engagement scope'],df['All_Hazards']]  #correspoding answers

regions_options = ['Oceania & Pacific','East Asia','South Asia','East Europe & Central Asia','Northern & Western Europe','North Africa and the Middle East','Sub-Saharan Africa','South America','Central America and Caribbean','North America']
priority_options = ['Women and girls','LGBTQIA+ people','Elderly','Children & Youth','Indigenous and traditional communities','Ethnic or religious minorities','Refugees','Disabled People','Low income communities']
areas_options = ['Cross-cutting enablers: Planning and Finance','Food and Agriculture Systems','Coastal and Oceanic Systems','Water and Nature Systems','Human Settlement Systems','Infrastructure Systems']
engagement_options = ['Individuals','Companies','Countries','Regions','Cities','Natural Systems']
hazards_options = ['Heat stress - lives & livelihoods combined','Heat stress - livelihoods (work)','Heat stress - lives','Extreme heat','Extreme cold','Snow and ice','Drought (agriculture focus)','Drought (other sectors)','Water stress (urban focus)','Water stress (rural focus)','Fire weather (risk of wildfires)','Urban flooding','Riverine flooding','Coastal flooding','Other coastal events','Oceanic events','Hurricanes/cyclones','Extreme wind']

st.sidebar.caption("**SELECT R2R PARTNER INFORMATION**")
st.sidebar.caption("If no specific filter is selected, all available information regarding R2R partners will be displayed. Please select filters for a more targeted display.")
#st.sidebar.markdown('**Resiliencia**')
areas_selection = st.sidebar.multiselect("Partner's Impact Systems",      areas_options)
engagement_selection = st.sidebar.multiselect("Partner's Engagement scope", engagement_options)  #add further multiselect if needed
#st.sidebar.markdown('**Vulnerablilidad**')
priority_selection = st.sidebar.multiselect('Priority groups aimed to make more resilient',   priority_options)
#st.sidebar.markdown('**Amenazas**')
hazards_selection = st.sidebar.multiselect('Hazards to provide resilience',   hazards_options)
#st.sidebar.markdown('**Territorialidad**')
macro_region_selection = st.sidebar.multiselect('Macro Regions where they operate',    regions_options)

selection = [macro_region_selection,priority_selection,areas_selection,engagement_selection,hazards_selection]   #extend if more multiselect

i=0
while i < len(selection):
    if len(selection[i])==0:
        selection[i]=defs[i]
    i=i+1

def index_selection_results(sel,col):
        results_index = []
        i=0
        while i < df_len:                  #going over all the rows
            for elem in sel:               #going over all the items in the selection
                if elem in col[i]:         #checking if item is contained in the string
                    results_index.append(i) #saving the correct item fulfilling the selection
            i=i+1
        return results_index

def common_member(a, b):                   #used to intersect any two lists
    result = [i for i in a if i in b]
    return result

final_list = list(range(0,df_len+1))
j = 0
while j < len(selection):
        temp_list  = list(set(index_selection_results(selection[j],poss[j]))) #avoidung index duplications
        final_list = list(set(common_member(temp_list,final_list)))
        j = j+1

df_filtered = df.iloc[final_list].reset_index().sort_values(by = 'Short name')
df_filtered.set_index("Master ID", inplace = True)

#__________________________________________________________________________________________________________________________________________________________________
# MAIN RESULTS
#__________________________________________________________________________________________________________________________________________________________________
#
selection_all = [["Oceania & Pacific","East Asia","South Asia","East Europe & Central Asia","Northern & Western Europe","North Africa and the Middle East","Sub-Saharan Africa","South America","Central America and Caribbean","North America",""],
  ["Women and girls","LGBTQIA+ people","Elderly","Children & Youth","Indigenous and traditional communities","Ethnic or religious minorities","Refugees","Disabled People","Low income communities",""],
  ["Cross-cutting enablers: Planning and Finance","Food and Agriculture Systems","Coastal and Oceanic Systems","Water and Nature Systems","Human Settlement Systems","Infrastructure Systems",""],
  ["Individuals","Companies","Countries","Regions","Cities","Natural Systems",""],
  ["Heat stress - lives & livelihoods combined","Heat stress - livelihoods (work)","Heat stress - lives","Extreme heat","Extreme cold","Snow and ice","Drought (agriculture focus)","Drought (other sectors)","Water stress (urban focus)","Water stress (rural focus)","Fire weather (risk of wildfires)","Urban flooding","Riverine flooding","Coastal flooding","Other coastal events","Oceanic events","Hurricanes/cyclones","Extreme wind",""]]

st.header('R2R DATA EXPLORER V2.0 Trial Fase')
if selection == selection_all:
    st.subheader('**COMPLETE R2R PARTNERS INFORMATION ON DISPLAY**')
else:
    st.subheader('DISPLAYED RESULTS SHOW R2R PARTNERS INFORMATION MEETING ALL SELECTED CRITERIA')

col1,col2,col3,col4 = st.columns((1,1,1,3))
col1.caption('Original dataframe shape')
col1.write(df.shape)
col2.caption('Filtered dataframe shape')
col2.write(df_filtered.shape)
#with st.expander("Review Raw Data"):
st.write(df_filtered[['Initiative_name','Short name','Priority group','Impact System','Engagement scope','Region','All_Hazards']])
st.markdown("""---""")

#_______________________________________________
