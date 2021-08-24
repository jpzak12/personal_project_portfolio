
def jWAR_QualityStarts(season):
    import requests
    import urllib.request
    import time
    from bs4 import BeautifulSoup
    import pandas as pd
    import numpy as np

    import sys



    # insert at 1, 0 is the script path (or '' in REPL)
    sys.path.insert(1, 'Fantasy_Rankings/Yearly_Stat_References/Yearly_Quality_Starts/')

    file= open('Yearly_Stat_References/Yearly_Quality_Starts/{}_QS.csv'.format(season))

    dq = pd.read_csv(file)
    dq.drop(['Rk','Age','Tm','G','GS','IP','Wgs','Lgs','ND','Wchp','Ltuf','Wtm','Ltm','tmW-L%','Wlst','Lsv','CG','SHO','QS%','GmScA','Best','Wrst','BQR','BQS','sDR','lDR','RS/GS','RS/IP','IP/GS','Pit/GS','<80','80-99','100-119','≥120','Max'],axis=1,inplace=True)
    dq['Name'] = dq['Name'].str.split("\\",expand=True)
    dq['Name'] = dq['Name'].str.split("*",expand=True)
    dqs = dq.fillna(0)
    #print(dq)
    return(dq)
#jWAR_QualityStarts(season)
