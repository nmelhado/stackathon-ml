from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import csv
import io


def get_specific_data(position, year, week):
    '''Gathers the stats for every pplayer at a position for a given
    year and week'''

    # Creates the url to scrape
    url = 'https://www.footballdb.com/fantasy-football/index.html?pos='
    url += position + '&yr=' + str(year) + '&wk=' + str(week) + '&rules=2'

    # Opens the url
    req = Request(url)
    page = urlopen(req).read()
    week_data = BeautifulSoup(page, "html.parser")
    # Grabs the data rows by isolating the <tr>s and saves them in an
    # list called players
    player_rows = week_data.find_all('tr', 'right')
    # Removes the header row that names the columns
    player_rows.pop(0)

    # loops through players to grab their individual stats
    for player in player_rows:
        player_stats = list()
        stat = None
        stats = player.find_all('td')
        for stat in stats:
            # Checks if its the first item, if it is, it further digs
            # into the <a> element, so that it gets just the name
            if len(player_stats) == 0:
                player_stats.append(stat.find('a').text)
            # Next it checks if its the second item, which is the home
            # and away item in the form: team1@team2
            elif len(player_stats) == 1:
                team = stat.find('b').text
                player_stats.append(team)
                home_and_away = stat.text.replace("@", "")
                opponent = home_and_away.replace(team, "")
                player_stats.append(opponent)
                h_or_a = 0 if home_and_away.startswith(team) else 1
                player_stats.append(h_or_a)
            # For the other items, it just adds it to the player_stats
            # list normally
            else:
                player_stats.append(stat.text)
        # calculates the fantasy points that player would have put up
        # using my league's scoring system
        points = (int(player_stats[7]) / 25) + (6 * int(player_stats[8]))
        points += (2 * int(player_stats[10])) - (2 * int(player_stats[9]))
        points += (int(player_stats[12]) / 10) + (int(player_stats[13]) * 6)
        points += (2 * int(player_stats[14])) + (int(player_stats[15]) / 2)
        points += (int(player_stats[16]) / 10) + (int(player_stats[17]) * 6)
        points += (2 * int(player_stats[18])) - (int(player_stats[19]) * 2)
        data_file = 'data/' + position.lower() + '_data.csv'
        # writes the stats to that position's csv file
        with io.open(data_file, 'a', newline='') as stat_file:
            stat_writer = csv.writer(stat_file)
            stat_writer.writerow([year, week, player_stats[0],
                                  player_stats[1], player_stats[2],
                                  player_stats[3], player_stats[5],
                                  player_stats[6], player_stats[7],
                                  player_stats[8], player_stats[9],
                                  player_stats[10], player_stats[11],
                                  player_stats[12], player_stats[13],
                                  player_stats[14], player_stats[15],
                                  player_stats[16], player_stats[17],
                                  player_stats[18], player_stats[19],
                                  str(round(points, 2))])
        stat_file.close()
