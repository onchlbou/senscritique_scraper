import pandas as pd
from justwatch import JustWatch
from pprint import pprint
import json

# INFO: > Paste the list csv, countries, services, csv_suffix you want in Constants
#       > install: python3.10 -m pip install pandas==1.3.4 justwatch==0.5.1 
#       > run:     python3.10 scrap_senscritique.py
#       > read:    top_<list_name>.csv    

class Service_Availability:

    def __init__(self):
        self.csv_files = [
            './top_film_Les_meilleurs_films_de_2021.csv',
            './top_film_les_meilleurs_films_de_2022.csv',
            './top_film_top111.csv']
        self.csv_suffix = "_updated.csv"
        self.countries = [
            "GB",
            "FR",
            #"US",
            #"DE",
        ]
        self.services = [
            #"apple",
            "netflix",
            "amazon",
            #"play",
            #"youtube",
            #"rakuten",
            #"microsoft",
            #"skystore",
            #"homecinema",
            #"virgintvgo"
        ]
        self.just_watch = {}
        self.init_justwatch()

    def init_justwatch(self):
        for country in self.countries:
            self.just_watch[country] = JustWatch(country=country)

    def get_country_result(self, country, search):
        self.just_watch[country].search_for_item(query=search)['items'][0]

    def get_available(self, search) -> dict:
        available = {}
        results = {}
        for country in self.countries:
            results.update({
                country: self.get_country_result(country, search)
            })
            for offer in results[country].get('offers',[]):
                for service in self.services:
                    if service in  offer['urls']['standard_web']:
                        #available[country][service]=True
                        available.update({country:{'services':''}})
                        current = available[country]['services']
                        if service not in current:
                            available[country]['services'] = current + service + ', '
            if country in available and "services" in available[country]:
                available[country]['services'] = available[country]['services'][:-2]
                if available[country]['services'] == '':
                    available[country].pop('services', None) 
        return available


    def update_csv(self):
        for csv_file in self.csv_files:
            df = pd.read_csv(csv_file, sep='|', names=["filmName", "directorName", "genre", "date", "duration", "ratingValue", 
                                                    "ratingCount", "reviewCount", "notes", "love", "wanted", "resume"])
            df['filmName'] = df['filmName'].str.replace('_',' ')
            df["services"] = "null"

            for index,row in df.iterrows():
                filmName = row['filmName']
                directorName = row['directorName']
                search = filmName + ' ' + directorName
                print(search)
                available_str = str(self.get_available(search))
                df.loc[index, 'services'] = available_str

            csv_file = csv_file.replace(".csv", self.csv_suffix)
            df.to_csv(csv_file, sep='|', index=False)


if __name__ == '__main__':
    sa = Service_Availability()
    print(sa.just_watch)