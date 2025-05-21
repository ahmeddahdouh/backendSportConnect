from app.models.notification import Notification
from config import db

class NotificationRepository:
    def create_notification(self, notification_data):
        """Create a new notification"""
        notification = Notification(**notification_data)
        db.session.add(notification)
        db.session.commit()
        return notification

    def get_notification_by_id(self, notification_id):
        """Get a notification by its ID"""
        return Notification.query.get(notification_id)

    def get_user_notifications(self, user_id, unread_only=False):
        """Get all notifications for a user, optionally filtered by read status"""
        query = Notification.query.filter_by(user_id=user_id)
        if unread_only:
            query = query.filter_by(is_read=False)
        return query.order_by(Notification.created_at.desc()).all()

    def mark_as_read(self, notification_id):
        """Mark a notification as read"""
        notification = self.get_notification_by_id(notification_id)
        if notification:
            notification.is_read = True
            db.session.commit()
        return notification

    def mark_all_as_read(self, user_id):
        """Mark all notifications for a user as read"""
        Notification.query.filter_by(user_id=user_id, is_read=False).update({"is_read": True})
        db.session.commit()

    def delete_notification(self, notification_id):
        """Delete a notification"""
        notification = self.get_notification_by_id(notification_id)
        if notification:
            db.session.delete(notification)
            db.session.commit()
        return notification

    def delete_all_user_notifications(self, user_id):
        """Delete all notifications for a user"""
        Notification.query.filter_by(user_id=user_id).delete()
        db.session.commit() 