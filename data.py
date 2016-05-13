import pandas as pd
import requests
from bs4 import BeautifulSoup

# url for Meetup API

API_KEY = '6cc211017f64141072497d1766550'
BASE_URL = 'https://api.meetup.com'


# Get Data

def get_data(urlname):

    events_url = BASE_URL + '/' + urlname + '/events'
    params = {'sign':'true','key': API_KEY, 'status': 'past'}
    response = requests.get(events_url, params = params)
    events = response.json()

    event_ids = []
    event_desc_raw= []

    for event in events:
        event_ids.append(event['id'])
        event_desc_raw.append(event['description'])

    event_description = []
    for i in xrange(len(event_ids)):
        soup = BeautifulSoup(event_desc_raw[i], 'html.parser')
        event_description.append(soup.get_text())
        
    df_events = pd.DataFrame([event_ids, event_description]).T
    df_events.columns = ['event_id', 'event_description']

    member_id = []
    event_id = []

    for i in event_ids:
        rsvps_url = BASE_URL + '/' + urlname +'/events/' + i + '/rsvps'
        params = {'sign':'true','key': API_KEY}
        response = requests.get(rsvps_url, params = params)
        rsvps = response.json()
        
        for rsvp in rsvps:
            member_id.append(rsvp['member']['id'])
            event_id.append(rsvp['event']['id'])
                   
    df_rsvps = pd.DataFrame([member_id, event_id]).T
    df_rsvps.columns = ['member_id', 'event_id']

    return df_events, df_rsvps

# Consolidate Data

def consolidate(df_events, df_rsvps):

    df = pd.merge(df_events, df_rsvps, on = 'event_id')
    df.drop('event_id', axis = 1, inplace = True)
    
    return df.groupby('member_id', axis = 0, as_index=False).sum()


    

if __name__ == '__main__':
    
    urlname = 'DS-ProD-SF'
    df_events, df_rsvps = get_data(urlname)
    df = consolidate(df_events, df_rsvps)
    df.to_pickle('data_consolidated.pkl')



