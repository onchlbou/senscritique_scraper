Senscritique Scraper
====================

#### Info
Provide a senscritique.com list url  
=> Generate a .csv  
=> Possibility to add a column called 'services' displaying streaming platform hosting that movie in Real Time  

#### Installation  
    python3.10 -m pip install -r requirements.txt  

#### Execution  
    python3.10 main.py -h                                                                     # Get help  
    python3.10 main.py --url="https://www.senscritique.com/films/tops/top111"                 # To get a csv of the movies   
    python3.10 main.py --url="https://www.senscritique.com/films/tops/top111" --show-services # To append services availables   
    python3.10 main.py --from-csv <my_csv_path1.csv> <my_csv_path2.csv>  --show-services      # To append services availables   

#### Execution with more details
    python3.10 main.py --from-csv <my_csv_path1.csv> <my_csv_path2.csv>  --show-services --services apple        
    python3.10 main.py --from-csv <my_csv_path1.csv> <my_csv_path2.csv>  --show-services --services apple --countries US DE  

#### Important Notes
Only working for movies

#### Remaining work
- Handle async for scraping
- Multi pages lists
- Add other types of content