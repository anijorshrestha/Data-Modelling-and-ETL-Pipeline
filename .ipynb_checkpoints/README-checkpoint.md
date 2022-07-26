# Sparkify (Data Modelling with Postgres and ETL pipeline with Python )

## Overview

Sparkify is a startup focusing in their new music straming app. This project is about creating a database schema and ETL pipeline for analysis of whats song users are listening to. Currently there data of songs and log is stored as JSON file, which makes it difficult to query and perform analysis. Therefore a database is designed as star schema which consist of one fact table (songplays) refrencing 4 dimension table (users, songs, artists and time). And the ETL scripts has been created using python.

## Project Structure
The project structure is as following:
* data : This folder consist of two folder named log_data and song_data which further consist of song files and log files on user activity in JSON format
* create_tables.py : When runing this python file, it connects with database and is used in creating and dropping tables.
* sql_queries.py : This file contains all the sql queries to create, insert and select from the table
* etl.py : etl.py defines ETl pipeline which extracts all the song and log files process it and insert data into relevant table.
* etl.ipnyb and test_ipnyb : etl.ipnyb consist of detailed ETL process and test_ipnyb file is used to confirm creation of table and to check the values in table.

## Schema

#### Fact Table 

##### Table songplays

`songplays (songplay_id SERIAL PRIMARY KEY, start_time timestamp NOT NULL, user_id int NOT NULL, level varchar, song_id varchar , artist_id varchar, session_id int, location varchar, user_agent varchar)`

#### Dimension Table

##### Table users

`users (user_id int PRIMARY KEY, first_name varchar, last_name varchar, gender varchar, level varchar)`

##### Table songs

`songs (song_id varchar PRIMARY KEY, title varchar NOT NULL, artist_id varchar NOT NULL , year int, duration DOUBLE PRECISION NOT NULL)
`
##### Table artist

`artists (artist_id varchar PRIMARY KEY, name varchar NOT NULL, location varchar, latitude DOUBLE PRECISION, longitude DOUBLE PRECISION)`

##### Table time

`time (time_id SERIAL PRIMARY KEY,songplay_id int,start_time timestamp, hour int, day int, week int, month int, year int, weekday varchar)`

## Running the project

First of all we need to created database and table which is done using create_tables.py file which wil import all the queries stored in sql_queries.py and execute it. sql_queries.py file consist of all the query to create , insert and select from different table. All the queries which is needed for analysis is stored here. Open a terminal and enter following code:

`python create_tables.py`

After creating database and tables, we will run etl.py file which defines the ETL pipeline. There are 3 main function which is described below:

1. process_data

This function takes connection, cursor, filepath and function as input. With the help of filepath, it gets all the files matching the extension from the directoy, dispalys total number of file found and iterate over those file to another function provided.

2. process_song_file

This function takes cursor and song filepath sent from process_data as input parameter. First it opens the song file provided in the filepath and then insert the song details and artist details into songs table and artist table respectively.

3. process_log_file

This function takes cursor and log filepath sent from process_data as input parameter. It also opens the log file as dataframe and filters by 'NextSong'. Then the timestap is converted into datatime and the resulting datetime is further distinguished into smaller units and inserted in time table. Furthermore users dataframe is created using certain user columns. Finally, song_id and artist_id is retrieved by joining songs table and artist table by artist id and using filter of title, name and duration. Then by iterating through log file, values in songplays table is added.

To run etl.py file we enter following code:

`python etl.py`

To confirm creation of table, proper values in table and some common errors , test.ipnyb is used.
