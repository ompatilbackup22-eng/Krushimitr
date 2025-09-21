from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Farmer(db.Model):
    __tablename__ = 'farmers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15), unique=True, nullable=False)
    village = db.Column(db.String(100), nullable=False)
    tehsil = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    soil_data = db.relationship('SoilData', backref='farmer', lazy=True, cascade='all, delete-orphan')
    weather_data = db.relationship('WeatherData', backref='farmer', lazy=True, cascade='all, delete-orphan')
    recommendations = db.relationship('Recommendation', backref='farmer', lazy=True, cascade='all, delete-orphan')
    alerts = db.relationship('Alert', backref='farmer', lazy=True, cascade='all, delete-orphan')
    queries = db.relationship('Query', backref='farmer', lazy=True, cascade='all, delete-orphan')

class SoilData(db.Model):
    __tablename__ = 'soil_data'
    
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'), nullable=False)
    ph = db.Column(db.Float, nullable=False)
    moisture = db.Column(db.Float, nullable=False)
    nitrogen = db.Column(db.Float, nullable=False)
    phosphorus = db.Column(db.Float, nullable=False)
    potassium = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    soil_type = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class WeatherData(db.Model):
    __tablename__ = 'weather_data'
    
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    rainfall = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

class Crop(db.Model):
    __tablename__ = 'crops'
    
    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False)
    season = db.Column(db.String(20), nullable=False)  # Kharif, Rabi, Summer
    duration_days = db.Column(db.Integer, nullable=False)
    ph_min = db.Column(db.Float, nullable=False)
    ph_max = db.Column(db.Float, nullable=False)
    temp_min = db.Column(db.Float, nullable=False)
    temp_max = db.Column(db.Float, nullable=False)
    moisture_req = db.Column(db.Float, nullable=False)
    nitrogen_req = db.Column(db.Float, nullable=False)
    phosphorus_req = db.Column(db.Float, nullable=False)
    potassium_req = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text)
    
    # Relationships
    recommendations = db.relationship('Recommendation', backref='crop', lazy=True, cascade='all, delete-orphan')
    alerts = db.relationship('Alert', backref='crop', lazy=True, cascade='all, delete-orphan')

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id'), nullable=False)
    recommended_date = db.Column(db.DateTime, default=datetime.utcnow)
    confidence_score = db.Column(db.Float, default=0.0)

class Alert(db.Model):
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'), nullable=False)
    crop_id = db.Column(db.Integer, db.ForeignKey('crops.id'), nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)  # irrigation, fertilizer, spray, harvest
    alert_date = db.Column(db.DateTime, nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, completed, dismissed

class Video(db.Model):
    __tablename__ = 'videos'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(50), default='General')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Query(db.Model):
    __tablename__ = 'queries'
    
    id = db.Column(db.Integer, primary_key=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmers.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, answered
    reply = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    answered_at = db.Column(db.DateTime)

def initialize_crops():
    """Initialize the crop knowledge base with sample data"""
    if Crop.query.count() == 0:
        crops_data = [
            {
                'crop_name': 'Soybean',
                'season': 'Kharif',
                'duration_days': 120,
                'ph_min': 6.0,
                'ph_max': 7.5,
                'temp_min': 20.0,
                'temp_max': 35.0,
                'moisture_req': 60.0,
                'nitrogen_req': 25.0,
                'phosphorus_req': 15.0,
                'potassium_req': 20.0,
                'notes': 'Good for protein content, requires well-drained soil'
            },
            {
                'crop_name': 'Cotton',
                'season': 'Kharif',
                'duration_days': 180,
                'ph_min': 5.5,
                'ph_max': 8.0,
                'temp_min': 21.0,
                'temp_max': 30.0,
                'moisture_req': 70.0,
                'nitrogen_req': 30.0,
                'phosphorus_req': 20.0,
                'potassium_req': 25.0,
                'notes': 'Requires warm climate and adequate water'
            },
            {
                'crop_name': 'Sugarcane',
                'season': 'Kharif',
                'duration_days': 365,
                'ph_min': 6.0,
                'ph_max': 7.5,
                'temp_min': 26.0,
                'temp_max': 32.0,
                'moisture_req': 80.0,
                'nitrogen_req': 40.0,
                'phosphorus_req': 25.0,
                'potassium_req': 35.0,
                'notes': 'Long duration crop, requires high water and nutrients'
            },
            {
                'crop_name': 'Moong',
                'season': 'Kharif',
                'duration_days': 90,
                'ph_min': 6.0,
                'ph_max': 7.5,
                'temp_min': 25.0,
                'temp_max': 35.0,
                'moisture_req': 50.0,
                'nitrogen_req': 20.0,
                'phosphorus_req': 10.0,
                'potassium_req': 15.0,
                'notes': 'Short duration pulse crop, drought tolerant'
            },
            {
                'crop_name': 'Tur (Pigeon Pea)',
                'season': 'Kharif',
                'duration_days': 150,
                'ph_min': 6.0,
                'ph_max': 7.5,
                'temp_min': 20.0,
                'temp_max': 30.0,
                'moisture_req': 55.0,
                'nitrogen_req': 15.0,
                'phosphorus_req': 12.0,
                'potassium_req': 18.0,
                'notes': 'Drought resistant, good for intercropping'
            },
            {
                'crop_name': 'Rice',
                'season': 'Kharif',
                'duration_days': 120,
                'ph_min': 5.0,
                'ph_max': 8.0,
                'temp_min': 20.0,
                'temp_max': 35.0,
                'moisture_req': 90.0,
                'nitrogen_req': 35.0,
                'phosphorus_req': 20.0,
                'potassium_req': 30.0,
                'notes': 'Requires standing water, high yielding'
            },
            {
                'crop_name': 'Jowar (Sorghum)',
                'season': 'Kharif',
                'duration_days': 100,
                'ph_min': 6.0,
                'ph_max': 8.5,
                'temp_min': 25.0,
                'temp_max': 35.0,
                'moisture_req': 45.0,
                'nitrogen_req': 25.0,
                'phosphorus_req': 15.0,
                'potassium_req': 20.0,
                'notes': 'Drought tolerant, good for dry areas'
            },
            {
                'crop_name': 'Wheat',
                'season': 'Rabi',
                'duration_days': 120,
                'ph_min': 6.0,
                'ph_max': 7.5,
                'temp_min': 15.0,
                'temp_max': 25.0,
                'moisture_req': 50.0,
                'nitrogen_req': 30.0,
                'phosphorus_req': 20.0,
                'potassium_req': 25.0,
                'notes': 'Winter crop, requires cool climate'
            }
        ]
        
        for crop_data in crops_data:
            crop = Crop(**crop_data)
            db.session.add(crop)
        
        db.session.commit()
