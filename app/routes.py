from flask import Blueprint, render_template, flash, redirect, url_for, request
from app import db
from app.models import District, School, Employee
from app.forms import EmployeeForm, SchoolForm, DistrictForm

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('index.html')

# ... (move all other routes from app.py here) ... 