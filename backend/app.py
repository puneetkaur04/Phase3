from flask_cors import CORS
from flask import Flask
import psycopg2
from flask import request, jsonify

app = Flask(__name__)
CORS(app)

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="ProjectDB",
        user="raunak",
        password="ron04",
        port=5432
    )

### ACCOUNT Endpoints

# Create an account
@app.route("/accounts/add_account", methods=["POST"])
def add_account():
    data = request.json
    username = data.get("ac_username")
    password = data.get("ac_password")
    date_created = data.get("ac_date_created")
    dob = data.get("ac_date_of_birth")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT MAX(ac_account_key) FROM Account")
        max_id = cur.fetchone()[0] or 0
        new_id = max_id + 1

        cur.execute(
            """
            INSERT INTO Account (ac_account_key, ac_username, ac_password, ac_date_created, ac_date_of_birth)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (new_id, username, password, date_created, dob)
        )
        conn.commit()

        return jsonify({
            "message": "Account created successfully",
            "ac_account_key": new_id
        })
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

# View own account info
@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_account(account_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT ac_account_key, ac_username, ac_password, ac_date_created, ac_date_of_birth FROM Account WHERE ac_account_key=%s",
        (account_id,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return jsonify({"error": "Account not found"}), 404

    return jsonify({
        "ac_account_key": row[0],
        "ac_username": row[1],
        "ac_password": row[2],
        "ac_date_created": str(row[3]),
        "ac_date_of_birth": str(row[4])
    })


# Update account info
@app.route("/accounts/update_account/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    data = request.json
    username = data.get("ac_username")
    password = data.get("ac_password")
    dob = data.get("ac_date_of_birth")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE Account SET ac_username=%s, ac_password=%s, ac_date_of_birth=%s WHERE ac_account_key=%s",
            (username, password, dob, account_id)
        )
        conn.commit()
        return jsonify({"message": "Account updated"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

#Login
@app.route("/accounts/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("ac_username")
    password = data.get("ac_password")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT ac_account_key FROM Account WHERE ac_username=%s AND ac_password=%s",
            (username, password)
        )
        row = cur.fetchone()
        if row:
            return jsonify({"ac_account_key": row[0]})
        else:
            return jsonify({"error": "Invalid username or password"}), 401
    finally:
        cur.close()
        conn.close()


### ALBUMS Endpoints

# View all albums
@app.route("/albums/all", methods=["GET"])
def get_all_albums():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT al_album_key, al_album_name, al_date, al_number_of_songs, 
            al_artist_key, ar_name
            FROM Album
            JOIN Artist ON al_artist_key = ar_artist_key
            ORDER BY al_album_name;
        """)
        albums = []
        for row in cur.fetchall():
            albums.append({
                "al_album_key": row[0],
                "al_album_name": row[1],
                "al_date": str(row[2]) if row[2] else None,
                "al_number_of_songs": row[3],
                "al_artist_key": row[4],
                "ar_name": row[5]
            })
        return jsonify(albums)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


# Add new album
@app.route("/albums/add_album", methods=["POST"])
def add_album():
    data = request.json
    name = data.get("al_album_name")
    date = data.get("al_date")
    artist_key = data.get("al_artist_key")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT ar_artist_key FROM Artist WHERE ar_artist_key=%s", (artist_key,))
        if not cur.fetchone():
            return jsonify({"error": "Artist does not exist"}), 400

        cur.execute("SELECT MAX(al_album_key) FROM Album")
        max_key = cur.fetchone()[0]
        new_key = max_key + 1

        cur.execute(
            "INSERT INTO Album (al_album_key, al_album_name, al_date, al_number_of_songs, al_artist_key) VALUES (%s, %s, %s, 0, %s)",
            (new_key, name, date, artist_key)
        )

        conn.commit()
        return jsonify({"message": "Album created", "al_album_key": new_key})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

### ARTISTS Endpoints

# Get all artists
@app.route("/artists/all", methods=["GET"])
def get_all_artists():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT ar_artist_key, ar_name FROM Artist ORDER BY ar_name")
        artists = []
        for row in cur.fetchall():
            artists.append({
                "ar_artist_key": row[0],
                "ar_name": row[1]
            })
        return jsonify(artists)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


