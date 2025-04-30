from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from extensions import mongo
from routes.auth import auth
from routes.predict import predict
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Configurations
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')  # Atlas URI from .env
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

# Initialize Extensions
mongo.init_app(app)
CORS(app, supports_credentials=True, origins=[
  "http://localhost:3000",
  "https://healthcare-cost-prediction-frontend.onrender.com"
])



jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(predict, url_prefix='/')

@app.route('/test_connection')
def test_connection():
    try:
        mongo.db.list_collection_names()  # Updated method for newer pymongo versions
        return "MongoDB Atlas Connection Successful", 200
    except Exception as e:
        return f"MongoDB Connection Failed: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
