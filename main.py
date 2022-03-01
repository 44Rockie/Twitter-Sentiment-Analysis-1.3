# A basic Twitter Sentiment Analysis program that does not require Twitter API keys or access tokens.  The first several
# attempts at creating a Twitter Sentiment Analysis program, I was having a great deal of difficulty getting Tweepy
# to search and authorize the access to scrape tweets from Twitter and spent around 7 hours trying to go down that route
# for the program. Since python is such a great coding environment in that it has multiple routes and methods, libraries
# and ways to accomplish similar tasks I began researching different methods to perform sentiment analysis on tweets.
# The total time it took for me to complete the assignment was around 14 hours with all the research and then the coding
# and running the program to ensure it was working correctly. I ended up using pandas, datetime, re,and nltk
# libraries to create a program that would scrape tweets and analyze sentiment.
# While several assignments ago I initially had difficulty downloading and importing nltk, it has been a powerful API
# that has enabled me to successfully complete several assignments now and I am huge fan of it!

# The imported libraries necessary to scrape tweets from Twitter and to perform sentiment analysis on them
import pandas as pd
import datetime as dt
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import snscrape.modules.twitter as sntwitter
import nltk

# Download for Sentiment Analysis
nltk.download('vader_lexicon')

# Global Constants for Main function
CHOICE_1 = 1
QUIT = 2


# Function that calls the menu with error handling and allows the user
# to keep search tweets until they are ready to quit
def main():
    menu()
    choice = 0
    while choice != QUIT:
        choice = int(input('Please Enter Your Selection: '))
        if choice == CHOICE_1:
            twitter_analysis()
        elif choice == QUIT:
            print('Hasta La Vista! See You Later!')
        else:
            print('Error. Please Enter a valid selection. ')


# main menu function gives, tells the user what the program
def menu():
    print()
    print('Welcome to Twitter and Sentiment Analysis')
    print('******************************************')
    print('Enter 1 To Search Tweets on Twitter for A Subject')
    print('Enter 2 To Quit the Program')
    print()


# primary function of the program to scrape tweets from Twitter and analyze their sentiment
def twitter_analysis():
    # Prompt for the user to enter a search subject
    search = input("Enter Subject You Would to Search: ")

    # If statements to ensure there is a valid user input for the search, number of tweets, and number of days
    if search != '':
        # prompt for the user to enter the number of tweets they wish to search
        num_of_Tweets = input("Enter the Number of Tweets You Wish To Search: ")
        if num_of_Tweets != '':
            # prompt for the user to input the number of days they wish to search tweets over
            num_of_days = input("Enter the number of days you want to Search Tweets for: ")
            # if statement to ensure the user has entered a valid input
            if num_of_days != '':
                # creation of a list to store the data
                tweets_list = []
                # variable to hold today's date
                today = dt.date.today()
                # format the date in the variable
                today = today.strftime('%Y-%m-%d')
                # variable to hold the range of days from current day through the number of days the user entered
                past = dt.date.today() - dt.timedelta(days=int(num_of_days))
                # format the date in the variable
                past = past.strftime('%Y-%m-%d')
                # scrapes Twitter in the parameters entered by the user inputs
                for i, tweet in enumerate(sntwitter.TwitterSearchScraper(
                        search + ' lang:en since:' + past + ' until:' + today + ' -filter:links -filter:replies').get_items()):
                    if i > int(num_of_Tweets):
                        break
                    # appends the results to the list created above
                    tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.username])

                # Creating a panda dataframe from the tweets scraped and stored in tweets_list
                stored_data = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])

                print(stored_data)

    # Function to remove mentions, hashtags, retweets, and hyperlinks and returns the text
    def clean_text(text):
        text = re.sub('@[A-Za-z0–9]+', '', text)  # Removing @mentions
        text = re.sub('#', '', text)  # Removing '#' hash tag
        text = re.sub('RT[\s]+', '', text)  # Removing RT
        text = re.sub('https?:\/\/\S+', '', text)  # Removing hyperlink
        return text

    # Use the clean_text function on the scraped tweets that were saved in the stored_data variable
    stored_data["Text"] = stored_data["Text"].apply(clean_text)

    # Function to perform sentiment analysis
    def percentage(part, whole):
        return 100 * float(part) / float(whole)

    # Initializing Variables
    positive = 0
    negative = 0
    neutral = 0
    # Initializing Empty List for the types of sentiment
    tweet_list1 = []
    neutral_list = []
    negative_list = []
    positive_list = []

    # A loop that processes the stored tweets and assigns sentiment
    for tweet in stored_data['Text']:
        tweet_list1.append(tweet)
        analyzer = SentimentIntensityAnalyzer().polarity_scores(tweet)
        neg = analyzer['neg']
        neu = analyzer['neu']
        pos = analyzer['pos']
        comp = analyzer['compound']

        if neg > pos:
            # If the tweet sentiment is negative it appends to the negative_list
            negative_list.append(tweet)
            # Adds 1 to the count of negative tweets if the sentiment is negative
            negative += 1
        elif pos > neg:
            # If the tweet sentiment is positive it appends to the positive_list
            positive_list.append(tweet)
            # Adds 1 to the count of positive tweets if the sentiment is positive
            positive += 1
        elif pos == neg:
            # If the tweet sentiment is neutral it appends to the neutral_list
            neutral_list.append(tweet)
            # Adds 1 to the count of neutral tweets if the sentiment is neutral
            neutral += 1  # increasing the count by 1

    positive = percentage(positive, len(stored_data))  # percentage is the function defined above
    negative = percentage(negative, len(stored_data))
    neutral = percentage(neutral, len(stored_data))

    # All of the lists are converted into panda dataframes for ease of the len function
    tweet_list1 = pd.DataFrame(tweet_list1)
    neutral_list = pd.DataFrame(neutral_list)
    negative_list = pd.DataFrame(negative_list)
    positive_list = pd.DataFrame(positive_list)

    # The len function is used for counting the tweets and also display
    print("")
    print("In the last " + num_of_days + " days, there have been", len(tweet_list1), "tweets on " + search, end='\n')
    print("")
    print("Positive Sentiment:", '%.2f' % len(positive_list), end='\n')
    print("Neutral Sentiment:", '%.2f' % len(neutral_list), end='\n')
    print("Negative Sentiment:", '%.2f' % len(negative_list), end='\n')
    print("")
    print("Positive Tweets")
    print("****************")
    print(positive_list)
    print("")
    print("Negative Tweets")
    print("****************")
    print(negative_list)
    print("")
    print("Neutral Tweets")
    print("***************")
    print(neutral_list)
    print("")
    menu()


# Calling the main function
main()
