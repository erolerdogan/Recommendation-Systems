import pymongo
from pymongo import MongoClient
import pandas as pd 
import matplotlib.pyplot as plt
cluster = MongoClient("mongodb+srv://erolerdogan:21erol21@hobbyhouse-wqfq5.mongodb.net/test?retryWrites=true&w=majority")
db = cluster["HobbyHouse"]
collection_movie = db["Movie"]
collection_tags = db["Tags"]
collection_movieID_tagID = db["MovieID and TagID"]
movies = pd.read_csv("hobbyhouse_dataset/movies.csv", names= ["MovieID", "Title", "Genres"])
movies = movies.iloc[1:]
ratings = pd.read_csv("hobbyhouse_dataset/ratings.csv", usecols=["userId", "movieId", "rating"])
links = pd.read_csv("hobbyhouse_dataset/links.csv")
tags = pd.read_csv("hobbyhouse_dataset/tags.csv")

new_ratings = pd.read_csv("hobbyhouse_dataset/new_ratings.csv")

movieIds = list(set(ratings["movieId"]))

"""#No need anymore because we got the mean of the datas
rate_info_list = []
for i in range(len(movieIds)):
    x = ratings[ratings["movieId"] == movieIds[i]]["rating"]
    rate_info_list.append((movieIds[i], round(x.mean(),2), len(x)))
    
cols = ["MovieID", "Rating", "NumberOfVotes"]
new_ratings = pd.DataFrame(rate_info_list,columns=cols)
new_ratings.to_csv("hobbyhouse_dataset/new_ratings_round.csv")"""

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

#Creating 'WeightedRanking' column using its function
voted_movies["WeightedRanking"] = voted_movies.apply(weighted_ranking, axis=1)
voted_movies = voted_movies.sort_values(by="WeightedRanking", ascending=False)

#need to convert the type of MovieID. Because one of them is str whereas other one is int
movies["MovieID"] = movies["MovieID"].astype(int)

#merging new ratings and movies based on MovieID columns and save it as a new csv. 
merged = voted_movies.merge(movies, on="MovieID")
merged.to_csv("hobbyhouse_dataset/merged.csv", index=False)
merged.head(10) 

%matplotlib inline
plt.figure(figsize=(12,4))
plt.barh(merged["Title"].head(10), merged["WeightedRanking"].head(10), align="center")

"""
#To create tag ID with Tag and store it in MongoDB as Tags
tags_list = list(set(tags["tag"].dropna()))
for i in range(len(tags_list)):
    collection_tags.insert_one({"_id":i, "tag":tags_list[i]})"""

"""
#To create movieID with Title and store it in MongoDB as Movie
for i in range(1, len(movies)):
    collection_movie.insert_one({"_id":int(movies["MovieID"][i]), "Title":movies["Title"][i]})"""

"""
#Adding MovieID and TagID to MongoDB
for asdf in range(len(tags["movieId"])):
    collection_movieID_tagID.insert_one({"_id":asdf, "MovieID":int(list(dictionary.keys())[asdf]), "TagID":dictionary[list(dictionary.keys())[asdf]] })"""

    dictionary = {}
for i in range(len(tags["movieId"])):
    liste = []
    if tags["movieId"][i] not in dictionary.keys():
        liste.append(int(tags["tag_id"][i]))
        dictionary[tags["movieId"][i]] = liste
    
    else:
        liste = dictionary[tags["movieId"][i]]
        if tags["tag_id"][i] not in liste:
            liste.append(int(tags["tag_id"][i]))
            dictionary[tags["movieId"][i]] = liste
        else:
            pass
            