import os
from app import app as flask_app

# Make the app variable available for Gunicorn
app = flask_app

if __name__ == '__main__':
    # Run the app when the program is run directly
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
