import datetime
import re
import ssl
import sys

import pymongo
import scrapy
from lxml.etree import tostring as htmlstring
from lxml.html import fromstring
from lxml.html.clean import Cleaner
from pip._vendor import requests
from scrapy.http import Request
from scrapy.spiders import Spider

from keyword_handler import keywordHandler

class BBCItem(scrapy.Item):
  title = scrapy.Field()

class BBCSpider(Spider):
  name = "tutsplus"
  allowed_domains   = ["bbc.com"]
  start_urls = ["http://www.bbc.com/"]

  #Delete previous entries from the DB
  try:
      client = pymongo.MongoClient(
      "mongodb://mahdi:Isentia@aws-ap-southeast-1-portal.2.dblayer.com:15312,aws-ap-southeast-1-portal.0.dblayer.com:15312/BBCArticles?ssl=true",
      ssl_cert_reqs=ssl.CERT_NONE)
      mydb = client['BBCArticles']
      my_collection = mydb['Articles']
      my_collection.delete_many({})
  except Exception:
      print("Unexpected error while connecting to the DB :", sys.exc_info()[0])
      print("Application exists.")
      sys.exit(2)

  def parse(self, response):
      links = response.xpath('//a/@href').extract()

      # print("Links are %s" %links)

      # We stored already crawled links in this list
      crawledLinks = []


      for link in links:
          # If it is a proper link and is not checked yet, yield it to the Spider
          # if linkPattern.match(link) and not link in crawledLinks:
          if not link in crawledLinks:
              link = "http://www.bbc.com" + link
              crawledLinks.append(link)
              yield Request(link, self.parse)

      crawledTitles = []
      titles = response.xpath("//a[@class='media__link']").extract()
      # titles = response.xpath('//a/@href').extract()
      print ("Maximum %d article links was found in the current page" % len(titles))
      print ("Starting traversing them")

      linkPattern = re.compile("^\/[\s\S]*")
      count = 0
      for title in titles:
          if not title in crawledTitles:
              count=count+1
              crawledTitles.append(title)
              item = BBCItem()
              item["title"] = title
              #print("Title is : %s" % title)

              #pdb.set_trace()
              tree = fromstring(title.encode('utf-8'))

              link = tree.xpath("//a/@href")
              if not linkPattern.match(link[0]): continue

              link = "http://www.bbc.com" + link[0]
              print("Populating the database with the entry at the link: %s" % link)

              response = requests.get(link)
              innerTree = fromstring(response.text.encode('utf-8'))

              """
              api = urllib2.urlopen("http://help.websiteos.com/websiteos/example_of_a_simple_html_page.htm")
              page = api.read()
              tree = etree.HTML(page)

              #table = tree.xpath("//div[@class='story-body__inner']")
              table = tree.xpath("//style[@type='text/css']")
              res = etree.tostring(table)
              print("res is ")
              """

              #print(div0.text_content())
              title = innerTree.xpath("//title/text()")
              headline = innerTree.xpath("//p[@class='story-body__introduction']/text()")
              divs = innerTree.cssselect('div.story-body__inner')
              if(len(divs)==0):
                  print("Omitting the link. The entry is not an article")
                  continue
              div0 = divs[0]
              #remoe script tag first
              cleaner = Cleaner(scripts=True, annoying_tags = True, remove_unknown_tags = True,comments = True, javascript = True, embedded=True, meta=True, page_structure=True, links=True, style=True,
                                remove_tags=['h1','span','figcaption'])  # ['a', 'li', 'td','div','ul','p','figure','figcaption','span','hr','img','h1','h2','h3'])
              cleanedTag=fromstring(cleaner.clean_html(htmlstring(div0)))
              #remove other tags as well
              innerBodyText=cleanedTag.text_content().encode('utf-8')

              cleanedInnerBodyText=" ".join(innerBodyText.split())

              try:
                  print("Inserting the record into the DB")
                  client = pymongo.MongoClient(
                      "mongodb://mahdi:Isentia@aws-ap-southeast-1-portal.2.dblayer.com:15312,aws-ap-southeast-1-portal.0.dblayer.com:15312/BBCArticles?ssl=true",
                      ssl_cert_reqs=ssl.CERT_NONE)

                  mydb = client['BBCArticles']
                  my_collection = mydb['Articles']

                  keyword_handler= keywordHandler()


                  keywords=keyword_handler.getKeywords(cleanedInnerBodyText)

                  """

                  print("innerBody text.")
                  print (cleanedInnerBodyText)

                  print("keywords are...")

                  print keywords
                  """

                  myrecord = {"Link": link,
                              "Title": title,
                              "HeadLine": headline,
                              "BodyText":innerBodyText,
                              "Keywords":keywords,
                              "date": datetime.datetime.utcnow()
                              }


                  result = my_collection.insert_one(myrecord, False)
              except Exception as ex:
                  print "Unexpected error while inserting record to the DB : ", ex
                  print ("Application exists.")
                  sys.exit(2)
              yield item






