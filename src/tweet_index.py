import csv
from typing import List, Tuple, Set
import time

from in_to_pos import processQueryToPostfix
from stack import Stack

def And(set1: Set[int], set2: Set[int]) -> Set[int]:
    return set1.intersection(set2)

def Or(set1: Set[int], set2: Set[int]) -> Set[int]:
    return set1.union(set2)

def Not(set1: Set[int], set2: Set[int]) -> Set[int]:
    return set1.difference(set2)

class TweetIndex:
    def __init__(self):
        self.list_of_tweets = []
        #dict to map timestamp to tweets
        self.tweet_dict = {}
        self.tweets_to_return = 5

    def process_tweets(self, list_of_timestamps_and_tweets: List[Tuple[str, int]]) -> None:


        #removing punctuations
        punctuation_list = [".", "?", "!", ",", ":", ";", "-", "[", "]", "(", ")", "{", "}", "\'", "\""]
        #using set for quick lookup
        p_list = set(punctuation_list)
        tokens = set()

        #all_docs_set is majorly used to handle "not" operations.
        all_docs_set = set()
        for row in list_of_timestamps_and_tweets:
            timestamp = int(row[0])
            tweet = str(row[1])
            #standardize the tweets
            processed_tweet = ''.join(c.lower() for c in tweet if c not in p_list)
            #print(f'{process_tweet}')
            tokens.update(processed_tweet.split(' '))
            #print(f'tokens: {tokens}\n')
            self.tweet_dict[timestamp] = tweet
            self.list_of_tweets.append((processed_tweet, timestamp))
            all_docs_set.add(timestamp)
        #print(f'all_docs_set: {all_docs_set}\n\n')
        terms = list(tokens)
        #tokens.sort()
        #print(terms)
        #create inverted index
        self.posting_list = {}
        for term in terms:
            self.posting_list[term] = set()
            for tweet in self.list_of_tweets:
                if term in tweet[0]:
                    self.posting_list[term].add(tweet[1])
        
        # adding all_docs_set in posting list for easier set operations
        self.posting_list["#"] = all_docs_set
        #print(self.posting_list)

    def search(self, query: str) -> List[Tuple[str, int]]:
        """
        
        Design decisions:
        1. used 2 step process to process query. first, query gets converted into postfix and then 
           the postfix query is evaluated. Used a 2-step process rather than directly handling the 
           infix query because I could easily use widely-used logic of infix-to-postfix conversion
           and then using postfix evaluation using stack rather than spending time on writing infix
           evaluation
        2. Also, using postfix evaluation uses one stack. infix evaluation uses 2 stacks 
           (operands, operators)
        """

        '''
        Old logic
        def runOld(query):
            list_of_words = query.split(" ")
            result_tweet, result_timestamp = "", -1
            for tweet, timestamp in self.list_of_tweets:
                words_in_tweet = tweet.split(" ")
                tweet_contains_query = True
                for word in list_of_words:
                    if word not in words_in_tweet:
                        tweet_contains_query = False
                        break
                if tweet_contains_query and timestamp > result_timestamp:
                    result_tweet, result_timestamp = tweet, timestamp
            return [(result_tweet, result_timestamp)] if result_timestamp != -1 else []
        '''

        def runNew(query):
            operators = set(['&', '|', '-', '(', ')' ])
            
            if len(query) > 1 and not(any(term in operators for term in query)):
                query = query.replace(" ", " & ")

            #print(f'new query: {query}')
            #exit()
            
            
            
            processed_query = processQueryToPostfix(query)
            processed_query = processed_query.split(" ")
            #print(f'wordsquery: {processed_query}')
            #Time and space complexity - O(q*m)
            def processQuery(query):
                #operators = set(['&', '|', '-', '(', ')' ])
                stack = Stack()
                for i in query:
                    if i not in operators:
                        try:
                            stack.push(self.posting_list[i])
                        except KeyError:
                            stack.push(set()) # when there's no tweet containing that term
                    else:
                        val1 = stack.pop()
                        val2 = stack.pop()
                        if i == '-':
                            stack.push(Not(val2, val1))
                        else:       
                        # switch statement to perform operation
                            #Complexity for logical operations
                            #   Time & Space - O(m) where m is number of tweets (documents)
                            switcher ={'&': And(val2,val1), '|': Or(val2, val1)}
                            stack.push(switcher.get(i))
                return stack.pop()

            ans = sorted(list(processQuery(processed_query)), reverse=True)
            ans = ans[:self.tweets_to_return]           # trimming set before fetching tweets so that we do not fetch tweets for
                                    # unwanted keys
            return [(self.tweet_dict[i], i) for i in ans] if ans else []
        
        #return runOld(query) 
        return runNew(query)


#def main():
    # A full list of tweets is available in data/tweets.csv for your use.
    # tweet_csv_filename = "../data/tweets.csv"
    # list_of_tweets = []
    # with open(tweet_csv_filename, "r") as f:
    #     csv_reader = csv.reader(f, delimiter=",")
    #     for i, row in enumerate(csv_reader):
    #         if i == 0:
    #             # header
    #             continue
    #         timestamp = int(row[0])
    #         tweet = str(row[1])
    #         list_of_tweets.append((timestamp, tweet))

    # ti = TweetIndex()
    # ti.process_tweets(list_of_tweets)
    #print(ti.search("stuff | (hello & neeva)"))
    #print(ti.search("daseqdasd | (hello & neeva)"))    #case where a term does not match any posting list key
    #start = time.time()
    #print(ti.search("neeva"))
    #end = time.time()
    #print(f'Elapsed time: {(end-start):.20f} seconds')
    #print(ti.search("hello"))
    #print(ti.search("hello this bob"))
    # assert ti.search("hello") == [('hello this is also neeva', 15)]
    # assert ti.search("hello me") == [('hello not me', 14)]
    # assert ti.search("hello bye") == [('hello bye', 3)]
    # assert ti.search("hello this bob") == [('hello neeva this is bob', 11)]
    # assert ti.search("notinanytweets") == []
    # print("Success!")

    #print(ti.search(""))


# if __name__ == "__main__":
#     main()
