__author__='Bazargani'

import subprocess
import sys, getopt

def main(argv):
   crawling_level = None
   try:
      opts, args = getopt.getopt(argv,"o:k",["option=", "keyword"])
   except getopt.GetoptError:
      print 'main.py -o <option> [ -k <keyword_name> ]'
      print "Available options are:"
      print "   crawl   Run crawler to crawl BBC.com"
      print "   search  -k <keyword_name>    Fetch articles by a specific keyword"
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
          print 'main.py -o <option> [ -k <keyword_name> ]'
          print "Available options are:"
          print "   crawl   Run crawler to crawl BBC.com"
          print "   search  -k <keyword_name>    Fetch articles by a specific keyword"
          sys.exit(2)
      elif opt in ("-o", "--option"):
           if arg=="crawl":
               scrapy_command = 'scrapy runspider {spider_name} -a crawling_level="{param_1}"'.format(
                   spider_name='src/crawler.py',
                   param_1=crawling_level)
               process = subprocess.Popen(scrapy_command, shell=True)
      elif opt in ("-k", "--keyword"):
                from src.api_access import API_Access
                api=API_Access()
                api.getArticlesbyKeywords(arg)

      elif():
          print "The correct usage is as follow:"
          print 'main.py -o <option> [ -k <keyword_name> ]'
          print "Available options are:"
          print "   crawl   Run crawler to crawl BBC.com"
          print "   search  -k <keyword_name>    Fetch articles by a specific keyword"
          sys.exit(2)

if __name__ == "__main__":
   main(sys.argv[1:])
