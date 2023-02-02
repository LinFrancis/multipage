import streamlit as st
import pandas as pd
import numpy as np

#_________________________________________________________________________________________________________________________________________________________________
# Export data
#__________________________________________________________________________________________________________________________________________________________________
#__________________________
#General Information Survey
#__________________________
df_gi = pd.read_csv('GI_27012013.csv',sep=';', header=None, prefix="q").iloc[2:]
df_gi.set_index("q0", inplace = True)
df_gi.index.names = ['Master ID']
df_gi = df_gi.dropna(how = 'all')
df_gi_names = pd.read_csv('GI_27012013.csv',sep=';').iloc[1:]

##rename
df_gi['q37'] = df_gi['q37'].replace(['Poor'], 'Low income communities')
df_gi['q50'] = df_gi['q50'].replace(['Finance'], 'Cross-cutting enablers: Planning and Finance')
df_gi['q51'] = df_gi['q51'].replace(['Food and agriculture system'], 'Food and Agriculture Systems')
df_gi['q52'] = df_gi['q52'].replace(['Ocean and coastal zone'], 'Coastal and Oceanic Systems')
df_gi['q53'] = df_gi['q53'].replace(['Water and land ecosystems'], 'Water and Nature Systems')
df_gi['q54'] = df_gi['q54'].replace(['Cities and human settlements'], 'Human Settlement Systems')
df_gi['q55'] = df_gi['q55'].replace(['Infrastructure and services'], 'Infrastructure Systems')
df_gi.rename(columns = { 'q1':'Initiative_name', 'q2':'Short name'}, inplace = True)
#creating new variables concatenating
df_gi['Region']           = df_gi[['q39','q40','q41','q42','q43','q44','q45','q46','q47','q48']].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_gi['Priority group']   = df_gi[['q29','q30','q31','q32','q33','q34','q35','q36','q37',     ]].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_gi['Impact System']    = df_gi[['q50','q51','q52','q53','q54','q55'                        ]].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)

#__________________________
#Pledge Statement Survey
#__________________________
df_pdg = pd.read_csv('Pledge_27012013.csv',sep=';', header=None, prefix="g").iloc[2:]
df_pdg.set_index("g0", inplace = True)
df_pdg.index.names = ['Master ID']
df_pdg = df_pdg.dropna(how = 'all')
df_pdg_names = pd.read_csv('Pledge_27012013.csv',sep=';').iloc[1:]
##rename
replacement_mapping_dict = {"Not targeted.": "0","2": "1","Mildly targeted but not exclusively.": "2","4": "3",
    "Main or unique target.": "4",}
df_pdg['g28'] = df_pdg['g28'].replace(['Poor'], 'Low income communities')
df_pdg["g20"] = df_pdg["g20"].replace(replacement_mapping_dict) #Women and girls ind
df_pdg["g21"] = df_pdg["g21"].replace(replacement_mapping_dict) #LGBTQIA+ ind
df_pdg["g22"] = df_pdg["g22"].replace(replacement_mapping_dict) #Elderly ind
df_pdg["g23"] = df_pdg["g23"].replace(replacement_mapping_dict) #Children and Youth ind
df_pdg["g24"] = df_pdg["g24"].replace(replacement_mapping_dict) #Disabled ind
df_pdg["g25"] = df_pdg["g25"].replace(replacement_mapping_dict) #Indigenous or traditional communities ind
df_pdg["g26"] = df_pdg["g26"].replace(replacement_mapping_dict) #Racial, ethnic and/or religious minorities ind
df_pdg["g27"] = df_pdg["g27"].replace(replacement_mapping_dict) #Refugees ind
df_pdg["g28"] = df_pdg["g28"].replace(replacement_mapping_dict) #Low income communities ind

##change format
df_pdg["g20"] = pd.to_numeric(df_pdg["g20"]) #Women and girls ind
df_pdg["g21"] = pd.to_numeric(df_pdg["g21"]) #LGBTQIA+ ind
df_pdg["g22"] = pd.to_numeric(df_pdg["g22"]) #Elderly ind
df_pdg["g23"] = pd.to_numeric(df_pdg["g23"]) #Children and Youth ind
df_pdg["g24"] = pd.to_numeric(df_pdg["g24"]) #Disabled ind
df_pdg["g25"] = pd.to_numeric(df_pdg["g25"]) #Indigenous or traditional communities ind
df_pdg["g26"] = pd.to_numeric(df_pdg["g26"]) #Racial, ethnic and/or religious minorities ind
df_pdg["g27"] = pd.to_numeric(df_pdg["g27"]) #Refugees ind
df_pdg["g28"] = pd.to_numeric(df_pdg["g28"]) #Low income communities ind
df_pdg["g30"] = pd.to_numeric(df_pdg["g30"])
df_pdg["g31"] = pd.to_numeric(df_pdg["g31"])
df_pdg["g458"] = pd.to_numeric(df_pdg["g458"])
df_pdg["g459"] = pd.to_numeric(df_pdg["g459"])
df_pdg["g865"] = pd.to_numeric(df_pdg["g865"])
df_pdg["g1272"] = pd.to_numeric(df_pdg["g1272"])
df_pdg["g1273"] = pd.to_numeric(df_pdg["g1273"])
df_pdg["g1679"] = pd.to_numeric(df_pdg["g1679"])
df_pdg["g1680"] = pd.to_numeric(df_pdg["g1680"])
df_pdg["g2093"] = pd.to_numeric(df_pdg["g2093"])
df_pdg["g2094"] = pd.to_numeric(df_pdg["g2094"])
##Creating list of series needed to treat multiquestionsº.
hazard_list_ind         = df_pdg.iloc[:, 32:50].apply(lambda x: x.str.strip()).columns.values.tolist() #Individual Engagement
hazard_list_comp        = df_pdg.iloc[:, 460:478].apply(lambda x: x.str.strip()).columns.values.tolist() #Companies engagement
hazard_list_countries   = df_pdg.iloc[:, 867:885].apply(lambda x: x.str.strip()).columns.values.tolist() #Countries
hazard_list_region      = df_pdg.iloc[:, 1274:1292].apply(lambda x: x.str.strip()).columns.values.tolist() #Regions
hazard_list_cities      = df_pdg.iloc[:, 1681:1699].apply(lambda x: x.str.strip()).columns.values.tolist() #Cities
hazard_list_nat_sys     = df_pdg.iloc[:, 2095:2113].apply(lambda x: x.str.strip()).columns.values.tolist() #Natural Systems
hazards_options         = ['Heat stress - lives & livelihoods combined','Heat stress - livelihoods (work)','Heat stress - lives','Extreme heat','Extreme cold','Snow and ice','Drought (agriculture focus)','Drought (other sectors)','Water stress (urban focus)','Water stress (rural focus)','Fire weather (risk of wildfires)','Urban flooding','Riverine flooding','Coastal flooding','Other coastal events','Oceanic events','Hurricanes/cyclones','Extreme wind']
companies_type_list     = df_pdg.iloc[:, 436:457].apply(lambda x: x.str.strip()).columns.values.tolist()
nat_syst_type_list      = df_pdg.iloc[:, 2079:2089].apply(lambda x: x.str.strip()).columns.values.tolist()


