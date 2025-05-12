from app.repositories.user_repository import UserRepository

user_repo = UserRepository()

class AdminUserService:
    def list_users(self):
        users = user_repo.get_all_users()
        return [{
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "firstname": u.firstname,
            "familyname": u.familyname,
            "city": u.city,
            "phone": u.phone,
            "age": u.age,
            "profileImage": u.profile_image
        } for u in users]

    def delete_user_by_id(self, user_id):
        user = user_repo.get_user_by_id(user_id)
        if not user:
            return {"message": "Utilisateur introuvable"}, 404

        events = user_repo.get_events_by_user(user.id)
        user_repo.delete_events(events)
        user_repo.delete_user(user)

        return {"message": "Utilisateur supprimé"}, 200
