import streamlit as st
import streamlit.components.v1 as components

def main_page():
    st.markdown('# Main page 🏈')
    tab1, tab2, tab3 = st.tabs(
        ["About", "How to navigate the project?", "Additional information"]
    )

    with tab1:
        st.markdown("""
        ## Why was this project born?
        I've always been a bigger baseball fan, and during the COVID pandemic, I started to get more and more curious about player stats.
        
        Another thing that I recently started picking up, was watching NFL matches. Since I'm new to this sport, I wanted to better understand player stats, how each position works, and so on.
        So I decided to build a dashboard to better analyze player stats and try to understand better how one's stats are above or below a certain team, or the league as a whole.

        One of the things I decided to implement as well, was past seasons, since I want to better understand why some players are considered better than others.
        """)

    with tab2:
        st.markdown("""
        ## How to navigate this project? 🔍
        As you can see there's a sidebar that's divided into two sections:
        - The first section doesn't have a name (yet), but here you can navigate between pages. It's divided into the following pages:
            - streamlit-main: it's the landing page, containing additional information (such as this manual).
            - passing: `work in progress`
            - receiving: `work in progress`
            - rushing: contains the necessary information to better analyze and understand player stats and the team's averages.
                - May implement additional features.
        - The second section is meant to give additional information on player actions.
            - Each section has information regarding the data that's being managed, what the stats represent.
            - ℹ️ `Each individual section will be updated.`
        """)
    with tab3:
        st.markdown("""
        ## Additional information ℹ️
        This project is meant to help people better understand players statistics so they can further enjoy watching NFL games.
        That's why if you see an issue, or would want me to add additional information, I'll be adding a form so that you can help further advance this project.

        `The form is a current work in progress.`
        """)
        # TODO: add Google form to site.
        # components.iframe()
    st.sidebar.markdown("# Main page 🏈")
    st.sidebar.markdown("Home page for the project, it contains information on the project (such as how to navigate the project).")


def rushing():
    st.markdown("# Rushing")
    st.sidebar.markdown("# Rushing")

    tab1, tab2 = st.tabs(["What does _Rushing_ mean?", "Definitions"])

    with tab1:
        st.markdown("""
        ## What does Rushing mean?
        In very basic and general terms, _Rushing_ refers to the stats a player gains when running with the football. It doesn't matter how they obtained it.
        """)

    with tab2:
        st.markdown("""
        ## Definitions

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
    st.markdown("# Passing")
    st.sidebar.markdown("# Passing")


def receiving():
    st.markdown("# Receiving")
    st.sidebar.markdown("# Receiving")


names_to_funcs = {
    "Main Page": main_page,
    "Passing": passing,
    "Receiving": receiving,
    "Rushing": rushing,
}

current_page = st.sidebar.selectbox(
    "Select a page in order to get more information on a subject", names_to_funcs)
names_to_funcs[current_page]()
