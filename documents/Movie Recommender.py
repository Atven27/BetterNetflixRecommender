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
reco_list = []
def Recommend_Movies(movie):
    global reco_list
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

#User input section

'''
parameter 1:
    more than one word: movie title
'|' is the delimiter
parameter 2:
    single word: one genre of the movie
'|' is the delimiter
parameter 3:
    Cast member name 
'''
errorKey = 0
inp_param = 'JAWS||'
param1 = str(inp_param.split('|',1)[0])
param2 = inp_param.split('|',1)[1].split('|',1)[0]
param3 = inp_param.rsplit('|',1)[1]

Recommend_Movies(param1)
    
recolistdf = pd.DataFrame(reco_list)
recolistdf = recolistdf.rename(columns={0: 'title'})

#recolistdf = recolistdf.merge(q_movies[['title','demog_score']], on  = "title",how="left")
recolistdf = recolistdf.merge(prep_df[['title','cast','director','imdb_votes','keywords','genre','imdb_score','popularity_score','description','tags']], on  = "title",how="left")
recolistdf = recolistdf.drop_duplicates(subset = ['title'],keep = 'last').reset_index(drop = True)

recolistdf[['imdb_score']] = recolistdf[['imdb_score']].fillna(value=0)
recolistdf[['imdb_votes']] = recolistdf[['imdb_votes']].fillna(value=0)
recolistdf[['popularity_score']] = recolistdf[['popularity_score']].fillna(value=0)

#recolistdf['imdb_votes'] = recolistdf['imdb_votes'].astype(float)
recolistdf['imdb_score'] = recolistdf['imdb_score'].astype(float)
recolistdf['popularity_score'] = recolistdf['popularity_score'].astype(float)
recolistdf['composite_score'] = recolistdf['imdb_score']*0.6+recolistdf['popularity_score']*0.4
#recolistdf = recolistdf.drop(columns=['imdb_votes', 'imdb_score','popularity_score'])
recolistdf = recolistdf.sort_values(by=['composite_score','title'], ascending=False)

#recolistdf = recolistdf.loc[recolistdf['overview'].str.contains('fun',na=False)]
if len(param2) > 0:
    recolistdf = recolistdf.loc[recolistdf['genre'].str.contains(param2.lower())]
if len(param3) > 0:
    recolistdf = recolistdf.loc[recolistdf['cast'].str.lower().str.contains(param3.lower())]

recolistdf

#recolistdf.head(10)
netflix_titles = pd.read_csv("10k_titles.csv")
for movie in recolistdf['title']:
    print(movie.lower().title())
    print(re.sub("[^A-Za-z ]","",str(netflix_titles.loc[netflix_titles['title'] == movie.lower().title()]['overview'].values)))
    print('\n')
