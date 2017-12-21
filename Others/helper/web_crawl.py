from bs4 import BeautifulSoup
import re
import requests
headers = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}

def create_sentences(text):
	pattern = r"[\।|\?|;]+"
	sentences = re.split(pattern, text.rstrip(pattern))
	sentences = "\n".join(sentence.strip() for sentence in sentences)
	if sentences[-1] != "\n":
		sentences += "\n"				
	return sentences

def crawl_rabindra_rochona():
	base_url = "http://www.tagoreweb.in/Render/"
	file = open("rabindra_upanyas.txt", "a")
	def crawl(url):
		while True:
			html_content = requests.get(base_url+url).content
			soup = BeautifulSoup(html_content, "lxml")
			main_content = soup.find('div', {'class': 'content'})
			print(base_url+url)
			file.write(create_sentences(main_content.text))
			break
	
#	html_content = requests.get(base_url+"ShowBook.aspx?ct=Essays&bi=14576005-A4A0-4035-B51D-B2EAEB60FB63").content
#	soup = BeautifulSoup(html_content, "lxml")
#	links = soup.find('table', {'class': 'indexTbl'}).findAll("a", href = True)
	links = ["ShowContent.aspx?ct=Novels&bi=09326CC8-A4A0-4025-351D-46AE438D0304&ti=09326CC8-A4A0-49E5-C51D-46AE438D0304", "ShowContent.aspx?ct=Novels&bi=FED824EF-A4A0-4035-151D-4C2B7D12265D&ti=FED824EF-A4A0-49E5-E51D-4C2B7D12265D", "ShowContent.aspx?ct=Novels&bi=FA9C5628-A4A0-4035-051D-43D11F751932&ti=FA9C5628-A4A0-4245-051D-43D11F751932", "ShowContent.aspx?ct=Novels&bi=EDDED9E1-A4A0-4055-351D-C70C8B1532CC&ti=EDDED9E1-A4A0-4A75-751D-C70C8B1532CC", "ShowContent.aspx?ct=Novels&bi=EDDED9E1-A4A0-4015-951D-C70C8B1532CC&ti=EDDED9E1-A4A0-4A65-B51D-C70C8B1532CC", "ShowContent.aspx?ct=Novels&bi=EDDED9E1-A4A0-4045-551D-C70C8B1532CC&ti=EDDED9E1-A4A0-49F5-351D-C70C8B1532CC", "ShowContent.aspx?ct=Novels&bi=EDDED9E1-A4A0-4025-251D-C70C8B1532CC&ti=EDDED9E1-A4A0-49E5-D51D-C70C8B1532CC", "ShowContent.aspx?ct=Novels&bi=EDDED9E1-A4A0-4015-A51D-C70C8B1532CC&ti=EDDED9E1-A4A0-49F5-151D-C70C8B1532CC", "ShowContent.aspx?ct=Novels&bi=EDDED9E1-A4A0-4005-C51D-C70C8B1532CC&ti=EDDED9E1-A4A0-4E85-551D-C70C8B1532CC", "ShowContent.aspx?ct=Novels&bi=EDDED9E1-A4A0-4045-651D-C70C8B1532CC&ti=72EE92F5-BE50-4A67-EE6E-0F7410664DA3", "ShowContent.aspx?ct=Novels&bi=EDDED9E1-A4A0-4035-951D-C70C8B1532CC&ti=EDDED9E1-A4A0-4A75-B51D-C70C8B1532CC", "ShowContent.aspx?ct=Novels&bi=EDDED9E1-A4A0-4005-D51D-C70C8B1532CC&ti=EDDED9E1-A4A1-40D5-151D-C70C8B1532CC", "ShowContent.aspx?ct=Novels&bi=E0BD0A8D-A4A0-4035-A51D-4D426502A110&ti=E0BD0A8D-A4A0-49F5-251D-4D426502A110"]
	for link in links:
#		href = link['href']
#		print("reading "+ href) 
		crawl(link)
	file.close()

def crawl_sorot_rochona():
	base_url = "http://www.sarat-rachanabali.nltr.org/"
	file = open("sorot_rochona2.txt", "a")
	def crawl(url):
		while True:
			html_content = requests.get(base_url+url).content
			soup = BeautifulSoup(html_content, "lxml")
			main_content = soup.find('div', {'id': 'mainContent'})	
			bottom_div = soup.find("td", {"valign": "bottom"})
			if bottom_div is None:
				break
			file.write(create_sentences(main_content.text))
			next_page_link = bottom_div.find('a', href = True)
			url = next_page_link['href']
			
	html_content = requests.get(base_url+"subCat.jsp?002").content
	soup = BeautifulSoup(html_content, "lxml")
	links = soup.findAll('table')[2].findAll("a", href = True)
	for link in links:
		href = link['href']
		print("reading "+ href) 
		crawl(href)
	file.close()
	
