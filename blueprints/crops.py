from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from models import Crop, Recommendation, SoilData, WeatherData, Farmer, db
from datetime import datetime, timedelta
from functools import wraps

crops_bp = Blueprint('crops', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'farmer_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@crops_bp.route('/crops')
@login_required
def index():
    farmer_id = session['farmer_id']
    recommendations = Recommendation.query.filter_by(farmer_id=farmer_id).order_by(Recommendation.recommended_date.desc()).all()
    return render_template('crops/index.html', recommendations=recommendations)

@crops_bp.route('/crops/recommend')
@login_required
def recommend():
    farmer_id = session['farmer_id']
    
    # Get latest soil and weather data
    latest_soil = SoilData.query.filter_by(farmer_id=farmer_id).order_by(SoilData.date.desc()).first()
    latest_weather = WeatherData.query.filter_by(farmer_id=farmer_id).order_by(WeatherData.date.desc()).first()
    
    if not latest_soil or not latest_weather:
        flash('Please add soil and weather data first to get crop recommendations!', 'error')
        return redirect(url_for('dashboard.index'))
    
    # Determine current season based on month
    current_month = datetime.now().month
    if current_month in [6, 7, 8, 9, 10]:
        current_season = 'Kharif'
    elif current_month in [11, 12, 1, 2]:
        current_season = 'Rabi'
    else:
        current_season = 'Summer'
    
    # Get suitable crops based on soil and weather conditions
    suitable_crops = []
    all_crops = Crop.query.filter_by(season=current_season).all()
    
    for crop in all_crops:
        score = 0
        total_conditions = 0
        
        # Check pH compatibility
        if crop.ph_min <= latest_soil.ph <= crop.ph_max:
            score += 1
        total_conditions += 1
        
        # Check temperature compatibility
        if crop.temp_min <= latest_weather.temperature <= crop.temp_max:
            score += 1
        total_conditions += 1
        
        # Check moisture compatibility (within 20% range)
        if abs(latest_soil.moisture - crop.moisture_req) <= 20:
            score += 1
        total_conditions += 1
        
        # Check NPK levels
        if latest_soil.nitrogen >= crop.nitrogen_req * 0.8:
            score += 0.5
        if latest_soil.phosphorus >= crop.phosphorus_req * 0.8:
            score += 0.5
        if latest_soil.potassium >= crop.potassium_req * 0.8:
            score += 0.5
        total_conditions += 1.5
        
        # Calculate confidence score
        confidence = (score / total_conditions) * 100
        
        if confidence >= 60:  # Only recommend crops with 60%+ compatibility
            suitable_crops.append({
                'crop': crop,
                'confidence': confidence,
                'score': score,
                'total_conditions': total_conditions
            })
    
    # Sort by confidence score
    suitable_crops.sort(key=lambda x: x['confidence'], reverse=True)
    
    return render_template('crops/recommend.html', 
                         suitable_crops=suitable_crops,
                         current_season=current_season,
                         soil_data=latest_soil,
                         weather_data=latest_weather)

@crops_bp.route('/crops/recommend/<int:crop_id>', methods=['POST'])
@login_required
def save_recommendation(crop_id):
    farmer_id = session['farmer_id']
    
    # Check if recommendation already exists
    existing = Recommendation.query.filter_by(farmer_id=farmer_id, crop_id=crop_id).first()
    if existing:
        flash('This crop is already in your recommendations!', 'warning')
        return redirect(url_for('crops.recommend'))
    
    # Create new recommendation
    recommendation = Recommendation(
        farmer_id=farmer_id,
        crop_id=crop_id,
        confidence_score=float(request.form.get('confidence', 0))
    )
    
    db.session.add(recommendation)
    db.session.commit()
    
    flash('Crop recommendation saved successfully!', 'success')
    return redirect(url_for('crops.index'))

@crops_bp.route('/crops/calendar/<int:crop_id>')
@login_required
def calendar(crop_id):
    farmer_id = session['farmer_id']
    crop = Crop.query.get(crop_id)
    
    if not crop:
        flash('Crop not found!', 'error')
        return redirect(url_for('crops.index'))
    
    # Generate crop calendar
    start_date = datetime.now()
    calendar_events = []
    
    # Sowing
    calendar_events.append({
        'date': start_date,
        'event': 'Sowing',
        'description': f'Plant {crop.crop_name} seeds',
        'type': 'sowing'
    })
    
    # Irrigation schedule (every 7 days for first month, then every 10 days)
    for i in range(1, crop.duration_days // 7 + 1):
        if i <= 4:  # First month
            event_date = start_date + timedelta(days=i*7)
            calendar_events.append({
                'date': event_date,
                'event': 'Irrigation',
                'description': f'Water {crop.crop_name} plants',
                'type': 'irrigation'
            })
        else:  # After first month
            event_date = start_date + timedelta(days=i*10)
            calendar_events.append({
                'date': event_date,
                'event': 'Irrigation',
                'description': f'Water {crop.crop_name} plants',
                'type': 'irrigation'
            })
    
    # Fertilizer application schedule
    fertilizer_dates = [
        (15, 'Nitrogen application'),
        (30, 'Phosphorus application'),
        (45, 'Potassium application'),
        (60, 'Balanced NPK application')
    ]
    
    for days, description in fertilizer_dates:
        if days < crop.duration_days:
            event_date = start_date + timedelta(days=days)
            calendar_events.append({
                'date': event_date,
                'event': 'Fertilizer',
                'description': f'{description} for {crop.crop_name}',
                'type': 'fertilizer'
            })
    
    # Pest/Disease spray reminders
    spray_dates = [20, 40, 60, 80]
    for days in spray_dates:
        if days < crop.duration_days:
            event_date = start_date + timedelta(days=days)
            calendar_events.append({
                'date': event_date,
                'event': 'Spray',
                'description': f'Pest/Disease control spray for {crop.crop_name}',
                'type': 'spray'
            })
    
    # Harvest
    harvest_date = start_date + timedelta(days=crop.duration_days)
    calendar_events.append({
        'date': harvest_date,
        'event': 'Harvest',
        'description': f'Harvest {crop.crop_name}',
        'type': 'harvest'
    })
    
    # Sort events by date
    calendar_events.sort(key=lambda x: x['date'])
    
    return render_template('crops/calendar.html', 
                         crop=crop, 
                         calendar_events=calendar_events,
                         start_date=start_date,
                         timedelta=timedelta)

@crops_bp.route('/crops/knowledge')
@login_required
def knowledge():
    crops = Crop.query.all()
    return render_template('crops/knowledge.html', crops=crops)

@crops_bp.route('/crops/knowledge/<int:crop_id>')
@login_required
def crop_details(crop_id):
    crop = Crop.query.get(crop_id)
    if not crop:
        flash('Crop not found!', 'error')
        return redirect(url_for('crops.knowledge'))
    
    return render_template('crops/crop_details.html', crop=crop)
