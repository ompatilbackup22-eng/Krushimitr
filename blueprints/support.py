from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models import Query, Farmer, db
from datetime import datetime
from functools import wraps

support_bp = Blueprint('support', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'farmer_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@support_bp.route('/support')
@login_required
def index():
    farmer_id = session['farmer_id']
    queries = Query.query.filter_by(farmer_id=farmer_id).order_by(Query.created_at.desc()).all()
    return render_template('support/index.html', queries=queries)

@support_bp.route('/support/ask', methods=['GET', 'POST'])
@login_required
def ask():
    if request.method == 'POST':
        farmer_id = session['farmer_id']
        question = request.form['question']
        
        if not question.strip():
            flash('Please enter your question!', 'error')
            return render_template('support/ask.html')
        
        # Create new query
        query = Query(
            farmer_id=farmer_id,
            question=question
        )
        
        db.session.add(query)
        db.session.commit()
        
        flash('Your question has been submitted successfully! Our experts will respond within 24-48 hours.', 'success')
        return redirect(url_for('support.index'))
    
    return render_template('support/ask.html')

@support_bp.route('/support/query/<int:query_id>')
@login_required
def view_query(query_id):
    farmer_id = session['farmer_id']
    query = Query.query.filter_by(id=query_id, farmer_id=farmer_id).first()
    
    if not query:
        flash('Query not found!', 'error')
        return redirect(url_for('support.index'))
    
    return render_template('support/view_query.html', query=query)

@support_bp.route('/support/faq')
@login_required
def faq():
    faqs = [
        {
            'question': 'How often should I test my soil?',
            'answer': 'It is recommended to test your soil at least once a year, preferably before the planting season. For intensive farming, testing every 6 months is ideal.'
        },
        {
            'question': 'What is the best time to apply fertilizers?',
            'answer': 'The best time to apply fertilizers depends on the crop and soil conditions. Generally, fertilizers should be applied during the active growing season when plants can absorb nutrients effectively.'
        },
        {
            'question': 'How can I improve soil moisture retention?',
            'answer': 'You can improve soil moisture retention by adding organic matter (compost, manure), using mulch, practicing crop rotation, and implementing proper irrigation techniques.'
        },
        {
            'question': 'What crops are suitable for my region?',
            'answer': 'Crop suitability depends on soil type, climate, and water availability. Use our crop recommendation system by entering your soil and weather data to get personalized suggestions.'
        },
        {
            'question': 'How do I identify nutrient deficiencies in plants?',
            'answer': 'Nutrient deficiencies can be identified by observing plant symptoms like yellowing leaves (nitrogen deficiency), stunted growth (phosphorus deficiency), or brown leaf edges (potassium deficiency).'
        },
        {
            'question': 'What is the ideal pH range for most crops?',
            'answer': 'Most crops grow best in soil with a pH range of 6.0 to 7.5. However, some crops like blueberries prefer acidic soil (pH 4.5-5.5) while others like asparagus prefer slightly alkaline soil (pH 7.0-8.0).'
        },
        {
            'question': 'How can I reduce water usage in farming?',
            'answer': 'You can reduce water usage by implementing drip irrigation, using drought-resistant crop varieties, practicing mulching, and scheduling irrigation based on soil moisture levels.'
        },
        {
            'question': 'What are the benefits of crop rotation?',
            'answer': 'Crop rotation helps maintain soil fertility, reduces pest and disease problems, improves soil structure, and can increase overall crop yields over time.'
        }
    ]
    
    return render_template('support/faq.html', faqs=faqs)

@support_bp.route('/support/contact')
@login_required
def contact():
    return render_template('support/contact.html')
