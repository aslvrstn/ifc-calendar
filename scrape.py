from bs4 import BeautifulSoup
import re
import urllib2

dateless_page = urllib2.urlopen('http://www.ifccenter.com/')
soup = BeautifulSoup(dateless_page, "html.parser")

for div in soup.find_all('div', id=re.compile('day_.*')):
  date = div.find('h4').string
  print date
