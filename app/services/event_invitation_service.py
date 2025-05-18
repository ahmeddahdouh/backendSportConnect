from app.repositories.event_invitation_repository import EventInvitationRepository
from app.repositories.event_repository import EventRepository
from app.repositories.user_repository import UserRepository
from app.services.notification_service import NotificationService

class EventInvitationService:
    def __init__(self):
        self.invitation_repository = EventInvitationRepository()
        self.event_repository = EventRepository()
        self.user_repository = UserRepository()
        self.notification_service = NotificationService()

    def invite_user_to_event(self, event_id, user_id, sender_id):
        """Invite a user to a private event"""
        # Verify event exists and is private
        event = self.event_repository.get_event_by_id(event_id)
        if not event:
            raise ValueError("Event not found")
        if not event.is_private:
            raise ValueError("Cannot invite users to non-private events")

        # Verify users exist
        if not self.user_repository.get_user_by_id(user_id):
            raise ValueError("Recipient user not found")
        if not self.user_repository.get_user_by_id(sender_id):
            raise ValueError("Sender user not found")

        # Check if user is already invited
        existing_invitation = self.invitation_repository.get_pending_invitation(event_id, user_id)
        if existing_invitation:
            raise ValueError("User already has a pending invitation")

        # Create invitation
        invitation = self.invitation_repository.create_invitation(event_id, user_id, sender_id)

        # Create notification
        notification_content = {
            "type": "event_invitation",
            "event_id": event_id,
            "event_name": event.event_name,
            "invitation_id": invitation.id,
            "sender_id": sender_id
        }
        self.notification_service.create_notification(
            user_id=user_id,
            sender_id=sender_id,
            notification_type="event_invitation",
            content=notification_content
        )

        return invitation

    def get_event_invitations(self, event_id):
        """Get all invitations for an event"""
        if not self.event_repository.get_event_by_id(event_id):
            raise ValueError("Event not found")
        
        invitations = self.invitation_repository.get_event_invitations(event_id)
        return [invitation.to_dict() for invitation in invitations]

    def get_user_invitations(self, user_id, status=None):
        """Get all invitations for a user"""
        if not self.user_repository.get_user_by_id(user_id):
            raise ValueError("User not found")
        
        invitations = self.invitation_repository.get_user_invitations(user_id, status)
        return [invitation.to_dict() for invitation in invitations]

    def get_sent_invitations(self, sender_id, status=None):
        """Get all invitations sent by a user"""
        if not self.user_repository.get_user_by_id(sender_id):
            raise ValueError("User not found")
        
        invitations = self.invitation_repository.get_sent_invitations(sender_id, status)
        return [invitation.to_dict() for invitation in invitations]

    def respond_to_invitation(self, invitation_id, user_id, response):
        """Respond to an event invitation (accept/reject)"""
        invitation = self.invitation_repository.get_invitation_by_id(invitation_id)
        if not invitation:
            raise ValueError("Invitation not found")
        if invitation.user_id != user_id:
            raise ValueError("Unauthorized to respond to this invitation")
        if invitation.status != "pending":
            raise ValueError("Invitation has already been responded to")

        if response not in ["accepted", "rejected"]:
            raise ValueError("Invalid response. Must be 'accepted' or 'rejected'")

        # Update invitation status
        invitation = self.invitation_repository.update_invitation_status(invitation_id, response)

        # If accepted, add user to event
        if response == "accepted":
            self.event_repository.add_user_to_event(user_id, invitation.event_id)

        return invitation

    def delete_invitation(self, invitation_id, user_id):
        """Delete an invitation"""
        invitation = self.invitation_repository.get_invitation_by_id(invitation_id)
        if not invitation:
            raise ValueError("Invitation not found")
        if invitation.user_id != user_id and invitation.sender_id != user_id:
            raise ValueError("Unauthorized to delete this invitation")

        return self.invitation_repository.delete_invitation(invitation_id) 