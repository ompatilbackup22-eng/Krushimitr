from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from models import SoilData, Farmer, db
from datetime import datetime
from functools import wraps

soil_bp = Blueprint('soil', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'farmer_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@soil_bp.route('/soil')
@login_required
def index():
    farmer_id = session['farmer_id']
    
    try:
        soil_data = SoilData.query.filter_by(farmer_id=farmer_id).order_by(SoilData.date.desc()).all()
        return render_template('soil/index.html', soil_data=soil_data)
    except Exception as e:
        flash('An error occurred while retrieving soil data. Please try again.', 'error')
        return render_template('soil/index.html', soil_data=[])

@soil_bp.route('/soil/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        farmer_id = session['farmer_id']
        
        try:
            ph = float(request.form['ph'])
            moisture = float(request.form['moisture'])
            nitrogen = float(request.form['nitrogen'])
            phosphorus = float(request.form['phosphorus'])
            potassium = float(request.form['potassium'])
            temperature = float(request.form['temperature'])
            soil_type = request.form['soil_type']
            
            # Validation
            if not (0 <= ph <= 14):
                flash('pH value must be between 0 and 14!', 'error')
                return render_template('soil/add.html')
            
            if not (0 <= moisture <= 100):
                flash('Moisture level must be between 0 and 100%!', 'error')
                return render_template('soil/add.html')
            
            if not (0 <= nitrogen <= 1000):
                flash('Nitrogen level must be between 0 and 1000 ppm!', 'error')
                return render_template('soil/add.html')
            
            if not (0 <= phosphorus <= 1000):
                flash('Phosphorus level must be between 0 and 1000 ppm!', 'error')
                return render_template('soil/add.html')
            
            if not (0 <= potassium <= 1000):
                flash('Potassium level must be between 0 and 1000 ppm!', 'error')
                return render_template('soil/add.html')
            
            if not (-10 <= temperature <= 50):
                flash('Temperature must be between -10°C and 50°C!', 'error')
                return render_template('soil/add.html')
            
            if not soil_type or soil_type.strip() == '':
                flash('Please select a soil type!', 'error')
                return render_template('soil/add.html')
            
            # Create soil data record
            soil_data = SoilData(
                farmer_id=farmer_id,
                ph=ph,
                moisture=moisture,
                nitrogen=nitrogen,
                phosphorus=phosphorus,
                potassium=potassium,
                temperature=temperature,
                soil_type=soil_type
            )
            
            db.session.add(soil_data)
            db.session.commit()
            
            flash('Soil data added successfully!', 'success')
            return redirect(url_for('soil.index'))
            
        except ValueError:
            flash('Please enter valid numeric values!', 'error')
            return render_template('soil/add.html')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while saving soil data. Please try again.', 'error')
            return render_template('soil/add.html')
    
    # Handle GET request - show the form
    return render_template('soil/add.html')
            

@soil_bp.route('/soil/<int:soil_id>')
@login_required
def view(soil_id):
    farmer_id = session['farmer_id']
    
    try:
        soil_data = SoilData.query.filter_by(id=soil_id, farmer_id=farmer_id).first()
        
        if not soil_data:
            flash('Soil data not found!', 'error')
            return redirect(url_for('soil.index'))
        
        return render_template('soil/view.html', soil_data=soil_data)
    except Exception as e:
        flash('An error occurred while retrieving soil data. Please try again.', 'error')
        return redirect(url_for('soil.index'))

@soil_bp.route('/soil/<int:soil_id>/delete', methods=['POST'])
@login_required
def delete(soil_id):
    farmer_id = session['farmer_id']
    soil_data = SoilData.query.filter_by(id=soil_id, farmer_id=farmer_id).first()
    
    if soil_data:
        try:
            db.session.delete(soil_data)
            db.session.commit()
            flash('Soil data deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while deleting soil data. Please try again.', 'error')
    else:
        flash('Soil data not found!', 'error')
    
    return redirect(url_for('soil.index'))

@soil_bp.route('/soil/analysis')
@login_required
def analysis():
    farmer_id = session['farmer_id']
    
    try:
        latest_soil = SoilData.query.filter_by(farmer_id=farmer_id).order_by(SoilData.date.desc()).first()
        
        if not latest_soil:
            flash('No soil data available for analysis!', 'error')
            return redirect(url_for('soil.index'))
    except Exception as e:
        flash('An error occurred while retrieving soil data. Please try again.', 'error')
        return redirect(url_for('soil.index'))
    
    # Basic soil analysis
    try:
        analysis_results = {
            'ph_status': 'Optimal' if 6.0 <= latest_soil.ph <= 7.5 else 'Needs attention',
            'moisture_status': 'Adequate' if latest_soil.moisture >= 50 else 'Low',
            'nitrogen_status': 'Sufficient' if latest_soil.nitrogen >= 20 else 'Deficient',
            'phosphorus_status': 'Sufficient' if latest_soil.phosphorus >= 15 else 'Deficient',
            'potassium_status': 'Sufficient' if latest_soil.potassium >= 20 else 'Deficient',
            'recommendations': []
        }
    except Exception as e:
        flash('An error occurred while analyzing soil data. Please try again.', 'error')
        return redirect(url_for('soil.index'))
    
    # Generate recommendations
    try:
        if latest_soil.ph < 6.0:
            analysis_results['recommendations'].append('Add lime to increase pH')
        elif latest_soil.ph > 7.5:
            analysis_results['recommendations'].append('Add sulfur to decrease pH')
        
        if latest_soil.moisture < 50:
            analysis_results['recommendations'].append('Increase irrigation frequency')
        
        if latest_soil.nitrogen < 20:
            analysis_results['recommendations'].append('Apply nitrogen-rich fertilizer')
        
        if latest_soil.phosphorus < 15:
            analysis_results['recommendations'].append('Apply phosphorus-rich fertilizer')
        
        if latest_soil.potassium < 20:
            analysis_results['recommendations'].append('Apply potassium-rich fertilizer')
        
        return render_template('soil/analysis.html', soil_data=latest_soil, analysis=analysis_results)
    except Exception as e:
        flash('An error occurred while generating recommendations. Please try again.', 'error')
        return redirect(url_for('soil.index'))
