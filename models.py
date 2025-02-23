from . import db
from datetime import datetime

class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    schools = db.relationship('School', backref='district', lazy=True)

class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'), nullable=False)
    employees = db.relationship('Employee', backref='school', lazy=True)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_no = db.Column(db.String(20), unique=True, nullable=False)
    station_code = db.Column(db.String(20), nullable=False)
    family_name = db.Column(db.String(50), nullable=False)
    given_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    
    # Original appointment details
    original_appointment_date = db.Column(db.Date, nullable=False)
    original_position = db.Column(db.String(100), nullable=False)
    original_salary_grade = db.Column(db.Integer, nullable=False)
    original_salary_step = db.Column(db.Integer, nullable=False)
    original_monthly_salary = db.Column(db.Float, nullable=False)
    
    # Current appointment details
    current_appointment_date = db.Column(db.Date)
    current_position = db.Column(db.String(100))
    current_salary_grade = db.Column(db.Integer)
    current_salary_step = db.Column(db.Integer)
    current_monthly_salary = db.Column(db.Float)
    
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
    
    @property
    def years_in_service(self):
        start_date = self.original_appointment_date
        return (datetime.now().date() - start_date).days // 365 