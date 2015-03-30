#!/usr/bin/python

# This script is intended to download all epub file from specific search query and automatically put the files in the current directory.
# For example, you can download all Jane Austen ebook (epub) from gutenberg.org
# There's no need to manually change the files name, since it has been changed automatically.

import requests
import bs4
import urllib2
import os
import re
import urllib

# To isolate etext book number from the index
hrefpat=re.compile("href=\"\/ebooks\/([0-9]{1,5})\"") # {1,5} shows range of the digit id.  e.g. 1342 (four digitid) for Jane Austen's Pride and Prejudice book.


ids=set()
f=urllib2.urlopen("http://www.gutenberg.org/ebooks/search/?query=jane+austen") # Search result for all Jane Austen's books
for line in f:
	m=hrefpat.search(line)
	if m:
		bookid=m.group(1) 
		ids.add(bookid)
		print "Found ebook id", bookid
		print 
		print ids

f.close()


def rename_file():
	r = requests.get("http://gutenberg.org/ebooks/%s"%id)
	soup = bs4.BeautifulSoup(r.content)
	title = soup.findAll("h1")
	title_str = str(title)
	title_final = title_str[21:-6] + '.epub'

	for filename in os.listdir("."):
		if filename.startswith("%s"%id):
			os.rename(filename, title_final)



for id in ids:
	new_url="http://gutenberg.org/ebooks/%s.epub.noimages"%id
	print new_url
	web_file=urllib.urlopen(new_url)
	local_file=open('%s.epub' %id, 'w')
	local_file.write(web_file.read())
	web_file.close()
	local_file.close()
	rename_file()
