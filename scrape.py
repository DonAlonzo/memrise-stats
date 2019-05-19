from bs4 import BeautifulSoup
from requests import session
from requests_oauthlib import OAuth2Session
from math import ceil
import re
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import urllib.parse as urlparse
from collections import Counter
import time
import random
import os
import sys
import warnings

warnings.simplefilter("ignore")

login_url = "https://decks.memrise.com/login/"
username = os.environ['MEMRISE_USERNAME']
password = os.environ['MEMRISE_PASSWORD']

topics = [
  {
    "name": "politics",
    "shortname": "po",
    "courses": [
      {
        "url": "https://decks.memrise.com/course/8783/current-world-leaders-2/",
        "#": 62
      }
    ]
  },

  {
    "name": "catalan",
    "shortname": "CA",
    "courses": [
      {
        "url": "https://decks.memrise.com/course/2011394/turbocharge-catalan/",
        "#": 41
      }
    ]
  },

  {
    "name": "spanish",
    "shortname": "ES",
    "courses": [
      {
        "url": "https://decks.memrise.com/course/737/first-5000-words-of-spanish/",
        "#": 63
      },
      {
        "url": "https://decks.memrise.com/course/343554/first-5000-words-of-spanish-top-up-1-2/",
        "#": 10
      },
      {
        "url": "https://decks.memrise.com/course/343575/first-5000-words-of-spanish-top-up-2/",
        "#": 10
      },
      {
        "url": "https://decks.memrise.com/course/343661/first-5000-words-of-spanish-top-up-3/",
        "#": 10
      },
      {
        "url": "https://decks.memrise.com/course/2016225/turbocharge-spanish/",
        "#": 15
      }
    ]
  },

  {
    "name": "italian",
    "shortname": "IT",
    "courses": [
      {
        "url": "https://decks.memrise.com/course/1415384/5000-most-frequent-italian-words-audio/",
        "#": 43
      }
    ]
  },

  {
    "name": "portuguese",
    "shortname": "PT",
    "courses": [
      {
        "url": "https://decks.memrise.com/course/572/5000-word-frequency-list-with-audio/",
        "#": 167
      }
    ]
  },

  {
    "name": "french",
    "shortname": "FR",
    "courses": [
      {
        "url": "https://decks.memrise.com/course/131111/5000-most-common-french-words/",
        "#": 33
      }
    ]
  },

  {
    "name": "finnish",
    "shortname": "FI",
    "courses": [
      {
        "url": "https://decks.memrise.com/course/349091/7000-most-used-finnish-words/",
        "#": 48
      }
    ]
  },

  {
    "name": "german",
    "shortname": "DE",
    "courses": [
      {
        "url": "https://decks.memrise.com/course/47049/5000-words-top-87-sorted-by-frequency/",
        "#": 337
      }
    ]
  },

  {
    "name": "dutch",
    "shortname": "NL",
    "courses": [
      {
        "url": "https://decks.memrise.com/course/1857239/5000-most-frequent-dutch-words-audio/",
        "#": 2
      }
    ]
  },
 
  {
    "name": "swedish-sign-language",
    "shortname": "SS",
    "courses": [
      {
        "url": "https://decks.memrise.com/course/2040467/svenskt-teckensprak/",
        "#": 56
      }
    ]
  },

  {
    "name": "chinese",
    "shortname": "ZH",
    "courses": [
      {
        "url": "https://decks.memrise.com/course/541/hsk-level-1-introductory-mandarin-with-audio/",
        "#": 17
      }
    ]
  },

  {
    "name": "latin",
    "shortname": "LA",
    "courses": [
      {
        "url": "https://decks.memrise.com/course/2199888/turbocharge-latin/",
        "#": 32
      }
    ]
  },
  
  {
    "name": "danish",
    "shortname": "DA",
    "courses": [
      {
        "url": "https://decks.memrise.com/course/1052543/danska-for-svenskar-danish-for-swedes/",
        "#": 16
      }
    ]
  },

  {
    "name": "romanian",
    "shortname": "RO",
    "courses": [
      {
        "url": "https://decks.memrise.com/course/2196538/turbocharge-romanian/",
        "#": 23
      }
    ]
  },

  {
    "name": "geography",
    "shortname": "geo",
    "courses": [
      {
        "url": "https://decks.memrise.com/course/72039/afghan-provinces/",
        "#": 10
      },
      {
        "url": "https://decks.memrise.com/course/52936/american-geography/",
        "#": 18
      },
      {
        "url": "https://decks.memrise.com/course/65916/belgian-provinces/",
        "#": 3
      },
      {
        "url": "https://decks.memrise.com/course/45822/brazilian-states/",
        "#": 15
      },
      {
        "url": "https://decks.memrise.com/course/42769/country-mapping/",
        "#": 54
      },
      {
        "url": "https://decks.memrise.com/course/56177/danish-regions/",
        "#": 3
      },
      {
        "url": "https://decks.memrise.com/course/81962/egyptian-governorates/",
        "#": 12
      },
      {
        "url": "https://decks.memrise.com/course/81975/ethiopian-regions/",
        "#": 3
      },
      {
        "url": "https://decks.memrise.com/course/48366/federal-subjects-of-russia/",
        "#": 31
      },
      {
        "url": "https://decks.memrise.com/course/633958/finlands-landskapsforbund-lan-och-hist-landskap/",
        "#": 3
      },
      {
        "url": "https://decks.memrise.com/course/430917/geography-of-ireland-2/",
        "#": 5
      },
      {
        "url": "https://decks.memrise.com/course/82304/indian-states-union-territories/",
        "#": 5
      },
      {
        "url": "https://decks.memrise.com/course/55360/italian-regions/",
        "#": 6
      },
      {
        "url": "https://decks.memrise.com/course/166362/london-boroughs-2/",
        "#": 2
      },
      {
        "url": "https://decks.memrise.com/course/55145/mexican-states/",
        "#": 6
      },
      {
        "url": "https://decks.memrise.com/course/37152/mountain-superlatives/",
        "#": 13
      },
      {
        "url": "https://decks.memrise.com/course/56078/north-korean-provinces/",
        "#": 2
      },
      {
        "url": "https://decks.memrise.com/course/68038/norwegian-counties/",
        "#": 3
      },
      {
        "url": "https://decks.memrise.com/course/2071980/oresundsregionen/",
        "#": 2
      },
      {
        "url": "https://decks.memrise.com/course/457764/pakistani-geography/",
        "#": 4
      },
      {
        "url": "https://decks.memrise.com/course/1621892/political-divisions-of-bosnia-and-herzegovina/",
        "#": 4
      },
      {
        "url": "https://decks.memrise.com/course/68379/portuguese-districts/",
        "#": 5
      },
      {
        "url": "https://decks.memrise.com/course/34913/provinces-of-china-2/",
        "#": 15
      },
      {
        "url": "https://decks.memrise.com/course/819884/provinces-of-cuba/",
        "#": 2
      },
      {
        "url": "https://decks.memrise.com/course/1622431/regions-and-states-of-venezuela/",
        "#": 4
      },
      {
        "url": "https://decks.memrise.com/course/1155958/regions-of-france-as-of-july-2016/",
        "#": 3
      },
      {
        "url": "https://decks.memrise.com/course/28784/rivers-lakes-and-seas/",
        "#": 20
      },
      {
        "url": "https://decks.memrise.com/course/65903/saudi-arabian-provinces/",
        "#": 2
      },
      {
        "url": "https://decks.memrise.com/course/991/the-federal-states-of-germany/",
        "#": 10
      }
    ]
  }
]

