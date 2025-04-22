#!/usr/bin/env python
"""
Run script for the College Cafeteria application.
This script provides a convenient way to start the application.
"""

from app import app

if __name__ == '__main__':
    print("Starting College Cafeteria application...")
    print("Visit http://127.0.0.1:5000/ in your web browser")
    app.run(debug=True, host='0.0.0.0', port=5000)