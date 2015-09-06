from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from icalendar import Calendar, Event
import re
import urllib2

homepage = urllib2.urlopen('http://www.ifccenter.com/')
soup = BeautifulSoup(homepage, 'html.parser')

cal = Calendar()
cal.add('prodid', '-//My calendar product//mxm.dk//')
cal.add('version', '2.0')
# cal.add('dtstart', datetime(2015, 01, 01))

for div in soup.find_all('div', id=re.compile('day_.*')):
  partial_date = div.find('h4').string
  showdate = datetime.strptime(partial_date, '%A, %B %d').replace(year=date.today().year)
  print showdate
  for movie in div.find_all('li'):
    movie_link = movie.a
    movie_title = movie.a.string
    print movie_title
    for showtime_str in movie.find_all('a', href=re.compile('http://www.movietickets.com/.*')):
      showtime = datetime.strptime(showtime_str.string, '%I:%M %p')
      full_showtime = datetime.combine(showdate.date(), showtime.time())
      print full_showtime
      event = Event()
      event.add('summary', movie_title)
      event.add('dtstart', full_showtime)
      # TODO: Look up running time
      event.add('dtend', full_showtime + timedelta(hours=2))
      cal.add_component(event)

f = open('/tmp/example.ics', 'wb')
f.write(cal.to_ical())
f.close()
