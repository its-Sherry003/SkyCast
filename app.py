from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
import os

app = Flask(__name__)

# Database config from environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:password@localhost/weatherdb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ── Model ──────────────────────────────────────────────────────────────────────
class SearchHistory(db.Model):
    __tablename__ = 'search_history'
    id          = db.Column(db.Integer, primary_key=True)
    city        = db.Column(db.String(100), nullable=False)
    country     = db.Column(db.String(10))
    temperature = db.Column(db.Float)
    description = db.Column(db.String(200))
    humidity    = db.Column(db.Integer)
    wind_speed  = db.Column(db.Float)
    searched_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':          self.id,
            'city':        self.city,
            'country':     self.country,
            'temperature': self.temperature,
            'description': self.description,
            'humidity':    self.humidity,
            'wind_speed':  self.wind_speed,
            'searched_at': self.searched_at.strftime('%Y-%m-%d %H:%M')
        }

# ── Routes ─────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

# CREATE + READ (search weather and save to DB)
@app.route('/weather', methods=['POST'])
def get_weather():
    city = request.json.get('city', '').strip()
    if not city:
        return jsonify({'error': 'City name is required'}), 400

    api_key = os.environ.get('OPENWEATHER_API_KEY')
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 404:
            return jsonify({'error': 'City not found'}), 404
        if res.status_code != 200:
            return jsonify({'error': 'Weather service unavailable'}), 503

        data = res.json()
        record = SearchHistory(
            city        = data['name'],
            country     = data['sys']['country'],
            temperature = data['main']['temp'],
            description = data['weather'][0]['description'].title(),
            humidity    = data['main']['humidity'],
            wind_speed  = data['wind']['speed']
        )
        db.session.add(record)
        db.session.commit()
        return jsonify({'weather': record.to_dict()})

    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timed out'}), 504
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# READ (fetch all history)
@app.route('/history', methods=['GET'])
def get_history():
    records = SearchHistory.query.order_by(SearchHistory.searched_at.desc()).limit(20).all()
    return jsonify([r.to_dict() for r in records])

# UPDATE (update city note / re-label a search)
@app.route('/history/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    record = SearchHistory.query.get_or_404(record_id)
    data = request.json
    if 'city' in data:
        record.city = data['city']
    db.session.commit()
    return jsonify({'message': 'Updated', 'record': record.to_dict()})

# DELETE
@app.route('/history/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    record = SearchHistory.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': f'Record {record_id} deleted'})

# ── Init DB ────────────────────────────────────────────────────────────────────
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)