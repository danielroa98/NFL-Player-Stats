import base64
import sys
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from datetime import datetime

st.markdown("# Passing stats")
st.sidebar.markdown("# Passing stats")

st.sidebar.markdown("Select a season to analyze")

# Get the current season's year + 1
date = datetime.now()
latest_season = int(date.strftime("%Y")) + 1

# Selecting a season to analyze
season_to_analyze = st.sidebar.selectbox('Season', reversed(list(range(1980, latest_season))))

st.sidebar.subheader("Sorting data")

tab1, tab2, tab3, tab4, tab5 = st.tabs(['About', 'General stats', 'NFL Average', 'Team Average', 'Player Analysis'])

# Web scraping function
# Taken from:
# https://www.pro-football-reference.com/years/{season}/passing.htm
@st.cache(allow_output_mutation=True)
def data_scrape(year: int):
    url = "https://www.pro-football-reference.com/years/" + \
        str(year)+"/passing.htm"
    # Reading the table found in the selected season
    html = pd.read_html(url, header=0)
    passing_df = html[0]
    clean_data = passing_df.drop(passing_df[passing_df.Age == 'Age'].index)
    clean_data = clean_data.fillna(0)
    passing_players = clean_data.drop(["Rk"], axis=1)

    # Replacing the position 0 to No Pos
    passing_players.loc[passing_players['Pos'] == 0, ['Pos']] = "No Pos"

    passing_players.rename(columns={'Yds.1': 'Yds Lost'}, inplace=True)

    # Converting data to numerical values
    passing_players[["Age", "G", "GS", "Cmp", "Att", "Cmp%", "Yds", "TD", "TD%", "Int", "Int%", "1D", "Lng", "Y/A", "AY/A", "Y/C", "Y/G", "Rate", "QBR", "Sk", "Yds Lost", "Sk%", "NY/A", "ANY/A", "4QC", "GWD"]] = passing_players[[
        "Age", "G", "GS", "Cmp", "Att", "Cmp%", "Yds", "TD", "TD%", "Int", "Int%", "1D", "Lng", "Y/A", "AY/A", "Y/C", "Y/G", "Rate", "QBR", "Sk", "Yds Lost", "Sk%", "NY/A", "ANY/A", "4QC", "GWD"]].apply(pd.to_numeric)

    passing_players.reset_index(drop=True, inplace=True)

    return passing_players


player_stats = data_scrape(season_to_analyze)

# Dataframe filtering

# Team selection
unique_team = sorted(player_stats["Tm"].unique())
selected_team = st.sidebar.multiselect("Team", unique_team, unique_team)

# Position filtering
unique_pos = sorted(player_stats["Pos"].unique())
selected_pos = st.sidebar.multiselect("Position", unique_pos, unique_pos)

# Age filtering
sort_player_ages = sorted(player_stats['Age'].unique())
age_filter = st.sidebar.multiselect('Player age', sort_player_ages, sort_player_ages)

# Applying the data filter
df_selected_team = player_stats[(player_stats['Tm'].isin(selected_team)) & (player_stats['Pos'].isin(selected_pos)) & (player_stats['Age'].isin(age_filter))]

# Function definitions


# Tabs
# About
with tab1:
    st.markdown("""
    ## Placeholder

    Doggo ipsum doing me a frighten long woofer blep what a nice floof very good spot pats, sub woofer shoober bork. Lotsa pats woofer snoot pats I am bekom fat h*ck, maximum borkdrive aqua doggo very hand that feed shibe. Big ol you are doin me a concern the neighborhood pupper much ruin diet adorable doggo, aqua doggo such treat tungg long doggo waggy wags, heckin good boys and girls thicc blop. Most angery pupper I have ever seen wow very biscit ruff puggo sub woofer, heckin angery woofer he made many woofs.
    """)
