from flask import Flask, request, jsonify
from pymongo import MongoClient

import datetime

app = Flask(__name__)

MONGO_URI = "mongodb+srv://pavan-kumar-2812:Venkat123@email-marketing-db.jihmhxe.mongodb.net/?retryWrites=true&w=majority&appName=email-marketing-db"
client = MongoClient(MONGO_URI)
db = client.email_marketing_db

@app.route('/')
def home():
    return "Marketing Email Backend is running"

@app.route('/api/subscribers', methods=['POST'])
def add_subscriber():
    data = request.json
    email = data.get('email')
    name = data.get('name', '')
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    # Check if subscriber exists
    if db.subscribers.find_one({'email': email}):
        return jsonify({'error': 'Subscriber already exists'}), 400
    
    db.subscribers.insert_one({'email': email,
                               'name': name,
                               'subscribed': True})
    return jsonify({'message': 'Subscriber added successfully'}), 201

@app.route('/api/campaigns', methods=['POST'])
def create_campaign():
    data = request.json
    name = data.get('name')
    subject = data.get('subject')
    content = data.get('content')

    if not all([name, subject, content]):
        return jsonify({'error': 'Name, subject and content are required'}), 400

    campaign = {
        'name': name,
        'subject': subject,
        'content': content,
        'created_at': datetime.utcnow(),
        'status': 'draft'  # status can be draft, sending, sent
    }

    result = db.campaigns.insert_one(campaign)
    return jsonify({'message': 'Campaign created', 'campaign_id': str(result.inserted_id)}), 201

if __name__ == "__main__":
    app.run(debug=True)