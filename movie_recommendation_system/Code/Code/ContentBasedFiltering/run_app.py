# Import all the variables and libraries
import pandas as pd
import numpy as np
from tf_idf_vector import df_tf_idf
from load_data import movies, ratings

# Helper functions
def norm(row):
    return np.sqrt(np.sum(np.square(row), axis=0))

# Filter out the movies with low ratings and retain only the unique movies
ratings = ratings[ratings['rating']>=4]
distinct_movies = np.unique(df_tf_idf['movieId'])

def get_recommendations(userId):
    user_data = ratings[ratings['userId']==userId] # The movies which the user liked (>=4)
    user_data = pd.merge(df_tf_idf,user_data, on = 'movieId', how = 'inner') # combining the df_tf_idf-idf vector and user-rating data for this specific user ID
    user_data = user_data.groupby(['tag'], as_index = False,sort = False).sum().rename(columns = {'vector_sim': 'tmp'})[['tag','tmp']]
    user_data['user']=userId
    df_final = pd.DataFrame() # Append into this the ratings for all movies for the given user
    for movie in distinct_movies:
        user_movie = df_tf_idf[df_tf_idf['movieId']==movie]
        merged_df = pd.merge(user_movie, user_data, on = 'tag', how = 'left')
        merged_df['tmp'] = merged_df['tmp'].fillna(0)
        merged_df['val'] = merged_df['vector_sim']*merged_df['tmp']
        tag_merge_final = merged_df.groupby(['user','movieId'])[['val']].sum().rename(columns = {'val': 'rating'}).reset_index()
        tag_merge_final['rating']=tag_merge_final['rating']/(norm(merged_df['vector_sim'])*norm(user_data['tmp'])) #normalized rating
        df_final = df_final.append(tag_merge_final, ignore_index=True)

    df_final = df_final.sort_values(['user','rating'], ascending=False) # Highest ratings are most suitable
    return df_final


