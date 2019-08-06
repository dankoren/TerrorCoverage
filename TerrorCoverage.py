import csv
import requests
import json
import datetime
import time
from operator import itemgetter, attrgetter
def fix_date(x):
    if(int(x) < 10):
        x = '0' + x
    return x



def DateOnStrike(year,month):
    if(year == 1978 and month >= 8 and month <= 11):
        return True
    return False


def ReadAndGenerateCSV():
    terror_record_list = [];
    column_names = [];
    counter_total = 0
    counter_filtered = 0
    with open('TerrorDataSource.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                for cell in row:
                    column_names.append(cell)
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
                eventId_index = column_names.index('eventid')
                nkill_index = column_names.index('nkill')
                year_index = column_names.index('iyear')
                month_index = column_names.index('imonth')
                day_index = column_names.index('iday')
                country_index = column_names.index('country_txt')
                terror_record_list.append(['eventId', 'Year', 'Month','Day','Region', 'Country', 'ProvState',
                                           'City','Latitude','Longitude', 'Summary', 'AttackType', 'Perpetrator', 'Killed', 'Wounded'])
            else:
                if(row[nkill_index] != '' and int(row[nkill_index]) >= 20 and
                        row[year_index]!= '0' and row[month_index]!='0' and
                        row[day_index]!= '0' and (not DateOnStrike(row[year_index],row[month_index]))): #and ("Hamas" in row[gname_index]):
                    year = row[year_index]
                    month = row[month_index]
                    day = row[day_index]
                    country = row[country_index]
                    nkill = row[nkill_index]
                    month = fix_date(month)
                    day = fix_date(day)
                    terror_record = [row[eventId_index],year, month, day,
                                     row[column_names.index('region_txt')],
                                     country,
                                     row[column_names.index('provstate')],
                                     row[column_names.index('city')],
                                     row[column_names.index('latitude')],
                                     row[column_names.index('longitude')],
                                     row[column_names.index('summary')],
                                     row[column_names.index('attacktype1_txt')],
                                     row[column_names.index('gname')],
                                     row[column_names.index('nkill')],
                                     row[column_names.index('nwound')],
                                     ]
                       # TerrorRecord(row[eventId_index],year, month, country)
                    #if docs:
                    #    terror_record = TerrorRecord(row[eventId_index],year, month, country, docs[0]['web_url'], docs[0]['snippet'])
                    #else:
                    #    terror_record = TerrorRecord(row[eventId_index],year, month, country, '', '')
                    terror_record_list.append(terror_record)
                    # print(row)
                    counter_filtered += 1
                counter_total += 1
                line_count += 1
        #print(f'Processed {line_count} lines.')
    print('Total=',counter_total)
    print('Filtered=',counter_filtered)
    for i in terror_record_list:
        print(i)
    with open('Terrors.csv', 'w', newline='') as csvFile:
       writer = csv.writer(csvFile)
       writer.writerows(terror_record_list)
    csvFile.close()


def AddApiCallsToCSV():
    terror_record_list = [];
    column_names = [];
    counter_total = 0
    counter_filtered = 0
    with open('Terrors.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                for cell in row:
                    column_names.append(cell)
                # print(f'Column names are {", ".join(row)}')
                line_count += 1
                eventId_index = column_names.index('eventId')
                year_index = column_names.index('Year')
                month_index = column_names.index('Month')
                day_index = column_names.index('Day')
                country_index = column_names.index('Country')
                city_index = column_names.index('City')
                state_index = column_names.index('ProvState')
                terror_record_list.append(['eventId', 'Year', 'Month', 'Country', 'ProvState',
                                           'City', 'Latitude', 'Longitude', 'Summary', 'AttackType', 'Perpetrator',
                                           'Killed', 'Wounded','CoveredByNYT','URL1','URL2'])
            else:
                year = row[year_index]
                month = row[month_index]
                day = row[day_index]
                state=row[state_index]
                country = row[country_index]
                city = row[city_index]
                if(state==""):
                    state="notvalidstate"
                if (city == ""):
                    state = "notvalidcity"
                if (country == ""):
                    state = "notvalidcountry"
                beginDate = year + month + day
                endDate = datetime.date(int(year), int(month), int(day)) + datetime.timedelta(days=3)
                endDate = str(endDate).replace('-', '')
                url_base = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
                url_parameters = 'fq=((glocations:(' + country + ')%20OR%20glocations:(' + city + ')' \
                                '%20OR%20glocations:("' + city +" "+'('+country+')' '")%20OR%20glocations:("' + state +" "+'('+country+')' '")%20OR%20glocations:(' + state + '))%20AND%20subject:(Terrorism))&sort=oldest&begin_date=' + beginDate + \
                                '&end_date=' + endDate + '&api-key=4AsaAANPGN3Vof2ABBGVBH45LGGRUMLB'
                URL = url_base + '?' + url_parameters
                print("URL = ", URL)
                r = requests.get(url=URL)
                data = r.json()
                print('Data=',data)
                docs = data['response']['docs']
                print('Docs=',docs)
                URL1=0
                URL2=0
                CoveredByNYT = 0
                if len(docs) >= 1:
                    URL1=docs[0]['web_url']
                    CoveredByNYT=1
                if len(docs)>=2:
                    URL2=docs[1]['web_url']
                print(line_count)
                terror_record = [row[eventId_index], year, month, country,
                                row[column_names.index('ProvState')],
                                row[column_names.index('City')],
                                row[column_names.index('Latitude')],
                                row[column_names.index('Longitude')],
                                row[column_names.index('Summary')],
                                row[column_names.index('AttackType')],
                                row[column_names.index('Perpetrator')],
                                row[column_names.index('Killed')],
                                row[column_names.index('Wounded')],
                                CoveredByNYT,URL1,URL2]
                terror_record_list.append(terror_record)
                if line_count % 10 == 0:
                    for i in terror_record_list:
                        print(i)
                    with open('TerrorsWithUrl.csv', 'a', newline='') as csvFile:
                        writer = csv.writer(csvFile)
                        writer.writerows(terror_record_list)
                    csvFile.close()
                    time.sleep(60)
                    terror_record_list = []
            line_count += 1
    print('Total=', counter_total)




#field_aggregated - e.g: Killed
#field_aggregator - e.g: Country
def GenerateCSVByField(export_file_name,field_aggregated, field_aggregator):
    resultMap = {}
    resultList = []
    with open('TerrorDataSource.csv') as csvFile:
        csv_reader = csv.reader(csvFile, delimiter=',')
        print(csv_reader)
        headerline = csv_reader.__next__()
        for row in csv_reader:
            field = row[headerline.index(field_aggregator)]
            if field not in resultMap:
                if(row[headerline.index(field_aggregated)]):
                    resultMap[field] = [int(row[headerline.index(field_aggregated)]),1,0] # Sum
            else:
                if (row[headerline.index(field_aggregated)]):
                    resultMap[field][0] += int(row[headerline.index(field_aggregated)])
                    resultMap[field][1] += 1

    for key, [sum,count,average] in resultMap.items():
        average = sum / count if count != 0 else 0
        temp = [key, sum,count,average]
        resultList.append(temp)
    resultList.sort(key=lambda x: x[0], reverse=True)
    print(resultList)
    with open(export_file_name, 'w', newline='') as csvFile:
       writer = csv.writer(csvFile)
       writer.writerows(resultList)
    csvFile.close()


def GenerateCSVByTwoFields(export_file_name, field_aggregated,aggregator1,aggregator2):
    killedByField = {}
    killedByFieldList = []
    with open('TerrorsWithUrl.csv') as csvFile:
        csv_reader = csv.reader(csvFile, delimiter=',')
        print(csv_reader)
        headerline = csv_reader.__next__()
        for row in csv_reader:
            field1 = row[headerline.index(aggregator1)]
            field2 = row[headerline.index(aggregator2)]
            if (field1,field2) not in killedByField:
                if(row[headerline.index(field_aggregated)]):
                    killedByField[(field1, field2)] = [int(row[headerline.index(field_aggregated)]),1,0]
            else:
                if row[headerline.index(field_aggregated)]:
                    killedByField[(field1, field2)][0] += int(row[headerline.index(field_aggregated)])
                    killedByField[(field1, field2)][1] += 1

    for (key1,key2), [sum,count,average] in killedByField.items():
        average = sum / count
        temp = (key1,key2,sum,count,average)
        killedByFieldList.append(temp)

    killedByFieldList.sort(key = itemgetter(0,1))
    print(killedByFieldList)
    with open(export_file_name, 'w', newline='') as csvFile:
       writer = csv.writer(csvFile)
       writer.writerows(killedByFieldList)
    csvFile.close()




#ReadAndGenerateCSV()
#AddApiCallsToCSV()

#GenerateCSVByField('KilledByCountry.csv', 'nkill','Country')
#GenerateCSVByField('KilledByAttackType.csv','nkill','AttackType')

#GenerateCSVByTwoFields('ApiByRegionOverTime.csv','CoveredByNYT','Year','Region')
#GenerateCSVByTwoFields('ApiByCountryOverTime.csv','CoveredByNYT' 'Year','Country')
