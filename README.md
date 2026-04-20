#  Flask Workout Tracker API

##  Project Description

This project uses Flask, SQLAlchemy, and Marshmallow to provide a backend API. Using a join table, it enables users (such as personal trainers) to design workouts, manage exercises, and monitor how activities are carried out inside workouts.

With further characteristics like sets, repetitions, and length, the system shows a many-to-many link between workouts and exercises.
---

## Installation Instructions

### 1. Clone the repository

```bash
git clone git@github.com:ctrlrobb/FLASK-WORKOUT-LAB-WK5.git
cd FLASK-WORKOUT-LAB-WK5
```

### 2. Install dependencies

```bash
pipenv install
```

### 3. Activate virtual environment

```bash
pipenv shell
```

---

## Database Setup

### Run migrations

```bash
export FLASK_APP=server.app
flask db upgrade
```

### Seed the database with sample data

```bash
python3 -m server.seed
```

---

##  Running the Application

Start the server:

```bash
python3 -m server.app
```

The API will run on:

```
http://127.0.0.1:5555
```

---

## API Endpoints

### Workouts

#### GET /workouts

Returns all workouts.

#### GET /workouts/<id>

Returns a specific workout.

#### POST /workouts

Creates a new workout.

Example:

```json
{
  "date": "2026-04-20",
  "duration_minutes": 60,
  "notes": "Full body training"
}
```

#### DELETE /workouts/<id>

Deletes a workout.

---

###  Exercises

#### GET /exercises

Returns all exercises.

#### GET /exercises/<id>

Returns a specific exercise.

#### POST /exercises

Creates a new exercise.

Example:

```json
{
  "name": "Bench Press",
  "category": "strength",
  "equipment_needed": true
}
```

#### DELETE /exercises/<id>

Deletes an exercise.

---

### WorkoutExercises (Join Table)

#### POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises

Adds an exercise to a workout with performance details.

Example:

```json
{
  "sets": 4,
  "reps": 10
}
```

OR

```json
{
  "duration_seconds": 90
}
```

---

##  Validations Implemented

### Table Constraints

* UniqueConstraint prevents duplicate workout-exercise pairs
* CheckConstraints ensure positive values for reps, sets, duration

### Model Validations


* Workout duration must be greater than 0
* Exercise name must not be blank
* Workout date cannot be in the future

### Schema Validations

* Exercise name must be at least 2 characters
* Category must be one of predefined values
* At least one of reps, sets, or duration_seconds must be provided

---

## 🧪 Testing

The API was tested using:

* curl
* Thunder Client / Postman

---

## Technologies Used

* Flask
* Flask-SQLAlchemy
* Flask-Migrate
* Marshmallow
* SQLite

---