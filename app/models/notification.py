from datetime import datetime, UTC
from sqlalchemy.dialects.postgresql import JSONB
from config import db

class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # e.g., 'event_invitation', 'team_invitation'
    content = db.Column(JSONB, nullable=False)  # Flexible JSON field for notification data
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))

    # Relationships
    user = db.relationship("User", foreign_keys=[user_id], backref="received_notifications")
    sender = db.relationship("User", foreign_keys=[sender_id], backref="sent_notifications")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "sender_id": self.sender_id,
            "type": self.type,
            "content": self.content,
            "is_read": self.is_read,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        } 