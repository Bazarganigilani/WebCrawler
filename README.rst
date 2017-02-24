Run "main - h" for instructions how to use this program.
The program is involved two steps
1- It crawls the web pages from BBC.com and insert article pages as an entry to the MongoDB database
2- it fetches the relevant articles based on a keyword 
The application identifies keywords for each article based on its frequency in the article's text body. By default, the most 5 frequent words in the text body of an article are keywords. A keyword is a noun and not a stopping or common word.
To do above two instructions manually:
  1- To crawl pages, run "Python main.py -o crawl"
  2- To fetch articles based on a keyword, run " Python main.py -k keyword_name"
