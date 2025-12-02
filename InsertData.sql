INSERT INTO Artist VALUES
(1, 'Taylor Swift', 'Pop', '1989-12-13', 'American singer-songwriter.'),
(2, 'Drake', 'Hip-Hop', '1986-10-24', 'Canadian rapper and singer.'),
(3, 'Adele', 'Soul', '1988-05-05', 'English singer and songwriter.'),
(4, 'Ed Sheeran', 'Pop', '1991-02-17', 'English singer-songwriter and guitarist.'),
(5, 'Billie Eilish', 'Alternative', '2001-12-18', 'American singer-songwriter known for her dark pop style.'),
(6, 'The Weeknd', 'R&B', '1990-02-16', 'Canadian singer known for his falsetto and cinematic music.'),
(7, 'Bruno Mars', 'Funk', '1985-10-08', 'American singer and performer known for energetic stage shows.'),
(8, 'Ariana Grande', 'Pop', '1993-06-26', 'American singer and actress known for her wide vocal range.'),
(9, 'Post Malone', 'Rap', '1995-07-04', 'American rapper and singer-songwriter blending genres.'),
(10, 'Olivia Rodrigo', 'Pop', '2003-02-20', 'American singer-songwriter known for emotional pop ballads.');

INSERT INTO Album VALUES
(1, 'Folklore', '2020-07-24', 16, 1),
(2, 'Midnights', '2022-10-21', 13, 1),
(3, 'Justice', '2021-06-17', 12, 2),
(4, 'Views', '2015-11-20', 11, 3),
(5, '30', '2021-10-29', 14, 4),
(6, 'No.6 Collaborations Project', '2019-03-29', 10, 5),
(7, 'When We All Fall Asleep, Where Do We Go?', '2022-01-07', 16, 6),
(8, 'Starboy', '2016-11-18', 12, 7),
(9, '24K Magic', '2018-08-17', 18, 8),
(10, 'Rockstar', '2023-05-12', 15, 9);


INSERT INTO Song VALUES
(1, 'Cardigan', '00:03:45', 'Pop', 1),
(2, 'The Last Great American Dynasty', '00:04:12', 'Pop', 1),
(3, 'Anti-Hero', '00:03:50', 'Pop', 2),
(4, 'Laugh Now Cry Later', '00:04:05', 'Hip-Hop', 3),
(5, 'Hello', '00:03:57', 'Soul', 4),
(6, 'Shivers', '00:04:21', 'Pop', 5),
(7, 'Bad Guy', '00:03:35', 'Alternative', 6),
(8, 'Blinding Lights', '00:04:15', 'R&B', 7),
(9, '24K Magic', '00:03:58', 'Funk', 8),
(10, 'Rockstar', '00:04:10', 'Rap', 10);

INSERT INTO Account VALUES
(1, 'melody_maker', 'pass1234', '2022-01-10', '2000-03-05'),
(2, 'beatlover', 'music2022', '2022-02-14', '1998-07-19'),
(3, 'tune_addict', 'poprocks', '2022-03-21', '1999-12-10'),
(4, 'groove_guru', 'groovy1', '2022-04-10', '1997-08-22'),
(5, 'rhythm_queen', 'rq12345', '2022-05-09', '2001-09-15'),
(6, 'bass_head', 'bassman', '2023-01-01', '1995-11-11'),
(7, 'vibe_master', 'vibe123', '2023-02-12', '1996-10-06'),
(8, 'lyric_lover', 'lyrics!', '2023-03-30', '2000-01-25'),
(9, 'sound_seek', 'seek99', '2023-05-18', '1998-06-09'),
(10, 'note_catcher', 'catch22', '2023-06-29', '2002-04-17');

INSERT INTO Playlist VALUES
(1, 'Morning Boost', '2023-01-10', 1),
(2, 'Chill Beats', '2023-01-15', 2),
(3, 'Late Night Drive', '2023-02-01', 3),
(4, 'Workout Pump', '2023-02-12', 4),
(5, 'Study Focus', '2023-03-04', 5),
(6, 'Weekend Party', '2023-03-25', 6),
(7, 'Throwback Vibes', '2023-04-02', 7),
(8, 'R&B Grooves', '2023-04-18', 8),
(9, 'Pop Mix', '2023-05-05', 9),
(10, 'New Discoveries', '2023-05-30', 10);

INSERT INTO Playlist_Song VALUES
(1, 1), (1, 2),
(2, 3), (2, 4),
(3, 5), (3, 6),
(4, 7), (4, 8),
(5, 9), (5, 10),
(6, 1), (6, 3),
(7, 2), (7, 5),
(8, 4), (8, 6),
(9, 7), (9, 9),
(10, 8), (10, 10);