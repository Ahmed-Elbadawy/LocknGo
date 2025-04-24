from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from .models import Note, Locker, User
from . import db
from flask import flash, redirect,url_for, render_template
import json
import random
from .models import Locker
import datetime
from flask_mail import Message
from . import mail
from werkzeug.security import generate_password_hash

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/notes', methods=['GET','POST'])
@login_required
def notes():
    if request.method == "POST":
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!')
    return render_template("Notes.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({})
        
        
@views.route('/AddToVault', methods=['GET', 'POST'])
@login_required
def add_to_vault():
    if request.method == 'POST':
        new_locker = Locker(
            name1=request.form.get('name1'),
            email=request.form.get('email'),
            phone_number=request.form.get('phone_number'),
            item_type=request.form.get('item_type'),
            color=request.form.get('color'),
            notes=request.form.get('notes'),
            cost=30,  # 30 EGP per hour
            time=datetime.datetime.utcnow(),
            item_status='Inside',
            paid=False
        )

        db.session.add(new_locker)
        db.session.commit()

        # Use the id (primary key) assigned by SQLAlchemy
        send_locker_registration_email(new_locker.email, new_locker.id)

        flash(f'Locker added successfully! The locker number is A-{new_locker.id}', category='success')
        return redirect(url_for('views.add_to_vault'))

    return render_template('AddToVault.html', user=current_user)


@views.route('/locker-list', methods=['GET'])
@login_required
def locker_list():
    lockers = Locker.query.all()
    
    # Calculate duration and cost for each locker
    for locker in lockers:
        if locker.time is None:
            locker.time = datetime.datetime.utcnow()
        # This assumes you have the calculated_cost property in your model
        # If not, you could calculate it here:
        # locker.calculated_cost = calculate_locker_cost(locker)
    
    return render_template('locker_list.html', lockers=lockers, user=current_user)

@views.route('/regulations')
def regulations():
    return render_template('regulations.html')



@views.route('/update_locker_status', methods=['POST'])
@login_required
def update_locker_status():
    data = request.get_json()
    locker_id = data.get('locker_id')
    new_status = data.get('status')

    # Find the locker and update its status
    locker = Locker.query.get(locker_id)
    if locker:
        locker.item_status = new_status

        # If the status is "Outside", reset the cost
        if new_status == "Outside":
            locker.cost = 0.0  # Reset cost to 0
        
        # Commit changes to the database
        db.session.commit()
        return jsonify({"success": True})
    else:
        return jsonify({"success": False}), 400
    
@views.route('/locker/details/<int:locker_id>')
@login_required
def locker_details(locker_id):
    locker = Locker.query.get_or_404(locker_id)  # Fetch the locker by ID
    return render_template('locker_details.html', locker=locker)


def send_locker_registration_email(owner_email, locker_id):
    # Create the message
    subject = "Locker Registration Confirmation"
    body = f"Thank you for using LocknGo! Your locker ID is: A-{locker_id}. Please keep this ID safe for future reference."

    # Send the email
    msg = Message(subject, recipients=[owner_email])
    msg.body = body
    mail.send(msg)

@views.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    if current_user.role != 'admin':
        flash("You are not authorized to access this page.", "error")
        return redirect(url_for('views.home'))

    return render_template("dashboard.html", user=current_user)


@views.route('/manage_users', methods=['GET', 'POST'])
@login_required
def manage_users():
    if request.method == 'POST':
        if 'first_name' in request.form and 'email' in request.form and 'password' in request.form:
            # Add Admin
            if 'role' not in request.form or request.form['role'] == 'admin':
                first_name = request.form.get('first_name')
                email = request.form.get('email')
                password = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256')
                new_admin = User(first_name=first_name, email=email, password=password, role='admin')
                db.session.add(new_admin)
                db.session.commit()
                flash("Admin added successfully!", category='success')

            # Add Organizer
            elif request.form['role'] == 'organizer':
                first_name = request.form.get('first_name')
                email = request.form.get('email')
                password = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256')
                new_organizer = User(first_name=first_name, email=email, password=password, role='organizer')
                db.session.add(new_organizer)
                db.session.commit()
                flash("Organizer added successfully!", category='success')
        return redirect(url_for('views.manage_users'))

    # Display Admins and Organizers
    admins = User.query.filter_by(role='admin').all()
    organizers = User.query.filter_by(role='organizer').all()

    return render_template('manage_users.html', admins=admins, organizers=organizers)


# Delete Admin
@views.route('/delete_admin/<int:id>', methods=['POST'])
@login_required
def delete_admin(id):
    admin = User.query.get(id)
    if admin:
        db.session.delete(admin)
        db.session.commit()
        flash("Admin deleted successfully.", category='success')
    return redirect(url_for('views.manage_users'))


# Delete Organizer
@views.route('/delete_organizer/<int:id>', methods=['POST'])
def delete_organizer(id):
    organizer = User.query.get(id)
    if organizer:
        db.session.delete(organizer)
        db.session.commit()
        flash("Organizer deleted successfully.", category='success')
    return redirect(url_for('views.manage_users'))