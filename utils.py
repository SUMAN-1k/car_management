from datetime import datetime

def calculatedays(start_date,end_date):
    d1=datetime.strptime(start_date, "%Y-%m-%d")
    d2=datetime.strptime(end_date, "%Y-%m-%d")
    return(d2-d1).days+1

#Converts string to date object=strptime