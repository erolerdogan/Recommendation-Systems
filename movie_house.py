import pymongo
from pymongo import MongoClient
import pandas as pd 

#Creating MongoDB connection
cluster = MongoClient("mongodb+srv://erolerdogan:21erol21@hobbyhouse-wqfq5.mongodb.net/test?retryWrites=true&w=majority")
db = cluster["HobbyHouse"]
collection = db["Movies"]

movies = pd.read_csv("hobbyhouse_dataset/movies.csv")
ratings = pd.read_csv("hobbyhouse_dataset/ratings.csv")
links = pd.read_csv("hobbyhouse_dataset/links.csv")
rat_feat = ["userId", "movieId", "rating"]
ratings = ratings[rat_feat]

movieIds = list(set(ratings["movieId"]))

"""#No need anymore because we got the mean of the datas
rate_info_list = []
for i in range(len(movieIds)):
    x = ratings[ratings["movieId"] == movieIds[i]]["rating"]
    rate_info_list.append((movieIds[i], round(x.mean(),2), len(x)))
    
cols = ["MovieID", "Rating", "NumberOfVotes"]
new_ratings = pd.DataFrame(rate_info_list,columns=cols)"""

new_ratings = pd.read_csv("hobbyhouse_dataset/new_ratings.csv")
cols = ["MovieID", "Rating", "NumberOfVotes"]
new_ratings = new_ratings[cols]
new_ratings["NumberOfVotes"] = new_ratings["NumberOfVotes"].fillna("")

C = new_ratings["Rating"].mean() #C is the mean vote across the whole report
m = new_ratings["NumberOfVotes"].quantile(0.9) #m is the minimum votes required to be listed in the chart

voted_movies = new_ratings.copy().loc[new_ratings["NumberOfVotes"] >= m]

#Weighted ranking is corresponding to popular ranking
def weighted_ranking(data, m=m, C=C):
    R = data["Rating"].mean()
    v = data["NumberOfVotes"]
    # Calculation based on the IMDB formula
    W = (v/(v+m) * R) + (m/(m+v) * C)
    print(data.shape)
    return round(W,3)

voted_movies["WeightedRanking"] = voted_movies.apply(weighted_ranking, axis=1)
voted_movies = voted_movies.sort_values(by="WeightedRanking", ascending=False)

print(voted_movies.head(10))