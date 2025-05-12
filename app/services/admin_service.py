import bcrypt
from flask import json
from flask_jwt_extended import create_access_token
from app.models.admin import Admin
from app.repositories.admin_repository import AdminRepository

adminRepository = AdminRepository()

class AdminService:
    
    def login_admin(self, email, password):
        admin = adminRepository.find_by_email(email)

        if not admin:
            return {"error": "Admin introuvable"}, 404

        if admin.password.startswith('$2b$'):
            if not bcrypt.checkpw(password.encode(), admin.password.encode()):
                return {"error": "Mot de passe incorrect"}, 401
        else:
            if password != admin.password:
                return {"error": "Mot de passe incorrect"}, 401

        admin_token = create_access_token(identity=json.dumps({
            "id": admin.id,
            "username": admin.username,
            "email": admin.email,
            "role": "admin"
        }))

        return {
            "admin_token": admin_token,
            "admin": {
                "id": admin.id,
                "username": admin.username
            }
        }, 200

    def list_admins(self):
        admins = adminRepository.get_all_admins()
        return [{
            "id": a.id,
            "username": a.username,
            "email": a.email,
            "firstname": a.firstname,
            "familyname": a.familyname,
            "city": a.city,
            "phone": a.phone,
            "age": a.age
        } for a in admins]

    def create_admin(self,data):
        if adminRepository.find_by_username_or_email(data['username'], data['email']):
            return None, "Admin existe déjà"
        
        hashed_password = bcrypt.hashpw(data['password'].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        new_admin = Admin(
            username=data['username'],
            email=data['email'],
            password=hashed_password,
            firstname=data['firstname'],
            familyname=data['familyname'],
            city=data['city'],
            phone=data['phone'],
            age=data['age']
        )
        adminRepository.add_admin(new_admin)
        return new_admin, None

    def remove_admin(self,admin_id):
        return adminRepository.delete_admin_by_id(admin_id)
