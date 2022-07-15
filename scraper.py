from bs4 import BeautifulSoup
import requests
import pymongo



client = pymongo.MongoClient('mongodb://127.0.0', serverSelectionTimeoutMS = 5000)
db = client.database

results = []
for page in range(1,39490):
                start_url = requests.get(f"https://stackoverflow.com/questions/tagged/python?tab=newest&page=%7Bpage%7D&pagesize=15%22)
                content = BeautifulSoup(start_url.text, 'lxml')

                questions = content.find_all('div', {'class':'s-post-summary js-post-summary' })

                for item in questions:
                            title = item.find('a', {'class': 's-link'}).text
                            links = 'https://stackoverflow.com/' + item.find('a', {'class': 's-link'})['href']
                            description = item.find("div", {"class": "s-post-summary--content-excerpt"}).text.strip().replace('\n','')


                            context = {'title': title, 'links':links, 'description': description}

                            results.append(context)

                            print(f'page scraped: {page}')

                print(len(results))


db.data.insert_many(results)

db.data.create_index([
    ('title', pymongo.TEXT)

])
