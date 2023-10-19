# This file keeps a list of the swimmers' birthdays that updates automatically
import datetime
import webscrape

# create a dictionary of swimmer birthdays
swimmer_bday = {
  'Leo Zhi': '2004-05-01',
  'Alfred Chen': '2011-08-12',
  'Sophia Dadivas': '2011-10-18',
  'Colin Du': '2013-10-14',
  'Khang Duong': '2010-11-16',
  'Tristan Gfrerer': '2010-07-31',
  'Frances Goleco': '2010-09-30',
  'Sam Halton': '2011-04-20',
  'Grace Ho': '2013-01-06',
  'Zach Lam': '2011-05-29',
  'Marlo Laurence': '2010-04-14',
  'Matthew Liang': '2010-10-10',
  'Ethan Man': '2012-03-26',
  'Paige Nesbitt': '2012-10-08',
  'Enzo Ronque': '2011-09-26',
  'Keen Shimakura-Thomas': '2012-02-26',
  'Connor Soong': ' 2011-01-30'
}


def getAge(swimmer):
  today = str(datetime.date.today()) # returns date in the format yyyy-mm-dd
  
  # find the name and birthday of the swimmer
  name, bday = webscrape.name_match(swimmer_bday,swimmer)

  if bday is None:
    return None
  
  # find the age of the swimmer
  age = int(today[0:4]) - int(bday[0:4])


  # if birthday has not yet passed
  if int(today[5:7]) < int(bday[5:7]):
    age -= 1

  elif int(today[5:7]) == int(bday[5:7]):
    if int(today[8:]) < int(bday[8:]):
      age -= 1

  return age
