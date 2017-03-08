import os
from flask import Flask, request
from twilio.jwt.access_token import AccessToken, VoiceGrant
from twilio.rest import Client
import twilio.twiml

ACCOUNT_SID = 'AC07299af52325ae34215e065d329c23d8'
API_KEY = 'SKb6e9ab277bf4cb0560c5cb246579b61e'
API_KEY_SECRET = '0FYHleybCkdRvNkJyunO6yyW7rM8y7M6'
PUSH_CREDENTIAL_SID = 'CR0880392c004ab618f7b64a0cc5d63189'
APP_SID = 'APb6ef77259278b257ce7569b8297ac0b9'

IDENTITY = 'voice_test'
CALLER_ID = 'quick_start'

app = Flask(__name__)

@app.route('/accessToken')
def token():
  account_sid = os.environ.get("ACCOUNT_SID", ACCOUNT_SID)
  api_key = os.environ.get("API_KEY", API_KEY)
  api_key_secret = os.environ.get("API_KEY_SECRET", API_KEY_SECRET)
  push_credential_sid = os.environ.get("PUSH_CREDENTIAL_SID", PUSH_CREDENTIAL_SID)
  app_sid = os.environ.get("APP_SID", APP_SID)

  grant = VoiceGrant(
    push_credential_sid=push_credential_sid,
    outgoing_application_sid=app_sid
  )

  token = AccessToken(account_sid, api_key, api_key_secret, IDENTITY)
  token.add_grant(grant)

  return str(token)

@app.route('/outgoing', methods=['GET', 'POST'])
def outgoing():
  resp = twilio.twiml.Response()
  resp.say("Congratulations! You have made your first oubound call! Good bye.")
  return str(resp)

@app.route('/incoming', methods=['GET', 'POST'])
def incoming():
  resp = twilio.twiml.Response()
  resp.say("Congratulations! You have received your first inbound call! Good bye.")
  return str(resp)

@app.route('/placeCall', methods=['GET', 'POST'])
def placeCall():
  account_sid = os.environ.get("ACCOUNT_SID", ACCOUNT_SID)
  api_key = os.environ.get("API_KEY", API_KEY)
  api_key_secret = os.environ.get("API_KEY_SECRET", API_KEY_SECRET)

  client = Client(api_key, api_key_secret, account_sid)
  call = client.calls.create(url=request.url_root + 'incoming', to='client:' + IDENTITY, from_='client:' + CALLER_ID)
  return str(call.sid)

@app.route('/', methods=['GET', 'POST'])
def welcome():
  resp = twilio.twiml.Response()
  resp.say("Welcome to Twilio")
  return str(resp)

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port, debug=True)
