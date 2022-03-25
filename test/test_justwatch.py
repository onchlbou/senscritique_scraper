from justwatch import JustWatch
from pprint import pprint
import json

movie='bac nord'
just_watch = {}
services = [
    "apple",
    "netflix",
    "amazon",
    "play",
    #"youtube",
    "rakuten",
    "microsoft",
    "skystore",
    "homecinema",
    #"virgintvgo"
]
countries = [
    "GB",
    "FR",
    #"US",
    #"DE",
]
available = {
    country:{
        #service: False 
        #for service in services
        "services":""
    } 
    for country in countries
}
#print(available)
#exit(1)
results = {}
for country in countries:
    just_watch[country] = JustWatch(country=country)
    results.update({country: just_watch[country].search_for_item(query=movie)['items'][0]})
    for offer in results[country].get('offers',[]):
        for service in services:
            if service in  offer['urls']['standard_web']:
                #available[country][service]=True
                current = available[country]['services']
                if service not in current:
                    available[country]['services']= current + service + ', '
    available[country]['services'] = available[country]['services'][:-2]

pprint(available)

with open('json_data.json', 'w') as outfile:
    json.dump(results, outfile, indent=4)