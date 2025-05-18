from app.repositories.notification_repository import NotificationRepository
from app.repositories.user_repository import UserRepository

class NotificationService:
    def __init__(self):
        self.notification_repository = NotificationRepository()
        self.user_repository = UserRepository()

    def create_notification(self, user_id, sender_id, notification_type, content):
        """Create a new notification"""
        # Verify that both users exist
        if not self.user_repository.get_user_by_id(user_id):
            raise ValueError("Recipient user does not exist")
        if not self.user_repository.get_user_by_id(sender_id):
            raise ValueError("Sender user does not exist")

        notification_data = {
            "user_id": user_id,
            "sender_id": sender_id,
            "type": notification_type,
            "content": content
        }
        return self.notification_repository.create_notification(notification_data)

    def get_user_notifications(self, user_id, unread_only=False):
        """Get all notifications for a user"""
        if not self.user_repository.get_user_by_id(user_id):
            raise ValueError("User does not exist")
        
        notifications = self.notification_repository.get_user_notifications(user_id, unread_only)
        return [notification.to_dict() for notification in notifications]

    def mark_notification_as_read(self, notification_id, user_id):
        """Mark a notification as read"""
        notification = self.notification_repository.get_notification_by_id(notification_id)
        if not notification:
            raise ValueError("Notification not found")
        if notification.user_id != user_id:
            raise ValueError("Unauthorized to modify this notification")
        
        return self.notification_repository.mark_as_read(notification_id)

    def mark_all_as_read(self, user_id):
        """Mark all notifications for a user as read"""
        if not self.user_repository.get_user_by_id(user_id):
            raise ValueError("User does not exist")
        
        self.notification_repository.mark_all_as_read(user_id)
        return {"message": "All notifications marked as read"}

    def delete_notification(self, notification_id, user_id):
        """Delete a notification"""
        notification = self.notification_repository.get_notification_by_id(notification_id)
        if not notification:
            raise ValueError("Notification not found")
        if notification.user_id != user_id:
            raise ValueError("Unauthorized to delete this notification")
        
        self.notification_repository.delete_notification(notification_id)
        return {"message": "Notification deleted successfully"}

    def delete_all_notifications(self, user_id):
        """Delete all notifications for a user"""
        if not self.user_repository.get_user_by_id(user_id):
            raise ValueError("User does not exist")
        
        self.notification_repository.delete_all_user_notifications(user_id)
        return {"message": "All notifications deleted successfully"} 