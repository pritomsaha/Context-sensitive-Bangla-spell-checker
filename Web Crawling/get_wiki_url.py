from bs4 import BeautifulSoup
import re
import requests
base_url = "https://bn.wikipedia.org"
url = "https://bn.wikipedia.org/wiki/বিশেষ:সব_পাতা/অ"
links = []
while True:
	html_content = requests.get(url).content
	soup = BeautifulSoup(html_content, "lxml")
	link_ul = soup.findAll('ul', {'class': 'mw-allpages-chunk'})[0]
	links += link_ul.findAll('a', href = True)

	pagination_div = soup.findAll('div', {'class': 'mw-allpages-nav'})[0]
	pagination_links = pagination_div.findAll('a', href = True)
	
	if(len(pagination_links)<2):
		break
	url = base_url + pagination_links[1]['href']
	print(url)

link_file = open("wiki_urls.txt", 'a')
for link in links:
	link_file.write(str(base_url+link['href'])+"\n")

link_file.close()


# url = "https://bn.wikipedia.org/wiki/%E0%A6%85"
# file = open("test.txt", 'a')


# html_content = requests.get(url).content
# soup = BeautifulSoup(html_content, "lxml")
# string = soup.find('div', {"id": "bodyContent"}).text
# string = re.sub('[,/\[\]:()><}.{০-৯0-9;a-zA-Z]', '', string)
# string = re.sub('[ ]+', '', string)
# file.write(string)
# file.close()

bn_char_pattern = re.compile(ur'[\u0980-\u0983\u0985-\u098C\u098F-\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BC-\u09C4\u09C7-\u09C8\u09CB-\u09CE\u09D7\u09DC-\u09DD\u09DF-\u09E3\u09F0-\u09FD]', re.UNICODE)


text = re.sub('[]', ' ', text)
