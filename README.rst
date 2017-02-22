Run "main - h" for instructions how to use this program.
The program is involved two steps
1- It crawls the web pages on BBC.COM and find the pages denoting an article
2- it fetch relevant articles based on a keyword
if you want to do above two instructions manually:
  1- To crawl pages, go to src package and run the crawler using: "scrapy runspider crawler.py"
  2- To fetch articles based on a keyword, run main.py -k 'keyword_name'