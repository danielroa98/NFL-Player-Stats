import pandas as pd

def data_scrape(year):
    """ Function data_scrape
        -----
        Receives:

        * year: int - Year a season started.

        Returns:

        * rushing_player: Pandas DataFrame containing the information from a 
     """
    # Define the URL that's going to be used to search for the data.
    url = "https://www.pro-football-reference.com/years/"+str(year)+"/rushing.htm"
    # Set the reading for the table found in the site established before.
    html = pd.read_html(url, header=1)
    rushing_df = html[0]
    clean_data = rushing_df.drop(rushing_df[rushing_df.Age == 'Age'].index)
    clean_data = clean_data.fillna(0)
    rushing_players = clean_data.drop(['Rk'], axis=1)
    rushing_players[["Age", "G", "GS", "Att", "Yds", "TD", "1D", "Lng", "Y/A", "Y/G", "Fmb"]] = rushing_players[[
        "Age", "G", "GS", "Att", "Yds", "TD", "1D", "Lng", "Y/A", "Y/G", "Fmb"]].apply(pd.to_numeric)
    return rushing_players
