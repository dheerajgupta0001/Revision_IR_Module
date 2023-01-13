# import argparse
import pandas as pd
import datetime
from src.config.appConfig import getFileMappings
from src.config.appConfig import getJsonConfig
from src.config.appConfig import initConfigs
from src.fetcher.wbes_data_fetcher import SectionWbesDataFetcher
from src.fetcher.wr_wbes_max_revision import SectionWbesMaxRevisionFetcher
from src.fetcher.wr_wbes_max_revision import SectionWbesMaxRevisionWithDateFetcher
from src.fetcher.wr_wbes_max_revision import SectionWbesAllRegionMaxRevisionFetcher
# from src.repos.dailyDataCalculator import daywiseDataCalculator


# get login config
initConfigs()
# get file config
appConfig = getFileMappings()

report_list = appConfig['Report Type'].dropna()
startDate = appConfig['Start Date'][0]
endDate = appConfig['End Date'][0]
targetDate = appConfig['Target Date'][0]
days = (endDate - startDate).days
wbesApiData = SectionWbesDataFetcher(
            getJsonConfig()['user'], getJsonConfig()['password'])
wbesRevisionData = SectionWbesMaxRevisionFetcher()
wbesRevisionDataWithDate = SectionWbesMaxRevisionWithDateFetcher()
wbesAllRegionRevisionDataWithDate = SectionWbesAllRegionMaxRevisionFetcher()
writer = pd.ExcelWriter('Output.xlsx', engine='xlsxwriter')

for curr_report in report_list:
    
    #     elif curr_report == 'Revision Number KPI':
    #         print("TODO")
    #     elif curr_report == 'Revision Summary':
    #         print("TODO")
    #     elif curr_report == 'IR Schedule matching':
    #         print("TODO")
            
    # dataDf = pd.DataFrame()
    if curr_report == 'Latest Revision':
        dataDf = pd.DataFrame(columns=['Date', curr_report])
        for i in range(days + 1):
            curr_date = startDate + datetime.timedelta(days=i)
            curr_date_rev = wbesRevisionData.makeApiCall(curr_date)
            dateRev = [curr_date , curr_date_rev]
            dataDf.loc[len(dataDf)] = dateRev
            dataDf.to_excel(writer, sheet_name=curr_report)
    elif curr_report == 'Revision Number KPI':
        dataDf = pd.DataFrame(columns=['Date', 'Revision Date', curr_report])
        for i in range(days + 1):
            nextDate = startDate + datetime.timedelta(days=i+1)
            curr_date = startDate + datetime.timedelta(days=i)
            rev_date, curr_date_rev = wbesRevisionDataWithDate.makeApiCall(curr_date, nextDate)
            dateRev = [curr_date, rev_date , curr_date_rev]
            dataDf.loc[len(dataDf)] = dateRev
            dataDf.to_excel(writer, sheet_name=curr_report)
    elif curr_report == 'Revision Summary':
        dataDf = pd.DataFrame(columns=['Date', 'WR', 'NR', 'ER', 'SR', 'NER', 'Remark', 'Revision Date'])
        for i in range(days + 1):
            # targetDate = startDate + datetime.timedelta(days=i+1)
            curr_date = startDate + datetime.timedelta(days=i)
            wr, nr, er, sr, ner, remark, strScheduleCreationDate = wbesAllRegionRevisionDataWithDate.makeApiCall(curr_date, targetDate)
            dateRev = [curr_date, wr, nr, er, sr, ner, remark, strScheduleCreationDate]
            dataDf.loc[len(dataDf)] = dateRev
            dataDf.to_excel(writer, sheet_name=curr_report)
    elif curr_report == 'Revision Summary Current Date':
        dataDf = pd.DataFrame(columns=['Date', 'WR', 'NR', 'ER', 'SR', 'NER', 'Remark', 'Revision Date'])
        for i in range(days + 1):
            targetDate = datetime.datetime.now()
            curr_date = startDate + datetime.timedelta(days=i)
            wr, nr, er, sr, ner, remark, strScheduleCreationDate = wbesAllRegionRevisionDataWithDate.makeApiCall(curr_date, targetDate)
            dateRev = [curr_date, wr, nr, er, sr, ner, remark, strScheduleCreationDate]
            dataDf.loc[len(dataDf)] = dateRev
            dataDf.to_excel(writer, sheet_name=curr_report)
            
writer.save()      
print("OK")
