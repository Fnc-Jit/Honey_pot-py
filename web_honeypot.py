#liabary    
import logging
import logging.handlers
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, redirect, url_for, flash

# Logging setup
logging_format = logging.Formatter('%(asctime)s - %(name)s - %(message)s')

#http loger
funnel_logger=logging.getLogger('HTTP_logger')
funnel_logger.setLevel(logging.INFO)
funnel_handler = RotatingFileHandler('http_audit.log', maxBytes=2000, backupCount=5)
funnel_handler.setFormatter(logging_format)
funnel_logger.addHandler(funnel_handler)


#baselie honeypot

def web_honey_pot(input_username='admin', input_password='password'):
    
    app = Flask(__name__)

    @app.route('/')

    def index():
        return render_template('wp-admin.html')
    
    @app.route('/wp-admin-login', methods=['POST'])

    def login():
        username = request.form['log']      # Changed from 'username' to 'log'
        password = request.form['pwd']      # Changed from 'password' to 'pwd'

        ip_address = request.remote_addr

        funnel_logger.info(f'Login attempt from {ip_address} with username: {username}, password: {password}')

        if username == input_username and password == input_password:
            return 'Login successful!'
        
        else:
            return 'Login failed!'
        
    return app    

def run_web_honey_pot(port=5000, input_username='admin', input_password='password'):
    run_web_honey_pot_app = web_honey_pot(input_username, input_password)
    run_web_honey_pot_app.run(debug=True,port=port,host='0.0.0.0')

    return run_web_honey_pot_app

