#!/usr/bin/env python3
"""
Minocrisy AI Tools - Main Application
A Flask-based web application for AI tools like Talking Head and Hype Remover.
"""
import os
from flask import Flask, render_template, jsonify
from flask_cors import CORS
from app import create_app

if __name__ == "__main__":
    # Create the Flask application
    app = create_app()
    
    # Get port from environment variable (for Google Cloud App Engine)
    port = int(os.environ.get("PORT", 8080))
    
    # Run the application
    app.run(host="0.0.0.0", port=port, debug=True)
