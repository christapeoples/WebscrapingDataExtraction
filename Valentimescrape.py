import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
    url = f'https://www.linkedin.com/jobs/search?keywords=Data%20Analysis&location=United%20States&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum={page}'
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    divs = soup.find_all('div', class_='base-search-card')
    for item in divs:
        title = item.find('h3', class_='base-search-card__title').text.strip()
        company = item.find('a', class_='hidden-nested-link').text.strip()
        location = item.find('span', class_='job-search-card__location').text.strip()
        try:
            salary = item.find('span', class_='job-search-card__salary-info').text.strip()
        except AttributeError:
            salary = ''

        job = {
            'title': title,
            'company': company,
            'location': location,
            'salary': salary
        }
        joblist.append(job)

joblist = []

for i in range(0, 40, 10):
    print(f'Getting page {i}')
    c = extract(i)
    transform(c)

df = pd.DataFrame(joblist)
print(df.head())
df.to_csv('jobs.csv', index=False)
