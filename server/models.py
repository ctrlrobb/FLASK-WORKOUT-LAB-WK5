from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint, UniqueConstraint
from datetime import date


db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = 'exercises'

# Table-level rule: exercise name must be longer than 1 character
    __table_args__ = (
        CheckConstraint("length(name) > 1", name = "check_exercise_name_length"),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False)

    # Relationship to access workouts an exercise is part of through the join table
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')

# Model-level validation to ensure exercise name is valid and category is one of the allowed categories
    @validates('name')
    def validate_name(self, key, value): 
        if not value or len(value) < 2:
            raise ValueError("Exercise name must be at lease 2 characterslong.")
        return value.strip()


# Model-level validation for category to ensure it is one of the allowed categories    
    @validates('category')
    def validate_category(self, key, value):
        allowed_categories = ['strength', 'cardio', 'mobility', 'flexibility', 'core']
        if not value:
            raise ValueError("Category is required.")
        value = value.strip().lower()
        if value not in allowed_categories:
            raise ValueError(f"Category must be one of: {', '.join(allowed_categories)}.")
        return value


class Workout(db.Model):
    __tablename__ = 'workouts'

# Table-level rule: workout duration must be greater than 0
    __table_args__ = (
        CheckConstraint("duration_minutes > 0", name = "check_duration_positive"),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    # Relationship to access exercises in a workout through the join table
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')

# Model-level validation to ensure workout duration: reject 0 or negative values
    @validates('duration_minutes')
    def validate_duration_minutes(self, key, value):
        if value is None or value <= 0:
            raise ValueError("Workout duration must be greater than 0. ")
        return value

        
    @validates('date')
    def validate_date(self, key, value):
        if value > date.today():
            raise ValueError("Workout date cannot be in the future.")
        return value


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    # Table-level rules to ensure clean data
    __table_args__ = (
        # Prevents same exercise from being added twice to the same workout
        UniqueConstraint('workout_id', 'exercise_id', name='unique_workout_exercise'),

        # Allow only positive or NULL values
        CheckConstraint('(reps IS NULL OR reps > 0)', name='check_reps_positive'),
        CheckConstraint('(sets IS NULL OR sets > 0)', name='check_sets_positive'),
        CheckConstraint('(duration_seconds IS NULL OR duration_seconds > 0)', name='check_duration_seconds_positive'),
    )

    id = db.Column(db.Integer, primary_key=True)

    # Foreign keys to link exercises and workouts
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)

    # fields to capture exercise details within a workout
    reps = db.Column(db.Integer, nullable=True)
    sets = db.Column(db.Integer, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)

# Relationships to easily access related data
# Each WorkoutExercise belongs to one Workout
    workout = db.relationship('Workout', back_populates='workout_exercises')

# Each WorkoutExercise belongs to one exercise
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    # Model-level validation to ensure data integrity
    @validates('reps')
    def validate_reps(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Reps must be greater than 0.")
        return value
    
    @validates('sets')
    def validate_sets(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Sets must be greater than 0 if provided.")
        return value


    @validates('duration_seconds')
    def validate_duration_seconds(self, key, value):
        if value is not None and value <= 0:
            raise ValueError("Duration in seconds must be greater than 0 if provided.")
        return value