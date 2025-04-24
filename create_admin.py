from website import create_app, db
from website.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Create an admin user
    admin_user = User(
        email='admin@gg',
        password=generate_password_hash('123123123', method='pbkdf2:sha256'),
        first_name='Admin',
        role='admin'
    )

    db.session.add(admin_user)
    db.session.commit()

    print("Admin user created successfully.")