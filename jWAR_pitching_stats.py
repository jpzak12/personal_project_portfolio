def jWAR_pitching_stats(season):
    import requests
    import urllib.request
    import time
    from bs4 import BeautifulSoup
    import pandas as pd
    import numpy as np
    import jWAR_QualityStarts

    ###### FETCH PITCHING STATS FROM FANGRAPHS #######################
    ###### Disclaimer: Does not include Quality Starts (QS) ##########
    pos = "all" #which positions
    stats = "pit" # pitching or hitting stats?
    lg = "all" # which league(s)?
    qual = "10"  # how many ABs to qualify
    type = "c,3,7,8,9,13,4,5,11,12,6,17,15,19,24,21" # Custom report
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

    #Clean Data and remove unwanted columns/rows
    pitchingStats = pd.DataFrame(tableRows, columns=columnHeader)
    pitchingStats.drop([0,1], axis=0,inplace=True)
    pitchingStats.drop(['#'],axis=1,inplace=True)
    pitStats = pd.merge(pitchingStats,jWAR_QualityStarts.jWAR_QualityStarts(season),on=['Name'],how='left')
    pitchStats = pitStats.fillna(0)
    #print(pitchStats.head(),pitchStats.shape)


    #Points per pitching stat
    CG_pts = float(5)
    IP_pts = float(3)
    W_pts = float(5)
    L_pts = float(-3)
    SV_pts = float(4)
    BS_pts = float(-2)
    ER_pts = float(-2)
    H_pts = float(-1)
    BB_pts = float(-1)
    K_pts = float(2)
    QS_pts = float(3)

    #Create array for points per stat
    points_pitching = [CG_pts,IP_pts,W_pts,L_pts,SV_pts,BS_pts,ER_pts,H_pts,BB_pts,K_pts,BB_pts,QS_pts]
    pts_pitching = np.array(points_pitching)
    pts_p = pts_pitching.reshape(12,1)

    # Convert Fangraphs stats into an array of floats
    p_stats = pitchStats[['CG','IP','W','L','SV','BS','ER','H','BB','SO','HBP','QS']]
    pit_stats = np.asfarray(p_stats)


    # Multiply points per stat array by Fangraphs stats array
    pitching_points = pit_stats.dot(pts_p)


    # Add points back to initial dataframe "Fangraphs Stats"
    pitchStats['pPoints'] = pitching_points


    #print(pitchStats)
    return pitchStats
#jWAR_pitching_stats()
