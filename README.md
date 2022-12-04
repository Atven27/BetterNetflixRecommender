# CS410 Course Project: BetterNetflixRecommender

Please fork this repository and paste the github link of your fork on Microsoft CMT. Detailed instructions are on Coursera under Week 1: Course Project Overview/Week 9 Activities.

Input Files:
---------------------------
1) titles.csv (5977 records): 
Fields >> id,title,type,description,release_year,age_certification,runtime,genres,production_countries,seasons,imdb_id,imdb_score,imdb_votes,tmdb_popularity,tmdb_score

2) netflix_originals.csv (585 records):
Fields >> Title,Genre,Premiere,Runtime,IMDB Score,Language

3) netflix_titles.csv (8809 records): 
Fields >> show_id,type,title,director,cast,country,date_added,release_year,rating,duration,listed_in,description

4) movies_metadata.csv (45572 records):
Fields >> adult,belongs_to_collection,budget,genres,homepage,id,imdb_id,original_language,original_title,overview,popularity,poster_path,production_companies,production_countries,release_date,revenue,runtime,spoken_languages,status,tagline,title,video,vote_average,vote_count

5) 10k movies data.csv (9984 records):
Fields >> rowid,Movie_id,title,Genres,release_date,Keywords,overview,poster_path,Budget,Revenue,popularity,vote_average,vote_count 

Code:
----------------
Movie Reviews - Data Prep.ipynb
Purpose: Read all the input data files and create a final file with custom fields for further processing. Since some processes will take time, we dont want to run them during recommender run-time.

Output Data File:
---------------------------
prep_movie_list.csv

Code:
----------------
Movie Recommender.ipynb
Purpose: The actual recommender code which takes user inputs and shows recommended list


