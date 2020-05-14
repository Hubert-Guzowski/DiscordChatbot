import requests
import json
import os


def analyze_tone(text):
    username = 'apikey'
    password = os.getenv('APIKEY')
    watson_url = 'https://api.eu-gb.tone-analyzer.watson.cloud.ibm.com/instances/5d086126-0e32-47fc-9f6e-51eb1054d6ca'
    headers = {"content-type": "text/plain"}
    data = '%'.join(text.strip().split())
    try:
        r = requests.get(watson_url + "/v3/tone?version=2017-09-21&text=" + data,
                         auth=(username, password), headers=headers)
        return r.text
    except Exception as e:
        print(e)
        return False


def results_to_list(data):
    data = json.loads(str(data))
    print(data)
    result = []
    for i in data['document_tone']['tones']:
        result.append([i['tone_name'], i['score']])
    return result
