from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models import Video, db
from datetime import datetime
from functools import wraps

videos_bp = Blueprint('videos', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'farmer_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@videos_bp.route('/videos')
@login_required
def index():
    videos = Video.query.order_by(Video.created_at.desc()).all()
    return render_template('videos/index.html', videos=videos)

@videos_bp.route('/videos/category/<category>')
@login_required
def category(category):
    videos = Video.query.filter_by(category=category).order_by(Video.created_at.desc()).all()
    return render_template('videos/category.html', videos=videos, category=category)

@videos_bp.route('/videos/<int:video_id>')
@login_required
def view(video_id):
    video = Video.query.get(video_id)
    if not video:
        flash('Video not found!', 'error')
        return redirect(url_for('videos.index'))
    
    # Get related videos (same category)
    related_videos = Video.query.filter(
        Video.category == video.category,
        Video.id != video_id
    ).limit(4).all()
    
    return render_template('videos/view.html', video=video, related_videos=related_videos)

@videos_bp.route('/videos/search')
@login_required
def search():
    query = request.args.get('q', '')
    if query:
        videos = Video.query.filter(
            Video.title.contains(query) | Video.description.contains(query)
        ).order_by(Video.created_at.desc()).all()
    else:
        videos = []
    
    return render_template('videos/search.html', videos=videos, query=query)

def initialize_videos():
    """Initialize the video database with sample BMP videos"""
    if Video.query.count() == 0:
        videos_data = [
            {
                'title': 'Soil Testing and Analysis',
                'description': 'Learn how to properly test your soil for pH, nutrients, and other important factors.',
                'url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',  # Replace with actual video URL
                'category': 'Soil Management'
            },
            {
                'title': 'Organic Fertilizer Preparation',
                'description': 'Step-by-step guide to preparing organic fertilizers at home.',
                'url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',  # Replace with actual video URL
                'category': 'Fertilizer Management'
            },
            {
                'title': 'Drip Irrigation Setup',
                'description': 'How to set up and maintain a drip irrigation system for efficient water usage.',
                'url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',  # Replace with actual video URL
                'category': 'Irrigation'
            },
            {
                'title': 'Pest and Disease Management',
                'description': 'Natural methods to control pests and diseases in your crops.',
                'url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',  # Replace with actual video URL
                'category': 'Pest Management'
            },
            {
                'title': 'Crop Rotation Techniques',
                'description': 'Learn about effective crop rotation strategies to maintain soil health.',
                'url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',  # Replace with actual video URL
                'category': 'Crop Management'
            },
            {
                'title': 'Harvesting Best Practices',
                'description': 'When and how to harvest your crops for maximum yield and quality.',
                'url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',  # Replace with actual video URL
                'category': 'Harvesting'
            },
            {
                'title': 'Seed Treatment Methods',
                'description': 'Proper seed treatment techniques to improve germination and plant health.',
                'url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',  # Replace with actual video URL
                'category': 'Seed Management'
            },
            {
                'title': 'Weather Monitoring for Farmers',
                'description': 'How to monitor weather conditions and make informed farming decisions.',
                'url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',  # Replace with actual video URL
                'category': 'Weather Management'
            }
        ]
        
        for video_data in videos_data:
            video = Video(**video_data)
            db.session.add(video)
        
        db.session.commit()
