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

# Get the current season's year
date = datetime.now()
latest_season = int(date.strftime("%Y"))

# Implement function to check 
# check_season_yr = 

# Selecting a season to analyze
season_to_analyze = st.sidebar.selectbox('Season', reversed(list(range(1980, latest_season))))

st.sidebar.subheader("Select the amount of data you want to see")
dataframe_info = st.sidebar.radio(
    "Data to display",
    ('All data','Basic')
)

st.sidebar.markdown("""
    - If you choose  _Basic_, then you'll only see columns with basic information.
""")

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

    passing_players["Player"] = passing_players["Player"].map(lambda x: x.rstrip('*+'))

    passing_players.sort_values(by="Yds", inplace=True, ascending=False)
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
    'Player age range', sort_player_ages, sort_player_ages)

# Work in progress
youngest_player = int(player_stats["Age"].min()) - 1
oldest_player = int(player_stats["Age"].max()) + 1

# age_filter_slider = st.sidebar.slider("Player age range (experimental)", min_value=youngest_player, max_value=oldest_player)

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

def simplify_df(filtered_df):
    return "Hello"

if dataframe_info == "All data":
    filtered_df = player_stats[(player_stats['Tm'].isin(selected_team)) & (
        player_stats['Pos'].isin(selected_pos)) & (player_stats['Age'].isin(age_filter))]
elif dataframe_info == "Basic":
    general_data = "basic"

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

    """)

# General stats
with tab2:
    st.markdown("## General stats")
    st.markdown("### Player with the most _Yards Gained by Passing_")

    # Best player regarding the yards gained
    best_player_yds = player_stats.iloc[player_stats["Yds"].idxmax()]
    player_name = best_player_yds["Player"]
    player_yds = best_player_yds["Yds"]

    top_two = player_stats["Yds"].nlargest(2)

    st.markdown(f"The best player with __Yards Gained by Passing__ is")
    # st.dataframe(best_player_yds, use_container_width=True)

    st.metric(label=f"with {player_yds} yards passed", value=f"{player_name}", delta=f"{player_yds-top_two[1]} yards above second place")

    tab1, tab2 = st.tabs(["All player", "Best player by position"])

    with tab1:

        st.markdown("### Displaying player stats with the selected filters")
        st.dataframe(filtered_df)
        # test_filter = filtered_df.applymap(simple_data_gs, subset=pd.IndexSlice["Age", "G", "GS", "Cmp", "Att", "Cmp%", "Yds", "TD", "TD%", "Int", "Int%", "1D", "Lng", "Y/A", "AY/A", "Y/C", "Y/G", "Rate", "QBR", "Sk", "Yds Lost", "Sk%", "NY/A", "ANY/A", "4QC", "GWD"])

    with tab2:
        st.markdown("""
        #### Best player by position
        
        Work in progress

        """)

        pos_lst = player_stats["Pos"].unique()
    
    st.markdown("-----")

    today = datetime.now()
    today_frmt = today.strftime("%d/%m/%Y")
    st.markdown(f"This was updated in real time, so it means it updates at the same time as you view the data, just check the date 🗓️ {today_frmt}.")

    

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

    col1, col2 = st.columns(2)

    with col1:
        selected_team = st.selectbox("Select a team from the box:", team_lst)

        avg_tm_stats = team_avg(player_df=player_stats, team=selected_team)

    with col2:
        team_age = round(avg_tm_stats["Age"][0], 2)
        team_gms_played = round(avg_tm_stats["G"][0], 2)
        team_yds = round(avg_tm_stats["Yds"][0], 2)
        # - Average games played: {team_gms_played}

        st.markdown(f"""
            Information about {selected_team}:
            - Age average: {team_age}
            - Average yards covered: {team_yds}

        """)
    st.markdown("----")
    with st.container():
        st.markdown(f"#### Additional information for {selected_team}")

        with st.expander(f"View {selected_team}'s table"):
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
