from wtforms import StringField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class PlaylistForm(FlaskForm):
    """Form for adding playlists."""

    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])


class SongForm(FlaskForm):
    """Form for adding songs."""

    title = StringField('Title', validators=[DataRequired()])
    artist = StringField('Artist', validators=[DataRequired()])


# DO NOT MODIFY THIS FORM - EVERYTHING YOU NEED IS HERE
class NewSongForPlaylistForm(FlaskForm):
    """Form for adding a song to playlist."""

    song = SelectField('Song To Add', coerce=int)
