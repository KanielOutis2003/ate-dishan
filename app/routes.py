import os
from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from werkzeug.utils import secure_filename
from app import db
from app.models import District, School, Employee
from app.forms import EmployeeForm, SchoolForm, DistrictForm, ImportForm  # Ensure ImportForm is correctly imported

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    print("Home route accessed")  # Debugging line
    return render_template('index.html')

@bp.route('/employees')
def employees():
    employees = Employee.query.all()
    return render_template('employees.html', employees=employees)

@bp.route('/schools')
def schools():
    schools = School.query.all()
    return render_template('schools.html', schools=schools)

@bp.route('/districts')
def districts():
    districts = District.query.all()
    return render_template('districts.html', districts=districts)

@bp.route('/district/add', methods=['GET', 'POST'])
def add_district():
    form = DistrictForm()
    if form.validate_on_submit():
        district = District(name=form.name.data)
        db.session.add(district)
        db.session.commit()
        flash('District added successfully!', 'success')
        return redirect(url_for('main.districts'))
    return render_template('add_district.html', form=form)

@bp.route('/school/add', methods=['GET', 'POST'])
def add_school():
    form = SchoolForm()
    if form.validate_on_submit():
        school = School(name=form.name.data)  # Only set the name
        db.session.add(school)
        db.session.commit()
        flash('School added successfully!', 'success')
        return redirect(url_for('main.schools'))
    return render_template('add_school.html', form=form)

@bp.route('/employee/add', methods=['GET', 'POST'])
def add_employee():
    form = EmployeeForm()
    form.school_id.choices = [(s.id, s.name) for s in School.query.all()]
    if form.validate_on_submit():
        new_school_name = request.form.get('new_school')
        if new_school_name:
            new_school = School(name=new_school_name)
            db.session.add(new_school)
            db.session.commit()
            school_id = new_school.id
        else:
            school_id = form.school_id.data

        employee = Employee(
            employee_no=form.employee_no.data,
            station_code=form.station_code.data,
            family_name=form.family_name.data,
            given_name=form.given_name.data,
            middle_name=form.middle_name.data,
            school_id=school_id,
        )
        db.session.add(employee)
        db.session.commit()
        flash('Employee added successfully!', 'success')
        return redirect(url_for('main.employees'))
    return render_template('add_employee.html', form=form, schools=School.query.all())

@bp.route('/employee/<int:id>')
def view_employee(id):
    employee = Employee.query.get_or_404(id)
    return render_template('view_employee.html', employee=employee)

@bp.route('/employee/<int:id>/edit', methods=['GET', 'POST'])
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    form = EmployeeForm(obj=employee)
    form.school_id.choices = [(s.id, s.name) for s in School.query.all()]
    if form.validate_on_submit():
        employee.employee_no = form.employee_no.data
        employee.station_code = form.station_code.data
        employee.family_name = form.family_name.data
        employee.given_name = form.given_name.data
        employee.middle_name = form.middle_name.data
        employee.school_id = form.school_id.data
        db.session.commit()
        flash('Employee updated successfully!', 'success')
        return redirect(url_for('main.employees'))
    return render_template('edit_employee.html', form=form)

@bp.route('/employee/<int:id>/delete', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash('Employee deleted successfully!', 'success')
    return '', 204  # No content response

@bp.route('/district/<int:id>')
def view_district(id):
    district = District.query.get_or_404(id)
    return render_template('view_district.html', district=district)

@bp.route('/district/<int:id>/edit', methods=['GET', 'POST'])
def edit_district(id):
    district = District.query.get_or_404(id)
    form = DistrictForm(obj=district)
    if form.validate_on_submit():
        district.name = form.name.data
        db.session.commit()
        flash('District updated successfully!', 'success')
        return redirect(url_for('main.districts'))
    return render_template('edit_district.html', form=form, district=district)

@bp.route('/district/<int:id>/delete', methods=['DELETE'])
def delete_district(id):
    district = District.query.get_or_404(id)
    db.session.delete(district)
    db.session.commit()
    flash('District deleted successfully!', 'success')
    return '', 204  # No content response

@bp.route('/school/<int:id>')
def view_school(id):
    school = School.query.get_or_404(id)
    return render_template('view_school.html', school=school)

@bp.route('/school/<int:id>/edit', methods=['GET', 'POST'])
def edit_school(id):
    school = School.query.get_or_404(id)
    form = SchoolForm(obj=school)
    if form.validate_on_submit():
        school.name = form.name.data
        db.session.commit()
        flash('School updated successfully!', 'success')
        return redirect(url_for('main.schools'))
    return render_template('edit_school.html', form=form)

@bp.route('/school/<int:id>/delete', methods=['DELETE'])
def delete_school(id):
    school = School.query.get_or_404(id)
    db.session.delete(school)
    db.session.commit()
    flash('School deleted successfully!', 'success')
    return '', 204  # No content response

@bp.route('/search')
def search():
    query = request.args.get('query', '')
    employees = Employee.query.filter(
        Employee.employee_no.ilike(f'%{query}%') |
        Employee.family_name.ilike(f'%{query}%') |
        Employee.given_name.ilike(f'%{query}%')
    ).all()
    return render_template('search_results.html', employees=employees)

@bp.route('/export_employees')
def export_employees():
    employees = Employee.query.all()
    return render_template('export_employees.html', employees=employees)

@bp.route('/export_schools')
def export_schools():
    schools = School.query.all()
    return render_template('export_schools.html', schools=schools)

@bp.route('/export_districts')
def export_districts():
    districts = District.query.all()
    return render_template('export_districts.html', districts=districts)

# 📌 FIXED: Single import function for Employees
@bp.route('/import_employees', methods=['GET', 'POST'])
def import_employees():
    form = ImportForm()
    if form.validate_on_submit():
        file = form.file.data
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join('uploads', filename))  # Make sure 'uploads' exists
            flash('Employees file uploaded successfully', 'success')
            return redirect(url_for('main.import_employees'))
    return render_template('import_employees.html', form=form)

# 📌 FIXED: Single import function for Schools
@bp.route('/import_schools', methods=['GET', 'POST'])
def import_schools():
    form = ImportForm()
    if form.validate_on_submit():
        file = form.file.data
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join('uploads', filename))
            flash('Schools file uploaded successfully', 'success')
            return redirect(url_for('main.import_schools'))
    return render_template('import_schools.html', form=form)

# 📌 FIXED: Single import function for Districts
@bp.route('/import_districts', methods=['GET', 'POST'])
def import_districts():
    form = ImportForm()
    if form.validate_on_submit():
        file = form.file.data
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join('uploads', filename))
            flash('Districts file uploaded successfully', 'success')
            return redirect(url_for('main.import_districts'))
    return render_template('import_districts.html', form=form)

@bp.route('/dashboard')
def dashboard():
    employees = Employee.query.all()
    schools = School.query.all()
    districts = District.query.all()
    return render_template('dashboard.html', employees=employees, schools=schools, districts=districts)
