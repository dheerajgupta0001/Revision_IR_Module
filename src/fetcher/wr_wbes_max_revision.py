from typing import List
import requests
import datetime as dt


class SectionWbesMaxRevisionFetcher():
    # def __init__(self,user:str, password:str) -> None:
    #     """constructor
    #     """
    #     self.user = user
    #     self.password = password

    def makeApiCall(self, dateKey: dt.datetime):
        dateStr = dt.datetime.strftime(dateKey, '%d-%m-%Y')
        # url = f'https://wbes.wrldc.in/WebAccess/GetFilteredSchdData?USER={self.user}&PASS={self.password}&DATE={dateStr}&ACR={self.acronymName}'
        url = f'https://wbes.wrldc.in/Report/GetCurrentDayFullScheduleMaxRev?regionid=2&ScheduleDate={dateStr}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3887.7 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        resp = requests.get(url, headers=headers)
        if not resp.status_code == 200:
            print(resp.status_code)
            print("unable to get data from wbes api")
            return []
        respJson = resp.json()
        paramsData = respJson["MaxRevision"]
        # if len(paramsData) == 0:
        #     return []
        return paramsData

class SectionWbesMaxRevisionWithDateFetcher():
    # def __init__(self,user:str, password:str) -> None:
    #     """constructor
    #     """
    #     self.user = user
    #     self.password = password

    def makeApiCall(self, dateKey: dt.datetime, nextDate: dt.datetime):
        dateStr = dt.datetime.strftime(dateKey, '%d-%m-%Y')
        # url = f'https://wbes.wrldc.in/WebAccess/GetFilteredSchdData?USER={self.user}&PASS={self.password}&DATE={dateStr}&ACR={self.acronymName}'
        # url = f'https://wbes.wrldc.in/Report/GetCurrentDayFullScheduleMaxRev?regionid=2&ScheduleDate={dateStr}'
        url = f'https://wbes.wrldc.in/Report/GetFullScheduleList?regionid=2&ScheduleDate={dateStr}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3887.7 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        resp = requests.get(url, headers=headers)
        if not resp.status_code == 200:
            print(resp.status_code)
            print("unable to get data from wbes api")
            return []
        respJson = resp.json()
        nextDate = nextDate.date()
        currDate = dateKey.date()
        for i in range(len(respJson)):
            rev_date = dt.datetime.strptime(respJson[i]['strScheduleCreationDate'], '%d-%m-%Y %H:%M:%S')
            rev_date = rev_date.date()
            if rev_date == nextDate or rev_date == currDate:
                return respJson[i]['strScheduleCreationDate'], respJson[i]['Revision']


class SectionWbesAllRegionMaxRevisionFetcher():
    # def __init__(self,user:str, password:str) -> None:
    #     """constructor
    #     """
    #     self.user = user
    #     self.password = password

    def makeApiCall(self, dateKey: dt.datetime, targetDate: dt.datetime):
        dateStr = dt.datetime.strftime(dateKey, '%d-%m-%Y')
        # url = f'https://wbes.wrldc.in/WebAccess/GetFilteredSchdData?USER={self.user}&PASS={self.password}&DATE={dateStr}&ACR={self.acronymName}'
        # url = f'https://wbes.wrldc.in/Report/GetCurrentDayFullScheduleMaxRev?regionid=2&ScheduleDate={dateStr}'
        url = f'https://wbes.wrldc.in/Report/GetFullScheduleList?regionid=2&ScheduleDate={dateStr}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3887.7 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        resp = requests.get(url, headers=headers)
        if not resp.status_code == 200:
            print(resp.status_code)
            print("unable to get data from wbes api")
            return []
        respJson = resp.json()
        # nextDate = nextDate.date()
        # currDate = dateKey.date()
        for i in range(len(respJson)):
            rev_date = dt.datetime.strptime(respJson[i]['strScheduleCreationDate'], '%d-%m-%Y %H:%M:%S')
            # rev_date = rev_date.date()
            if rev_date <= targetDate:
                return respJson[i]['RevisonMapper']['Wr'], respJson[i]['RevisonMapper']['Nr'], respJson[i]['RevisonMapper']['Er'], respJson[i]['RevisonMapper']['Sr'], respJson[i]['RevisonMapper']['Ner'], respJson[i]['Remark'], respJson[i]['strScheduleCreationDate']






