from flask import Blueprint, render_template, request, flash, redirect, url_for, session, make_response
from models import Farmer, SoilData, WeatherData, Recommendation, Alert, Crop, db
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
from functools import wraps

reports_bp = Blueprint('reports', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'farmer_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@reports_bp.route('/reports')
@login_required
def index():
    farmer_id = session['farmer_id']
    farmer = Farmer.query.get(farmer_id)
    
    # Get data for report summary
    latest_soil = SoilData.query.filter_by(farmer_id=farmer_id).order_by(SoilData.date.desc()).first()
    latest_weather = WeatherData.query.filter_by(farmer_id=farmer_id).order_by(WeatherData.date.desc()).first()
    recommendations = Recommendation.query.filter_by(farmer_id=farmer_id).order_by(Recommendation.recommended_date.desc()).all()
    pending_alerts = Alert.query.filter_by(farmer_id=farmer_id, status='pending').order_by(Alert.alert_date.asc()).all()
    
    return render_template('reports/index.html', 
                         farmer=farmer,
                         latest_soil=latest_soil,
                         latest_weather=latest_weather,
                         recommendations=recommendations,
                         pending_alerts=pending_alerts)

@reports_bp.route('/reports/generate')
@login_required
def generate_report():
    farmer_id = session['farmer_id']
    farmer = Farmer.query.get(farmer_id)
    
    # Get all data for the report
    soil_data = SoilData.query.filter_by(farmer_id=farmer_id).order_by(SoilData.date.desc()).all()
    weather_data = WeatherData.query.filter_by(farmer_id=farmer_id).order_by(WeatherData.date.desc()).all()
    recommendations = Recommendation.query.filter_by(farmer_id=farmer_id).order_by(Recommendation.recommended_date.desc()).all()
    alerts = Alert.query.filter_by(farmer_id=farmer_id).order_by(Alert.alert_date.asc()).all()
    
    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    story.append(Paragraph("KrishiMitra: Agriband - Farmer Report", title_style))
    story.append(Spacer(1, 12))
    
    # Farmer Information
    story.append(Paragraph("Farmer Information", styles['Heading2']))
    farmer_info = [
        ['Name:', farmer.name],
        ['Mobile:', farmer.mobile],
        ['Village:', farmer.village],
        ['Tehsil:', farmer.tehsil],
        ['District:', farmer.district],
        ['Pincode:', farmer.pincode]
    ]
    
    farmer_table = Table(farmer_info, colWidths=[2*inch, 4*inch])
    farmer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(farmer_table)
    story.append(Spacer(1, 20))
    
    # Latest Soil Data
    if soil_data:
        story.append(Paragraph("Latest Soil Analysis", styles['Heading2']))
        latest_soil = soil_data[0]
        soil_info = [
            ['Parameter', 'Value', 'Unit'],
            ['pH Level', f"{latest_soil.ph:.2f}", ''],
            ['Moisture', f"{latest_soil.moisture:.2f}", '%'],
            ['Nitrogen', f"{latest_soil.nitrogen:.2f}", 'ppm'],
            ['Phosphorus', f"{latest_soil.phosphorus:.2f}", 'ppm'],
            ['Potassium', f"{latest_soil.potassium:.2f}", 'ppm'],
            ['Temperature', f"{latest_soil.temperature:.2f}", '°C'],
            ['Soil Type', latest_soil.soil_type, ''],
            ['Test Date', latest_soil.date.strftime('%Y-%m-%d'), '']
        ]
        
        soil_table = Table(soil_info, colWidths=[2*inch, 1.5*inch, 1*inch])
        soil_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(soil_table)
        story.append(Spacer(1, 20))
    
    # Latest Weather Data
    if weather_data:
        story.append(Paragraph("Latest Weather Data", styles['Heading2']))
        latest_weather = weather_data[0]
        weather_info = [
            ['Parameter', 'Value', 'Unit'],
            ['Temperature', f"{latest_weather.temperature:.2f}", '°C'],
            ['Humidity', f"{latest_weather.humidity:.2f}", '%'],
            ['Rainfall', f"{latest_weather.rainfall:.2f}", 'mm'],
            ['Date', latest_weather.date.strftime('%Y-%m-%d'), '']
        ]
        
        weather_table = Table(weather_info, colWidths=[2*inch, 1.5*inch, 1*inch])
        weather_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(weather_table)
        story.append(Spacer(1, 20))
    
    # Crop Recommendations
    if recommendations:
        story.append(Paragraph("Crop Recommendations", styles['Heading2']))
        rec_data = [['Crop Name', 'Season', 'Confidence Score', 'Recommended Date']]
        
        for rec in recommendations:
            rec_data.append([
                rec.crop.crop_name,
                rec.crop.season,
                f"{rec.confidence_score:.1f}%",
                rec.recommended_date.strftime('%Y-%m-%d')
            ])
        
        rec_table = Table(rec_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        rec_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(rec_table)
        story.append(Spacer(1, 20))
    
    # Upcoming Alerts
    if alerts:
        story.append(Paragraph("Upcoming Alerts", styles['Heading2']))
        alert_data = [['Alert Type', 'Crop', 'Date', 'Message']]
        
        for alert in alerts[:10]:  # Show only first 10 alerts
            alert_data.append([
                alert.alert_type.title(),
                alert.crop.crop_name,
                alert.alert_date.strftime('%Y-%m-%d'),
                alert.message[:50] + '...' if len(alert.message) > 50 else alert.message
            ])
        
        alert_table = Table(alert_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 2.5*inch])
        alert_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(alert_table)
        story.append(Spacer(1, 20))
    
    # Footer
    story.append(Paragraph(f"Report Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Paragraph("KrishiMitra: Agriband - Smart Farming Decision Support System", styles['Normal']))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    
    # Create response
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=farmer_report_{farmer.name}_{datetime.now().strftime("%Y%m%d")}.pdf'
    
    return response

@reports_bp.route('/reports/soil-history')
@login_required
def soil_history():
    farmer_id = session['farmer_id']
    soil_data = SoilData.query.filter_by(farmer_id=farmer_id).order_by(SoilData.date.desc()).all()
    return render_template('reports/soil_history.html', soil_data=soil_data)

@reports_bp.route('/reports/weather-history')
@login_required
def weather_history():
    farmer_id = session['farmer_id']
    weather_data = WeatherData.query.filter_by(farmer_id=farmer_id).order_by(WeatherData.date.desc()).all()
    return render_template('reports/weather_history.html', weather_data=weather_data)
