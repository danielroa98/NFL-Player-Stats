import base64
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from datetime import datetime

st.markdown("# Rushing")
st.sidebar.markdown("# Rushing")

st.sidebar.markdown("Select a season to analyze")

season_to_analyze = st.sidebar.selectbox(
    'Season', reversed(list(range(1980, 2023))))

st.sidebar.subheader("Sorting data")


tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ['About', 'General stats', 'NFL Average', 'Team Average', 'Player Analysis'])

# Web scraping data
# Taken from the site:
# https://www.pro-football-reference.com/years/{season}/rushing.htm
@st.cache(allow_output_mutation=True)
def data_scrape(year: int):
    # Define the URL that's going to be used to search for the data.
    url = "https://www.pro-football-reference.com/years/" + \
        str(year)+"/rushing.htm"
    # Set the reading for the table found in the site established before.
    html = pd.read_html(url, header=1)
    rushing_df = html[0]
    clean_data = rushing_df.drop(rushing_df[rushing_df.Age == 'Age'].index)
    clean_data = clean_data.fillna(0)
    rushing_players = clean_data.drop(['Rk'], axis=1)
    rushing_players[["Age", "G", "GS", "Att", "Yds", "TD", "1D", "Lng", "Y/A", "Y/G", "Fmb"]] = rushing_players[[
        "Age", "G", "GS", "Att", "Yds", "TD", "1D", "Lng", "Y/A", "Y/G", "Fmb"]].apply(pd.to_numeric)

    rushing_players.reset_index(drop=True, inplace=True)

    rushing_players.loc[rushing_players['Pos'] == 0, ['Pos']] = "No Pos"

    rushing_players["Player"]=rushing_players["Player"].map(lambda x: x.rstrip('*+'))

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
    now = datetime.now()
    date = now.strftime("%d-%m-%Y_at_%H:%M:%S")
    fileName = f"player_stats_{date}.csv"
    href = f'<a href="data:file/csv;base64,{b64}" download="{fileName}">Download CSV File</a>'
    return href


def league_avg(player_df):
    temp_df = pd.DataFrame(columns=player_df.columns)
    temp_series = player_df.mean()

    temp_df = temp_df.append(temp_series, ignore_index=True)
    temp_df.drop(labels=["Player", "Tm", "Pos"], inplace=True, axis=1)
    return temp_df


def team_avg(player_df, team):
    temp_df = pd.DataFrame(columns=player_df.columns)

    temp_tm_df = pd.DataFrame(columns=player_df.columns)
    temp_tm_df = player_df.loc[player_df['Tm'] == team]
    temp_series = temp_tm_df.mean()

    temp_df = temp_df.append(temp_series, ignore_index=True)
    temp_df.drop(labels=["Player", "Tm", "Pos"], inplace=True, axis=1)

    return temp_df


def player_information(player_df, player_name):
    temp_df = pd.DataFrame(columns=player_df.columns)

    temp_tm_df = pd.DataFrame(columns=player_df.columns)
    temp_tm_df = player_df.loc[player_df['Player'] == player_name]

    temp_df = temp_df.append(temp_tm_df, ignore_index=True)

    temp_df.drop(labels=["Player", "Tm", "Pos"], inplace=True, axis=1)

    return temp_df


def second_tm_avg(player_df, team):
    temp_df = pd.DataFrame(columns=player_df.columns)

    temp_tm_df = pd.DataFrame(columns=player_df.columns)
    temp_tm_df = player_df.loc[player_df['Tm'] == team]
    temp_series = temp_tm_df.mean()

    temp_df = temp_df.append(temp_series, ignore_index=True)
    temp_df.drop(labels=["Player", "Tm", "Pos"], inplace=True, axis=1)

    return temp_df


def compare_tms_df(team_df_1, team_df_2, team1_nm, team2_nm):
    team_comp_df = pd.DataFrame(columns=team_df_1.columns)
    team_comp_df = team_comp_df.append(team_df_1, ignore_index=True)

    team_comp_df.insert(loc=0, column="Tm", value=[[team1_nm, team2_nm]])

    team_comp_df.at[0, 'Tm'] = team1_nm

    team_comp_df = team_comp_df.append(team_df_2, ignore_index=True)
    team_comp_df.at[1, 'Tm'] = team2_nm

    return team_comp_df

def compare_players_df(player_1_data, player_2_data, player_1_name, player_2_name):
    player_comp_df = pd.DataFrame(columns=player_1_data.columns)
    player_comp_df = player_comp_df.append(player_1_data, ignore_index=True)

    player_comp_df.insert(loc=0, column="Player", value=[[player_1_name, player_2_name]])

    player_comp_df.at[0, "Player"] = player_1_name

    player_comp_df = player_comp_df.append(player_2_data, ignore_index=True)

    player_comp_df.at[1, "Player"] = player_2_name

    return player_comp_df

