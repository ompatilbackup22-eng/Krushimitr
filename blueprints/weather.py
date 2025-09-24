from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from models import WeatherData, Farmer, db
from datetime import datetime
import requests
import os
from functools import wraps

weather_bp = Blueprint('weather', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'farmer_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@weather_bp.route('/weather')
@login_required
def index():
    farmer_id = session['farmer_id']
    weather_data = WeatherData.query.filter_by(farmer_id=farmer_id).order_by(WeatherData.date.desc()).all()
    return render_template('weather/index.html', weather_data=weather_data)

@weather_bp.route('/weather/fetch')
@login_required
def fetch_weather():
    farmer_id = session['farmer_id']
    farmer = Farmer.query.get(farmer_id)
    
    # OpenWeather API key (you should set this as an environment variable)
    api_key = os.getenv('OPENWEATHER_API_KEY', 'your-api-key-here')
    
    if api_key == 'your-api-key-here':
        flash('Weather API key not configured. Please add weather data manually.', 'warning')
        return redirect(url_for('weather.add'))
    
    try:
        # Get weather data by pincode (using a weather service that supports postal codes)
        # For demo purposes, we'll use a mock API call
        # In production, you would use a real weather API
        
        # Mock weather data for demonstration
        weather_data = {
            'temperature': 28.5,
            'humidity': 65.0,
            'rainfall': 0.0
        }
        
        # Create weather data record
        weather_record = WeatherData(
            farmer_id=farmer_id,
            temperature=weather_data['temperature'],
            humidity=weather_data['humidity'],
            rainfall=weather_data['rainfall']
        )
        
        db.session.add(weather_record)
        db.session.commit()
        
        flash('Weather data fetched and saved successfully!', 'success')
        
    except Exception as e:
        flash(f'Error fetching weather data: {str(e)}', 'error')
    
    return redirect(url_for('weather.index'))

@weather_bp.route('/weather/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        farmer_id = session['farmer_id']
        
        try:
            temperature = float(request.form['temperature'])
            humidity = float(request.form['humidity'])
            rainfall = float(request.form['rainfall'])
            
            # Validation
            if not (-50 <= temperature <= 50):
                flash('Temperature must be between -50°C and 50°C!', 'error')
                return render_template('weather/add.html')
            
            if not (0 <= humidity <= 100):
                flash('Humidity must be between 0 and 100%!', 'error')
                return render_template('weather/add.html')
            
            if rainfall < 0:
                flash('Rainfall cannot be negative!', 'error')
                return render_template('weather/add.html')
            
            # Create weather data record
            weather_data = WeatherData(
                farmer_id=farmer_id,
                temperature=temperature,
                humidity=humidity,
                rainfall=rainfall
            )
            
            db.session.add(weather_data)
            db.session.commit()
            
            flash('Weather data added successfully!', 'success')
            return redirect(url_for('weather.index'))
            
        except ValueError:
            flash('Please enter valid numeric values!', 'error')
            return render_template('weather/add.html')
    
    return render_template('weather/add.html')

@weather_bp.route('/weather/<int:weather_id>')
@login_required
def view(weather_id):
    farmer_id = session['farmer_id']
    weather_data = WeatherData.query.filter_by(id=weather_id, farmer_id=farmer_id).first()
    
    if not weather_data:
        flash('Weather data not found!', 'error')
        return redirect(url_for('weather.index'))
    
    return render_template('weather/view.html', weather_data=weather_data)

@weather_bp.route('/weather/<int:weather_id>/delete', methods=['POST'])
@login_required
def delete(weather_id):
    farmer_id = session['farmer_id']
    weather_data = WeatherData.query.filter_by(id=weather_id, farmer_id=farmer_id).first()
    
    if weather_data:
        db.session.delete(weather_data)
        db.session.commit()
        flash('Weather data deleted successfully!', 'success')
    else:
        flash('Weather data not found!', 'error')
    
    return redirect(url_for('weather.index'))

@weather_bp.route('/weather/forecast')
@login_required
def forecast():
    farmer_id = session['farmer_id']
    farmer = Farmer.query.get(farmer_id)
    
    # Get recent weather data for trend analysis
    recent_weather = WeatherData.query.filter_by(farmer_id=farmer_id).order_by(WeatherData.date.desc()).limit(7).all()
    
    # Simple forecast based on recent trends
    forecast_data = {
        'current': recent_weather[0] if recent_weather else None,
        'trend': 'stable',
        'recommendations': []
    }
    
    if recent_weather:
        avg_temp = sum(w.temperature for w in recent_weather) / len(recent_weather)
        avg_humidity = sum(w.humidity for w in recent_weather) / len(recent_weather)
        total_rainfall = sum(w.rainfall for w in recent_weather)
        
        if avg_temp > 30:
            forecast_data['recommendations'].append('High temperature - increase irrigation')
        elif avg_temp < 15:
            forecast_data['recommendations'].append('Low temperature - protect crops from frost')
        
        if avg_humidity > 80:
            forecast_data['recommendations'].append('High humidity - watch for fungal diseases')
        
        if total_rainfall > 50:
            forecast_data['recommendations'].append('Heavy rainfall - ensure proper drainage')
        elif total_rainfall < 10:
            forecast_data['recommendations'].append('Low rainfall - increase irrigation')
    
    return render_template('weather/forecast.html', forecast=forecast_data, recent_weather=recent_weather)
