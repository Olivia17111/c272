import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'ACddcf12c0578e41f662ecb67fd85b1370'
    TWILIO_SYNC_SERVICE_SID = 'IS2d3bb7c97d50c8575e7d32030a3176d6' 
    TWILIO_API_KEY = 'SK3ed807097331113fbe09e9543b8496d3' 
    TWILIO_API_SECRET = 'bmnHfJ5iXSwKFXTj3SDVXM8o8ZxPiAwS' 

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():
    text_from_notepad = request.form['text']
    with open('workfile.txt', 'w') as f:
        f.write(text_from_notepad)

    path_to_store_txt = "workfile.txt"

    return send_file(path_to_store_txt, as_attachment= True)    

if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
