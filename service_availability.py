import pandas as pd
from justwatch import JustWatch
from pprint import pprint
import json, time
import asyncio

# INFO: > This adds the available services in the last column 'services' of the csv
#       > Please update the list csv_files, countries, services, csv_suffix you want in Constants
#       > Install: python3.10 -m pip install pandas==1.3.4 justwatch==0.5.1 
#       > Run:     python3.10 scrap_senscritique.py

class Service_Availability:

    def __init__(self, csv_files=[], countries=[], services=[]):
        self.csv_suffix = "_updated.csv"
        self.csv_files = csv_files
        self.countries = countries
        self.services = services
        if not csv_files: self.csv_files = self.get_default_csv_files()
        if not countries: self.countries = self.get_default_countries()
        if not services: self.services = self.get_default_services()
        self.just_watch = {}
        self.init_justwatch()

    def get_default_csv_files(self):
        obj_list = [
            './top_film_Les_meilleurs_films_de_2021.csv',
            './top_film_les_meilleurs_films_de_2022.csv',
            './top_film_top111.csv']
        return obj_list

    def get_default_countries(self):
        obj_list = [
            "GB",
            "FR",
            #"US",
            #"DE",
        ]
        return obj_list
    
    def get_default_services(self):
        obj_list = [
            #"apple",
            "netflix",
            #"amazon",
            "prime",
            #"play",
            #"youtube",
            #"rakuten",
            #"microsoft",
            #"skystore",
            #"homecinema",
            #"virgintvgo"
        ]
        return obj_list

    def init_justwatch(self):
        for country in self.countries:
            self.just_watch[country] = JustWatch(country=country)

    async def get_country_result(self, country, search):
        try:
            results = self.just_watch[country].search_for_item(query=search)['items'][0]
        except Exception as e:
            #print(f"get_country_result err: {e}")
            results = {}
        result = self.populate_available(country, results)
        print(f"Execute -> ({country}) - {search}")
        return result

    def populate_available(self, country, results) -> dict:
        available = {country:""}
        for offer in results.get('offers',[]):
            for service in self.services:
                if service in  offer['urls']['standard_web']:
                    current = available[country]
                    if service not in current:
                       available[country] = current + service + ', '
        if country in available:
            available[country] = available[country][:-2]
            if available[country] == '':
                available.pop(country, None) 
        return available

    def get_tasks(self, searches:list) -> dict:
        tasks=[]
        for country in self.countries:
            for search in searches:
                t = asyncio.create_task( self.get_country_result(country, search) )
                tasks.append(t)
        print(f"{len(tasks)} Tasks started!")
        return tasks

    async def run_it(self, searches):
        result = await asyncio.gather(*self.get_tasks(searches))
        return result

    def update_csv(self):
        for csv_file in self.csv_files:
            df = pd.read_csv(csv_file, sep='|', names=["filmName", "directorName", "genre", "date", "duration", "ratingValue", 
                                                       "ratingCount", "reviewCount", "notes", "love", "wanted", "resume"])
            df['filmName'] = df['filmName'].str.replace('_',' ')
            df.to_csv("debug_df.csv", sep='|', index=False)
            searches = list(df[['filmName', 'directorName']].agg(' '.join, axis=1))
            # Concurrently run tasks 
            start = time.time()
            results = asyncio.run(self.run_it(searches))
            end = time.time()
            print(f"{csv_file} parsed in {round(end-start, 3)}s")
        
            len_index = len(df.index)
            for index,row in df.iterrows():
                if index < len(results)/len(self.countries): 
                    available = {}
                    for i in range(0, len(self.countries)):
                        try:
                            available |= results[index + i * len_index]
                        except Exception as e:
                            print(f"update_csv err: {e}")
                    df.loc[index, 'services'] = str(available)

            csv_file = csv_file.replace(".csv", self.csv_suffix)
            df.to_csv(csv_file, sep='|', index=False)

if __name__ == '__main__':
    sa = Service_Availability()
    sa.update_csv()