# ask-the-tweeter
Logical Query Processor for tweets searching

Once tweet corpus is stored in the format:
```
timestamp, tweet
```
The processor can be passed a logical query to fetch the satisfying tweet set.<br/><br/>
The processor can handle complex logical queries made up of & (and), | (or) and !(not)
```
Sample query: hello & (this & is & !(jeeves | bertie))
```