# Add new artist
@app.route("/artists/add_artist", methods=["POST"])
def add_artist():
    data = request.json
    name = data.get("ar_name")
    genre = data.get("ar_genre")
    dob = data.get("ar_date_of_birth")
    bio = data.get("ar_biography")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT MAX(ar_artist_key) FROM Artist")
        max_key = cur.fetchone()[0]
        new_key = max_key + 1

        cur.execute(
            "INSERT INTO Artist (ar_artist_key, ar_name, ar_genre, ar_date_of_birth, ar_biography) VALUES (%s, %s, %s, %s, %s)",
            (new_key, name, genre, dob, bio)
        )

        conn.commit()
        return jsonify({"message": "Artist created", "ar_artist_key": new_key})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

#PLAYLIST Endpoints

# Create playlist
@app.route("/playlists/add_playlist", methods=["POST"])
def add_playlist():
    data = request.json
    name = data.get("p_name")
    account_id = data.get("p_account_key")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT ac_account_key FROM Account WHERE ac_account_key=%s", (account_id,))
        if not cur.fetchone():
            return jsonify({"error": "Account does not exist"}), 400

        cur.execute("SELECT MAX(p_playlist_key) FROM Playlist")
        max_key = cur.fetchone()[0]
        new_key = max_key + 1

        cur.execute(
            "INSERT INTO Playlist (p_playlist_key, p_name, p_number_of_songs, p_account_key) VALUES (%s, %s, 0, %s)",
            (new_key, name, account_id)
        )

        conn.commit()
        return jsonify({"message": "Playlist created", "p_playlist_key": new_key})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()


