from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from models import Farmer, SoilData, WeatherData, Recommendation, Alert, db
from datetime import datetime, timedelta
from functools import wraps

dashboard_bp = Blueprint('dashboard', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'farmer_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@dashboard_bp.route('/dashboard')
@login_required
def index():
    farmer_id = session['farmer_id']
    farmer = Farmer.query.get(farmer_id)
    
    # Get latest soil data
    latest_soil = SoilData.query.filter_by(farmer_id=farmer_id).order_by(SoilData.date.desc()).first()
    
    # Get latest weather data
    latest_weather = WeatherData.query.filter_by(farmer_id=farmer_id).order_by(WeatherData.date.desc()).first()
    
    # Get active recommendations
    recommendations = Recommendation.query.filter_by(farmer_id=farmer_id).order_by(Recommendation.recommended_date.desc()).limit(5).all()
    
    # Get pending alerts
    pending_alerts = Alert.query.filter_by(farmer_id=farmer_id, status='pending').order_by(Alert.alert_date.asc()).all()
    
    # Get recent soil data history
    soil_history = SoilData.query.filter_by(farmer_id=farmer_id).order_by(SoilData.date.desc()).limit(5).all()
    
    # Get recent weather data history
    weather_history = WeatherData.query.filter_by(farmer_id=farmer_id).order_by(WeatherData.date.desc()).limit(5).all()
    
    return render_template('dashboard/index.html',
                         farmer=farmer,
                         latest_soil=latest_soil,
                         latest_weather=latest_weather,
                         recommendations=recommendations,
                         pending_alerts=pending_alerts,
                         soil_history=soil_history,
                         weather_history=weather_history,
                         current_date=datetime.now().date())

@dashboard_bp.route('/profile')
@login_required
def profile():
    farmer_id = session['farmer_id']
    farmer = Farmer.query.get(farmer_id)
    return render_template('dashboard/profile.html', farmer=farmer)

@dashboard_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    farmer_id = session['farmer_id']
    farmer = Farmer.query.get(farmer_id)
    
    if request.method == 'POST':
        farmer.name = request.form['name']
        farmer.village = request.form['village']
        farmer.tehsil = request.form['tehsil']
        farmer.district = request.form['district']
        farmer.pincode = request.form['pincode']
        
        db.session.commit()
        session['farmer_name'] = farmer.name
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('dashboard.profile'))
    
    return render_template('dashboard/edit_profile.html', farmer=farmer)
