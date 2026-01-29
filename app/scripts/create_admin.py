from sqlalchemy.orm import Session
from database.sqllite_engine import SessionLocal
from app.models.users_model import User
from app.security.password_hash import hash_password
from app.constants.roles import ROLE_ADMIN

ADMIN_EMAIL = "admin123@gmail.com"
ADMIN_PASSWORD = "Admin@123"  # change after first login
ADMIN_NAME = "System Admin"

def run():
    db: Session = SessionLocal()

    try:
        existing = db.query(User).filter(User.email == ADMIN_EMAIL).first()
        if existing:
            print("Admin already exists. Skipping.")
            return

        admin = User(
            name=ADMIN_NAME,
            email=ADMIN_EMAIL,
            password=hash_password(ADMIN_PASSWORD),
            role=ROLE_ADMIN,
            must_change_password=True,
            is_active=True
        )

        db.add(admin)
        db.commit()
        print("Admin created successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    run()