with open("stats", "a") as file:
  file.write(time.strftime("\n%y-%m-%d\n"))
  file.write("     MEAN     SD   Now     7    30    60    90   7^-1  30^-1  60^-1  90^-1\n")
  file.flush()

  with session() as c:
    result = c.get(login_url, allow_redirects=True)
    page = BeautifulSoup(result.text, "lxml")
    next = page.find("input", {"type": "hidden", "name": "next"}).get("value")
    token = page.find("input", {"name": "csrfmiddlewaretoken"}).get("value")
    result = c.post(
      result.url,
      data = {
        'csrfmiddlewaretoken': token,
        'username': username,
        'password': password,
        'next': next
      },
      headers = dict(referer = result.url)
    )
    
    if len(sys.argv) > 1:
      topics = filter(lambda topic: topic["name"] in sys.argv, topics)

    for topic in topics:
      print(topic["name"])

      values = []
      for course in topic["courses"]:
        for i in range(1, course["#"] + 1):
          ix_url = course["url"] + str(i)
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

          print("{}/{}".format(i, course["#"]))
          #time.sleep(random.randrange(1, 3, 1))

      if len(values) != 0:
        mean = sum(values) / float(len(values))
        sd = (sum((xi - mean) ** 2 for xi in values) / float(len(values))) ** (1/2)
        now = values.count(0)
        print("mean: {}".format(mean))
        print("sd: {}".format(sd))
        print("now: {}".format(now))

        len_7 = len([word for word in values if word <= 7])
        len_30 = len([word for word in values if word <= 30])
        len_60 = len([word for word in values if word <= 60])
        len_90 = len([word for word in values if word <= 90])
        print("no. of words (7): {}".format(len_7))
        print("no. of words (30): {}".format(len_30))
        print("no. of words (60): {}".format(len_60))
        print("no. of words (90): {}".format(len_90))

        file.write("{} {:>6.2f} {:>6.2f} {:>5} {:>5} {:>5} {:>5} {:>5} {:>6.2f} {:>6.2f} {:>6.2f} {:>6.2f}\n".format(topic["shortname"], mean, sd, now, len_7, len_30, len_60, len_90, len_7/7, len_30/30, len_60/60, len_90/90))
        
        plt.hist(values, bins = max(values), edgecolor = 'black', facecolor = 'green', linewidth=0.8)
        counter = Counter(values)
        y_max = values.count(max(values, key = counter.get))
        plt.axis([0, max(values), 0, y_max])
        #plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(25))
        #plt.gca().yaxis.set_minor_locator(ticker.MultipleLocator(5))
        plt.grid(True)
        plt.savefig(os.path.join("graphs/days", "{}-{}.png".format(topic["name"], time.strftime("%y%m%d"))), dpi=600)
        plt.clf()
        plt.cla()
        
        plt.hist(values, bins = ceil(max(values) / 7), edgecolor = 'black', facecolor = 'green', linewidth=0.8)
        counter = Counter(values)
        y_max = values.count(max(values, key = counter.get))
        plt.axis([0, max(values), 0, y_max])
        #plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(25))
        #plt.gca().yaxis.set_minor_locator(ticker.MultipleLocator(5))
        plt.grid(True)
        plt.savefig(os.path.join("graphs/weeks", "{}-{}.png".format(topic["name"], time.strftime("%y%m%d"))), dpi=600)
        plt.clf()
        plt.cla()

        plt.hist(values, bins = max(values), edgecolor = 'black', facecolor = 'green', linewidth=0.8)
        plt.axis([0, 180, 0, 100])
        #plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(25))
        #plt.gca().yaxis.set_minor_locator(ticker.MultipleLocator(5))
        plt.grid(True)
        plt.savefig(os.path.join("graphs/days-norm", "{}-norm-{}.png".format(topic["name"], time.strftime("%y%m%d"))), dpi=600)
        plt.clf()
        plt.cla()

        plt.hist(values, bins = ceil(max(values) / 7), edgecolor = 'black', facecolor = 'green', linewidth=0.8)
        plt.axis([0, 180, 0, 700])
        #plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(25))
        #plt.gca().yaxis.set_minor_locator(ticker.MultipleLocator(5))
        plt.grid(True)
        plt.savefig(os.path.join("graphs/weeks-norm", "{}-norm-week-{}.png".format(topic["name"], time.strftime("%y%m%d"))), dpi=600)
        plt.clf()
        plt.cla()
      else:
        print("mean: N/A")
        print("sd: N/A")
        print("now: N/A")
        file.write("{}    N/A    N/A   N/A   N/A   N/A   N/A\n".format(topic["shortname"]))
      file.flush()
