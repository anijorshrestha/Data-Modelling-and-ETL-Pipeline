# DROP TABLES

songplay_table_drop = "DROP table if exists songplays;"
user_table_drop = "DROP table if exists users;"
song_table_drop = "DROP table if exists songs;"
artist_table_drop = "DROP table if exists artists;"
time_table_drop = "DROP table if exists time;"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (songplay_id SERIAL PRIMARY KEY, start_time timestamp NOT NULL, user_id int NOT NULL, level varchar, song_id varchar , artist_id varchar, session_id int, location varchar, user_agent varchar);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (user_id int PRIMARY KEY, first_name varchar, last_name varchar, gender varchar, level varchar);
""");

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (song_id varchar PRIMARY KEY, title varchar NOT NULL, artist_id varchar NOT NULL , year int, duration int NOT NULL);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (artist_id varchar PRIMARY KEY, name varchar NOT NULL, location varchar, latitude DOUBLE PRECISION, longitude DOUBLE PRECISION);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (time_id SERIAL PRIMARY KEY,songplay_id int,start_time timestamp, hour int, day int, week int, month int, year int, weekday varchar);
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays(start_time , user_id , level , song_id , artist_id , session_id , location , user_agent ) VALUES (%s, %s, %s,%s, %s,%s, %s, %s) ON CONFLICT DO NOTHING;
           
""")

user_table_insert = ("""
INSERT INTO users(user_id , first_name , last_name , gender , level ) VALUES (%s, %s, %s,%s, %s) ON CONFLICT(user_id) DO UPDATE SET level=EXCLUDED.level;
""")

song_table_insert = ("""
INSERT INTO songs (song_id , title , artist_id , year , duration ) VALUES (%s, %s, %s,%s, %s) ON CONFLICT DO NOTHING;
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location , latitude , longitude  ) VALUES (%s, %s, %s,%s, %s) ON CONFLICT (artist_id) DO UPDATE SET name=EXCLUDED.name, location=EXCLUDED.location, latitude=EXCLUDED.latitude, longitude= EXCLUDED.longitude;
""")


time_table_insert = ("""
INSERT INTO time (start_time,hour , day , week , month , year,weekday ) VALUES (%s, %s, %s,%s, %s,%s, %s);
""")

# FIND SONGS

song_select = ("""
select s.song_id,a.artist_id from songs s join artists a on a.artist_id = s.artist_id where s.title = %s and a.name=%s and s.duration=%s;
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]