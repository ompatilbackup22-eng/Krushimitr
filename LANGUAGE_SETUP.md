# Multi-Language Support Setup

## Overview
KrishiMitra now supports multiple languages to make the platform accessible to farmers across India. Currently supported languages:
- English (en) - Default
- Hindi (hi) - हिन्दी
- Marathi (mr) - मराठी

## Features Added

### 1. Language Switcher
- Added a language dropdown in the navigation bar
- Users can switch between English, Hindi, and Marathi
- Language preference is saved in the session

### 2. Translation Support
- All navigation menus are translated
- Homepage content is fully translated
- Footer content is translated
- Error messages and flash messages support translation

### 3. Technical Implementation
- Flask-Babel for internationalization
- Translation files in `translations/` directory
- Automatic locale detection from session
- Fallback to English if translation is missing

## Files Modified

### Core Application
- `app.py` - Added Flask-Babel configuration and language switching routes
- `requirements.txt` - Added Flask-Babel dependency

### Templates
- `templates/base.html` - Added language switcher and translation support
- `templates/index.html` - Translated all homepage content

### Translation Files
- `translations/hi/LC_MESSAGES/messages.po` - Hindi translations
- `translations/mr/LC_MESSAGES/messages.po` - Marathi translations
- `babel.cfg` - Babel configuration file

## How to Use

### For Users
1. Click on the "Language" dropdown in the navigation bar
2. Select your preferred language (English/Hindi/Marathi)
3. The entire website will switch to the selected language
4. Your language preference will be remembered during the session

### For Developers

#### Adding New Translations
1. Add new text to the translation files:
   - `translations/hi/LC_MESSAGES/messages.po` for Hindi
   - `translations/mr/LC_MESSAGES/messages.po` for Marathi

2. Compile the translations:
   ```bash
   pybabel compile -d translations -D messages
   ```

#### Adding New Languages
1. Add the language to `app.config['LANGUAGES']` in `app.py`
2. Create a new translation directory: `translations/[lang_code]/LC_MESSAGES/`
3. Copy `messages.po` template and translate the content
4. Compile the translations

#### Using Translations in Templates
```html
<!-- Use the _() function for translations -->
<h1>{{ _('Welcome to KrishiMitra') }}</h1>
<p>{{ _('Smart farming made simple') }}</p>
```

#### Using Translations in Python Code
```python
from flask_babel import gettext

# In your route functions
message = gettext('Welcome to the dashboard')
flash(message, 'success')
```

## Installation

1. Install Flask-Babel:
   ```bash
   pip install Flask-Babel==4.0.0
   ```

2. Compile translation files:
   ```bash
   pybabel compile -d translations -D messages
   ```

3. Run the application:
   ```bash
   python app.py
   ```

## Translation Guidelines

### For Hindi Translations
- Use simple, commonly understood Hindi
- Avoid overly technical Sanskrit terms
- Use Devanagari script
- Keep sentences short and clear

### For Marathi Translations
- Use standard Marathi language
- Avoid regional dialects
- Use Devanagari script
- Maintain consistency with Hindi translations where possible

## Future Enhancements

1. **More Languages**: Add support for other Indian languages like Gujarati, Tamil, Telugu, etc.
2. **RTL Support**: Add right-to-left language support for Arabic/Urdu if needed
3. **Dynamic Translations**: Allow users to suggest translations or corrections
4. **Regional Variants**: Support different regional variants of the same language
5. **Voice Interface**: Add text-to-speech in local languages

## Testing

To test the language functionality:

1. Start the application
2. Visit the homepage
3. Use the language switcher to change languages
4. Verify that all text changes to the selected language
5. Check that the language preference persists across page navigation

## Troubleshooting

### Common Issues

1. **Translations not showing**: Make sure to compile the translation files
2. **Missing translations**: Check if the text is wrapped in `_()` function
3. **Language not switching**: Verify the session is working properly
4. **Encoding issues**: Ensure UTF-8 encoding for translation files

### Debug Mode
Set `BABEL_DEFAULT_LOCALE` to test a specific language:
```python
app.config['BABEL_DEFAULT_LOCALE'] = 'hi'  # Force Hindi
```

## Contributing

To contribute translations:

1. Fork the repository
2. Add/update translations in the appropriate `.po` files
3. Test the translations thoroughly
4. Submit a pull request with your changes

## Support

For issues related to language support, please contact the development team or create an issue in the project repository.
