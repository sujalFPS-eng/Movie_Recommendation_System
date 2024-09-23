import pandas as pd
from zipfile import ZipFile as extract_zip

with extract_zip("ml-latest-small.zip","r") as zipfile_:
    zipfile_.extractall()

movies = pd.read_csv("ml-latest-small/movies.csv")
links = pd.read_csv("ml-latest-small/links.csv")
tags = pd.read_csv("ml-latest-small/tags.csv")
ratings = pd.read_csv("ml-latest-small/ratings.csv")





