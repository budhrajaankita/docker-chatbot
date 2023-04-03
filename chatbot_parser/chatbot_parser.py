# -*- coding: utf-8 -*-

from http import server
from flask import Flask, jsonify, request
import os, json
import requests
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@postgres_container:5432/chatbot"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.errorhandler(404)
def page_not_found(e):
    return "This route doesn't exist! {}".format(e)


class commands(db.Model):
    command = db.Column(db.String(20), primary_key=True)
    server_url = db.Column(db.String(200))

    def to_dict(self):
        return {
            'command': self.command,
            'server_url': self.server_url,
        }


#Post Endpoint to take data json as input and return data json output
@app.route('/message', methods=['POST'])
def handle_message():
    try:
        req = request.get_json()
        msg = req['data']['message']

        if not msg:
            return jsonify({'error': 'No JSON data provided'}), 400
        if str(msg).startswith("/"):
            cmd, _, new_msg = msg.partition(' ')
            if cmd == "/" or new_msg == "":
                return jsonify({'error': 'Incorrect format for command'}), 400
            else:
                resp = {"data": {"command": cmd[1:], "message": new_msg}}
                stmt = text("SELECT server_url FROM commands WHERE command = :x")
                stmt = stmt.bindparams(x=cmd[1:])
                url = db.session.execute(stmt).all()
                if not url:
                     return jsonify(resp)
                else:
                    response = requests.post(url[0][0] + '/execute', json=resp)
                    return response.json()
        else:
            resp = {'command': None, 'message': msg}
        
        return jsonify({"data": resp})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/register', methods=['POST'])
def register_server():
    try:
        req = request.get_json()
        cmd = req['data']['command']
        url = req['data']['server_url']

        if not url:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        q = commands.query.filter_by(command=cmd).filter_by(server_url=url).first()
        q2 = commands.query.filter_by(command=cmd).first()
        if q:
            return "", 400
        elif q2:
            new_command = commands(command=cmd, server_url = url)
            commands.query.filter_by(command=cmd).update({'server_url': url})
            try:
                db.session.commit()
                #return jsonify(new_command.to_dict()), 201
            except IntegrityError as e:
                db.session.rollback()
                return "", 400
        else:
            new_command = commands(command=cmd, server_url=url)
            db.session.add(new_command)
            try:
                db.session.commit()
                #return jsonify(new_command.to_dict()), 201
            except IntegrityError as e:
                db.session.rollback()
                return "", 400

        resp = {'command': cmd, 'message': 'saved' }
        return jsonify({"data": resp})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(port=5050, host='0.0.0.0',debug=True)