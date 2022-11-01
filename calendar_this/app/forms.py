from flask_wtf import FlaskForm
from wtforms.fields import BooleanField, DateField, StringField, SubmitField, TextAreaField, TimeField
from wtforms.validators import DataRequired

class AppointmentForm(FlaskForm):
    name = StringField("name")
    start_datetimeD = DateField('start_date', validators=[DataRequired()])
    start_datetimeT = TimeField('start_time', validators=[DataRequired()])
    end_datetimeD = DateField('start_date', validators=[DataRequired()])
    end_datetimeT = TimeField('start_time', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    private = BooleanField('private')
    submit = SubmitField('Save')
