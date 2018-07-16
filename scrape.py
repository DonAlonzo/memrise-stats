from bs4 import BeautifulSoup
from requests import session
import re
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from collections import Counter
import time
import random
import os

login_url = "https://www.memrise.com/login/"
username = os.environ['MEMRISE_USERNAME']
password = os.environ['MEMRISE_PASSWORD']

courses = [
  [
    "https://www.memrise.com/course/737/first-5000-words-of-spanish/",
    "spanish",
    "ES",
    63
  ],
  [
    "https://www.memrise.com/course/1415384/5000-most-frequent-italian-words-audio/",
    "italian",
    "IT",
    43
  ],
  [
    "https://www.memrise.com/course/572/5000-word-frequency-list-with-audio/",
    "portuguese",
    "PT",
    167
  ],
  [
    "https://www.memrise.com/course/131111/5000-most-common-french-words/",
    "french",
    "FR",
    33
  ],
  [
    "https://www.memrise.com/course/349091/7000-most-used-finnish-words/",
    "finnish",
    "FI",
    48
  ],
  [
    "https://www.memrise.com/course/47049/5000-words-top-87-sorted-by-frequency/",
    "german",
    "DE",
    337
  ],
  [
    "https://www.memrise.com/course/1857239/5000-most-frequent-dutch-words-audio/",
    "dutch",
    "NL",
    2
  ],
  [
    "https://www.memrise.com/course/541/hsk-level-1-introductory-mandarin-with-audio/",
    "chinese",
    "ZH",
    13
  ]
]

with open("stats", "a") as file:
  file.write(time.strftime("\n%y-%m-%d\n"))
  file.flush()

  with session() as c:
    result = c.get(login_url)

    login = BeautifulSoup(result.text, "lxml")
    token = login.find("input", {"name": "csrfmiddlewaretoken"}).get("value")

    result = c.post(
      login_url,
      data = {
        'username': username,
        'password': password,
        'csrfmiddlewaretoken': token
      },
      headers = dict(referer = login_url)
    )

    for course in courses:
      print(course[1])

      values = []
      for i in range(1, course[3] + 1):
        ix_url = course[0] + str(i)
        response = c.get(
          ix_url,
          headers = dict(referer = ix_url)
        )

        page = BeautifulSoup(response.text, "lxml")
        statuses = [status.string for status in page.find_all("div", {"class": "status"})]
        
        matcher = lambda status: re.search("in (.*) (.*)", status)
        matches = list(map(matcher, filter(lambda status: status != "Ignored", statuses)))

        parser = lambda duration, type: {
          'days': 1 if (duration == "about a" or duration == "about an") else int(duration),
          'day': 1,
          'hours': 0,
          'hour': 0,
          'minutes': 0,
          'minute': 0,
          'seconds': 0,
          'second': 0
        }[type]
        converter = lambda match: parser(match.group(1), match.group(2)) if match != None else 0
        values.extend(list(map(converter, matches)))

        print("{}/{}".format(i, course[3]))
        time.sleep(random.randrange(1, 15, 1))

      if len(values) != 0:
        mean = sum(values) / float(len(values))
        sd = (sum((xi - mean) ** 2 for xi in values) / float(len(values))) ** (1/2)
        now = values.count(0)
        print("mean: {}".format(mean))
        print("sd: {}".format(sd))
        print("now: {}".format(now))
        file.write("{} {:0.2f} {:0.2f} {}\n".format(course[2], mean, sd, now))
        
        plt.hist(values, bins = max(values), edgecolor = 'black', facecolor = 'green', linewidth=0.8)
        counter = Counter(values)
        y_max = values.count(max(values, key = counter.get))
        plt.axis([0, max(values), 0, y_max])
        #plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(25))
        #plt.gca().yaxis.set_minor_locator(ticker.MultipleLocator(5))
        plt.grid(True)
        plt.savefig(os.path.join("graphs", "{}-{}.png".format(course[1], time.strftime("%y%m%d"))), dpi=600)
        plt.clf()
        plt.cla()

        plt.hist(values, bins = max(values), edgecolor = 'black', facecolor = 'green', linewidth=0.8)
        plt.axis([0, 180, 0, 50])
        #plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(25))
        #plt.gca().yaxis.set_minor_locator(ticker.MultipleLocator(5))
        plt.grid(True)
        plt.savefig(os.path.join("graphs", "{}-norm-{}.png".format(course[1], time.strftime("%y%m%d"))), dpi=600)
        plt.clf()
        plt.cla()
      else:
        print("mean: N/A")
        print("sd: N/A")
        print("now: N/A")
        file.write("{} N/A   N/A   N/A\n".format(course[2]))
      file.flush()
