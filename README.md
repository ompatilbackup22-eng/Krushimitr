# KrishiMitra: Agriband - Smart Farming Decision Support System

A comprehensive web application built with Flask that helps farmers make informed decisions about crop selection, soil management, and farming practices.

**Founded by:** Kapse Shraddha & More Harshad

## Features

### 🌱 Core Features
- **Farmer Registration & Authentication**: Secure farmer profiles with location details
- **Soil Data Management**: Comprehensive soil testing and analysis
- **Weather Monitoring**: Real-time weather data integration and manual entry
- **Crop Recommendations**: AI-powered crop suggestions based on soil and weather conditions
- **Crop Calendar**: Detailed farming schedules with stage-wise activities
- **Smart Alerts**: Timely reminders for irrigation, fertilization, and pest control
- **Educational Videos**: Best Management Practices (BMP) tutorial videos
- **Expert Support**: Query submission system for agricultural experts
- **PDF Reports**: Comprehensive farming reports generation

### 🎯 Supported Crops
- Soybean, Cotton, Sugarcane, Moong, Tur (Pigeon Pea)
- Rice, Jowar (Sorghum), Wheat
- Support for Kharif, Rabi, and Summer seasons

### 📊 Soil Analysis
- pH level monitoring
- Moisture content analysis
- NPK (Nitrogen, Phosphorus, Potassium) levels
- Soil temperature and type classification

### 🌤️ Weather Integration
- Temperature, humidity, and rainfall tracking
- Weather forecast integration (OpenWeather API ready)
- Manual weather data entry

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (expandable to PostgreSQL/MySQL)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **PDF Generation**: ReportLab
- **Weather API**: OpenWeather API (configurable)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Soil_detection
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your browser and go to `http://localhost:5000`
   - Register as a new farmer or login with existing credentials

## Project Structure

```
Soil_detection/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── blueprints/           # Flask blueprints
│   ├── auth.py          # Authentication
│   ├── dashboard.py     # Farmer dashboard
│   ├── soil.py          # Soil data management
│   ├── weather.py       # Weather data management
│   ├── crops.py         # Crop recommendations
│   ├── alerts.py        # Alerts and notifications
│   ├── videos.py        # Video platform
│   ├── support.py       # Expert support
│   └── reports.py       # Report generation
├── templates/           # HTML templates
│   ├── base.html       # Base template
│   ├── index.html      # Homepage
│   ├── about.html      # About page
│   ├── auth/           # Authentication templates
│   ├── dashboard/      # Dashboard templates
│   ├── soil/           # Soil management templates
│   ├── weather/        # Weather templates
│   ├── crops/          # Crop templates
│   ├── alerts/         # Alert templates
│   ├── videos/         # Video templates
│   ├── support/        # Support templates
│   └── reports/        # Report templates
└── static/             # Static files
    ├── css/           # Stylesheets
    ├── js/            # JavaScript files
    └── images/        # Images
```

## Database Schema

### Core Tables
- **farmers**: Farmer profiles and authentication
- **soil_data**: Soil test results and analysis
- **weather_data**: Weather conditions and forecasts
- **crops**: Crop knowledge base with requirements
- **recommendations**: Crop recommendations for farmers
- **alerts**: Farming schedule alerts and reminders
- **videos**: Educational video content
- **queries**: Expert support queries

## Usage Guide

### 1. Registration & Login
- Register with your personal and location details
- Login with mobile number and password

### 2. Soil Data Entry
- Add soil test results (pH, moisture, NPK levels)
- View soil analysis and recommendations
- Track soil data history

### 3. Weather Data
- Fetch weather data automatically (API integration)
- Add weather data manually
- View weather forecasts and trends

### 4. Crop Recommendations
- Get personalized crop suggestions based on soil and weather
- View crop compatibility scores
- Access detailed crop information

### 5. Crop Calendar
- Generate farming schedules for recommended crops
- View irrigation, fertilization, and harvest timelines
- Set up automated alerts

### 6. Alerts & Notifications
- Receive timely reminders for farming activities
- Mark alerts as completed or dismissed
- View upcoming farming tasks

### 7. Educational Resources
- Watch BMP tutorial videos
- Browse videos by category
- Search for specific topics

### 8. Expert Support
- Submit questions to agricultural experts
- View FAQ section
- Track query status

### 9. Reports
- Generate comprehensive PDF reports
- View soil and weather data history
- Export farming data

## Configuration

### Environment Variables
- `OPENWEATHER_API_KEY`: Your OpenWeather API key for weather data
- `SECRET_KEY`: Flask secret key for session management

### Database Configuration
- Default: SQLite (`sqlite:///krishimitra.db`)
- Can be changed to PostgreSQL or MySQL in `app.py`

## API Integration

### OpenWeather API
To enable automatic weather data fetching:
1. Get an API key from [OpenWeather](https://openweathermap.org/api)
2. Set the `OPENWEATHER_API_KEY` environment variable
3. Update the weather fetching logic in `blueprints/weather.py`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Founders

**Kapse Shraddha** - Co-Founder & CEO
- Visionary leader driving innovation in agricultural technology and farmer empowerment
- Passionate about sustainable farming and rural development

**More Harshad** - Co-Founder & CTO  
- Technical architect behind the smart farming platform and data-driven solutions
- Expert in developing scalable agricultural technology solutions

## Support

For support and questions:
- Email: support@krishimitra.com
- Phone: +91-XXX-XXX-XXXX

## Future Enhancements

- [ ] Machine Learning for soil type detection from images
- [ ] SMS/Email alert notifications
- [ ] Mobile app development
- [ ] Advanced analytics and insights
- [ ] Integration with IoT sensors
- [ ] Multi-language support
- [ ] Advanced weather forecasting
- [ ] Market price integration

---

**KrishiMitra: Agriband** - Empowering farmers with smart technology for sustainable and profitable farming practices.
