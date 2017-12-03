import pandas as pd
import numpy as np
import random
import math
import scipy.spatial.distance as ssd

#feature_columns - список колонок-фичей, чтобы по ним потом считать расстояние
def prepare(data2):
    del data2['lat']
    del data2['lon']
    feature_columns = [x for x in data2.columns if x!= 'location']
    return data2, feature_columns

# ищет ближайший локейшн по df
def find_closest_location(df, lat, lon):
    print('find clsest location!')
    if (lat, lon) in df['location']:
        return lat, lon
    df['evc'] = df['location'].map(lambda x: math.sqrt((float(x[0])-float(lat))**2 + (float(x[1])-float(lon))**2))
    df = df.sort_values(['evc'], ascending=True)
    if len(df) == 0:
        return None
    return df.iloc[0]['location']

#считает расстояние location до каждого из df
def count_distances(df, columns, location, mode):
    if location not in df['location']:
        location = find_closest_location(df, location[0], location[1])
    vdf = df[df['location'] == location]
    vector = vdf[columns].as_matrix()
    if vector.shape[0] != 1:
        vector = [vector[0]]
    matrix = df[columns].as_matrix()
    if mode == 'cos':
        res = count_cosine(matrix, vector)
    else:
        res = count_euclid(matrix, vector)
    df['metrics'] = res
    df = df.sort_values(['metrics'])
    return df.drop(df.index[[0]])

#косинусное расстояние
def count_cosine(matrix, vector):
    cos = []
    for i in matrix:
        cos.append(ssd.cosine(i, vector))
    return cos

#евклидово расстояние
def count_euclid(matrix, vector):
    cos = []
    for i in matrix:
        cos.append(ssd.euclidean(i, vector))
    return cos


def get_name(input_new_latitude, input_new_longitude):
    from geopy.geocoders import Nominatim
    geolocator = Nominatim()
    string = str(input_new_latitude) + ', ' + str(input_new_longitude)
    location = geolocator.reverse(string, language='ru')
    lr = location.raw
    return lr['display_name']


def process_engine(input_latitude, input_longitude):
    data = pd.read_csv('all_feat_data.csv')
    del data['Unnamed: 0']
    data['location'] = list(zip(data['lat'], data['lon']))
    data, feature_columns = prepare(data)
    d = count_distances(data, feature_columns, (input_latitude, input_longitude), 'cos')
    d.to_csv('predict_for_{0}_{1}.csv'.format(input_latitude, input_longitude))
    d = d.reset_index()
    res = list(d.loc[[0, 1, 2]]['location'])
    return res