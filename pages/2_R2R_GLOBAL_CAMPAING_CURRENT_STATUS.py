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
st.set_page_config(page_title="R2R CAMPAIGN CURRENT STATUS", page_icon="🌱", layout="wide", initial_sidebar_state="expanded")

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

st.write(df)  #GETTING DF CLEAN FORM Data_cleaning.py . It includes GI, PLEDGE;RA

#__________________________________________________________________________________________________________________________________________________________________
# HAZARDS  PLEDGE
#__________________________________________________________________________________________________________________________________________________________________
#Sample size hazards from selection.
df2_sz = df['All_Hazards'].replace(['; ; ; ; ; '], np.nan).dropna()
sz = str(df2_sz.count())
#dataframe to workwith (All data from the selection).
df2 = df['All_Hazards'].str.split(";", expand=True).apply(lambda x: x.str.strip())
df2 = df2.stack().value_counts()
df2 = df2.iloc[1:].sort_index().reset_index(name='Frecuency')  #Check what happend whit blank information.
#creating new columms based in a dictionary
heat_list     = {'Heat stress - lives & livelihoods combined':'Heat','Heat stress - livelihoods (work)':'Heat','Heat stress - lives':'Heat','Extreme heat':'Heat'}
cold_list     = {'Extreme cold':'Cold','Snow and ice':'Cold'}
drought_list  = {'Drought (agriculture focus)':'Drought','Drought (other sectors)':'Drought'}
water_list    = {'Water stress (urban focus)':'Water','Water stress (rural focus)':'Water'}
fire_list     = {'Fire weather (risk of wildfires)':'Fire'}
flooding_list = {'Urban flooding':'Flooding','Riverine flooding':'Flooding','Coastal flooding':'Flooding'}
coastal_list  = {'Other coastal events':'Coastal / Ocean','Oceanic events':'Coastal / Ocean'}
wind_list     = {'Hurricanes/cyclones':'Wind','Extreme wind':'Wind'}
hazard_dictionary = {**heat_list,**cold_list,**drought_list,**water_list,**fire_list,**flooding_list,**coastal_list,**wind_list}
df2['group'] = df2['index'].map(hazard_dictionary)
df2['% hazard'] = ((df2['Frecuency']/df2['Frecuency'].sum())*100).round(1)
#df2 = df2.groupby(['group']).value_counts(normalize=True).sort_index().reset_index(name='%group')
#df2['%group'] = df2['%index']*100

#treemap
#st.write(df2)
fig = px.treemap(df2, path=[px.Constant("Hazards"),'group','index'], values = '% hazard')
fig.update_traces(root_color="lightgray")
fig.update_layout(title_text='Hazards aimed to provide resilience by R2R Partners')
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
fig.add_annotation(x=1, y=0,
                text='Out of '+ sz +' Partners reporting information related to Harzards (Source: All Data. R2R Pledge Attributes Survey)',showarrow=False,
                yshift=-20)
st.plotly_chart(fig)
st.markdown("""---""")
#__________________________________________________________________________________________________________________________________________________________________
# PRIORITY GROUPS PLEDGE
#__________________________________________________________________________________________________________________________________________________________________
#
#Sample size hazards from selection.
df2_sz = df['Priority group'].replace(['; ; ; ; ; '], np.nan).dropna()
sz = str(df2_sz.count())
#dataframe to workwith (All data from the selection).
df2 = df
list = {'g20','g21','g22','g23','g24','g25','g26','g27','g28'} #making a list with all the columns name use in the graph
df2= df2[df2[list].notna()] #cleaning na
pg0 = df2["g20"].mean() #Women and girls
pg1 = df2["g21"].mean() #LGBTQIA+
pg2 = df2["g22"].mean() #Elderly
pg3 = df2["g23"].mean() #Children and Youth
pg4 = df2["g24"].mean() #Disabled
pg5 = df2["g25"].mean() #Indigenous or traditional communities
pg6 = df2["g26"].mean() #Racial, ethnic and/or religious minorities
pg7 = df2["g27"].mean() #Refugees
pg8 = df2["g28"].mean() #Low income communities

s_df2 = pd.DataFrame(dict(
    r=[pg0, pg1, pg2, pg3, pg4, pg5, pg6, pg7, pg8],
    theta=['Women and girls','LGBTQIA+','Elderly','Children and Youth','Disabled','Indigenous or traditional communities','Racial, ethnic and/or religious minorities','Refugees','Low income communities']))
s_fig_ra_general = px.line_polar(s_df2, r='r', theta='theta', line_close=True, title="Priority groups (Only for Individuals Scope)")
s_fig_ra_general.update_traces(line_color='#FF37D5', line_width=1)
s_fig_ra_general.update_traces(fill='toself')
s_fig_ra_general.add_annotation(x=1, y=0,
            text='Out of '+ sz +' Partners reporting information about the Priority Groups pledged to make more resilient',showarrow=False,
            yshift=-60)
st.write(s_fig_ra_general)
st.markdown("""---""")
#__________________________________________________________________________________________________________________________________________________________________
# SCATTER PLOT INLAND. RURAL - All Engagement Scope
#__________________________________________________________________________________________________________________________________________________________________
#
#Data preparation
df2 = df
costal_list = {'g30','g458','g865','g1272','g1679','g2093'}
rural_list  = {'g31','g459','g866','g1273','g1680','g2094'}
df2_costal  = df2[costal_list]
df2_rural   = df2[rural_list ]
df2['costal_average'] = df2_costal.mean(axis=1,numeric_only=True,skipna=True)
df2['rural_average'] = df2_rural.mean(axis=1,numeric_only=True,skipna=True)
df2 = df2[df2['costal_average'].notna()]
df2 = df2[df2['rural_average'].notna()]
df2.rename(columns = {'costal_average':'C', 'rural_average':'R', 'Short name':'Name'}, inplace = True)

