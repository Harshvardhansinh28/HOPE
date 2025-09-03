from backend.app.database import SessionLocal, init_db
from backend.app.models.user import User
from backend.app.auth import get_password_hash

init_db()

db = SessionLocal()
admin = db.query(User).filter(User.username == 'admin').first()
if not admin:
    admin = User(username='admin', hashed_password=get_password_hash('ChangeMe123!'), role='admin')
    db.add(admin)
    db.commit()
    print('Created admin user with username=admin and password=ChangeMe123!')
else:
    print('Admin user already exists')

db.close()
