from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import Farmer, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        village = request.form['village']
        tehsil = request.form['tehsil']
        district = request.form['district']
        pincode = request.form['pincode']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('auth/register.html')
        
        if Farmer.query.filter_by(mobile=mobile).first():
            flash('Mobile number already registered!', 'error')
            return render_template('auth/register.html')
        
        # Create new farmer
        farmer = Farmer(
            name=name,
            mobile=mobile,
            village=village,
            tehsil=tehsil,
            district=district,
            pincode=pincode,
            password_hash=generate_password_hash(password)
        )
        
        db.session.add(farmer)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mobile = request.form['mobile']
        password = request.form['password']
        
        farmer = Farmer.query.filter_by(mobile=mobile).first()
        
        if farmer and check_password_hash(farmer.password_hash, password):
            session['farmer_id'] = farmer.id
            session['farmer_name'] = farmer.name
            flash(f'Welcome back, {farmer.name}!', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid mobile number or password!', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))
