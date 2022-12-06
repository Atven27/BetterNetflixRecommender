import move_recommender as rec
import pandas as pd
import numpy as np
import os
import ast
import re
import PySimpleGUI as sg
from tkinter import *
from  tkinter import ttk

prep_df = pd.read_csv("prep_movie_list_original.csv", sep=',', encoding='latin-1')

layout = [[sg.Text("Enter Netflix Movie Info to Find Similar Options!")],
          [sg.Text("All fields not required, please leave blank if not used")],
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
rec_list = rec.Recommend_Movies(values[0])
reco_list = rec_list

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
inp_param = values[0] + "|" + values[1] + "|" + values[2]
print(inp_param)

param1 = str(inp_param.split('|',1)[0])
param2 = inp_param.split('|',1)[1].split('|',1)[0]
param3 = inp_param.rsplit('|',1)[1]

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

print(recolistdf.loc[:,"title"])

s2 = '\n'.join([str(i) for i in recolistdf.loc[:,"title"]])
s = '\n'.join([str(i) for i in rec_list])
sg.PopupScrolled("The Following Movies are Recommended:", f"{s2}")

# testing
#print('Values', values[0])
#print('Rec actual', rec.recommend_movie("stranger thing"))

window.close()