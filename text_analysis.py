"""
Part 1: Harvesting Text from the Internet
I chose to harvest the text from IMDb movie reviews
"""

import pprint 
from imdb import Cinemagoer
import nltk  
nltk.download('stopwords')
nltk.download('vader_lexicon')
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# create an instance of the Cinemagoer class
ia = Cinemagoer()

# search movie
title = "Elf"
movie = ia.search_movie("Elf")[0]
print(f"Movie Title: {title}")
print(f"IMDb ID: {movie.movieID}")
#0319343

movie_reviews = ia.get_movie_reviews('0319343')

reviews_dictionary = {}


if 'reviews' in movie_reviews['data']:
    reviews = movie_reviews['data']['reviews']

    for index, review in enumerate (reviews, start=1):
        review_content = review['content']
        reviews_dictionary[f"Review {index}"] = review_content
        print(f"Review {index}: {review_content}")
else:
    print(movie_reviews['data']['reviews'][0]['content'])

# pprint.pprint(reviews_dictionary)

def total_words(hist):
    """
    Returns the total of the frequencies in a histogram.
    """
    all_text = " ".join(reviews_dictionary.values())
    words = all_text.split()

    stop_words = set(stopwords.words('english')) #I used this video (https://www.youtube.com/watch?v=LLl3bQXhhzI) as a reference for the stopwords
    filtered_words = []
    for word in words:
        if word not in stop_words:
            filtered_words.append(word)

    total = len(filtered_words)
    return total 

total_words_count = total_words(reviews_dictionary)
# print(f"Total nuber of total words in reviews without stop words is: {total_words_count}")


def different_words(hist, stop_words):
    """
    Returns the total sum of different words
    """
    word_count = {}
    for review in hist.values():
        words = review.split()
        for word in words:
            if word.lower() not in stop_words:
                word_count[word] = word_count.get(word, 0) + 1

    total_of_diff_words = len(word_count)
    return total_of_diff_words

stop_words = set(stopwords.words('english'))
total_of_diff_words = different_words(reviews_dictionary, stop_words)
# print(f"The number of different words in these reviews excluding the typical english stop words is: {total_of_diff_words}")

def count_stopwords(reviews_dict):
    """
    This function is called count_stopwords and finds the amount of total stop words within the reviews for Elf
    """
    stop_words = set(stopwords.words('english'))
    count = 0
    for review_content in reviews_dict.values():
        words = review_content.split()
        stopwords_review = []
        for word in words: 
            if word.lower() in stop_words:
                stopwords_review.append(word.lower())
        count += len(stopwords_review)
    
    return count 

total_stopwords = count_stopwords(reviews_dictionary)
# print(f"The total number of stopwords in the reviews is: {total_stopwords}")


#Transitioning to sentiment scores!

def sentiment_score(reviews):
    """
    This function finds the sentiment scores for the movie reviews using the Sentiment Intensity Analyzer
    """
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(reviews)
    return sentiment_scores

for reveiw_number, content in reviews_dictionary.items():
    sentiment_scores = sentiment_score(content)
    # print(f"The review '{reveiw_number}' sentiment score is: {sentiment_scores}")

#See below for the shared link for Part 3: Learning with ChatGPT1

def compound(reviews_dict):
    """
    This function is called compound and finds the average compound score from the sentiment scores 
    I asked ChatGPT what are some common practices when using the sentiment analyzer and it gave me the idea to find the average
    compound score since this is one of the ways that we can determine the polarity response of the movie
    Here is the shared link: https://chat.openai.com/share/7dfe968f-a6f8-4240-8dfc-fedd81b05b72 
    """
    analyzer = SentimentIntensityAnalyzer()
    compound_scores = []
    for review_content in reviews_dict.values():
        sentiment_scores = analyzer.polarity_scores(review_content)
        compound_scores.append(sentiment_scores['compound'])
    if compound_scores:
        average_score = sum(compound_scores) / len(compound_scores)
    else:
        print("There is no average for compound scores.")
    
    return average_score

average_compound = compound(reviews_dictionary)
# print(f"The average compound score for the reviews is: {average_compound}")

def main():
    """
    This function is called main and acts as a driver to call on the functions and print the results.
    """
    hist = reviews_dictionary
    # print(reviews_dictionary)
    print(f"The total number of words without stop words is: {total_words(hist)}")
    print(f"Total number of different words in reviews without stop words is: {total_of_diff_words}")
    print(f"The total number of stopwords in the reviews is: {total_stopwords}")
    print(f"The average compound score for the reviews is: {average_compound}")
    print("See below for the sentiment scores for each review: ")
    for reveiw_number, content in reviews_dictionary.items():
        sentiment_scores = sentiment_score(content)
        print(f"The review '{reveiw_number}' sentiment score is: {sentiment_scores}")

if __name__ == "__main__":
    main()