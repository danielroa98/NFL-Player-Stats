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
latest_season = int(date.strftime("%Y"))

# Selecting a season to analyze
season_to_analyze = st.sidebar.selectbox(
    'Season', reversed(list(range(1980, latest_season))))

st.sidebar.subheader("Sorting data")

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ['About', 'General stats', 'NFL Average', 'Team Average', 'Player Analysis'])

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
age_filter = st.sidebar.multiselect(
    'Player age', sort_player_ages, sort_player_ages)

# Applying the data filter
filtered_df = player_stats[(player_stats['Tm'].isin(selected_team)) & (
    player_stats['Pos'].isin(selected_pos)) & (player_stats['Age'].isin(age_filter))]

# Function definitions


def league_avg(player_df: pd.DataFrame):
    temp_df = pd.DataFrame(columns=player_df.columns)
    temp_series = player_df.mean()

    temp_df = temp_df.append(temp_series, ignore_index=True)
    temp_df.drop(labels=["Player", "Tm", "Pos", "QBrec"], inplace=True, axis=1)
    return temp_df


def team_avg(player_df, team):
    temp_df = pd.DataFrame(columns=player_df.columns)

    temp_tm_df = pd.DataFrame(columns=player_df.columns)
    temp_tm_df = player_df.loc[player_df['Tm'] == team]
    temp_series = temp_tm_df.mean()

    temp_df = temp_df.append(temp_series, ignore_index=True)
    temp_df.drop(labels=["Player", "Tm", "Pos", "QBrec"], inplace=True, axis=1)

    return temp_df


def player_information(player_df, player_name):
    temp_df = pd.DataFrame(columns=player_df.columns)

    temp_tm_df = pd.DataFrame(columns=player_df.columns)
    temp_tm_df = player_df.loc[player_df["Player"] == player_name]

    temp_df = temp_df.append(temp_tm_df, ignore_index=True)
    temp_df.drop(labels=["Player", "Tm", "Pos"], inplace=True, axis=1)

    return temp_df


# Tabs
# About
with tab1:
    st.markdown("""
    ## About this section

    The main usage for the _Passing_ section is to better understand and analyze passing statistics players had during a season.

    Just as the other sections, it may be from a past or current season.

    ## About the data

    ## How can I filter the data?

    As far as _Passing_ goes, it uses the same parameters as the other sections, you can filter by the following attributes:
    * Season
        * The seasons range from 1980 to the current season.
            * As an additional note, __

    """)

# General stats
with tab2:
    st.markdown("### Displaying player stats with the selected filters")
    st.dataframe(filtered_df)

    avg_t1, avg_t2, avg_t3 = st.tabs(
        ["Best player in _Passing_", "Best player by position", '"Worst" player in _Passing_'])

    with avg_t1:
        st.markdown("### Player with the most _Yards Gained by Passing_")

        # Best player regarding the yards gained
        best_player_yds = player_stats.iloc[player_stats["Yds"].idxmax()]
        player_name = best_player_yds["Player"]
        player_yds = best_player_yds["Yds"]

        st.markdown(
            f"The best player is __{player_name}__ with __{player_yds}__ _Yards Gained by Passing_")
        st.dataframe(best_player_yds, use_container_width=True)

        today = datetime.now()
        today_frmt = today.strftime("%d/%m/%Y")
        st.markdown(
            f"This was updated in real time, so it means it updates at the same time as you view the data, just check the date 🗓️ {today_frmt}.")

    with avg_t2:
        st.markdown(""" 
        ### Best player by position
        
        Work in progress
        """)

    with avg_t3:
        st.markdown('''
        ### "Worst" player in passing
        
        Work in progress
        ''')

# NFL average
with tab3:
    avg_nfl_stats = league_avg(player_df=player_stats)

    st.markdown(
        f"### Passing average in the NFL in the {season_to_analyze} season")

    st.dataframe(avg_nfl_stats, use_container_width=True)

    st.markdown(f"#### Graph of the NFL in the {season_to_analyze} season")
    st.markdown("Pending minor fixes")
    # plot_title = f"League stats for the {season_to_analyze} season"
    # plt.figure()
    # sns.set(rc={'figure.figsize':(20,12)})
    # ax = sns.barplot(data=avg_nfl_stats).set(title=plot_title)
    # st.pyplot()

# Team averages
with tab4:
    st.markdown("### Select a team you'd like to visualize")

    raw_team_list = list(player_stats["Tm"].unique())
    team_lst = sorted(raw_team_list)

    selected_team = st.selectbox("Select a team from the box:", team_lst)

    avg_tm_stats = team_avg(player_df=player_stats, team=selected_team)

    st.markdown(f"#### Average statistics for {selected_team}")
    st.dataframe(avg_tm_stats)

    tm_title = f"{selected_team} average"

    st.markdown("Pending minor fixes in the graph")

    # st.markdown(f"#### Viewing stats for {selected_team}")
    # plt.figure()
    # sns.barplot(data=avg_tm_stats).set(title=tm_title)
    # st.pyplot()

with tab5:
    st.markdown("### Which player would you like to visualize?")

    raw_player_list = list(player_stats["Player"].unique())
    player_list = sorted(raw_player_list)

    selected_player = st.selectbox("Select a player", player_list)

    player_info = player_information(player_df=player_stats, player_name=selected_player)

    st.markdown(f"#### Statistics for {selected_player}")
    st.dataframe(player_info, use_container_width=True)

# Warning removal
st.set_option('deprecation.showPyplotGlobalUse', False)
