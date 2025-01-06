from flask import Flask, request, jsonify
from rasa.core.agent import Agent
import os

app = Flask(__name__)

# Load the trained Rasa model
model_path = "Newchatbot\rasa_backend\models"  # Change this to where your model is stored
agent = Agent.load(model_path)

@app.route('/')
def hello():
    return 'Hello, Render!'

@app.route('/webhook', methods=['POST'])
def webhook():
    # Get the message from the user
    message = request.json.get('message')

    # Process the message through Rasa
    responses = agent.handle_text(message)
    return jsonify({"responses": responses})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render assigns the dynamic PORT
    app.run(host='0.0.0.0', port=port)
