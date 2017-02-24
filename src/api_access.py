import ssl
import pymongo
import sys


class API_Access():

    def getArticlesbyKeywords(self,keyword,showBody=False):
        try:
            client = pymongo.MongoClient(
            "mongodb://mahdi:Isentia@aws-ap-southeast-1-portal.2.dblayer.com:15312,aws-ap-southeast-1-portal.0.dblayer.com:15312/BBCArticles?ssl=true",
            ssl_cert_reqs=ssl.CERT_NONE)

            mydb = client['BBCArticles']
            ##mydb.adminCommand({'setParameter': True, 'textSearchEnabled': True})
            my_collection = mydb['Articles']
            my_collection.create_index([("Keywords.key", "text")])
            print 'Articles containing  higher occurences of the keyword is sorted as follow:'
            #for doc in my_collection.find({"Keywords":{"$elemMatch" : {"$elemMatch": {"$in": [keyword]}}}}):
            for doc in my_collection.find(
                    {"$text": {"$search": keyword}}):#.sort({"score": {"$meta": "textScore"}}):
                print(doc)
        except Exception as ex:
            print "Unexpected error while connecting to the DB : ", ex
            print ("Application exists.")
            sys.exit(2)

#api=API_Access()
##api.getArticlesbyKeywords("north")