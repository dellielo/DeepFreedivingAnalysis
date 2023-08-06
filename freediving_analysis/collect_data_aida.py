import requests 
import pandas as pd 
from lxml import etree
from bs4 import BeautifulSoup as bs

URL_RESULTS = 'https://www.aidainternational.org/Events/Event{Results}-{index_event}'
URL_REQUEST_DAY = "https://www.aidainternational.org/Events/fetch_live_days.php?selector=day&event_id={index_event}&day_index={day_index}"
URL_DETAILS = 'https://www.aidainternational.org/Events/EventDetails-{index_event}'

def get_details_event(index_event):
    url = URL_DETAILS.format(index_event)
    r = requests.get(url)
 
    tree = bs(r.text, "lxml")

    if tree.title.text != "AIDA | Event Details":
        # special case for 3017 / World championship 2017
        list_info = {"Title Event": "Depth World Championship", 
                     "Event Type": "Depth Competition",
                     "Disciplines": "FIM  CWT CWTB CNF",}
        return list_info
        
    title_event = tree.find("h3").text

    description = tree.find_all("div", class_="page__content")
    for i in description:
        titles = i.find_all('span', {'class':'u-actionlist__action'})
        contents = i.find_all('span', {'class':'u-actionlist__content'})
    list_info = {title.text.strip().replace(':',''): content.text.strip() for title, content in zip(titles, contents)}
    list_info['Title Event'] = title_event
    return list_info

def get_days_competition(index_event):
    url_results = URL_RESULTS.format(Results='Results', index_event=index_event) # normally same between startlist and results
    r = requests.get(url_results)
    tree = bs(r.text, "lxml")
    print(url_results)
    days_form = {}

    list_days = tree.find_all("div", class_='pagination-container')
    if list_days is None or len(list_days) == 0:
        return days_form # the competition has not results !!!
    
    list_days = list_days[0]
    days = list_days.find_all("li")
    
    for day in days :
        id_day = day.find("a").get("id")
        if id_day is not None :
            days_form[id_day] = day.text
    return days_form

def add_info_competition(df, infos_compet):
    df['Title Event'] = infos_compet['Title Event']
    df['Event Type'] = infos_compet['Event Type']  
    return df


def get_results_event_per_day(index_event, day_index, type_results='Results'):
    df_results = None

    infos_compet = get_details_event(index_event)
    # print(infos_compet)
    if 'Event Type' not in infos_compet :
        print('Event Type doesn''t exist')
        return None
    
    # if 'Event Type' in infos_compet and infos_compet['Event Type'] == 'Pool Competition':
    #     print('Pool Competition', index_event)
    #     return None # Condition to keep just Depth Competition
    
    if 'Disciplines' in infos_compet:
        list_disci = infos_compet['Disciplines'].split()
        # if not(set(list_disci).intersection(set(['FIM', 'CWT', 'CWTB', 'CNF']))):
        #     print('list_disci', list_disci, index_event)
        #     return None # Condition to keep just Depth Competition
    else : 
        list_disci = []
    
    payload = {}
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': 'Cookie_1=value; PHPSESSID=orcla350op7e0u6q1kqmbchpcr'
    }

    s = requests.Session()
    url_php_day = URL_REQUEST_DAY.format(index_event=index_event, day_index=day_index)
    url_results = URL_RESULTS.format(Results=type_results, index_event=index_event)
    r = s.get(url_php_day, data=payload, headers=headers)
    re = s.get(url_results, headers=headers)
    print(url_php_day)
    print(url_results)
    soup = re.text

    try :
        tables = pd.read_html(str(soup))
        if len(tables) == 1 : 
            df_results_cur = tables[0]
            # print(df_results_cur)
            if df_results_cur.shape[0] == 1 and df_results_cur.iloc[0][0] == 'Rest Day':
                df_results_cur = None
            else :
                df_results_cur = add_info_competition(df_results_cur, infos_compet)
                df_results = df_results_cur if df_results is None else pd.concat([df_results, df_results_cur])
    except :
        print(f"No table for {index_event} , day {day_index} ")

    return df_results

def get_results_event_list_days(index_event, days_compet, type_results): 
    df_results = None
    for index_day, value in days_compet.items():
        print(" ######  " , index_event, len(days_compet), index_day, value)
        df_day = get_results_event_per_day(index_event, index_day.split("_")[1], type_results)
        if df_day is not None and df_day.shape[0] > 0 :
            df_day["Day"] = value
            print(f"--> {index_event} - {value} - {df_day.shape[0]}")
            df_results = df_day if df_results is None else pd.concat([df_results, df_day])
    return df_results 

def get_results_event(index_event):
    df_results = None
    days_compet = get_days_competition(index_event)
    get_results_event_list_days(index_event, days_compet)
    return df_results

def get_results_events(list_events):
    df_results = None
    for event in list_events:
        df_day = get_results_event(event)
        if df_day is not None and df_day.shape[0] > 0 :
            df_results = df_day if df_results is None else pd.concat([df_results, df_day])
    return df_results