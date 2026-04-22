import os
from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from marshmallow import ValidationError

from server.models import db, Exercise, Workout, WorkoutExercise
from server.schema import (
    exercise_schema,
    exercises_schema,
    workout_schema,
    workouts_schema,
    workout_exercise_schema
)

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'app.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


# ── Workouts ────────────────────────────────────────────────────────────────

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(jsonify(workouts_schema.dump(workouts)), 200)


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout_by_id(id):
    # FIX: .query.get() is deprecated in SQLAlchemy 2.0 — use .session.get() instead
    workout = db.session.get(Workout, id)

    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)

    return make_response(jsonify(workout_schema.dump(workout)), 200)


@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = workout_schema.load(request.get_json())

        new_workout = Workout(
            date=data['date'],
            duration_minutes=data['duration_minutes'],
            notes=data.get('notes')
        )

        db.session.add(new_workout)
        db.session.commit()

        return make_response(jsonify(workout_schema.dump(new_workout)), 201)

    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 400)

    except ValueError as err:
        return make_response(jsonify({"error": str(err)}), 400)


# FIX: Added missing PATCH route so workouts can be updated
@app.route('/workouts/<int:id>', methods=['PATCH'])
def update_workout(id):
    workout = db.session.get(Workout, id)

    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)

    try:
        # partial=True allows sending only the fields you want to update
        data = workout_schema.load(request.get_json(), partial=True)

        if 'date' in data:
            workout.date = data['date']
        if 'duration_minutes' in data:
            workout.duration_minutes = data['duration_minutes']
        if 'notes' in data:
            workout.notes = data['notes']

        db.session.commit()

        return make_response(jsonify(workout_schema.dump(workout)), 200)

    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 400)

    except ValueError as err:
        return make_response(jsonify({"error": str(err)}), 400)


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = db.session.get(Workout, id)  # FIX: deprecated .query.get()

    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)

    db.session.delete(workout)
    db.session.commit()

    return make_response(jsonify({"message": f"Workout {id} deleted successfully"}), 200)


# ── Exercises ────────────────────────────────────────────────────────────────

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(jsonify(exercises_schema.dump(exercises)), 200)


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise_by_id(id):
    exercise = db.session.get(Exercise, id)  # FIX: deprecated .query.get()

    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)

    return make_response(jsonify(exercise_schema.dump(exercise)), 200)


@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json())

        new_exercise = Exercise(
            name=data['name'],
            category=data['category'],
            equipment_needed=data['equipment_needed']
        )

        db.session.add(new_exercise)
        db.session.commit()

        return make_response(jsonify(exercise_schema.dump(new_exercise)), 201)

    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 400)

    except ValueError as err:
        return make_response(jsonify({"error": str(err)}), 400)


# FIX: Added missing PATCH route so exercises can be updated
@app.route('/exercises/<int:id>', methods=['PATCH'])
def update_exercise(id):
    exercise = db.session.get(Exercise, id)

    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)

    try:
        data = exercise_schema.load(request.get_json(), partial=True)

        if 'name' in data:
            exercise.name = data['name']
        if 'category' in data:
            exercise.category = data['category']
        if 'equipment_needed' in data:
            exercise.equipment_needed = data['equipment_needed']

        db.session.commit()

        return make_response(jsonify(exercise_schema.dump(exercise)), 200)

    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 400)

    except ValueError as err:
        return make_response(jsonify({"error": str(err)}), 400)


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)  # FIX: deprecated .query.get()

    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)

    db.session.delete(exercise)
    db.session.commit()

    return make_response(jsonify({"message": f"Exercise {id} deleted successfully"}), 200)


# ── WorkoutExercises ─────────────────────────────────────────────────────────

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)    # FIX: deprecated .query.get()
    exercise = db.session.get(Exercise, exercise_id)  # FIX: deprecated .query.get()

    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)

    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)

    try:
        incoming_data = request.get_json() or {}

        # Inject route parameters into the payload before schema validation
        incoming_data['workout_id'] = workout_id
        incoming_data['exercise_id'] = exercise_id

        data = workout_exercise_schema.load(incoming_data)

        new_workout_exercise = WorkoutExercise(
            workout_id=data['workout_id'],
            exercise_id=data['exercise_id'],
            reps=data.get('reps'),
            sets=data.get('sets'),
            duration_seconds=data.get('duration_seconds')
        )

        db.session.add(new_workout_exercise)
        db.session.commit()

        return make_response(jsonify(workout_exercise_schema.dump(new_workout_exercise)), 201)

    except ValidationError as err:
        return make_response(jsonify({"errors": err.messages}), 400)

    except ValueError as err:
        return make_response(jsonify({"error": str(err)}), 400)

    except Exception as err:
        db.session.rollback()
        return make_response(jsonify({"error": str(err)}), 400)


if __name__ == '__main__':
    app.run(port=5555, debug=True)