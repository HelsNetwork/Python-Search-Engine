from bs4 import BeautifulSoup
import requests
import pymongo


hearder = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36'}

client = pymongo.MongoClient('mongodb://127.0.0.1', serverSelectionTimeoutMS = 5000)
db = client.db.results


results = []
page = 1
while page != 39490:
                start_url = requests.get("https://stackoverflow.com/questions/tagged/python?tab=newest&page=%7Bpage%7D&pagesize=50%22")
                content = BeautifulSoup(start_url.text, 'lxml')

                questions = content.find_all('div', {'class':'s-post-summary js-post-summary' })

                for item in questions:
                            title = item.find('a', {'class': 's-link'}).text
                            links = 'https://stackoverflow.com/' + item.find('a', {'class': 's-link'})['href']
                            description = item.find("div", {"class": "s-post-summary--content-excerpt"}).text.strip().replace('\n','')

                            results.append({'title': title, 'links': links, 'description': description})

                            context = {
                                'results':results
                            }

                            print(f'page scraped: {page}')

                page = page + 1

                print(len(results))


db.insert_one(context)


db.create_index([
    ('title', pymongo.TEXT),
    ('links', pymongo.TEXT),
    ('description', pymongo.TEXT)
], name= 'results', default_language='english')
