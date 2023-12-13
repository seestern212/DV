import pandas as pd
import altair as alt
import streamlit as st
import warnings
from pathlib import Path

warnings.filterwarnings('ignore')

st.set_page_config(layout="wide")

alt.data_transformers.enable('default', max_rows=None)

dir = Path(__file__).parent


@st.cache_data
def get_data():
    df = pd.read_csv('wdi_app.csv')
    df['gdp_capita'] = df.gdp / df.population
    return df


df = get_data()

st.title('Life Expectancy Explorer')

with st.sidebar:

    ###################################
    # Filter
    ###################################
    # Choose 1 particular year
    sel_year = st.slider(label="Please pick a year",
                         min_value=1980, max_value=2020, value=2000)

    continents = df.continent[df.continent.notna()].unique()
    sel_continent = st.multiselect(
        label='Please select a continent', options=continents, default='Africa')

    ###################################
    # X/Y-Variable
    ###################################
    
    sel_xvar = st.radio(label='Please select a x-Variable',
                        options = ['GDP per capita in USD', 
                                   'Population', 
                                   'Average number of children per woman', 
                                   'Health expenditure share of GDP'], 
                        horizontal = False)
                        #options=['gdp_capita', 'population', 'fertility', 'health_expenditure_share'], horizontal=False)

    sel_options = ['linear', 'log']
    if sel_xvar == 'population':
        sel_options = ['log']

    sel_x_scale = st.selectbox(
        label='Please select scale of x-axis', options=sel_options)


# Make x- and or y-axis variables selectable

df_filtered = df[(df.year == sel_year) & (df.continent.isin(sel_continent))]

scale_log = 'linear'

# x-axis title dictionary
x_title_dict = {'gdp_capita': 'GDP per capita in USD',
                'population': 'Population',
                'fertility': 'Average number of children per woman',
                'health_expenditure_share': 'Health expenditure share of GDP'}

x_value_dict = { 'GDP per capita in USD' : 'gdp_capita',
                 'Population' : 'population',
                 'Average number of children per woman' : 'fertility',
                 'Health expenditure share of GDP' : 'health_expenditure_share'}


plot = alt.Chart(df_filtered).mark_point().encode(
    x=alt.X(x_value_dict[sel_xvar]).scale(type=sel_x_scale).title(sel_xvar),
    y=alt.Y('life_expectancy').scale(
        zero=False, domain=[40, 90]).title('Life Expectancy in years'),
    color='continent',
    tooltip=['name']
).properties(height=500)

st.altair_chart(plot, use_container_width=True)

st.markdown(
    f"""This app shows the relationship between **{sel_xvar}** and **Life Expectancy**. Currently, you have applied filters to only show: 
    
- _year_: {sel_year}
- countries of the following _continents_: {', '.join(sel_continent)}""")

st.dataframe(df_filtered)
