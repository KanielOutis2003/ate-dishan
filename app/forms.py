from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, DateField, SelectField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, NumberRange

class EmployeeForm(FlaskForm):
    employee_no = StringField('Employee No', validators=[DataRequired()])
    station_code = StringField('Station Code', validators=[DataRequired()])
    family_name = StringField('Family Name', validators=[DataRequired()])
    given_name = StringField('Given Name', validators=[DataRequired()])
    middle_name = StringField('Middle Name')
    school_id = SelectField('School', coerce=int)
    submit = SubmitField('Add Employee')

class SchoolForm(FlaskForm):
    name = StringField('School Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class DistrictForm(FlaskForm):
    name = StringField('District Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

# ✅ FIX: Add missing ImportForm
class ImportForm(FlaskForm):
    file = FileField('Upload File', validators=[DataRequired()])
    submit = SubmitField('Import')
