from app import create_app
import os
from dotenv import load_dotenv

load_dotenv()

# Create the Flask app using the application factory
app = create_app()

if __name__ == '__main__':
    # Get port from environment variables or default to 5001
    port = int(os.environ.get("PORT", 5001))
    # debug=False is recommended for production
    app.run(host='0.0.0.0', port=port, debug=True)