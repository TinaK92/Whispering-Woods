from flask import Blueprint, jsonify
from app.models import Size
from dotenv import load_dotenv
import os
import requests
import logging

logging.basicConfig(level=logging.DEBUG)

# Loading my enviorment variables from my .env
load_dotenv()

sizes_routes = Blueprint("sizes", __name__, url_prefix="/api/sizes")


@sizes_routes.route("", methods=["GET"])
def get_sizes():
    """
    Get all available sizes.
    """
    try:
        sizes = Size.query.all()
        logging.debug(f"Sizes fetched: {sizes}")
        sizes_list = [size.to_dict() for size in sizes]
        return jsonify({"sizes": sizes_list}), 200
    except Exception as e:
        logging.error(f"Error fetching sizes: {str(e)}")
        return jsonify({"error": str(e)}), 500
