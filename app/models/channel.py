from config import db

class Channel(db.Model):
    __tablename__ = "channels"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    event = db.relationship("Event", backref=db.backref("channel", uselist=False))
    admin = db.relationship("User", backref="admin_channels")
    members = db.relationship("ChannelMember", back_populates="channel")
    messages = db.relationship("Message", backref="channel", lazy=True)
