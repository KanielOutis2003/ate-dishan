from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class DistrictForm(FlaskForm):
    name = StringField('District Name', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Submit')

class SchoolForm(FlaskForm):
    school_id = StringField('School ID', validators=[DataRequired(), Length(max=20)])
    name = StringField('School Name', validators=[DataRequired(), Length(max=100)])
    level = SelectField('School Level', 
                       choices=[('elementary', 'Elementary'), 
                              ('junior_high', 'Junior High'),
                              ('senior_high', 'Senior High')],
                       validators=[DataRequired()])
    district_id = SelectField('District', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')

class EmployeeForm(FlaskForm):
    employee_no = StringField('Employee No.', validators=[DataRequired(), Length(max=20)])
    station_code = StringField('Station Code', validators=[DataRequired(), Length(max=20)])
    family_name = StringField('Family Name', validators=[DataRequired(), Length(max=50)])
    given_name = StringField('Given Name', validators=[DataRequired(), Length(max=50)])
    middle_name = StringField('Middle Name', validators=[Length(max=50)])
    
    # Original appointment details
    original_appointment_date = DateField('Original Appointment Date', validators=[DataRequired()])
    original_position = StringField('Original Position', validators=[DataRequired(), Length(max=100)])
    original_salary_grade = IntegerField('Original Salary Grade', validators=[DataRequired(), NumberRange(min=1, max=33)])
    original_salary_step = IntegerField('Original Salary Step', validators=[DataRequired(), NumberRange(min=1, max=8)])
    original_monthly_salary = FloatField('Original Monthly Salary', validators=[DataRequired()])
    
    # Current appointment details
    current_appointment_date = DateField('Current Appointment Date')
    current_position = StringField('Current Position', validators=[Length(max=100)])
    current_salary_grade = IntegerField('Current Salary Grade', validators=[NumberRange(min=1, max=33)])
    current_salary_step = IntegerField('Current Salary Step', validators=[NumberRange(min=1, max=8)])
    current_monthly_salary = FloatField('Current Monthly Salary')
    
    school_id = SelectField('School', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit') 