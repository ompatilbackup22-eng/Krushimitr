from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_babel import Babel, gettext, ngettext, get_locale
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import requests
import os
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///krishimitra.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Babel configuration
app.config['LANGUAGES'] = {
    'en': 'English',
    'hi': 'हिन्दी',
    'mr': 'मराठी'
}
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

# Import models and initialize db
from models import db, Farmer, SoilData, WeatherData, Crop, Recommendation, Alert, Video, Query, initialize_crops
db.init_app(app)

# Import blueprints
from blueprints.auth import auth_bp
from blueprints.dashboard import dashboard_bp
from blueprints.soil import soil_bp
from blueprints.weather import weather_bp
from blueprints.crops import crops_bp
from blueprints.alerts import alerts_bp
from blueprints.videos import videos_bp
from blueprints.support import support_bp
from blueprints.reports import reports_bp

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(soil_bp)
app.register_blueprint(weather_bp)
app.register_blueprint(crops_bp)
app.register_blueprint(alerts_bp)
app.register_blueprint(videos_bp)
app.register_blueprint(support_bp)
app.register_blueprint(reports_bp)

# Locale selector function (moved after app is fully configured)
def get_locale():
    try:
        # Check if language is set in session
        if 'language' in session:
            lang = session['language']
            if lang in app.config['LANGUAGES']:
                return lang
        # Check if language is in URL parameters
        if request.args.get('lang'):
            lang = request.args.get('lang')
            if lang in app.config['LANGUAGES']:
                return lang
        # Default to English
        return 'en'
    except Exception as e:
        print(f"Error in get_locale: {e}")
        return 'en'

# Initialize Babel with locale selector
babel = Babel(app, locale_selector=get_locale)

# Make get_locale and other functions available in templates
@app.context_processor
def inject_get_locale():
    from flask_babel import get_locale as babel_get_locale
    return dict(
        get_locale=babel_get_locale,
        current_language=session.get('language', 'en')
    )

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'farmer_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/debug_language')
def debug_language():
    from flask_babel import get_locale
    current_locale = get_locale()
    session_lang = session.get('language', 'None')
    return f"""
    <h1>Language Debug Info</h1>
    <p>Current Locale: {current_locale}</p>
    <p>Session Language: {session_lang}</p>
    <p>Available Languages: {list(app.config['LANGUAGES'].keys())}</p>
    <p>Test Translation: {gettext('Home')}</p>
    <a href="/">Back to Home</a>
    """

@app.route('/test_language')
def test_language():
    return render_template('test_language.html')

@app.route('/set_language/<language>')
def set_language(language=None):
    if language and language in app.config['LANGUAGES']:
        session['language'] = language
        flash(f'Language changed to {app.config["LANGUAGES"][language]}', 'success')
    else:
        flash('Invalid language selection', 'error')
    return redirect(request.referrer or url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Initialize crop knowledge base
        from models import initialize_crops
        initialize_crops()
        # Initialize video database
        from blueprints.videos import initialize_videos
        initialize_videos()
    port = int(os.environ.get('PORT', 5000))
    # Use threaded=True and disable reloader to avoid Windows socket issues
    app.run(debug=True, host='127.0.0.1', port=port, threaded=True, use_reloader=False)

