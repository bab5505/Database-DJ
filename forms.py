from wtforms import StringField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class PlaylistForm(FlaskForm):
    """Adding playlists."""

    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])


class SongForm(FlaskForm):
    """Adding songs."""

    title = StringField('Title', validators=[DataRequired()])
    artist = StringField('Artist', validators=[DataRequired()])


class NewSongForPlaylistForm(FlaskForm):
    """Adding a song to playlist."""

    song = SelectField('Song To Add', coerce=int)
