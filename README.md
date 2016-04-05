The Coding challenge was done in Python

The python libraries(Dependencies) which are required for this code to run are
1.pandas
2.os
3.datetime
4.timedelta
5.simplejson


PROBLEM STATEMENT:
Each tweet has one or more hashtags. Calculate the rolling average scores as the new tweet comes by updating the 60 second sliding window with respect to the latest tweet.

BACKGROUND AND THE THOUGHT PROCESS TO ARRIVE AT AN ALGORITHM TO COMPUTE THE ROLLING AVERAGE SCORE

Average score = (Sum of each hashtag score)/(# of unique hashtags)

Instead of calculating each hashtag score and summing up, I came up with a unique formula which effectively does the same

Since the numerator of the score is a summation of all the hashtags score, we can write the above formula as

Average score = sum(the Contribution of all the hashtags @ Tweetlvl ) for all tweets /(# of unique hashtags)

(sum of the Contribution of all the hashtags @ Tweetlvl )
=(# of hashtags in a tweet - 1)* # NewHashtags + #NewHashtags*(# of hashtags in a tweet - #NewHashtags)

#NewHashtags = # of NewHastags which are there in the new tweet when compared to all the hashtags from the previous tweets included in the 60 second sliding window.

NOTES:
Before calculating the score, we always update the sliding window and remove the tweets which do not fall in the 60's window

For example: if there are 4 hashtags(#A,#B,#C,#D) in a tweet, then the total contribution of this tweet is 3*4 = 12 
Similarly this score is caclulated for each tweet and summed up for the tweets within the 60 second sliding window.


After Loading the tweets present in the tweets.txt

The following algorithm is employed whenever a new tweet comes

1. Load each tweet into a rolling dataframe
2. Add the new tags into a list which records the unique hashtags. Unique hastags will be updated everytime a new tweet comes
2. Filter the tweets based on the 60 second sliding window
3. Calculate the Contribution of all the hashtags @ Tweetlvl 
4. Sum the Contribution of all the hashtags @ Tweetlvl for all tweets in the filtered dataframe
5. Calculate the # of unique hastags from the list of unique hastags obtained after filtering tweets based on the 60's window
6. Calculate the Average Degree by using the formula mentioned in the background and thought process section


