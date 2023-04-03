from flask import Flask, jsonify, request
import json
import os
import sendgrid
from sendgrid.helpers.mail import Mail
import redis
from worker import send_email

app = Flask(__name__)

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")


#redis_client = redis.Redis(host='redis_container', port=6379)


@app.route('/execute', methods=['POST'])
def execute():
    try:
        response_code = 400
        data = request.json['data']
        
        if "command" not in data or not data["command"]:
            return "", response_code
        if "message" not in data or not data["message"]:
            return "", response_code

        cmd = data["command"]
        msg = data["message"]

        from_email = "***"
        email =  msg.split()[0]
        subject = msg.split()[1]
        body = ' '.join(msg.split()[2:])

        if email and subject and body:
            #sg = sendgrid.SendGridAPIClient(api_key=API_key)
            #content = Mail(from_email=from_email, to_emails=email, subject=subject, html_content=body)
            #sg.send(content)
            
            #resp = { "data": { 'command': cmd, 'message': 'Email was sent' }}
            send_email.delay(from_email, email, subject, body)
            resp = { "data": { 'command': cmd, 'message': 'Email was queued' }}
            response_code = 200
        else:
            resp = { "data": { 'command': cmd, 'message': 'Email was not queued' }}
            #response_code = 200
           
        #else:
        #    resp = { "data": { 'command': cmd, 'message': 'Email was not sent' }}
        return jsonify(resp), response_code
    except Exception as e:
        return str(e), 400


if __name__ == '__main__':
    app.run(port=5052, host='0.0.0.0',debug=True)