from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Length, Optional


class CategoryForm(FlaskForm):
    name = StringField("Nombre de la categoría", validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])
    submit = SubmitField("Crear categoría")

class OptionForm(FlaskForm):
    name = StringField("Nombre de la opción", validators=[DataRequired()])
    category = SelectField("Categoría", coerce=int, validators=[DataRequired()])
    image = FileField("Imagen", validators=[Optional()])
    submit = SubmitField("Crear opción")