def jWA_player_list(season):
    import requests
    import urllib.request
    import time
    from bs4 import BeautifulSoup
    import pandas as pd
    import numpy as np
    import re

    ####FETCH HITTING STATS FROM FANGRAPHS############
    pos = "all" #which positions
    stats = "bat" # pitching or hitting stats?
    lg = "all" # which league(s)?
    qual = "50"  # how many ABs to qualify
    type = "c,3,4,5,6,7,8,9,10,11,12,13,14,15,17,16,21,22,23,39" # Custom report
    #season = "2019" # Season of interest
    month = "0" # Beg month
    #season1 = "2019" # end season
    ind = "0" # (0) regular (1) Split Season (2) Rookies only
    team = "0" # All teams
    rost = "0" # Default Roster
    age = "0" # Default age filter range
    filter = "" # Type of filter... leave empty string
    players = "0" # Default player list
    startdate = "{}-01-01".format(season) #Starting range of date
    enddate = "{}-12-31".format(season) #Ending range of date
    p = 1 # Set begging page at 1
    page = "{}_50".format(p) # Page reference

    payload = {"pos":pos,"stats":stats,"lg":lg,"qual":qual,"type":type,"season":season,"month":month,"season1":season,"ind":ind,"team":team,"rost":rost,"age":age,"filter":filter,"players":players,"startdate":startdate,"enddate":enddate,"page":page}
    url = 'https://www.fangraphs.com/leaders.aspx'
    response = requests.get(url,params=payload)

    #print("Response:", response.status_code,response.url) #200 means it went through


    soup = BeautifulSoup(response.text,'html.parser')

    #The website table is partitioned into multiple pages.  We need to know how many pages to iterate

    pagingText = soup.find("div",{"class": "rgWrap rgNumPart"})

    pagingLinks = pagingText.findAll("a")
    pages = len(pagingLinks)
    #print("Number of page links:",len(pagingLinks))

    #Get Header for the table
    columnHeader = []
    header = soup.find('table', attrs={'id':'LeaderBoard1_dg1_ctl00'}).find_all('th')
    for c in header:
        columnHeader.append(c.text)
    columnHeader = [c.strip('\n') for c in columnHeader]


    tableRows = []

    for pg in range(1,pages+1):

        #pause our code for a second so that we are not spamming the website with requests. This helps us avoid getting flagged as a spammer.
        time.sleep(0.5)

        #update page number in payload
        payload["page"] = "{}_50".format(pg)
        response = requests.get(url,params=payload)
        #print("Page:",pg,"url:",response.url)
        soup = BeautifulSoup(response.text,'html.parser')
        table = soup.find('table', attrs={'id':'LeaderBoard1_dg1_ctl00'})
        rows = table.find_all('tr')

        for row in rows:
            cols = row.find_all('td')
            if cols:
                cols = [ele.text.strip() for ele in cols]
                tableRows.append([ele for ele in cols if ele])


    hittingStats = pd.DataFrame(tableRows, columns=columnHeader)
    hittingStats.drop([0,1], axis=0,inplace=True)
    hittingStats.drop(['#'],axis=1,inplace=True)



    #Points per hitting stat
    CS_pts = float(-1)
    Double_pts = float(3)
    HBP_pts = float(1.5)
    HR_pts = float(6)
    RBI_pts = float(1.5)
    R_pts = float(1.5)
    SB_pts = float(3)
    SO_pts = float(-0.5)
    BB_pts = float(1.5)
    Triple_pts = float(4.5)
    Single_pts = float(1.5)

    #Create array for points per stat
    points_hitting = [Single_pts,Double_pts,Triple_pts,HR_pts,R_pts,RBI_pts,BB_pts,BB_pts,HBP_pts,SO_pts,SB_pts,CS_pts]
    pts_hitting = np.array(points_hitting)
    pts_hit = pts_hitting.reshape(12,1)

    # Convert Fangraphs stats into an array of floats
    h_stats = hittingStats[['1B','2B','3B','HR','R','RBI','BB','IBB','HBP','SO','SB','CS']]
    hit_stats = np.asfarray(h_stats)


    # Multiply points per stat array by Fangraphs stats array
    hitting_points = hit_stats.dot(pts_hit)
    #print(hitting_points)

    # Add points back to initial dataframe "Fangraphs Stats"
    hittingStats['hPoints'] = hitting_points


    return hittingStats
