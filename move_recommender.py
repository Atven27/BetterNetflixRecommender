import pandas as pd
import numpy as np
import os
import ast
import re

# Read the prepared data file
prep_df = pd.read_csv("prep_movie_list_original.csv", sep=',', encoding='latin-1')
#prep_df.head(2)
#print(len(prep_df.index))

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
CV= CountVectorizer(max_features=5000, stop_words="english")
vector=CV.fit_transform(prep_df['listtags']).toarray()
#check random features name
#CV.get_feature_names()[1000]

tfidf=TfidfVectorizer(max_features=5000,analyzer='word',stop_words="english")
tfdf_features=tfidf.fit_transform(prep_df['listtags'])

from sklearn.metrics.pairwise import cosine_similarity

similarity=cosine_similarity(vector)
#prep_df[prep_df['title']=='DARK SKIES'].index[0]

sorted(list(enumerate(similarity[0])), reverse=True, key=lambda x : x[1])[1:6] # key define second column basis sort
tfdf_similarity=cosine_similarity(tfdf_features)

#Recommender function
def Recommend_Movies(movie):
    reco_list = []
    try:
        movie_index=prep_df[prep_df['title']==movie].index[0]
        distance=tfdf_similarity[movie_index]
        
        movies_list=sorted(list(enumerate(distance)), reverse=True, key=lambda x : x[1])[1:11]

        if len(movies_list) > 0:
            for i in movies_list:
                #print(df8.iloc[i[0]].title)
                t=prep_df.iloc[i[0]].title
                
                reco_list.append(t)
        else:
            print('Movie '+ movie +' does not have any matching recommendation. Please try another one.')
    except:
        print('Movie '+ movie +' not present in Netflix. Please try another one.')
    
    return reco_list