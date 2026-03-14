#!/usr/bin/env python3
"""
Initialize database safely for Sistem Pelacakan Alumni.
Run: cd sistem-pelacakan-alumni && python init_db.py
"""
from app import app, db, Admin
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    
    # Create default admin if not exists
    if not Admin.query.filter_by(email='admin@kampus.ac.id').first():
        admin = Admin(
            email='admin@kampus.ac.id',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin)
        db.session.commit()
        print("✓ Created default admin: admin@kampus.ac.id / admin123")
    else:
        print("✓ Default admin already exists")
    
    print("✓ Database initialized successfully! Tables: admin, alumni, hasil_pelacakan")
    print("Run: python app.py to start server")

