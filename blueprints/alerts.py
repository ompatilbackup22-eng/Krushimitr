from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from models import Alert, Recommendation, Crop, Farmer, db
from datetime import datetime, timedelta
from functools import wraps

alerts_bp = Blueprint('alerts', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'farmer_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@alerts_bp.route('/alerts')
@login_required
def index():
    farmer_id = session['farmer_id']
    alerts = Alert.query.filter_by(farmer_id=farmer_id).order_by(Alert.alert_date.asc()).all()
    return render_template('alerts/index.html', alerts=alerts)

@alerts_bp.route('/alerts/generate')
@login_required
def generate_alerts():
    farmer_id = session['farmer_id']
    
    # Get active recommendations
    recommendations = Recommendation.query.filter_by(farmer_id=farmer_id).all()
    
    alerts_created = 0
    
    for rec in recommendations:
        crop = rec.crop
        start_date = rec.recommended_date
        
        # Generate irrigation alerts (every 7 days for first month, then every 10 days)
        for i in range(1, crop.duration_days // 7 + 1):
            if i <= 4:  # First month
                alert_date = start_date + timedelta(days=i*7)
            else:  # After first month
                alert_date = start_date + timedelta(days=i*10)
            
            if alert_date > datetime.now():  # Only future alerts
                existing_alert = Alert.query.filter_by(
                    farmer_id=farmer_id,
                    crop_id=crop.id,
                    alert_type='irrigation',
                    alert_date=alert_date
                ).first()
                
                if not existing_alert:
                    alert = Alert(
                        farmer_id=farmer_id,
                        crop_id=crop.id,
                        alert_type='irrigation',
                        alert_date=alert_date,
                        message=f'Time to irrigate {crop.crop_name} plants'
                    )
                    db.session.add(alert)
                    alerts_created += 1
        
        # Generate fertilizer alerts
        fertilizer_dates = [
            (15, 'nitrogen', 'Apply nitrogen fertilizer'),
            (30, 'phosphorus', 'Apply phosphorus fertilizer'),
            (45, 'potassium', 'Apply potassium fertilizer'),
            (60, 'balanced', 'Apply balanced NPK fertilizer')
        ]
        
        for days, fert_type, message in fertilizer_dates:
            if days < crop.duration_days:
                alert_date = start_date + timedelta(days=days)
                
                if alert_date > datetime.now():  # Only future alerts
                    existing_alert = Alert.query.filter_by(
                        farmer_id=farmer_id,
                        crop_id=crop.id,
                        alert_type='fertilizer',
                        alert_date=alert_date
                    ).first()
                    
                    if not existing_alert:
                        alert = Alert(
                            farmer_id=farmer_id,
                            crop_id=crop.id,
                            alert_type='fertilizer',
                            alert_date=alert_date,
                            message=f'{message} for {crop.crop_name}'
                        )
                        db.session.add(alert)
                        alerts_created += 1
        
        # Generate spray alerts
        spray_dates = [20, 40, 60, 80]
        for days in spray_dates:
            if days < crop.duration_days:
                alert_date = start_date + timedelta(days=days)
                
                if alert_date > datetime.now():  # Only future alerts
                    existing_alert = Alert.query.filter_by(
                        farmer_id=farmer_id,
                        crop_id=crop.id,
                        alert_type='spray',
                        alert_date=alert_date
                    ).first()
                    
                    if not existing_alert:
                        alert = Alert(
                            farmer_id=farmer_id,
                            crop_id=crop.id,
                            alert_type='spray',
                            alert_date=alert_date,
                            message=f'Apply pest/disease control spray for {crop.crop_name}'
                        )
                        db.session.add(alert)
                        alerts_created += 1
        
        # Generate harvest alert
        harvest_date = start_date + timedelta(days=crop.duration_days)
        if harvest_date > datetime.now():  # Only future alerts
            existing_alert = Alert.query.filter_by(
                farmer_id=farmer_id,
                crop_id=crop.id,
                alert_type='harvest',
                alert_date=harvest_date
            ).first()
            
            if not existing_alert:
                alert = Alert(
                    farmer_id=farmer_id,
                    crop_id=crop.id,
                    alert_type='harvest',
                    alert_date=harvest_date,
                    message=f'Time to harvest {crop.crop_name}'
                )
                db.session.add(alert)
                alerts_created += 1
    
    db.session.commit()
    
    if alerts_created > 0:
        flash(f'{alerts_created} new alerts generated successfully!', 'success')
    else:
        flash('No new alerts to generate.', 'info')
    
    return redirect(url_for('alerts.index'))

@alerts_bp.route('/alerts/<int:alert_id>/complete', methods=['POST'])
@login_required
def complete_alert(alert_id):
    farmer_id = session['farmer_id']
    alert = Alert.query.filter_by(id=alert_id, farmer_id=farmer_id).first()
    
    if alert:
        alert.status = 'completed'
        db.session.commit()
        flash('Alert marked as completed!', 'success')
    else:
        flash('Alert not found!', 'error')
    
    return redirect(url_for('alerts.index'))

@alerts_bp.route('/alerts/<int:alert_id>/dismiss', methods=['POST'])
@login_required
def dismiss_alert(alert_id):
    farmer_id = session['farmer_id']
    alert = Alert.query.filter_by(id=alert_id, farmer_id=farmer_id).first()
    
    if alert:
        alert.status = 'dismissed'
        db.session.commit()
        flash('Alert dismissed!', 'info')
    else:
        flash('Alert not found!', 'error')
    
    return redirect(url_for('alerts.index'))

@alerts_bp.route('/alerts/<int:alert_id>/delete', methods=['POST'])
@login_required
def delete_alert(alert_id):
    farmer_id = session['farmer_id']
    alert = Alert.query.filter_by(id=alert_id, farmer_id=farmer_id).first()
    
    if alert:
        db.session.delete(alert)
        db.session.commit()
        flash('Alert deleted successfully!', 'success')
    else:
        flash('Alert not found!', 'error')
    
    return redirect(url_for('alerts.index'))

@alerts_bp.route('/alerts/upcoming')
@login_required
def upcoming():
    farmer_id = session['farmer_id']
    
    # Get alerts for next 7 days
    next_week = datetime.now() + timedelta(days=7)
    upcoming_alerts = Alert.query.filter(
        Alert.farmer_id == farmer_id,
        Alert.alert_date <= next_week,
        Alert.alert_date >= datetime.now(),
        Alert.status == 'pending'
    ).order_by(Alert.alert_date.asc()).all()
    
    return render_template('alerts/upcoming.html', upcoming_alerts=upcoming_alerts, current_date=datetime.now().date())
