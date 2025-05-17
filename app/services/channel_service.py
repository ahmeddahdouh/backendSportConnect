from config import db
from app.models.channel import Channel
from app.models.channel_member import ChannelMember
from app.models.message import Message
from app.models.user import User
from flask import abort, jsonify


class ChannelService:
    def create_channel(self, name, event_id, admin_id):
        existing = Channel.query.filter_by(event_id=event_id).first()
        if existing:
            return existing

        new_channel = Channel(name=name, event_id=event_id, admin_id=admin_id)
        db.session.add(new_channel)
        db.session.flush()  

        
        member = ChannelMember(channel_id=new_channel.id, user_id=admin_id)
        db.session.add(member)
        db.session.commit()
        return new_channel

    def add_member(self, event_id, user_id):
        channel = Channel.query.filter_by(event_id=event_id).first()
        if not channel:
            abort(404, description="Canal non trouvé")

        existing = ChannelMember.query.filter_by(channel_id=channel.id, user_id=user_id).first()
        if existing:
            return {"message": "Déjà membre"}, 200

        member = ChannelMember(channel_id=channel.id, user_id=user_id)
        db.session.add(member)
        db.session.commit()
        return {"message": "Membre ajouté"}, 201

    def remove_member(self, event_id, user_id, current_user_id):
        channel = Channel.query.filter_by(event_id=event_id).first()
        if not channel:
            abort(404, description="Canal non trouvé")

        if channel.admin_id != current_user_id:
            abort(403, description="Seul l'admin peut retirer un membre")

        member = ChannelMember.query.filter_by(channel_id=channel.id, user_id=user_id).first()
        if not member:
            abort(404, description="Membre non trouvé")

        db.session.delete(member)
        db.session.commit()
        return {"message": "Membre retiré"}, 200

    def send_message(self, event_id, user_id, content):
        channel = Channel.query.filter_by(event_id=event_id).first()
        if not channel:
            abort(404, description="Canal non trouvé")

        member = ChannelMember.query.filter_by(channel_id=channel.id, user_id=user_id).first()
        if not member:
            abort(403, description="Vous n'êtes pas membre du canal")

        msg = Message(content=content, channel_id=channel.id, user_id=user_id)
        db.session.add(msg)
        db.session.commit()
        return {"message": "Message envoyé"}, 201

    def get_messages(self, event_id):
        channel = Channel.query.filter_by(event_id=event_id).first()
        if not channel:
            abort(404, description="Canal non trouvé")

        messages = Message.query.filter_by(channel_id=channel.id).order_by(Message.created_at.asc()).all()
        result = [
            {
                "id": m.id,
                "content": m.content,
                "username": m.user.username,
                "created_at": m.created_at.isoformat()
            }
            for m in messages
        ]
        return result
