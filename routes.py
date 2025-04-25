from flask import Blueprint, request, jsonify
from models import db, Client, HealthProgram, Enrollment

routes = Blueprint('routes', __name__)

@routes.route('/program', methods=['POST'])
def create_program():
    name = request.json['name']
    program = HealthProgram(name=name)
    db.session.add(program)
    db.session.commit()
    return jsonify({'message': 'Program created'}), 201

@routes.route('/client', methods=['POST'])
def register_client():
    data = request.json
    client = Client(name=data['name'], age=data['age'], gender=data['gender'])
    db.session.add(client)
    db.session.commit()
    return jsonify({'message': 'Client registered'}), 201

@routes.route('/enroll', methods=['POST'])
def enroll_client():
    client_id = request.json['client_id']
    program_ids = request.json['program_ids']
    for pid in program_ids:
        enrollment = Enrollment(client_id=client_id, program_id=pid)
        db.session.add(enrollment)
    db.session.commit()
    return jsonify({'message': 'Enrollment successful'}), 200

@routes.route('/clients', methods=['GET'])
def search_clients():
    query = request.args.get('q', '')
    clients = Client.query.filter(Client.name.contains(query)).all()
    return jsonify([{'id': c.id, 'name': c.name} for c in clients])

@routes.route('/client/<int:client_id>', methods=['GET'])
def view_profile(client_id):
    client = Client.query.get_or_404(client_id)
    enrollments = Enrollment.query.filter_by(client_id=client_id).all()
    programs = [HealthProgram.query.get(e.program_id).name for e in enrollments]
    return jsonify({
        'name': client.name,
        'age': client.age,
        'gender': client.gender,
        'enrolled_programs': programs
    })
