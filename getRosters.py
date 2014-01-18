import urllib2, gLatLong, re, csv
from BeautifulSoup import BeautifulSoup

# Here is the method that collects the origins of sports players
def get_players(league, region):
    
    # Get the page in question
    url = "http://sports.yahoo.com/"+league+"/teams/"+region+"/roster"
    script = urllib2.urlopen(url).read()

    # Parse it with BeautifulSoup
    tree = BeautifulSoup(script)

    # initialize the lists to be used
    origins = []
    
    # Search for games
    if league == "mls": #soccer has a slightly different format than the other sports
        for post in tree.findAll('tr', attrs={'valign':"top"}):
            text = "%s" %post # convert the post into a string
            text = text.splitlines() # split the post into lines
    
            # Search for the origins and extract them
            for line in text:
                # If the string is the birthplace
                if (',' in line and 'href' not in line and '&nbsp' not in line):
                   
                    # Clean up the place name
                    line = line.split(',')
                    line[0] = line[0].strip(' ')
                    line[1] = line[1].rpartition(' </td>')
                    line[1] = line[1][0]
                    line[1] = line[1].strip(' ')
                    
                    #print line
                   
                    # Add the birthplace to the list
                    origins.append(line)
    else:
        #Search for the origins and extract them
        roster_area = league+" phatable"
        for roster in tree.findAll('table', attrs={'class':roster_area}):
            #print roster
            for players in roster.findAll('tbody'):
                for player in players.findAll('tr'):
                    birthplacetext = "%s" %player.findAll('td', attrs={'class':'birthplace'})
                    if not birthplacetext == "[]":
                        birthplacetext = birthplacetext.partition('">')
                        birthplace = birthplacetext[2].strip('</td>]')
                        birthplace = birthplace.split(', ')
                        line = birthplace
                    
                        #print line
                        
                        # Add the birthplace to the list
                        origins.append(line)
            
    return origins

# Find the origins of players from 3 Boston area professional sports teams
hockey = get_players("nhl", "bos")
fball = get_players("nfl", "nwe")
bball = get_players("nba", "bos")
tball = get_players("mlb", "bos")
soccer = get_players("mls", "nwe")

a = [hockey, fball, bball, tball, soccer]
titles = ["bruins", "patriots", "celtics", "redsox", "revolutions"]

for x in a:
    icon = Icon()   # variables to control the appearance of our map
    tmap = Map()
    tmap.zoom = 3

    total_lat=0   # these variables will be used to center the map after
    total_long=0  # we collect all the points
    points_count=0
    
    #html file to display the map
    with open("%s_origins.csv" %titles[a.index(x)], "w+") as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerow(["X-Coordinate", "Y-Coordinate"])
    
    for k in x:
        EVENT_ID= k
        location= gLatLong.get_coords("%s" %k[0] + " %s" %k[1])
        
        if location <> None:
            with open("%s_origins.csv" %titles[a.index(x)], "a") as csvfile:
                spamwriter = csv.writer(csvfile)
                spamwriter.writerow([location[0], location[1]])
            
        else: #Print to console what location we couldn't find
            print "No location found for " + "%s, " %k
            
    print "Finished mapping %s" %titles[a.index(x)]