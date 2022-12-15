import base64
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.markdown("# Rushing stats")
st.sidebar.markdown("# Rushing stats")

st.markdown('## About this section')
st.markdown('The main usage for the _Rushing_ section is to better understand and analyze the rushing statistics the players had during a season.\
    It can be a past season or a current season.')

st.sidebar.subheader("User input features")
season_to_analyze = st.sidebar.selectbox(
    'Season', reversed(list(range(1980, 2023))))

# Web scraping data
# Taken from the site:
# https://www.pro-football-reference.com/years/2022/rushing.htm
@st.cache
def data_scrape(year):
    # Define the URL that's going to be used to search for the data.
    url = "https://www.pro-football-reference.com/years/" + \
        str(year)+"/rushing.htm"
    # Set the reading for the table found in the site established before.
    html = pd.read_html(url, header=1)
    rushing_df = html[0]
    clean_data = rushing_df.drop(rushing_df[rushing_df.Age == 'Age'].index)
    clean_data = clean_data.fillna(0)
    rushing_players = clean_data.drop(['Rk'], axis=1)
    rushing_players[["Age", "G", "GS", "Att", "Yds", "TD", "1D", "Lng", "Y/A", "Y/G", "Fmb"]] = rushing_players[["Age", "G", "GS", "Att", "Yds", "TD", "1D", "Lng", "Y/A", "Y/G", "Fmb"]].apply(pd.to_numeric)
    return rushing_players


player_stats = data_scrape(season_to_analyze)
# st.dataframe(player_stats)

# Dataframe filtering
# Team selection
sort_unique_team = sorted(player_stats.Tm.unique())
select_team = st.sidebar.multiselect(
    'Team', sort_unique_team, sort_unique_team)

# Position selection
unique_position = ['RB', 'QB', 'WR', 'FB', 'TE']
select_pos = st.sidebar.multiselect(
    'Position', unique_position, unique_position)

# Age filtering
sort_player_ages = sorted(player_stats['Age'].unique())
age_filter = st.sidebar.multiselect(
    'Player age', sort_player_ages, sort_player_ages)

# Data filtering
df_selected_team = player_stats[(player_stats['Tm'].isin(select_team)) & (
    player_stats['Pos'].isin(select_pos)) & (player_stats['Age'].isin(age_filter))]


def download_csv(team_df):
    csv = team_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="player_stats.csv">Download CSV File</a>'
    return href


# Data displaying
st.markdown("### Displaying player stats of the Selected team(s)")
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(
    df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)
st.markdown(download_csv(df_selected_team), unsafe_allow_html=True)


def league_avg(player_df):
    temp_df = pd.DataFrame(columns=player_df.columns)
    temp_series = player_df.mean()

    temp_df = temp_df.append(temp_series, ignore_index=True)
    temp_df.drop(labels=["Player","Tm","Pos"], inplace=True, axis=1)
    return temp_df

# average_stats = get_averages(player_stats)

def team_avg(player_df, team):
    temp_df = pd.DataFrame(columns=player_df.columns)

    temp_tm_df = pd.DataFrame(columns=player_df.columns)
    temp_tm_df = player_df.loc[player_df['Tm'] == team]
    temp_series = temp_tm_df.mean()

    temp_df = temp_df.append(temp_series, ignore_index=True)
    temp_df.drop(labels=["Player","Tm","Pos"], inplace=True, axis=1)

    return temp_df


average_league_stats = league_avg(player_stats)

# st.markdown("### Average statistics per team")
# st.dataframe(average_stats)

st.markdown(f"### Average statistics for the entire NFL in the {season_to_analyze} season")
st.dataframe(average_league_stats)

if st.button("View League bargraph"):
    st.markdown("#### Graph of the NFL")
    # average_league_stats.to_csv('output.csv', index=False)
    # df=pd.read_csv('output.csv')
    plt.figure()
    sns.barplot(data=average_league_stats).set(title="League Average")
    st.pyplot()


st.markdown("### Which team would you like to visualize?")

raw_team_list = list(player_stats['Tm'].unique())
team_list = sorted(raw_team_list)

selected_team = st.selectbox(
    "Select a team from the box:",
    team_list
)

avg_team_stats = team_avg(player_stats, team=selected_team)

st.markdown(f"### Average statistics for {selected_team}")
st.dataframe(avg_team_stats)

# if st.button("View team bargraph"):
tm_title = f"{selected_team} Average"
st.markdown(f"#### Viewing stats for {selected_team}")
# average_league_stats.to_csv('output.csv', index=False)
# df=pd.read_csv('output.csv')
plt.figure()
sns.barplot(data=avg_team_stats).set(title=tm_title)
st.pyplot()

# Graphs
# if st.button('View ')

st.set_option('deprecation.showPyplotGlobalUse', False)