def crawl_ebanglalibrary(writer_name, start=1):
	print("writer >>> "+ writer_name)
	base_url = "https://www.ebanglalibrary.com/"+writer_name
	with open("BanglaLiterature/"+writer_name+".txt", "a") as infile:
		html_content = requests.get(base_url, headers = headers).content
		soup = BeautifulSoup(html_content, "lxml")
		pages_span = soup.find("span", {"class": "pages"})
		num_pages = int(re.split(r"[/| ]+", pages_span.text.rstrip(r"[/| ]+"))[-1])
		
		for i in range(start, num_pages+1):
			url = base_url+"/page/"+str(i)
			html_content = requests.get(url, headers = headers).content
			soup = BeautifulSoup(html_content, "lxml")
			articles = soup.findAll("article")
			print("page number >>> "+ str(i)+" out of "+str(num_pages))
			for article in articles:
				link = article.find("h2", {"class": "entry-title"}).find("a", href = True)
				print("reading >>> "+link.text)
				html_content = requests.get(link["href"], headers = headers).content
				soup = BeautifulSoup(html_content, "lxml")
				entry_content = soup.find("div", {"class": "entry-content"})
				if entry_content:
					infile.write(create_sentences(entry_content.text))
		
def crawl_popular_writers():
	crawl_ebanglalibrary("humayunahmed")
	crawl_ebanglalibrary("sunil")
	crawl_ebanglalibrary("jasimuddin")
	crawl_ebanglalibrary("jibanananda")
	crawl_ebanglalibrary("joygoswami")
	crawl_ebanglalibrary("sukantabhattacharya")
	crawl_ebanglalibrary("purnendupatri")
	crawl_ebanglalibrary("sharatchandra")
	crawl_ebanglalibrary("nirendranath")
	crawl_ebanglalibrary("mahadevsaha")
	crawl_ebanglalibrary("shakti")
	crawl_ebanglalibrary("bankim")
	crawl_ebanglalibrary("rabindranath", 128)

def crawl_writers():
	base_url = "https://www.ebanglalibrary.com/লেখক-রচনা/"
	html_content = requests.get(base_url, headers = headers).content
	soup = BeautifulSoup(html_content, "lxml")
	writer_list_links = soup.find('div', {'id': 'writers-list'}).findAll('a')
	for link in writer_list_links:
		writer_name = link.text	
		html_content = requests.get(link['href'], headers = headers).content
		soup = BeautifulSoup(html_content, "lxml")
		post_content = soup.find('div', {'class': 'post-content'})
		print("writer >>> "+ writer_name)
		
		with open("BanglaLiterature/"+writer_name+".txt", "a") as infile:
			if post_content is None:
				write_to_file(link["href"], infile)
			else:
				li_list = post_content.findAll('li')
				for li in li_list:
					if li.find('ul', {'class': 'children'}):
						continue
					link = li.find('a')
					print("section >>> "+ link.text)
					write_to_file(link['href'], infile)
				

def write_to_file(base_url,infile, start=1):
	html_content = requests.get(base_url, headers = headers).content
	soup = BeautifulSoup(html_content, "lxml")
	num_pages = 1
	pages_span = soup.find("span", {"class": "pages"})
	if pages_span:
		num_pages = int(re.split(r"[/| ]+", pages_span.text.rstrip(r"[/| ]+"))[-1])
	
	for i in range(start, num_pages+1):
		url = base_url+"/page/"+str(i)
		html_content = requests.get(url, headers = headers).content
		soup = BeautifulSoup(html_content, "lxml")
		articles = soup.findAll("article")
		print("page number >>> "+ str(i)+" out of "+str(num_pages))
		for article in articles:
			link = article.find("h2", {"class": "entry-title"}).find("a", href = True)
			print("reading >>> "+link.text)
			html_content = requests.get(link["href"], headers = headers).content
			soup = BeautifulSoup(html_content, "lxml")
			entry_content = soup.find("div", {"class": "entry-content"})
			if entry_content:
				infile.write(create_sentences(entry_content.text))
				
def crawl_prothom_alo(start_date_str, end_date_str):
	from datetime import datetime, timedelta
	base_url = "http://www.prothom-alo.com"
	archive_url = base_url+"/archive/"
	start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
	end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
	delta = end_date - start_date
	infile = open('NewsPaper/prothom_alo'+start_date_str+"_to_"+end_date_str+".txt", "a")
	for i in range(delta.days + 1):
		date = start_date + timedelta(days = i)
		url = archive_url+date.strftime("%Y-%m-%d")
		while url:
			print("reading url >>> "+url)
			html_content = requests.get(url, headers = headers).content
			soup = BeautifulSoup(html_content, "lxml")
			links = soup.findAll('a', {'class': 'link_overlay'}, href = True)
			for link in links:
				inner_html_content = requests.get(base_url+link['href'], headers = headers).content
				inner_soup = BeautifulSoup(inner_html_content, "lxml")
				articleBody = inner_soup.find('div', {'itemprop': 'articleBody'})
				if articleBody:
					headline = inner_soup.find('div', {'class': 'right_title'}).text
					print("headline >>> "+headline)
					infile.write(headline+"\n")
					infile.write(create_sentences(articleBody.text))
			
			pagination_div = soup.find('div', {'class': 'pagination'})
			url = None
			if pagination_div:
				next_page_link = pagination_div.find('a', {'class': 'next_page'}, href = True)
				if next_page_link:
					url = archive_url + next_page_link['href']
	infile.close()
		
if __name__ == '__main__':
	# crawl_prothom_alo("2017-03-08","2017-06-01")
	crawl_prothom_alo("2016-01-20","2016-06-01")
