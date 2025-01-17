import movie_recommender as rec
import pandas as pd
import numpy as np
import os
import ast
import re
import PySimpleGUI as sg
from tkinter import *
from  tkinter import ttk
import sys

prep_df = pd.read_csv("prep_movie_list.csv", sep=',', encoding='latin-1')

layout = [[sg.Text("Enter Netflix Movie Info to Find Similar Options!")],
          [sg.Text("Title field required. All others are not. Please leave blank if not used")],
          [sg.Text("Title", size =(15, 1)), sg.Input()],
          [sg.Text("Genre", size =(15, 1)), sg.Input()],
          [sg.Text("Actor", size =(15, 1)), sg.Input()],
          [sg.Button('Submit')]]
window = sg.Window('BetterFlix', layout)
event, values = window.read()

#cleans whitespace before and after
values[0].strip()
#print('Vals after strip', values[0])
#List
#rec_list = rec.Recommend_Movies(values[0])
#reco_list = rec_list

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
#inp_param = 'JAWS||'

inp_param = values[0].upper() + "|" + values[1].upper() + "|" + values[2].upper()
print(inp_param)

param1 = str(inp_param.split('|',1)[0])
param2 = inp_param.split('|',1)[1].split('|',1)[0]
param3 = inp_param.rsplit('|',1)[1]

#print(param1)
#print(param2)
#print(param3)
reco_list = []
reco_list = rec.Recommend_Movies(param1)

if reco_list == -2:
    sg.Popup(f"Movie {values[0]} not present in Netflix. Please try another one.")
    window.close()
    exit()


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

if recolistdf.empty:
    sg.Popup(f"Movie details entered for {values[0]} does not have any matching recommendation. Please try another title.")
    window.close()
    exit()

print(recolistdf.loc[:,"title"])

final_list = []
i = 1
netflix_titles = pd.read_csv("10k_titles.csv")
for movie in recolistdf['title']:
    print(movie.lower().title())
    movie_str = str(i) + ".      " + movie.lower().title()
    final_list.append(movie_str)
    print(re.sub("[^A-Za-z ]","",str(netflix_titles.loc[netflix_titles['title'] == movie.lower().title()]['overview'].values)))
    final_list.append(re.sub("[^A-Za-z ]","",str(netflix_titles.loc[netflix_titles['title'] == movie.lower().title()]['overview'].values)))
    print('\n')
    final_list.append(' ')
    i = i + 1


s2 = '\n'.join([str(i) for i in final_list])
#s = '\n'.join([str(i) for i in rec_list])
sg.PopupScrolled("The Following Movies are Recommended:", "\n", f"{s2}")

# testing
#print('Values', values[0])
#print('Rec actual', rec.recommend_movie("stranger thing"))

window.close()