# def best_players_yds(player_df:pd.DataFrame):
#     temp_df = pd.DataFrame(columns=player_df.columns)
#     positions = list(player_df["Pos"].unique())

#     for i in positions:
#         pos_df = player_df[player_df["Pos"] == i]
        
#         # temp_df.append(temp, ignore_index=True)

#         return pos_df

# st.markdown("### Average statistics per team")
# st.dataframe(average_stats)


with tab1:
    st.markdown("""
    ## About this section
    The main usage for the _Rushing_ section is to better understand and analyze the rushing statistics the players had during a season.

    It can be a past season or a current season.

    ## About the data
    Some players have been in multiple teams throughout a season, that's why you may find some team names such as __2TM__.

    At the moment, the data from these players will be managed as if they had belonged to a team named "__2TM__" or whichever amount of teams they've been at in a single season.

    ## How can I (as a user) filter the data?
    It's pretty easy, in the sidebar you'll find a section titled _Sort data_ in there you'll have the following options to filter the data:
    - Season
        - The seasons range from 1980 to the current season (2022).
    - Team 
    - Position
    - Player age
    """)

with tab2:
    # Data displaying
    st.markdown("### Displaying player stats with the applied filters")
    # st.write('There are ' + str(df_selected_team.shape[0]) + ' players and ' + str(df_selected_team.shape[1]) + ' columns.')
    st.dataframe(df_selected_team, use_container_width=True)
    st.markdown(download_csv(df_selected_team), unsafe_allow_html=True)
    # st.markdown("""
    # ### Overall player stats

    # ```
    # Work in progress

    # This section will be displaying player stats (such as who in the NFL is better based on Rushing Yards Gained, position, etc...)
    # ```

    # Any suggestions will be more than appreciated.
    # """)
    avg_t1, avg_t2 = st.tabs(["Best player", "Best player by position"])
    with avg_t1:
        st.markdown("#### The overall leading player in Rushing is")

        best_player_yds = player_stats.iloc[player_stats["Yds"].idxmax()]
        player_name = best_player_yds['Player']
        player_yds_stat = best_player_yds['Yds']

        st.markdown(f"{player_name} with {player_yds_stat} _Rushing yards gained_")
        st.dataframe(best_player_yds, use_container_width=True)

        today = datetime.now()
        today_frmt = today.strftime("%d/%m/%Y")
        st.markdown(f"This was updated in real time, so it means it updates at the same time as you view the data, just check the date 🗓️ {today_frmt}.")

    with avg_t2:
        st.markdown("""
        #### Best player by position
        
        Work in progress

        """)
        # test = best_players_yds(player_stats)
        
        # st.dataframe(test)

        pos_lst = player_stats["Pos"].unique()

        # st.markdown(pos_lst)

        # for i in pos_lst:

        #     temp_df = player_stats.loc[player_stats["Pos"] == i]
        #     # st.dataframe(temp_df)
        #     temp_df_max = temp_df.iloc[player_stats["Yds"].idxmax()]

        #     st.markdown(f"Best {i} is: ")
        #     st.dataframe(temp_df_max, use_container_width=True)
        #     # st.markdown(f"The best {i} is {player_stats.loc[player_stats['Pos'] == i]}")


with tab3:
    # League average
    average_league_stats = league_avg(player_stats)

    st.markdown(f"### Average statistics for the entire NFL in the {season_to_analyze} season for _Rushing_")

    st.dataframe(average_league_stats, use_container_width=True)

    st.markdown(f"#### Graph of the NFL in the {season_to_analyze} season")

    plot_title = f"League Avgs. for the {season_to_analyze} season"
    plt.figure()
    sns.barplot(data=average_league_stats).set(title=plot_title)
    st.pyplot()

