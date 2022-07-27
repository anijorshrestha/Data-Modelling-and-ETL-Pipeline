import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    This function processes a song file whose filepath has been provided as an arugment.
    It extracts the song information in order to store it into the songs table.
    Then it extracts the artist information in order to store it into the artists table.

    INPUTS: 
    * cur the cursor variable
    * filepath the file path to the song file
    """

    # open song file
    df = pd.read_json(filepath, lines= True)

    # insert song record
    song_data = (df[['song_id','title','artist_id','year','duration']].values.tolist()[0])
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = (df[['artist_id' , 'artist_name' , 'artist_location' , 'artist_longitude' , 'artist_longitude']].values.tolist()[0])
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    This fucntion processes a log file whose filepath has been provided as an arugment.
    It filters the file with 'NextSong' filter, coverts the timestamp to datetime and insert into time table.
    Likewise user info columns are retrieved and inserted in user column.
    song_id and artist_id is retrieved by joining artists and songs table on the basis of artists_is with filter of song,artist     and length.
    Then songplays table is populated using retieved artist and song id with other user information

    INPUTS: 
    * cur the cursor variable
    * filepath the file path to the song file
    """

    # open log file
    df = pd.read_json(filepath, lines= True)

    # filter by NextSong action
    df = df[df.page == "NextSong"]

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit ='ms')
    
    # insert time data records
    time_data = (t,t.dt.hour,t.dt.day, t.dt.week,t.dt.month,t.dt.year,t.dt.weekday)
    column_labels = ("start_time","hour","day","week","month","year","weekday")
    time_df = pd.concat(time_data, keys=column_labels, axis=1)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']].drop_duplicates()

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)
    
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    # insert songplay records
    for index, row in df.iterrows():
        print(row.song, row.artist, row.length)
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts,row.userId,row.level,songid,artistid,row.sessionId,row.location,row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    This function takes connection, cursor, filepath and function as input. With the help of filepath, it gets all the files         matching the extension from the directoy, dispalys total number of file found and iterate over those file to another             function provided.
    
    INPUTS: 
    * conn for the connection to database
    * cur the cursor variable
    * filepath the file path to the song file
    * func to use function to process either song or log
    """

    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()