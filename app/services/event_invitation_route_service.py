from flask import request
import json
from app.services.event_invitation_service import EventInvitationService

class EventInvitationRouteService:
    def __init__(self):
        self.event_invitation_service = EventInvitationService()

    def get_current_user_id(self, current_user):
        """Extract user ID from JWT identity"""
        if isinstance(current_user, str):
            current_user = json.loads(current_user)
        return int(current_user["id"])

    def invite_user(self, event_id, user_id, current_user):
        """Invite a user to a private event"""
        sender_id = self.get_current_user_id(current_user)
        return self.event_invitation_service.invite_user_to_event(event_id, user_id, sender_id)

    def get_event_invitations(self, event_id):
        """Get all invitations for an event"""
        return self.event_invitation_service.get_event_invitations(event_id)

    def get_user_invitations(self, current_user):
        """Get all invitations for the current user"""
        user_id = self.get_current_user_id(current_user)
        status = request.args.get('status')
        return self.event_invitation_service.get_user_invitations(user_id, status)

    def get_sent_invitations(self, current_user):
        """Get all invitations sent by the current user"""
        sender_id = self.get_current_user_id(current_user)
        status = request.args.get('status')
        return self.event_invitation_service.get_sent_invitations(sender_id, status)

    def respond_to_invitation(self, invitation_id, current_user, response):
        """Respond to an event invitation"""
        user_id = self.get_current_user_id(current_user)
        
        if response not in ['accepted', 'rejected']:
            raise ValueError('Invalid response. Must be either "accepted" or "rejected"')
        
        invitation = self.event_invitation_service.respond_to_invitation(invitation_id, user_id, response)
        
        # Delete the invitation after responding
        self.event_invitation_service.delete_invitation(invitation_id, user_id)
        
        return invitation 