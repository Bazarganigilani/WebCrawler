import nltk

class keywordHandler():
    def __init__(self, corpusPath='C:\\nltk_data', numberofKeywords=5):
        self.corpusPath = corpusPath
        self.numberofKeywords = numberofKeywords


    def getKeywords(self, text):
        # words=text.split(' ')
        nltk.download("punkt", self.corpusPath)
        nltk.download("stopwords", self.corpusPath)
        nltk.download("universal_tagset", self.corpusPath)
        words = nltk.word_tokenize(text)

        # NLTK's default stopwords
        default_stopwords = set(nltk.corpus.stopwords.words('english'))

        custom_stopwords = set([u'This', u'That'])

        all_stopwords = default_stopwords | custom_stopwords

        # Remove single-character tokens (mostly punctuation)
        words = [word for word in words if len(word) > 1]

        # Lowercase all words (default_stopwords are lowercase too)
        words = [word.lower() for word in words]

        # Stemming words seems to make matters worse, disabled
        # stemmer = nltk.stem.snowball.SnowballStemmer('german')
        # words = [stemmer.stem(word) for word in words]
        # Remove stopwords
        words = [word for word in words if word not in all_stopwords]

        taggedWords = nltk.pos_tag(words, 'universal')


        taggedWords = [word for (word, tag) in taggedWords if tag == 'ADV' or tag == 'ADJ' or tag == 'NOUN']

        # Calculate frequency distribution
        fdist = nltk.FreqDist(taggedWords).most_common(self.numberofKeywords)

        # finalWords=list(set(nltk.word_tokenize(text)) - set(nltk.corpus.stopwords.words('english')))

        dict=[[word, count] for (word,count) in fdist]
        return dict
