import requests
from bs4 import BeautifulSoup
import csv
import os


date = input("Enter the date (YYYY-MM-DD): ")
try:
    page = requests.get(f'https://www.yallakora.com/Match-Center?date={date}')
    if page.status_code == 200:
        print("Page fetched successfully.")
    else:
        print(f"Failed to fetch the page. Status code: {page.status_code}")
except Exception as e:
    print(f"An error occurred while fetching the page: {e}")


try:
    soup = BeautifulSoup(page.content, 'lxml')
    print("Page parsed successfully.")
    
    champions = soup.find_all("div", {"class": "matchCard"})
    if champions:
        print(f"Found {len(champions)} match cards.")
    else:
        print("No match cards found.")
except Exception as e:
    print(f"An error occurred while parsing the page: {e}")

match_details = []

def get_match_info(champion):
    try:
        champion_title = champion.find("div", {"class": "title"}).find("h2").text.strip()
        print(f"Champion title: {champion_title}")
        
        all_matches = champion.find("div", {"class": "ul"}).find_all("div", {"class": "item future liItem"})
        print(f"Found {len(all_matches)} matches.")
        
        for match in all_matches:
            try:
                team_A = match.find('div', {"class": "teamA"}).text.strip()
                team_B = match.find('div', {"class": "teamB"}).text.strip()
                print(f"Match: {team_A} vs {team_B}")
                
                match_result = match.find('div', {"class": "MResult"}).find_all('span', {"class": "score"})
                score = f"{match_result[0].text.strip()} - {match_result[1].text.strip()}"
                match_time = match.find('div', {"class": "MResult"}).find('span', {"class": "time"}).text.strip()
                
                match_details.append({
                    'champion_title': champion_title,
                    'team_A': team_A,
                    'team_B': team_B,
                    'match_time': match_time,
                    'score': score
                })
            except Exception as e:
                print(f"An error occurred while processing a match: {e}")
    except Exception as e:
        print(f"An error occurred while processing the champion: {e}")

# Loop through each champion and extract match info
for n in range(len(champions)):
    get_match_info(champions[n])




try:
    if match_details:
        keys = match_details[0].keys()
        os.makedirs(r'C:\Users\DELL\Desktop\pythonScraping1', exist_ok=True)
        
        with open(r'C:\Users\DELL\Desktop\pythonScraping1\match_info.csv', 'w', newline='', encoding='utf-8') as myfile:
            dict_writer = csv.DictWriter(myfile, keys)
            dict_writer.writeheader()
            dict_writer.writerows(match_details)
            print("File created successfully.")
    else:
        print("No match details available to write to the file.")
except Exception as e:
    print(f"An error occurred while writing to the file: {e}")