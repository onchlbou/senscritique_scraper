#!/usr/bin/python3.10
import argparse
from scrap_senscritique import Scrap_Senscritique
from service_availability import Service_Availability


def main():
    parser = argparse.ArgumentParser()
    # Add an argument
    parser.add_argument('--url', type=str, required=False, help='senscritique list url')
    parser.add_argument('--from-csv', nargs='+', required=False, help='csv files path e.g. --from-csv ./top_film1970.csv ./top_film1980.csv')
    parser.add_argument('--show-services', action="store_true", help='switch to add available services in .csv file')
    parser.add_argument('--countries', nargs='+', required=False, help='countries where to check services e.g. --countries FR GB US')
    parser.add_argument('--services', nargs='+', required=False, help='services to check e.g. --services netflix amazon')
    args = parser.parse_args()

    if url := args.url:
        print(f"{url=}")
        ss = Scrap_Senscritique(url)
        ss.scrap_it()
        csv_files = [ ss.output_csv_file ]

        if show_services := args.show_services:
            print(f"{show_services=}")
            
            if countries := args.countries:
                print(f"{countries=}")
            else:
                countries=[]

            if services := args.services:
                print(f"{services=}")
            else:
                services=[]
            
            sa = Service_Availability(csv_files=csv_files, countries=countries, services=services)
            sa.update_csv()

    elif from_existing_csv := args.from_csv:
        print(f"{from_existing_csv=}")

        if show_services := args.show_services:
            print(f"{show_services=}")

            if csv_files := args.from_csv:
                print(f"{csv_files=}")
            else:
                csv_files=[]
            
            if countries := args.countries:
                print(f"{countries=}")
            else:
                countries=[]

            if services := args.services:
                print(f"{services=}")
            else:
                services=[]
            
            sa = Service_Availability(csv_files=csv_files, countries=countries, services=services)
            sa.update_csv()
    
    else:
        exit("Please provide an option...")





if __name__ == '__main__':
    main()
