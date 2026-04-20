from marshmallow import (
    Schema,
    fields,
    validate,
    validates,
    validates_schema,
    ValidationError,
    pre_load
)


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=2))
    category = fields.Str(
        required=True,
        validate=validate.OneOf(['strength', 'cardio', 'mobility', 'flexibility', 'core'])
    )
    equipment_needed = fields.Bool(required=True)

    # Clean string input before validation
    @pre_load
    def clean_string_input(self, data, **kwargs):
        if 'name' in data and isinstance(data['name'], str):
            data['name'] = data['name'].strip()
        if 'category' in data and isinstance(data['category'], str):
            data['category'] = data['category'].strip().lower()
        return data

    # Extra validation for blank names
    @validates('name')
    def validate_name_not_blank(self, value):
        if not value.strip():
            raise ValidationError("Exercise name cannot be blank or spaces only.")


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str(allow_none=True)

    # Clean notes before validation
    @pre_load
    def clean_notes_input(self, data, **kwargs):
        if 'notes' in data and isinstance(data['notes'], str):
            data['notes'] = data['notes'].strip()
        return data


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(allow_none=True, validate=validate.Range(min=1))
    sets = fields.Int(allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Int(allow_none=True, validate=validate.Range(min=1))

    # Require at least one performance detail
    @validates_schema
    def validate_performance_details(self, data, **kwargs):
        reps = data.get('reps')
        sets = data.get('sets')
        duration_seconds = data.get('duration_seconds')

        if reps is None and sets is None and duration_seconds is None:
            raise ValidationError(
                "At least one of reps, sets, or duration_seconds must be provided."
            )


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)