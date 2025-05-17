from config import db

class ChannelMember(db.Model):
    __tablename__ = "channel_members"

    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey("channels.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    channel = db.relationship("Channel", back_populates="members")
    user = db.relationship("User", backref="channel_memberships")