#All Hazards Treatment
df_pdg[hazard_list_ind] = df_pdg[hazard_list_ind].where(df_pdg['g32'] != 'All Hazard', hazards_options)  #Recode "All Hazard" = Apply to all Hazard"
df_pdg[hazard_list_comp] = df_pdg[hazard_list_comp].where(df_pdg['g460'] != 'All Hazard', hazards_options)
df_pdg[hazard_list_countries] = df_pdg[hazard_list_countries].where(df_pdg['g867'] != 'All Hazard', hazards_options)
df_pdg[hazard_list_region] = df_pdg[hazard_list_region].where(df_pdg['g1274'] != 'All Hazard', hazards_options)
df_pdg[hazard_list_cities] = df_pdg[hazard_list_cities].where(df_pdg['g1681'] != 'All Hazard', hazards_options)
df_pdg[hazard_list_nat_sys] = df_pdg[hazard_list_nat_sys].where(df_pdg['g2095'] != 'All Hazard', hazards_options)
#Concatenating columns
df_pdg['Engagement scope'] = df_pdg[['g13','g14','g15','g16','g17','g18']].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_pdg['Hazards_ind'] = df_pdg[hazard_list_ind].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1) #Concatenate
df_pdg['Hazards_comp'] = df_pdg[hazard_list_comp].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_pdg['Hazards_countries'] = df_pdg[hazard_list_countries].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_pdg['Hazards_region'] = df_pdg[hazard_list_region].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_pdg['Hazards_cities'] = df_pdg[hazard_list_cities].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_pdg['Hazards_nat_sys'] = df_pdg[hazard_list_nat_sys].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_pdg['All_Hazards'] = df_pdg[['Hazards_ind','Hazards_comp','Hazards_countries','Hazards_region','Hazards_cities','Hazards_nat_sys']].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_pdg['Companies Types'] = df_pdg[companies_type_list].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_pdg['Natural Systems Types'] = df_pdg[nat_syst_type_list].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
#Confirmation that works!
    #st.write(hazard_list_ind,hazard_list_comp, hazard_list_countries,hazard_list_region,hazard_list_cities,hazard_list_nat_sys)
    #st.table(df_pdg[['g32','Hazards_ind','g460','Hazards_comp','g867','Hazards_countries','g1274','Hazards_region','g1681','Hazards_cities','g2095','Hazards_nat_sys','All_Hazards']])
#continents for indivdual engagement
#table_continents_ind = df_pdg.iloc[:, 52:57] #selecting all columns and making a new dataframe
#v_continents_ind = table_continents_ind.columns.values.tolist() #making a list with the names of the columns
#df_pdg['continents_ind'] = df_pdg[v_continents_ind].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)

#countries for indivdual engagement
#table_countries_ind = df_pdg.iloc[:, 58:243] #selecting all columns and making a new dataframe
#v_countries_ind = table_countries_ind.columns.values.tolist() #making a list with the names of the columns
#df_pdg['countries_ind'] = df_pdg[v_countries_ind].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)

#Plan Statement Survey
df_plan = pd.read_csv('Plan_27012013.csv',sep=';', header=None, prefix="p").iloc[2:]
df_plan.set_index("p0", inplace = True)
df_plan.index.names = ['Master ID']
df_plan = df_plan.dropna(how = 'all')

#confirmar uso de dummy item para vincular encuesta plan. Ver video aquí: https://www.youtube.com/watch?v=iZUH1qlgnys&list=PLtqF5YXg7GLmCvTswG32NqQypOuYkPRUE&index=7

#Resilience Attributes Survey
df_ra = pd.read_csv('RA_27012013.csv',sep=';', header=None, prefix="r").iloc[2:]
df_ra.set_index("r0", inplace = True)
df_ra.index.names = ['Master ID']
df_ra = df_ra.dropna(how = 'all')

#Making one database
df = pd.concat([df_gi,df_pdg,df_ra], axis=1)
df_len = len(df.index)

#st.write(df.shape)
