## README

# NBDATA: An NBA Visualizer

Our project is a website that deals with NBA teams and their acquisitions and losses during the summer and early season, be it via trades, free agent signings, or draft picks. With this data, we can display both new players and lost players of a given team.

Most interestingly, however, we can use our data to be a predictor of a team’s success this season. Using a team’s statistics from last season, and adjusting for the added and subtracted values of players acquired and lost, we can calculate expected team stats for this year (such as points, rebounds, etc.). Using the holistic “win shares” statistic for each player on a team, we can also predict a team’s final record for this season.

## Scraping the Data:

There are a number of technical challenges involved with the project. One of the most prominent is actually getting the data, which we were able to accomplish by scraping the web, specifically Basketball-Reference.com. Without web scraping, we would have spent as much time finding and entering raw data as we did actually coding.

We scraped the data into python objects and then stored them in postgresql databases on amazon web services with sqlalchemy.

The scraping functions and code can be found in 'scrape.py' as well as 'helpers.py'

## Database design and implementation:

Our table design meets the criteria for the third normal form (3NF). Each column in our table is dependent only on its primary key. These tables include Teams(name, wins, losses, points, rebounds, assists), DraftPicks(name, year, team, points, rebounds, assists, winshares), FreeAgents(name, points, rebounds, assists, winshares, oldteam, newteam), and TradedPlayers(name, points, rebounds, assists, winshares, oldteam, newteam).

## Putting together the front-end:

The website was assembled on the Flask framework, and hosted on the Heroku app platform.

The main landng page was set up to show all 30 NBA teams in a grid format, with their logos, names, and team abbreviations. In addition, a search bar was implemented allowing for searches of any given team. For each team, a number of possible matching terms was mapped to the corresponding teams, so that, for example, a search of "Warriors," "GSW," or "Golden State" would all show the page for the Golden State Warriors. Any searches that did not match to a team were redirected to the main page.

For the team stats pages, a list of last-season and predicted current-season stats is displayed. The team's lost and gained players between the seasons are also listed. Clicking the title 'NBDATA' will bring the user back to the home page, or alternatively, additional searches may be conducted with the search bar that remains present on the team stats pages.

## Additional Notes:

The most interesting factor of our project is our predictions - based on players’ and teams’ performances in the past, we can see where they should be this season. And by taking our predictions and comparing it to the real results, users can see which acquisitions may have not panned out as predicted, or which losses may not have stung as previously thought. The current NBA season is ⅓ of the way through, and many of our predictions are already ringing true. A number of prominent transactions over the NBA offseason are highlighted in our results. Lebron James was one of the most coveted free agents in recent history, and we have his added value helping the Lakers win 12 more games in our model. In real life, the Lakers are on track to make the playoffs for the first time in 6 years. Our model also predicts the Raptors to finish with the best record in the NBA, and they do indeed currently hold the top spot. The model is not perfect, for instance it does not account for individual player development from season to season,  but is strictly based on the previous year’s statistics. Additionally, it cannot account for how players will have different values on different teams: A good player on a bad team will see his points decrease, and will provide less win share value if he is traded to a good team. However, thus far our model has delivered fairly accurate predictions of how NBA teams will perform this season.

## Live Site URL:

[nba-visualizer.herokuapp.com](https://nba-visualizer.herokuapp.com)