# View all playlists of a user
@app.route("/playlists/account/<int:account_id>", methods=["GET"])
def get_account_playlists(account_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT p_playlist_key, p_name, p_number_of_songs FROM Playlist WHERE p_account_key=%s", (account_id,))
    playlists = [{"p_playlist_key": r[0], "p_name": r[1], "p_number_of_songs": r[2]} for r in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(playlists)


# View playlist info including songs
@app.route("/playlists/<int:playlist_id>", methods=["GET"])
def get_playlist(playlist_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT p_name, p_number_of_songs, p_account_key
        FROM Playlist
        WHERE p_playlist_key=%s
    """, (playlist_id,))
    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return jsonify({"error": "Playlist not found"}), 404

    playlist_name, num_songs, account_id = row

    cur.execute("""
        SELECT 
            s_song_key,
            s_song_name,
            s_time,
            s_genre,
            ar_name,
            al_album_name
        FROM Playlist_Song
        JOIN Song ON ps_song_key = s_song_key
        JOIN Album ON s_album_key = al_album_key
        JOIN Artist ON al_artist_key = ar_artist_key
        WHERE ps_playlist_key = %s;
    """, (playlist_id,))

    songs = []
    for row in cur.fetchall():
        s_key, s_name, s_time, s_genre, ar_name, al_name = row
        songs.append({
            "s_song_key": s_key,
            "s_song_name": s_name,
            "s_time": s_time.isoformat() if s_time else None,
            "s_genre": s_genre,
            "ar_name": ar_name,
            "al_album_name": al_name
        })

    cur.close()
    conn.close()

    return jsonify({
        "p_playlist_key": playlist_id,
        "p_name": playlist_name,
        "p_number_of_songs": num_songs,
        "p_account_key": account_id,
        "songs": songs
    })


# Add song to playlist
@app.route("/playlists/add_song", methods=["POST"])
def add_song_to_playlist():
    data = request.json
    playlist_id = data.get("p_playlist_key")
    song_id = data.get("s_song_key")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO Playlist_Song (ps_playlist_key, ps_song_key) VALUES (%s, %s)", (playlist_id, song_id))
        cur.execute("UPDATE Playlist SET p_number_of_songs = (SELECT COUNT(*) FROM Playlist_Song WHERE ps_playlist_key=%s) WHERE p_playlist_key=%s", (playlist_id, playlist_id))
        conn.commit()
        return jsonify({"message": "Song added to playlist"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()


# Delete song from playlist
@app.route("/playlists/delete_song", methods=["POST"])
def delete_song_from_playlist():
    data = request.json
    playlist_id = data.get("p_playlist_key")
    song_id = data.get("s_song_key")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Playlist_Song WHERE ps_playlist_key=%s AND ps_song_key=%s", (playlist_id, song_id))
        cur.execute("UPDATE Playlist SET p_number_of_songs = (SELECT COUNT(*) FROM Playlist_Song WHERE ps_playlist_key=%s) WHERE p_playlist_key=%s", (playlist_id, playlist_id))
        conn.commit()
        return jsonify({"message": "Song removed from playlist"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()


# Delete playlist and if there are any, delete all songs in the playlist
@app.route("/playlists/delete_playlist/<int:playlist_id>", methods=["DELETE"])
def delete_playlist(playlist_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Playlist_Song WHERE ps_playlist_key=%s", (playlist_id,))
        cur.execute("DELETE FROM Playlist WHERE p_playlist_key=%s", (playlist_id,))
        conn.commit()
        return jsonify({"message": "Playlist deleted"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()


# Update playlist info
@app.route("/playlists/update_playlist/<int:playlist_id>", methods=["PUT"])
def update_playlist(playlist_id):
    data = request.json
    name = data.get("p_name")
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE Playlist SET p_name=%s WHERE p_playlist_key=%s", (name, playlist_id))
        conn.commit()
        return jsonify({"message": "Playlist updated"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()


### SONGS Endpoints

# Add new song to the overall database
@app.route("/songs/add_song", methods=["POST"])
def add_song():
    data = request.json
    name = data.get("s_song_name")
    time = data.get("s_time")
    genre = data.get("s_genre")
    album_key = data.get("s_album_key")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT al_album_key FROM Album WHERE al_album_key=%s", (album_key,))
        if not cur.fetchone():
            return jsonify({"error": "Album does not exist"}), 400

        cur.execute("SELECT MAX(s_song_key) FROM Song")
        max_key = cur.fetchone()[0]
        new_key = max_key + 1

        cur.execute(
            "INSERT INTO Song (s_song_key, s_song_name, s_time, s_genre, s_album_key) VALUES (%s, %s, %s, %s, %s)",
            (new_key, name, time, genre, album_key)
        )

        cur.execute(
            "UPDATE Album SET al_number_of_songs = (SELECT COUNT(*) FROM Song WHERE s_album_key=%s) WHERE al_album_key=%s",
            (album_key, album_key)
        )

        conn.commit()
        return jsonify({"message": "Song created", "s_song_key": new_key})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

#Search for songs by title, artist, or album
@app.route("/songs/search", methods=["GET"])
def search_songs():
    by = (request.args.get("by") or "title").lower()
    query = request.args.get("query") or ""
    pattern = f"%{query.strip().lower()}%"

    conn = get_connection()
    cur = conn.cursor()
    try:
        if by == "artist":
            cur.execute("""
                SELECT s.s_song_key, s.s_song_name, s.s_time, s.s_genre,
                       a.al_album_key, a.al_album_name, ar.ar_artist_key, ar.ar_name
                FROM Song s
                JOIN Album a ON s.s_album_key = a.al_album_key
                JOIN Artist ar ON a.al_artist_key = ar.ar_artist_key
                WHERE LOWER(ar.ar_name) LIKE %s
                ORDER BY s.s_song_name
                LIMIT 200
            """, (pattern,))
        elif by == "album":
            cur.execute("""
                SELECT s.s_song_key, s.s_song_name, s.s_time, s.s_genre,
                       a.al_album_key, a.al_album_name, ar.ar_artist_key, ar.ar_name
                FROM Song s
                JOIN Album a ON s.s_album_key = a.al_album_key
                JOIN Artist ar ON a.al_artist_key = ar.ar_artist_key
                WHERE LOWER(a.al_album_name) LIKE %s
                ORDER BY s.s_song_name
                LIMIT 200
            """, (pattern,))
        else:
            cur.execute("""
                SELECT s.s_song_key, s.s_song_name, s.s_time, s.s_genre,
                       a.al_album_key, a.al_album_name, ar.ar_artist_key, ar.ar_name
                FROM Song s
                LEFT JOIN Album a ON s.s_album_key = a.al_album_key
                LEFT JOIN Artist ar ON a.al_artist_key = ar.ar_artist_key
                WHERE LOWER(s.s_song_name) LIKE %s
                ORDER BY s.s_song_name
                LIMIT 200
            """, (pattern,))

        rows = cur.fetchall()
        results = []
        for r in rows:
            results.append({
                "s_song_key": r[0],
                "s_song_name": r[1],
                "s_time": r[2].isoformat() if r[2] is not None else None,
                "s_genre": r[3],
                "al_album_key": r[4],
                "al_album_name": r[5],
                "ar_artist_key": r[6],
                "ar_name": r[7]
            })
        return jsonify(results)
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()




if __name__ == "__main__":
    app.run(debug=True)
