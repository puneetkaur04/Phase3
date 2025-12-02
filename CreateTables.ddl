CREATE TABLE Artist (
    ar_artist_key INT PRIMARY KEY,
    ar_name VARCHAR(50) NOT NULL,
    ar_genre VARCHAR(20) NOT NULL,
    ar_date_of_birth DATE NOT NULL,
    ar_biography TEXT
);

CREATE TABLE Album (
    al_album_key INT PRIMARY KEY,
    al_album_name VARCHAR(50) NOT NULL,
    al_date DATE NOT NULL,
    al_number_of_songs INT NOT NULL,
    al_artist_key INT REFERENCES Artist(ar_artist_key)
);

CREATE TABLE Song (
    s_song_key INT PRIMARY KEY,
    s_song_name VARCHAR(50) NOT NULL,
    s_time TIME,
    s_genre VARCHAR(20) NOT NULL,
    s_album_key INT REFERENCES Album(al_album_key)
);

CREATE TABLE Account (
    ac_account_key INT PRIMARY KEY,
    ac_username VARCHAR(32) NOT NULL UNIQUE,
    ac_password VARCHAR(40) NOT NULL,
    ac_date_created DATE NOT NULL,
    ac_date_of_birth DATE NOT NULL
);

CREATE TABLE Playlist (
    p_playlist_key INT PRIMARY KEY,
    p_name VARCHAR(32) NOT NULL,
    p_number_of_songs INT NOT NULL,
    p_account_key INT REFERENCES Account(ac_account_key)
);


CREATE TABLE Playlist_Song (
    ps_playlist_key INT REFERENCES Playlist(p_playlist_key),
    ps_song_key INT REFERENCES Song(s_song_key),
    PRIMARY KEY (ps_playlist_key, ps_song_key)
);
