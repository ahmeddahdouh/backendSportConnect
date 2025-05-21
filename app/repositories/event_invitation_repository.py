from app.associations.event_invitations import EventInvitation
from config import db

class EventInvitationRepository:
    def create_invitation(self, event_id, user_id, sender_id):
        """Create a new event invitation"""
        invitation = EventInvitation(event_id=event_id, user_id=user_id, sender_id=sender_id)
        db.session.add(invitation)
        db.session.commit()
        return invitation

    def get_invitation_by_id(self, invitation_id):
        """Get an invitation by its ID"""
        return EventInvitation.query.get(invitation_id)

    def get_event_invitations(self, event_id):
        """Get all invitations for an event"""
        return EventInvitation.query.filter_by(event_id=event_id).all()

    def get_user_invitations(self, user_id, status=None):
        """Get all invitations for a user, optionally filtered by status"""
        query = EventInvitation.query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        return query.all()

    def get_sent_invitations(self, sender_id, status=None):
        """Get all invitations sent by a user, optionally filtered by status"""
        query = EventInvitation.query.filter_by(sender_id=sender_id)
        if status:
            query = query.filter_by(status=status)
        return query.all()

    def update_invitation_status(self, invitation_id, status):
        """Update the status of an invitation"""
        invitation = self.get_invitation_by_id(invitation_id)
        if invitation:
            invitation.status = status
            db.session.commit()
        return invitation

    def delete_invitation(self, invitation_id):
        """Delete an invitation"""
        invitation = self.get_invitation_by_id(invitation_id)
        if invitation:
            db.session.delete(invitation)
            db.session.commit()
        return invitation

    def get_pending_invitation(self, event_id, user_id):
        """Get a pending invitation for a specific event and user"""
        return EventInvitation.query.filter_by(
            event_id=event_id,
            user_id=user_id,
            status="pending"
        ).first() 