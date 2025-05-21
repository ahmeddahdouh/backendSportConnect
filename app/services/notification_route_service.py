from flask import request
import json
from app.services.notification_service import NotificationService

class NotificationRouteService:
    def __init__(self):
        self.notification_service = NotificationService()

    def get_current_user_id(self, current_user):
        """Extract user ID from JWT identity"""
        if isinstance(current_user, str):
            current_user = json.loads(current_user)
        return int(current_user["id"])

    def get_notifications(self, current_user):
        """Get all notifications for the current user"""
        user_id = self.get_current_user_id(current_user)
        unread_only = request.args.get("unread_only", "false").lower() == "true"
        return self.notification_service.get_user_notifications(user_id, unread_only)

    def mark_as_read(self, notification_id, current_user):
        """Mark a notification as read"""
        user_id = self.get_current_user_id(current_user)
        notification = self.notification_service.mark_notification_as_read(notification_id, user_id)
        return notification.to_dict()

    def mark_all_as_read(self, current_user):
        """Mark all notifications as read for the current user"""
        user_id = self.get_current_user_id(current_user)
        return self.notification_service.mark_all_as_read(user_id)

    def delete_notification(self, notification_id, current_user):
        """Delete a notification"""
        user_id = self.get_current_user_id(current_user)
        return self.notification_service.delete_notification(notification_id, user_id)

    def delete_all_notifications(self, current_user):
        """Delete all notifications for the current user"""
        user_id = self.get_current_user_id(current_user)
        return self.notification_service.delete_all_notifications(user_id) 