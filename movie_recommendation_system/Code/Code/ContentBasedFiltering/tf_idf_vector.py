import numpy as np
import pandas as pd
from load_data import tags
import math

def normalize(df):
    vector_length = df[['movieId','tf-idf']]
    vector_length['tf-idf-sq'] = vector_length['tf-idf']**2
    vector_length = vector_length.groupby(['movieId'], as_index=False, sort=False).sum().rename(columns = {'tf-idf-sq':'tf-idf-sq-total'})[['movieId','tf-idf-sq-total']]
    vector_length['len'] = np.sqrt(vector_length[['tf-idf-sq-total']].sum(axis=1))
    df = pd.merge(tf, vector_length, on='movieId', how='left')
    df['vector_sim'] = df['tf-idf']/df['len']
    return df

# Local variables
unique_tags = np.unique(tags['movieId'])

# Drop the duplicate after aggregating by tags
df = tags[['tag','movieId']].drop_duplicates().groupby(['tag'], as_index=False, sort=False).count()
df.columns = ['tag', 'count']

# Compute the tf values dataframe
tf = tags.groupby(['tag','movieId'], as_index=False, sort=False).count().rename(columns = {'userId':'tf_count'})[['movieId','tag','tf_count']]

# compute IDF values
df['idf'] = math.log10(len(unique_tags)) - np.log10(df['count'])
tf = pd.merge(tf, df, on='tag', how='left')

# From the formula mentioned in the report
tf['tf-idf'] = tf['tf_count']*tf['idf']

df_tf_idf = normalize(tf)




