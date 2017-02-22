import ssl
import pymongo

class API_Access():

    def getArticlesbyKeywords(self,keyword,showBody=False):
        client = pymongo.MongoClient(
            "mongodb://mahdi:Isentia@aws-ap-southeast-1-portal.2.dblayer.com:15312,aws-ap-southeast-1-portal.0.dblayer.com:15312/BBCArticles?ssl=true",
            ssl_cert_reqs=ssl.CERT_NONE)

        mydb = client['BBCArticles']
        ##mydb.adminCommand({'setParameter': True, 'textSearchEnabled': True})
        my_collection = mydb['Articles']
        my_collection.create_index([("Keywords.key", "text")])
        print 'Articles containing  higher occurences of the keyword is sorted as follow:'
        for doc in my_collection.find({"Keywords":{"$elemMatch" : {"$elemMatch": {"$in": [keyword]}}}}):
            print(doc)



api=API_Access()
api.getArticlesbyKeywords("UK")
