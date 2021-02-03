
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from scipy.spatial.distance import cdist
import numpy as np
from sklearn.manifold import TSNE
import plotly.express as px
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from collections import defaultdict
import os
from os import getenv
import pandas as pd
import pickle


df = pd.read_csv('Pages\spotify_df.csv')

number_cols = ['acousticness', 'danceability', 'duration_ms', 'energy', 'explicit', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode',
               'popularity', 'speechiness', 'tempo', 'valence']

SPOTIPY_CLIENT_ID = getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_SECRET_ID = getenv('SECRET_ID')

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID,
                                                           client_secret=SPOTIPY_SECRET_ID))

def find_song(name):
  song_data = defaultdict()
  results = sp.search(q='track: {}'.format(name), limit=1)
  if results['tracks']['items'] == []:
    return None

  results = results['tracks']['items'][0]
  track_id = results['id']
  audio_features = sp.audio_features(track_id)[0]

  song_data['name'] = [name]  
  # song_data['year'] = [year]
  song_data['explicit'] = [int(results['explicit'])]
  song_data['duration_ms'] = [results['duration_ms']]
  song_data['popularity'] = [results['popularity']]

  for key, value in audio_features.items():
    song_data[key] = value

  return pd.DataFrame(song_data)

def get_song_data(song, df):

  try:
    song_data = df[(df['name'] == song['name'])].iloc[0]
     
    return song_data
  
  except IndexError:
    return find_song(song['name']) # , song['year']


def get_mean_vector(song_list, df):
  
  song_vectors = []

  for song in song_list:
    song_data = get_song_data(song, df)
    if song_data is None:
      print('Warning: {} does not exist in Spotify or in database'.format(song['name']))
      continue
    song_vector = song_data[number_cols].values
    song_vectors.append(song_vector)

  song_matrix = np.array(list(song_vectors))
  return np.mean(song_matrix, axis=0)


def flatten_dict_list(dict_list):
  flattened_dict = defaultdict()
  for key in dict_list[0].keys():
    flattened_dict[key] = []
  
  for dictionary in dict_list:
    for key, value in dictionary.items():
      flattened_dict[key].append(value)
  return flattened_dict
  

def recommend_songs(song_list, df=df, n_songs=10):

  song_cluster_pipeline = pickle.load(open("Pages\cluster.pickle", "rb"))
  metadata_cols = ['name', 'artists']
  song_dict = flatten_dict_list(song_list)

  song_center = get_mean_vector(song_list, df)
  scaler = song_cluster_pipeline.steps[0][1]
  scaled_data = scaler.transform(df[number_cols])
  scaled_song_center = scaler.transform(song_center.reshape(1,-1))
  distances = cdist(scaled_song_center, scaled_data, 'cosine')
  index = list(np.argsort(distances)[:, :n_songs][0])

  rec_songs = df.iloc[index]
  rec_songs = rec_songs[~rec_songs['name'].isin(song_dict['name'])]
  return rec_songs[metadata_cols].to_dict(orient='records')

def get_recomendations(input):
  input_dict = {'name': str(input)}
  return recommend_songs([input_dict])