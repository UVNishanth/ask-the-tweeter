
import csv

from tweet_index import TweetIndex


tweet_csv_filename = "../data/sample.csv"

class TestTweetSearcher:

    def __init__(self):
        global tweet_csv_filename
        list_of_tweets = []
        with open(tweet_csv_filename, "r") as f:
            csv_reader = csv.reader(f, delimiter=",")
            for i, row in enumerate(csv_reader):
                if i == 0:
                    # header
                    continue
                timestamp = int(row[0])
                tweet = str(row[1])
                list_of_tweets.append((timestamp, tweet))

        self.ti = TweetIndex()
        self.ti.process_tweets(list_of_tweets)

    def test_simple_search(self):
        assert self.ti.search("hello") == [('hello this is also jeeves', 15), ('hello not me', 14), 
                                    ('hello me', 13), ('hello stuff', 12), 
                                    ('hello jeeves this is bertie', 11)]
        assert self.ti.search("hello me") == [('hello not me', 14), ('hello me', 13),
                                    ('hello this is me', 6), ('hello jeeves me', 5)]
        assert self.ti.search("hello bye") == [('hello bye', 3)]
        assert self.ti.search("hello this bertie") == [('hello jeeves this is bertie', 11)]
        assert self.ti.search("notinanytweets") == []
        print("Success: test Simple Search")

    def test_logical_query(self):
        assert self.ti.search("hello & jeeves") == [('hello this is also jeeves', 15),
                                ('hello jeeves this is bertie', 11), ('hello jeeves this is jeeves', 10), 
                                ('hello jeeves me', 5), ('hello this is jeeves', 4)]
        assert self.ti.search("hello | this") == [('hello this is also jeeves', 15), ('hello not me', 14),
                                ('hello me', 13), ('hello stuff', 12), ('hello jeeves this is bertie', 11)]
        assert self.ti.search("!hello") == [('jeeves', 7), ('some tweet', 2), ('yay', 0)]
        print("Success: test Logical Query")

    def test_complex_query(self):
        assert self.ti.search("stuff | (hello & jeeves)") == [('hello this is also jeeves', 15),
                                ('hello stuff', 12), ('hello jeeves this is bertie', 11), 
                                ('hello jeeves this is jeeves', 10), ('hello jeeves me', 5)]
        assert self.ti.search("(hello & jeeves) & !this") == [('hello jeeves me', 5)]
        assert self.ti.search("hello & (this & is & !(jeeves | bertie))") == [('hello this is me', 6)]
        print("Success: test Complex Query")

    def test_unusual_case(self):
        # where a query term is not present in the inverted index
        assert self.ti.search("daseqdasd | (hello & jeeves)") == [('hello this is also jeeves', 15), 
                                ('hello jeeves this is bertie', 11), 
                                ('hello jeeves this is jeeves', 10), ('hello jeeves me', 5), 
                                ('hello this is jeeves', 4)]

        # when empty string is passed as query
        assert self.ti.search("") == []
        print("Success: test Unusual Case")

def main():
    tester = TestTweetSearcher()
    tester.test_simple_search()
    tester.test_logical_query()
    tester.test_complex_query()
    tester.test_unusual_case()

if __name__ == "__main__":
    main()
    
 