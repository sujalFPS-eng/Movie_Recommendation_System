import pandas as pd
from run_app import get_recommendations
from load_data import movies
import numpy as np

def main():
    df = get_recommendations(2) # Get movie recommendations
    
    df['movieId'] = df['movieId'].apply(np.int64)
    df['user'] = df['user'].apply(np.int64)
    df = pd.merge(df, movies, on = 'movieId', how = "inner")
    df = df.loc[:,('user','movieId', 'title','rating')]

    print(df.head(10))

if __name__ == "__main__":
    main()