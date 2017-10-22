from wikipedia import search, page


if __name__ == '__main__':
	titles = search("বাংলা")
	wikipage = page("https://bn.wikipedia.org/wiki/%E0%A6%85")
	print(wikipage.url)
	