import streamlit as st

def main_page():
    st.markdown('# Main page 🏈')
    st.markdown("""
    ## General definitions
    ### Rushing
    Definition
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
    st.sidebar.markdown("# Main page 🏈")

def rushing():
    st.markdown("# Rushing stats")
    st.sidebar.markdown("# Rushing stats")

def passing():
    st.markdown("# Passing stats")
    st.sidebar.markdown("# Passing stats")

def receiving():
    st.markdown("# Receiving stats")
    st.sidebar.markdown("# Receiving stats")

names_to_funcs = {
    "Main Page": main_page,
    "Rushing": rushing,
    "Passing": passing,
    "Receiving": receiving
}

current_page = st.sidebar.selectbox("Select a page to visualize", names_to_funcs)
names_to_funcs[current_page]()