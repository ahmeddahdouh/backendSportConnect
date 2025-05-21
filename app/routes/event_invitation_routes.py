from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.event_invitation_route_service import EventInvitationRouteService
import traceback

event_invitation_bp = Blueprint('event_invitation', __name__)
event_invitation_route_service = EventInvitationRouteService()

@event_invitation_bp.route('/event/<int:event_id>/invite/<int:user_id>', methods=['POST'])
@jwt_required()
def invite_user(event_id, user_id):
    """Invite a user to a private event"""
    try:
        current_user = get_jwt_identity()
        invitation = event_invitation_route_service.invite_user(event_id, user_id, current_user)
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
        invitations = event_invitation_route_service.get_event_invitations(event_id)
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
        invitations = event_invitation_route_service.get_user_invitations(current_user)
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
        invitations = event_invitation_route_service.get_sent_invitations(current_user)
        return jsonify(invitations), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500

@event_invitation_bp.route('/invitation/<int:invitation_id>/respond', methods=['POST'])
@jwt_required()
def respond_to_invitation(invitation_id):
    """Respond to an event invitation"""
    try:
        current_user = get_jwt_identity()
        data = request.get_json()
        response = data.get('response')
        
        invitation = event_invitation_route_service.respond_to_invitation(invitation_id, current_user, response)
        return jsonify(invitation.to_dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Error in respond_to_invitation: {str(e)}")
        print(f"Stack trace: {traceback.format_exc()}")
        return jsonify({'error': 'An unexpected error occurred'}), 500 