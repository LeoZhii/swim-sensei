from bs4 import BeautifulSoup
import requests
import csv

# the goal of this file is to scrape swim canada's website for
# each swimmer's best time and race info. This data is then stored
# in a unique csv file for each swimmer.

# create a dictionary of swimmer IDs
swimmer_ID = {
  'Leo Zhi': 4914314,
  'Alfred Chen': 5589593,
  'Sophia Dadivas': 5589598,
  'Colin Du': 5586875,
  'Khang Duong': 5561009,
  'Tristan Gfrerer': None,
  'Frances Goleco': 5246304,
  'Sam Halton': 5586878,
  'Grace Ho': 5629827,
  'Zach Lam': 5607310,
  'Marlo Laurence': 5557466,
  'Matthew Liang': 5319398,
  'Ethan Man': 5589612,
  'Paige Nesbitt': 5589615,
  'Enzo Ronque': 5608921,
  'Keen Shimakura-Thomas': 5589619,
  'Connor Soong': 5589620
}


# make the dictionary searchable
def name_match(dictionary, search_string):
  for key, value in dictionary.items():
    if search_string.lower() in key.lower():
      return key, value
  return search_string, None  # Return None if no partial match is found


# create a csv file
def create(id):
  # create the unique url for each swimmer
  # swimmer = 'Leo Zhi'
  # id = swimmer_ID[swimmer]
  url = f'https://www.swimming.ca/en/swimmer/{id}/'

  # store website html as a variable
  html_text = requests.get(url).text
  soup = BeautifulSoup(html_text, 'lxml')

  # find all timed results tags <tr>
  athelete_container = soup.find('section', id='athlete-results-container')
  results = athelete_container.find('tbody')
  dataset = results.find_all('td')

  # only keep text
  items = []
  for i in range(len(dataset)):
    items.append(dataset[i].text)

  # organize items into a csv
  with open(f'{id}.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    # Split the data into rows starting with distance
    row = []
    prefixes = ['50m ', '100', '200', '400', '800']

    for item in items:
      if any(item.startswith(prefix) for prefix in prefixes) and row:
        writer.writerow(row)
        row = []
      row.append(item)


def update():
  for name in swimmer_ID:
    if swimmer_ID[name] is None:
      pass
    else:
      create(swimmer_ID[name])
