import streamlit as st

def main_page():
    st.markdown('# Main page 🏈')
    st.markdown("""
    ## Why was this project born?
    I've always been a bigger baseball fan, and during the COVID pandemic, I started to get more and more curious about player stats.
    
    Another thing that I recently started picking up, was watching NFL matches. Since I'm new to this sport, I wanted to better understand player stats, how each position works, and so on.
    So I decided to build a dashboard to better analyze player stats and try to understand better how one's stats are above or below a certain team, or the league as a whole.

    One of the things I decided to implement as well, was past seasons, since I want to better understand why some players are considered better than others.
    """)
    st.sidebar.markdown("# Main page 🏈")

def rushing():
    st.markdown("# Rushing stats")
    st.sidebar.markdown("# Rushing stats")
    st.markdown("""
    ## What does Rushing mean?
    In very basic and general terms, _Rushing_ refers to the stats a player gains when running with the football. It doesn't matter how they obtained it.
    ## Definitions
    """)
    st.markdown("""
    In the table, you'll see the following headers being referred to constantly, these mean the following:
    * Player - Player's name
    * Tm - Current team
        * If the player has been on multiple teams in a season, it's being marked as '2TM'
    * Age - Player's age
    * Pos - Position they play in.
    * G - Games played
    * GS - Games started (as defensive or offensive).
    * Att - Rushing attempts
    * Yds - Rushing yards gained
    * TD - Rushing Touchdowns
    * 1D - First Down rushing
    * Lng - Longest rushing attempt
    * Y/A - Rushing yards per attempt
    * Y/G - Rushing Yards per game
    * Fmb - Number of times fumbled
    """)
    st.sidebar.markdown("Get to know more about the data being handled for _Rushing_ stats as well as it's basic definition.")

def passing():
    st.markdown("# Passing stats")
    st.sidebar.markdown("# Passing stats")

def receiving():
    st.markdown("# Receiving stats")
    st.sidebar.markdown("# Receiving stats")

names_to_funcs = {
    "Main Page": main_page,
    "Passing": passing,
    "Receiving": receiving,
    "Rushing": rushing,
}

current_page = st.sidebar.selectbox("Select a page in order to get more information on a subject", names_to_funcs)
names_to_funcs[current_page]()