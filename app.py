from flask import render_template, flash, redirect, url_for, request
from . import create_app, db
from .models import District, School, Employee
from .forms import EmployeeForm, SchoolForm, DistrictForm

app = create_app()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/employees')
def employees():
    employees = Employee.query.all()
    return render_template('employees.html', employees=employees)

@app.route('/schools')
def schools():
    schools = School.query.all()
    return render_template('schools.html', schools=schools)

@app.route('/districts')
def districts():
    districts = District.query.all()
    return render_template('districts.html', districts=districts)

@app.route('/district/add', methods=['GET', 'POST'])
def add_district():
    form = DistrictForm()
    if form.validate_on_submit():
        district = District(name=form.name.data)
        db.session.add(district)
        db.session.commit()
        flash('District added successfully!', 'success')
        return redirect(url_for('districts'))
    return render_template('district_form.html', form=form, title='Add District')

@app.route('/school/add', methods=['GET', 'POST'])
def add_school():
    form = SchoolForm()
    form.district_id.choices = [(d.id, d.name) for d in District.query.all()]
    if form.validate_on_submit():
        school = School(
            school_id=form.school_id.data,
            name=form.name.data,
            level=form.level.data,
            district_id=form.district_id.data
        )
        db.session.add(school)
        db.session.commit()
        flash('School added successfully!', 'success')
        return redirect(url_for('schools'))
    return render_template('school_form.html', form=form, title='Add School')

@app.route('/employee/add', methods=['GET', 'POST'])
def add_employee():
    form = EmployeeForm()
    form.school_id.choices = [(s.id, s.name) for s in School.query.all()]
    if form.validate_on_submit():
        employee = Employee(
            employee_no=form.employee_no.data,
            station_code=form.station_code.data,
            family_name=form.family_name.data,
            given_name=form.given_name.data,
            middle_name=form.middle_name.data,
            original_appointment_date=form.original_appointment_date.data,
            original_position=form.original_position.data,
            original_salary_grade=form.original_salary_grade.data,
            original_salary_step=form.original_salary_step.data,
            original_monthly_salary=form.original_monthly_salary.data,
            current_appointment_date=form.current_appointment_date.data,
            current_position=form.current_position.data,
            current_salary_grade=form.current_salary_grade.data,
            current_salary_step=form.current_salary_step.data,
            current_monthly_salary=form.current_monthly_salary.data,
            school_id=form.school_id.data
        )
        db.session.add(employee)
        db.session.commit()
        flash('Employee added successfully!', 'success')
        return redirect(url_for('employees'))
    return render_template('employee_form.html', form=form, title='Add Employee')

@app.route('/employee/<int:id>')
def view_employee(id):
    employee = Employee.query.get_or_404(id)
    return render_template('employee_detail.html', employee=employee)

@app.route('/employee/<int:id>/edit', methods=['GET', 'POST'])
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    form = EmployeeForm(obj=employee)
    form.school_id.choices = [(s.id, s.name) for s in School.query.all()]
    
    if form.validate_on_submit():
        form.populate_obj(employee)
        db.session.commit()
        flash('Employee updated successfully!', 'success')
        return redirect(url_for('view_employee', id=employee.id))
    
    return render_template('employee_form.html', form=form, title='Edit Employee')

@app.route('/employee/<int:id>/delete', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    return '', 204

@app.route('/district/<int:id>')
def view_district(id):
    district = District.query.get_or_404(id)
    return render_template('district_detail.html', district=district)

@app.route('/district/<int:id>/edit', methods=['GET', 'POST'])
def edit_district(id):
    district = District.query.get_or_404(id)
    form = DistrictForm(obj=district)
    
    if form.validate_on_submit():
        form.populate_obj(district)
        db.session.commit()
        flash('District updated successfully!', 'success')
        return redirect(url_for('view_district', id=district.id))
    
    return render_template('district_form.html', form=form, title='Edit District')

@app.route('/district/<int:id>/delete', methods=['DELETE'])
def delete_district(id):
    district = District.query.get_or_404(id)
    db.session.delete(district)
    db.session.commit()
    return '', 204

@app.route('/search')
def search():
    query = request.args.get('q', '')
    
    employees = Employee.query.filter(
        db.or_(
            Employee.family_name.ilike(f'%{query}%'),
            Employee.given_name.ilike(f'%{query}%'),
            Employee.employee_no.ilike(f'%{query}%')
        )
    ).all()
    
    schools = School.query.filter(
        School.name.ilike(f'%{query}%')
    ).all()
    
    return render_template('search_results.html', 
                         employees=employees, 
                         schools=schools, 
                         query=query)

if __name__ == '__main__':
    app.run(debug=True)