#Scatterplot for coastal/rural in individual scope
st.markdown("Scatterplot for coastal/rural in individual scope (Mean of % of all Engagement Scope)")

x = df2['C']
y = df2['R']
z = df2['Name']

fig = plt.figure(figsize=(10, 10))

for i in range(len(df2)):
    plt.scatter(x,y,c='#FF37D5', marker='o')

#plt.title("Individuals' environment ""[%]""",fontsize=14)
plt.xlabel('Inland'+' '*74+'Coastal',fontsize=13)
plt.ylabel('Urban'+' '*49+'Rural',fontsize=13)
plt.gca().spines['top']  .set_visible(False)
plt.gca().spines['right'].set_visible(False)

for i in range(len(df2)):
     plt.text(df2.C[df2.Name ==z[i]],df2.R[df2.Name==z[i]],z[i], fontdict=dict(color='black', alpha=0.5, size=12))

plt.xlim([0, 100])
plt.ylim([0, 100])    #more ideas: https://matplotlib.org/stable/gallery/pie_and_polar_charts/polar_scatter.html

col1, col2, col3 = st.columns((0.4,2.2,0.4))
col2.pyplot(fig)
st.markdown("""---""")
#__________________________________________________________________________________________________________________________________________________________________
# Companies type
#__________________________________________________________________________________________________________________________________________________________________
#
df2 = df['Companies Types'].str.split(";", expand=True).apply(lambda x: x.str.strip())
df2 = df2.stack().value_counts()
df2 = df2.iloc[1:].sort_index().reset_index(name='Frecuency')
df2['Percentaje'] = ((df2['Frecuency']/df2['Frecuency'].sum())*100).round(2)

companies_type_rename_list = {'A. Agriculture, forestry and fishing':'Agriculture, forestry and fishing','B. Mining and quarrying':'Mining and quarrying','C. Manufacturing':'Manufacturing','D. Electricity, gas, steam and air conditioning supply':'Electricity, gas, steam and air conditioning supply','E. Water supply; sewerage, waste management and remediation activities':'Water supply; sewerage, waste management and remediation activities','F. Construction':'Construction','G. Wholesale and retail trade; repair of motor vehicles and motorcycles':'Wholesale and retail trade; repair of motor vehicles and motorcycles','H. Transportation and storage':'Transportation and storage','I. Accommodation and food service activities':'Accommodation and food service activities','J. Information and communication':'Information and communication','K. Financial and insurance activities':'Financial and insurance activities','L. Real estate activities':'Real estate activities','M. Professional, scientific and technical activities':'Professional, scientific and technical activities','N. Administrative and support service activities':'Administrative and support service activities','O. Public administration and defence; compulsory social security':'Public administration and defence; compulsory social security','P. Education':'Education','Q. Human health and social work activities':'Human health and social work activities','R. Arts, entertainment and recreation':'Arts, entertainment and recreation','S. Other service activities':'Other service activities','T. Activities of households as employers; undifferentiated goods- and services-producing activities of households for own use':'Activities of households as employers; undifferentiated goods- and services-producing activities of households for own use','U. Activities of extraterritorial organizations and bodies':'Activities of extraterritorial organizations and bodies'}
df2['index'] = df2['index'].replace(companies_type_rename_list)

fig, ax = plt.subplots()
ax  = sns.barplot(x="Percentaje", y="index", data=df2,label="Types of Companies", color="#FF37D5")
ax.bar_label(ax.containers[0],padding=3)
#ax.set_xlim(right=15)
ax.xaxis.set_major_formatter(mtick.PercentFormatter())
ax.set(ylabel=None)
plt.title('Types of companies as R2R Partners Members', fontsize=13, loc='left')
st.pyplot(fig)
st.markdown("""---""")

#__________________________________________________________________________________________________________________________________________________________________
# Natural Systems
#__________________________________________________________________________________________________________________________________________________________________

df2 = df['Natural Systems Types'].str.split(";", expand=True).apply(lambda x: x.str.strip())
df2 = df2.stack().value_counts()
df2 = df2.iloc[1:].sort_index().reset_index(name='Frecuency')
df2['Percentaje'] = ((df2['Frecuency']/df2['Frecuency'].sum())*100).round(1)

nat_sys_dict ={'T Terrestrial':'Terrestrial','S Subterranean':'Subterranean','SF Subterranean-Freshwater':'Subterranean-Freshwater','SM Subterranean-Marine':'Subterranean-Marine','FT Freshwater-Terrestrial':'Freshwater-Terrestrial','F Freshwater':'Freshwater','FM Freshwater-Marine':'Freshwater-Marine','M Marine':'Marine','MT Marine-Terrestrial':'Marine-Terrestrial','MFT Marine-Freshwater-Terrestrial':'Marine-Freshwater-Terrestrial'}
df2['index'] = df2['index'].replace(nat_sys_dict)

fig, ax = plt.subplots()
ax  = sns.barplot(x="Percentaje", y="index", data=df2,label="Types of Natural Systems", color="#FF37D5")
ax.bar_label(ax.containers[0],padding=3)
#ax.set_xlim(right=70)
ax.xaxis.set_major_formatter(mtick.PercentFormatter())
ax.set(ylabel=None)
plt.title('Types of Natural Systems pledged to have an impact', fontsize=13, loc='left')
st.pyplot(fig)
st.markdown("""---""")
