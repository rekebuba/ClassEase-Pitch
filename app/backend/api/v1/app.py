#!/usr/bin/python3
"""Main module for the API"""

from api import create_app

app = create_app('development')

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    
    error = False
    while True:
        try:
            app.run(host=host, port=port, debug=True)
        except Exception as e:
            if error == False:
                print(f"Error occurred: {e}")
                error = True
            else:
                print("Error occurred again. Exiting...")
                break
