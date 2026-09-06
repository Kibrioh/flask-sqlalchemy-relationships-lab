#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate

from models import db, Event, Session, Speaker, Bio

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

def event_to_dict(event):
    return {
        "id": event.id,
        "name": event.name,
        "location": event.location,
    }


def session_to_dict(session):
    return {
        "id": session.id,
        "title": session.title,
        "start_time": session.start_time.isoformat() if session.start_time else None,
    }


def speaker_to_dict(speaker, include_bio=False):
    data = {
        "id": speaker.id,
        "name": speaker.name,
    }

    if include_bio:
        data["bio_text"] = speaker.bio.bio_text if speaker.bio else "No bio available"

    return data

@app.route('/events')
def get_events():
    events = Event.query.all()
    return jsonify([event_to_dict(event) for event in events]), 200


@app.route('/events/<int:id>/sessions')
def get_event_sessions(id):
    event = db.session.get(Event, id)

    if not event:
        return jsonify({"error": "Event not found"}), 404

    return jsonify([session_to_dict(session) for session in event.sessions]), 200


@app.route('/speakers')
def get_speakers():
    speakers = Speaker.query.all()
    return jsonify([speaker_to_dict(speaker) for speaker in speakers]), 200


@app.route('/speakers/<int:id>')
def get_speaker(id):
    speaker = db.session.get(Speaker, id)

    if not speaker:
        return jsonify({"error": "Speaker not found"}), 404

    return jsonify(speaker_to_dict(speaker, include_bio=True)), 200


@app.route('/sessions/<int:id>/speakers')
def get_session_speakers(id):
    session = db.session.get(Session, id)

    if not session:
        return jsonify({"error": "Session not found"}), 404

    return jsonify([
        speaker_to_dict(speaker, include_bio=True)
        for speaker in session.speakers
    ]), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
