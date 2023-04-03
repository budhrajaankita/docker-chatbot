from flask import Flask, jsonify, request

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return "This route doesn't exist! {}".format(e)

#Post Endpoint to execute data json as input and return data json output
@app.route('/execute', methods=['POST'])
def handle_message():
    try:
        req = request.get_json()
        cmd = req['data']['command']
        msg = req['data']['message']

        if not msg:
            return jsonify({'error': 'No data provided'}), 400
        if str(cmd).lower() == "shrug":
            new_msg = str(msg) +  "¯\_(ツ)_/¯"
            resp = {'command': cmd, 'message': new_msg}
        else:
            resp = {'command': cmd, 'message': msg}
        
        return jsonify({"data": resp})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(port=5051, host='0.0.0.0', debug=True)