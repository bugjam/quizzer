from flask import *
from flask_session import Session
from spotify import SpotifyClient
import quizzer

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SERVER_NAME'] = 'localhost:5000'
Session(app)

spotify : SpotifyClient = None

@app.route("/")
def welcome():
    g.welcome_message = quizzer.welcome_message()
    return render_template('welcome.html')

@app.route("/quiz/new/by_playlist")
def quiz_new_select_playlist():
    if 'user' in session:
        g.playlists = spotify.playlists()
        g.plalist_action = url_for('quiz_new_by_playlist')
        return render_template('playlists.html')
    else:
        flash('Please authenticate with Spotify first', 'error')
        return redirect('/')

@app.route("/quiz/new/by_artist")
def quiz_new_select_artist():
    g.artists = spotify.following_artists() if 'user' in session else []
    g.plalist_action = url_for('quiz_new_by_artist')
    return render_template('artists.html')
    
@app.route("/quiz/new/by_playlist", methods=['POST'])
def quiz_new_by_playlist():
    playlist = request.form.get('playlist')
    artists = spotify.playlist_artists(playlist)
    session['quiz'] = quizzer.ArtistsQuiz(artists)
    return redirect(url_for('quiz_play'))

@app.route("/quiz/new/by_artist", methods=['POST'])
def quiz_new_by_artist():
    if 'artist_id' in request.form:
        artist = spotify.artist(request.form.get('artist_id')).name
    else:
        artist = request.form.get('artist_name')
    session['quiz'] = quizzer.ArtistsQuiz([artist])
    return redirect(url_for('quiz_play'))

@app.route("/quiz/play")
def quiz_play():
    g.quiz = session['quiz']
    return render_template('quiz.html')

@app.route("/quiz/question")
def quiz_question():
    question = session['quiz'].ask_question()
    question.update({"question_number": session['quiz'].question_number})
    session.modified = True
    return jsonify(question)

@app.route("/quiz/question", methods=['POST'])
def quiz_answer():
    n = request.form.get('answer')
    answer = session['quiz'].answers[int(n)]
    feedback = session['quiz'].check_answer(answer)
    feedback.update({"correct_answers": session['quiz'].correct_answers})
    session.modified = True
    return jsonify(feedback)

@app.route("/spotify/authenticate")
def spotify_authenticate():
    return app.redirect(spotify.auth_manager.get_authorize_url())

@app.route("/spotify/callback")
def spotify_callback():
    state = request.args.get('state')
    error = request.args.get('error')
    code = request.args.get('code')
    if state != spotify.auth_manager.state :
        flash('State mismatch', 'error')
    elif error :
        flash(error, 'error')
    else:
        try:
            spotify.auth_manager.get_access_token(code=code, as_dict=False, check_cache=False)
            session['user'] = spotify.who_am_i()
        except Exception as e:
            flash(e, 'error')
    return app.redirect('/')

with app.app_context():
    spotify = SpotifyClient(session=session, redirect_uri=url_for('spotify_callback', _external=True))
