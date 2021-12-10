# NBA-Defensive-Impact
 Project to analyze NBA defensive matchup data


### DESCRIPTION

The package contains Python and R code files and Tableau workbook files. 

The technologies required for this project are Python 3.7+, R 4.1+, Tableau 2021.3+, and Gephi 0.9.2+. 

We used Python to scrape the NBA data, perform exploratory data analysis (EDA), conduct data manipulation & cleansing, and prepare the final data file output. Our IDE's were Visual Studio Code, Sublime Text, PyCharm, and Jupyter notebook. However, these IDEs are not required for replication. We ultimately used *.py files for all of our Python code. 

We used the R language, in R Studio, for some additional EDA and data file outputs. 

Our network visualization was created using Gephi per the instructions at the link below, and our dashboard visualizations are created in and served by Tableau. 

The NBA data is scraped from the site stats.nba.com, which provides documented API endpoints for developers to download data from. The API is fully documented on GitHub at the following URL:  https://github.com/swar/nba_api.

We used the following endpoints to gather our data:

    CommonAllPlayers -- Overall career information on each NBA player, both past and current.
    CommonPlayerInfo -- Detailed biographical information on current players, by season.
    LeagueSeasonMatchups -- Detailed offensive-defensive matchup information by season. This endpoint provides the detailed information for our metrics and analysis.
    LeagueDashTeamStats -- Extensive team summary statistics by team and season. This endpoint provides the team scoring information for the analysis.
    LeagueDashPlayerStats -- Extensive individual player statistics by season. Includes breakouts for each team and season totals, when a player was on multiple teams for one season. This endpoint provides the player scoring information for the analysis.
    
There is a Python package, "nba_api", that abstracts the API details and allows developers to use Python to scrape that data and manipulate using Python's libraries (pandas, numpy, etc.). We used this package to do the web scraping. The package's site is hosted on GitHub at https://github.com/swar/nba_api.


### INSTALLATION

To install and setup the code, ensure that the above listed tools, Python, R, Gephi, and Tableau, are installed on the working computer. Additionally, there should be an IDE to work in the Python files and R Studio for the R code work.

In Python, install the "nba_api" package library via pip install nba-api. Instructions for installing and basic usage for the nba_api package are at the following URL:  https://www.playingnumbers.com/2019/12/how-to-get-nba-data-using-the-nba_api-python-module-beginner/. We followed these instructions in our installation and usage.

The project root directory holds this file and the documentation that the project team generated (proposal, progress, and final reports). There are two sub-directories:  CODE and DATA.

The Python and R code files are all stored in the CODE directory. 

The code generates various CSV files for Tableau to read and display. All of the data files are stored in the DATA directory.

The Tableau workbook is located in the same directory as the CSV files. When opened, it will display the dashboards and reports from there.


### EXECUTION

With the tools installed and the files saved to the appropriate directories, perform the following steps:

1. Scrape the NBA data by running the following Python code files:  final_player_stats.py, nba_matchup_scrape.py, nba_playerID_scrape_final.py, and nba_team_totals.py. Note that that nba_api only allows one to scrape data on a per-season basis, and it throttles the volume of data that can be downloaded per session, so one will need to manually change the seasons in each file to get the data for each season and type.

2. To perform the EDA, run the files get_eda_data.py and Player_Network[labels-name&position].py to generate the files for EDA, then run the EDA files:  EDA_Impact_Metrics.ipynb, EDA_Project.RMD, nba_impactAnalysis.py, and network_cluster_exploration.py.

3. The next step is to join the various data files and produce the final CSV outputs for Tableau. Do this by running the following scripts:  best_matchups.py, generate_tableau_files.R, nba_groupBy.py, nba_joined_data.py, player_pos.py, and season_stats.py.

4. With the final data files in the DATA directory, create the Tableau network file, "Packaged Player Network.twbx". The process to create this network file for Tableau is to use "Player_Network[labels-name&position].py" to generate "nodes.csv" and "weighted_edges.csv". Load these files into Gephi to build the network graph and output coordinates file, which we join with the "weighted_edges.csv" in order to create "main_network.csv". This is the file that is used to create the Tableau network file, "Packaged Player Network.twbx". The tutorial at the following link has the detailed steps to follow (along with a link to download Gephi):  https://tessellationtech.io/how-to-create-network-visualizations-tableau/.

5. Finally, use the data and network data files to create the Tableau dashboard model file, NBA_Defense_Dashboard.twbx. Create the dashboard in the same directory as the data files are located.

6. To view the analysis and Tableau dashboard, open the prepared NBA_Defense_Dashboard.twbx
    6.1 If not opened to the '***Home***' dashboard, select said tab to navigate to it.
    6.2 Within the Home Tab, either select the hyperlink or select the corresponding tab name to review/use any of the 7 listed dashboards. 
    6.3 There is an accompanying description for each dashboard within the '***Home***' page. In addition, each dashboard has an executive summary, end-user walkthrough and glossary to guide the user through its purpose and interactive abilities.


