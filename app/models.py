from app import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Remove extra SQLAlchemy instance (db is already imported from app)
# db = SQLAlchemy()  ❌ Not needed

# Define School Model
class School(db.Model):
    __tablename__ = 'school'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(50), nullable=True)
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'), nullable=True)
    district = db.relationship('District', backref='schools')

# Define District Model
class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Define Employee Model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_no = db.Column(db.String(50), unique=True, nullable=False)
    station_code = db.Column(db.String(50), nullable=False)
    family_name = db.Column(db.String(100), nullable=False)
    given_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    original_appointment_date = db.Column(db.Date)
    original_position = db.Column(db.String(100))
    original_salary_grade = db.Column(db.String(50))
    original_salary_step = db.Column(db.String(50))
    original_monthly_salary = db.Column(db.Float)
    current_appointment_date = db.Column(db.Date)
    current_position = db.Column(db.String(100))
    current_salary_grade = db.Column(db.String(50))
    current_salary_step = db.Column(db.String(50))
    current_monthly_salary = db.Column(db.Float)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
    school = db.relationship('School', backref=db.backref('employees', lazy=True))

# Optional: A model to test relationships (Not needed if not used)
class SpecificModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<SpecificModel {self.name}>'
