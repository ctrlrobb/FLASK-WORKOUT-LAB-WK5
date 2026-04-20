from datetime import date
from server.app import app
from server.models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    # Clear already existing data
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    # Create sample exercises
    push_up = Exercise(
        name='Push Up',
        category='strength',
        equipment_needed=False
    )

    squat = Exercise(
        name='Squat',
        category='strength',
        equipment_needed=False
    )

    plank = Exercise(
        name='Plank',
        category='core',
        equipment_needed=False
    )

    treadmill_run = Exercise(
        name='Treadmill Run',
        category='cardio',
        equipment_needed=True
    )

    # Create sample workouts
    workout1 = Workout(
        date=date(2026, 4, 16),
        duration_minutes=40,
        notes='Upper body and core session'
    )

    workout2 = Workout(
        date=date(2026, 4, 15),
        duration_minutes=30,
        notes='Quick cardio workout'
    )

    # Saving exercises and workouts to the database
    db.session.add_all([push_up, squat, plank, treadmill_run, workout1, workout2])
    db.session.commit() 

    # Create join table records to link exercises to workouts
    we1 = WorkoutExercise(
        workout_id=workout1.id,
        exercise_id=push_up.id,  
        sets=3,
        reps=12
    )

    we2 = WorkoutExercise(
        workout_id=workout1.id,
        exercise_id=plank.id,
        duration_seconds=60
    )

    we3 = WorkoutExercise(
        workout_id=workout2.id,
        exercise_id=treadmill_run.id,
        duration_seconds=900
    )

    we4 = WorkoutExercise(
        workout_id=workout2.id,
        exercise_id=squat.id,
        sets=3,
        reps=15
    )

    # Saving join table records to the database
    db.session.add_all([we1, we2, we3, we4])
    db.session.commit()

    print("Database seeded successfully!")