with tab4:
    # Team visualizations
    st.markdown("### Which team would you like to visualize?")

    raw_team_list = list(player_stats['Tm'].unique())
    team_list = sorted(raw_team_list)

    selected_team = st.selectbox(
        "Select a team from the box:",
        team_list
    )

    avg_team_stats = team_avg(player_stats, team=selected_team)

    st.markdown(f"#### Average statistics for {selected_team}")
    st.dataframe(avg_team_stats, use_container_width=True)

    # if st.button(f"View {} bargraph"):
    tm_title = f"{selected_team} Average"
    st.markdown(f"#### Viewing stats for {selected_team}")

    plt.figure()
    sns.barplot(data=avg_team_stats).set(title=tm_title)
    st.pyplot()

    st.markdown(
        f"If you want to compare another team with {selected_team}, select one from below")

    selected_2nd_team = st.selectbox(
        "Select the second team:",
        team_list
    )

    with st.expander(f"Comparing {selected_team} with {selected_2nd_team}"):

        avg_2team_stats = team_avg(player_stats, selected_2nd_team)

        two_teams_df = compare_tms_df(avg_team_stats, avg_2team_stats, team1_nm=selected_team, team2_nm=selected_2nd_team)

        st.dataframe(two_teams_df, use_container_width=True)

        tm_vs_tm2 = f"{selected_team} vs. {selected_2nd_team}"

        plt.figure()
        team_2_plt = sns.barplot(data=avg_2team_stats).set(title=tm_vs_tm2)
        team_1_plt = sns.scatterplot(data=avg_team_stats.transpose())
        st.pyplot()

        st.markdown(
            f"The scatter plot belongs to {selected_team} and the bar plot belongs to {selected_2nd_team}.")

    with st.expander(f"See how {selected_team} compares with the NFL in the {season_to_analyze} season"):
        tm_vs_nfl = f"{selected_team} vs. NFL"
        plt.figure()
        league_plot = sns.barplot(
            data=average_league_stats).set(title=tm_vs_nfl)
        tm_plot = sns.scatterplot(data=avg_team_stats.transpose())
        st.pyplot()


with tab5:
    # Player visualizations
    st.markdown("### Which player would you like to visualize?")

    raw_player_list = list(player_stats['Player'].unique())
    player_list = sorted(raw_player_list)

    selected_player = st.selectbox("Select a player", player_list)

    individual_player = player_information(
        player_df=player_stats, player_name=selected_player)

    st.markdown(f"#### Statistics for {selected_player}")
    st.dataframe(individual_player, use_container_width=True)

    with st.expander(f"View the stats of {selected_player} vs the NFL in the {season_to_analyze} season"):
        st.markdown(f"The stats for the NFL in the {season_to_analyze} are:")
        st.dataframe(average_league_stats, use_container_width=True)

        # if st.button(f"View {selected_player}'s stats"):
        # tm_title = f"{selected_team} Average"
        st.markdown(
            f"#### Viewing stats for {selected_player} against the NFL")

        graph_title = f"Stats for {selected_player} compared with the NFL"

        plt.figure()
        league_plot = sns.barplot(
            data=average_league_stats).set(title=graph_title)
        player_plot = sns.scatterplot(data=individual_player.transpose())
        player_plot.legend_.remove()
        st.pyplot()
    
    with st.expander(f"View how {selected_player} compares against another player"):
        second_player = st.selectbox("Select another player", player_list)

        player_2_cmpr = player_information(player_df=player_stats, player_name=second_player)

        p1_vs_p2 = compare_players_df(player_1_data=individual_player, player_2_data=player_2_cmpr, player_1_name=selected_player, player_2_name=second_player)

        st.dataframe(p1_vs_p2, use_container_width=True)

        p_v_p_title = f"{selected_player} vs. {second_player}"

        plt.figure()
        player_comp_plot = sns.barplot(data=player_2_cmpr).set(title=p_v_p_title)
        main_player_plot = sns.scatterplot(data=individual_player.transpose())
        st.pyplot()
        st.caption(f"""
        The scatterplot contains {selected_player}'s stats, meanwhile the bargraph contains {second_player}'s stats.
        """)

    with st.expander(f"View how {selected_player} compares against another team"):
        raw_team_list = list(player_stats['Tm'].unique())
        team_list = sorted(raw_team_list)

        selected_team = st.selectbox("Select a team:", team_list)

        avg_team_stats = team_avg(player_stats, team=selected_team)
        
        st.markdown(f"{selected_team}'s statistics for the {season_to_analyze} season")
        st.dataframe(avg_team_stats, use_container_width=True)

        p_v_t_title = f"{selected_player} compared against {selected_team}"

        plt.figure()
        team_plot = sns.barplot(data=avg_team_stats).set(title=p_v_t_title)
        player_plot = sns.scatterplot(data=individual_player.transpose())
        st.pyplot()
        st.caption(f""" 
        The scatterplot contains {selected_player}'s stats, meanwhile the bargraph contains {selected_team}'s stats.
        """)


# TODO: implement function to compare team stats and print if it was better, average or worse than the NFL's averages.


# Graphs
# if st.button('View ')

st.set_option('deprecation.showPyplotGlobalUse', False)
