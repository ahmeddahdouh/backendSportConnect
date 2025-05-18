from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.event_invitation_service import EventInvitationService
import json
import traceback

event_invitation_bp = Blueprint('event_invitation', __name__)
event_invitation_service = EventInvitationService()

@event_invitation_bp.route('/event/<int:event_id>/invite/<int:user_id>', methods=['POST'])
@jwt_required()
def invite_user(event_id, user_id):
    """Invite a user to a private event"""
    try:
        current_user = get_jwt_identity()
        current_user_json = json.loads(current_user)
        sender_id = current_user_json["id"]
        invitation = event_invitation_service.invite_user_to_event(event_id, user_id, sender_id)
        return jsonify(invitation.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Exception in invite_user: {e}")
        traceback.print_exc()
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

@event_invitation_bp.route('/event/<int:event_id>/invitations', methods=['GET'])
@jwt_required()
def get_event_invitations(event_id):
    """Get all invitations for an event"""
    try:
        invitations = event_invitation_service.get_event_invitations(event_id)
        return jsonify(invitations), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500

@event_invitation_bp.route('/user/invitations', methods=['GET'])
@jwt_required()
def get_user_invitations():
    """Get all invitations for the current user"""
    try:
        current_user = get_jwt_identity()
        current_user_json = json.loads(current_user)
        user_id = current_user_json["id"]
        status = request.args.get('status')
        invitations = event_invitation_service.get_user_invitations(user_id, status)
        return jsonify(invitations), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500

@event_invitation_bp.route('/user/sent-invitations', methods=['GET'])
@jwt_required()
def get_sent_invitations():
    """Get all invitations sent by the current user"""
    try:
        current_user = get_jwt_identity()
        current_user_json = json.loads(current_user)
        sender_id = current_user_json["id"]
        status = request.args.get('status')
        invitations = event_invitation_service.get_sent_invitations(sender_id, status)
        return jsonify(invitations), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500

@event_invitation_bp.route('/invitation/<int:invitation_id>/respond', methods=['POST'])
@jwt_required()
def respond_to_invitation(invitation_id):
    try:
        current_user = get_jwt_identity()
        if isinstance(current_user, str):
            current_user = json.loads(current_user)
        user_id = current_user.get('id')
        
        data = request.get_json()
        response = data.get('response')
        
        if response not in ['accepted', 'rejected']:
            return jsonify({'error': 'Invalid response. Must be either "accepted" or "rejected"'}), 400
        
        invitation = event_invitation_service.respond_to_invitation(invitation_id, user_id, response)
        
        # Delete the invitation after responding
        event_invitation_service.delete_invitation(invitation_id, user_id)
        
        return jsonify(invitation.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Error in respond_to_invitation: {str(e)}")
        print(f"Stack trace: {traceback.format_exc()}")
        return jsonify({'error': 'An unexpected error occurred'}), 500 