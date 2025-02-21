from flask import Blueprint, jsonify, request
from app.models import Color, db
from dotenv import load_dotenv
import os
import requests

# Loading my enviorment variables from my .env
load_dotenv()

colors_routes = Blueprint('colors', __name__, url_prefix='/api/colors')

@colors_routes.route('', methods=['GET'])
def get_colors():
    """
    Get all available colors.
    """
    try:
        colors = Color.query.all()
        colors_list = [color.to_dict() for color in colors]
        return jsonify({"colors": colors_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@colors_routes.route('/new', methods=['POST'])
def create_color():
    """
    Create a new color.
    """
    try:
        data = request.get_json()  # Parse incoming JSON
        color_name = data.get('name')

        if not color_name:
            return jsonify({"error": "Color name is required"}), 400

        # Check if the color already exists
        existing_color = Color.query.filter_by(name=color_name).first()
        if existing_color:
            return jsonify({"error": "Color already exists"}), 400

        # Create the new color
        new_color = Color(name=color_name)
        db.session.add(new_color)
        db.session.commit()

        return jsonify(new_color.to_dict()), 201  # Return the new color
    except Exception as e:
        return jsonify({"error": str(e)}), 500