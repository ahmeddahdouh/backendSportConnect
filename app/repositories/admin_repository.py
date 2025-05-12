from app.models.admin import Admin
from config import db


class AdminRepository:
    def find_by_email(self, email):
        return Admin.query.filter_by(email=email).first()
    
    def get_all_admins(self):
        return Admin.query.all()

    def find_by_username_or_email(username, email):
        return Admin.query.filter((Admin.username == username) | (Admin.email == email)).first()

    def add_admin(admin):
        db.session.add(admin)
        db.session.commit()

    def delete_admin_by_id(admin_id):
        admin = Admin.query.get(admin_id)
        if admin:
            db.session.delete(admin)
            db.session.commit()
        return admin
