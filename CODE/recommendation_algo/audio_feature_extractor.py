import csv
import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials

def get_movies(fp):
    movies = []
    with open(fp, newline='') as f:
        movie_reader = csv.reader(f, delimiter=',')
        for i, row in enumerate(movie_reader):
            if i == 0: continue
            movies.append({
                'id': row[1],
                'imdb_id': row[2],
                'original_title': row[3]
            })
    return movies

def get_spotipy_handler():
    client_id = "0054a24f2fc643c69d56d020dd5f70be"
    client_secret = "98b4a4b772ad4eca934a92ca60c246a0"
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp

# search for albums based on query keywords
# use the first album as the album of the soundtracks
def get_first_album_id(sp, movie_name):
    # FIXME: how to formulate query keywords?
    result = sp.search(q=movie_name + ' soundtrack', limit=10, type='album')

    if len(result['albums']['items']) != 0:
        return result['albums']['items'][0]['id']
    
    result = sp.search(q=movie_name + ' original', limit=10, type='album')
    if len(result['albums']['items']) != 0:
        return result['albums']['items'][0]['id']
    
    result = sp.search(q=movie_name, limit=10, type='album')
    if len(result['albums']['items']) != 0:
        return result['albums']['items'][0]['id']
    
    movies_wo_soundtracks.append(movie_name)
    return None

# get tracks one album at a time
def get_album_tracks(album_id):
    if album_id is None:
        return None
    album_tracks_info = sp.album_tracks(album_id=album_id)
    return album_tracks_info['items']

def get_audio_features(sp, track_ids):
    # extract audio features in batch
    # audio_feature_for_one = sp.audio_analysis(track_id=tracks[0]['id'])   # NOTE: sp.audio_analysis() contains more info, may be used later
    if track_ids is None:
        return None
    audio_feature_batch = sp.audio_features(track_ids)
    return audio_feature_batch

# extract audio features for soundtracks of each movie
def extract_audio_features_for_movies(sp, movies):
    for i in range(len(movies)):
        # FIXME: remove break point once finished
        if i == count:
            break

        name = movies[i]['original_title']
        movies[i]['spotify_album_id'] = get_first_album_id(sp, movies[i]['original_title'])
        tracks = get_album_tracks(movies[i]['spotify_album_id'])
        movies[i]['tracks_ids'] = [t['id'] for t in tracks] if tracks is not None else None
        movies[i]['tracks_names'] = [t['name'] for t in tracks] if tracks is not None else None
        movies[i]['tracks_audio_features'] = get_audio_features(sp, movies[i]['tracks_ids'])
        if movies[i]['tracks_ids'] is not None:
            print(f'search for movie {i}: \'{name}\' successful')
        else:
            print(f'WARNING: soundtracks not found for movie {i}: \'{name}\'')
    return movies

def get_fieldnames(movies):
    fieldnames = [
        'movie_id', 'imdb_id', 'original_title',
        'spotify_album_id', 'track_id', 'track_name'
    ]
    audio_feature_fieldnames = list((movies[0]['tracks_audio_features'][0].keys()))
    audio_feature_fieldnames.remove('id')
    audio_feature_fieldnames.remove('type')
    fieldnames.extend(audio_feature_fieldnames)
    return fieldnames

def write_to_csv(movies, portion_no):
    with open(f'audio_features_dataset{int(portion_no)}.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=get_fieldnames(movies))
        writer.writeheader()
        for no, m in enumerate(movies):
            try:
                if m['tracks_ids'] is None:
                    continue
            except KeyError:
                break

            name = m['original_title']
            print(f'writing for movie {no}: {name}')        # FIXME
                
            for i in range(len(m['tracks_ids'])):
                if m['tracks_audio_features'][i] is None:
                    continue
                # NOTE: need to update fieldnames if below columns are modified
                writer.writerow({
                    'movie_id': m['id'],
                    'imdb_id': m['imdb_id'],
                    'original_title': m['original_title'],
                    'spotify_album_id': m['spotify_album_id'],
                    'track_id': m['tracks_ids'][i],
                    'track_name': m['tracks_names'][i],
                    'danceability': m['tracks_audio_features'][i]['danceability'],
                    'energy': m['tracks_audio_features'][i]['energy'],
                    'key': m['tracks_audio_features'][i]['key'],
                    'loudness': m['tracks_audio_features'][i]['loudness'],
                    'mode': m['tracks_audio_features'][i]['mode'],
                    'speechiness': m['tracks_audio_features'][i]['speechiness'],
                    'acousticness': m['tracks_audio_features'][i]['acousticness'],
                    'instrumentalness': m['tracks_audio_features'][i]['instrumentalness'],
                    'liveness': m['tracks_audio_features'][i]['liveness'],
                    'valence': m['tracks_audio_features'][i]['valence'],
                    'tempo': m['tracks_audio_features'][i]['tempo'],
                    'uri': m['tracks_audio_features'][i]['uri'],
                    'track_href': m['tracks_audio_features'][i]['track_href'],
                    'analysis_url': m['tracks_audio_features'][i]['analysis_url'],
                    'duration_ms': m['tracks_audio_features'][i]['duration_ms'],
                    'time_signature': m['tracks_audio_features'][i]['time_signature']
                })

count = 10000
movies_wo_soundtracks = []
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python3 audio_feature_extractor.py <portion_no> <total_num_portions> <fp/to/movie_list.csv')
        exit(1)
    portion_no = float(sys.argv[1])
    total_portion_num = float(sys.argv[2])
    movie_names_filepath = sys.argv[3]

    movies = get_movies(movie_names_filepath)
    portion_size = int(len(movies)/total_portion_num)
    start_index = int(portion_no * portion_size)
    end_index = int((portion_no+1) * portion_size)
    print(start_index, end_index)   # FIXME
    movies = movies[start_index:end_index]
    
    sp = get_spotipy_handler()
    movies = extract_audio_features_for_movies(sp, movies)
    print('data collection complete, begin writing')
    write_to_csv(movies, portion_no)

    with open('movies_wo_soundtracks' + str(int(portion_no)), 'w') as f:
        for n in movies_wo_soundtracks:
            f.write(f'{n}\n')

    