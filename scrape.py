from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta
from icalendar import Calendar, Event
from pytz import timezone
import re
import urllib2

homepage = urllib2.urlopen('http://www.ifccenter.com/')
soup = BeautifulSoup(homepage, 'html5lib')

cal = Calendar()
cal.add('prodid', '-//My calendar product//mxm.dk//')
cal.add('version', '2.0')

for div in soup.find_all('div', id=re.compile('day_.*')):
  partial_date = div.find('h4').string
  showdate = datetime.strptime(partial_date, '%A, %B %d').replace(year=date.today().year)
  for movie in div.find_all('li'):
    movie_link = movie.a
    movie_title = movie_link.string
    for showtime_str in movie.find_all('a', href=re.compile('http://www.movietickets.com/.*')):
      showtime = datetime.strptime(showtime_str.string, '%I:%M %p')
      naive_full_showtime = datetime.combine(showdate.date(), showtime.time())
      full_showtime = timezone('US/Eastern').localize(naive_full_showtime)

      event = Event()
      event.add('summary', movie_title)
      event.add('dtstart', full_showtime)
      # TODO: Look up running time
      event.add('dtend', full_showtime + timedelta(hours=2))
      cal.add_component(event)

f = open('ifccalendar.ics', 'wb')
f.write(cal.to_ical())
f.close()
