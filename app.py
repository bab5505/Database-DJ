from flask import Flask, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

migrate = Migrate(app, db)
connect_db(app)


debug = DebugToolbarExtension(app)


@app.route("/")
def root():
    """Homepage"""
    return redirect("/playlists")


@app.route("/playlists")
def show_all_playlists():
    """List of playlists."""
    playlists = Playlist.query.all()
    return render_template("playlists.html", playlists=playlists)


@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show playlist."""
    with app.app_context():
        playlist = Playlist.query.get_or_404(playlist_id)
        return render_template("playlist.html", playlist=playlist)


@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    """Add-playlist form"""
    with app.app_context():
        form = PlaylistForm()
        if form.validate_on_submit():
            playlist = Playlist(name=form.name.data, description=form.description.data)
            db.session.add(playlist)
            db.session.commit()
            return redirect("/playlists")
        return render_template("add_playlist.html", form=form)


@app.route("/songs")
def show_all_songs():
    """List of songs."""
    songs = Song.query.all()
    return render_template("songs.html", songs=songs)


@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """Return a song."""
    with app.app_context():
        song = Song.query.get_or_404(song_id)
        return render_template("song.html", song=song)


@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    """Add-song form:"""
    with app.app_context():
        form = SongForm()
        if form.validate_on_submit():
            song = Song(title=form.title.data, artist=form.artist.data)
            db.session.add(song)
            db.session.commit()
            return redirect("/songs")
        return render_template("add_song.html", form=form)


@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a song to a playlist & redirect to the playlist."""
    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()
    choices = [(song.id, song.title) for song in Song.query.all() if song not in playlist.songs]
    form.song.choices = choices
    if form.validate_on_submit():
        song_id = form.song.data
        playlist_song = PlaylistSong(playlist_id=playlist_id, song_id=song_id)
        db.session.add(playlist_song)
        db.session.commit()
        return redirect(f"/playlists/{playlist_id}")
    return render_template("add_song_to_playlist.html", playlist=playlist, form=form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
