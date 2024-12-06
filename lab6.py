from flask import Blueprint, render_template, request, redirect, session
lab6 = Blueprint('lab6', __name__)

#venv\Scripts\activate.bat


@lab6.route('/lab6/')
def lab():
    return render_template('lab6/lab6.html')