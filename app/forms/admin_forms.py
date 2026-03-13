from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FileField, TextAreaField, DecimalField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

class CategoryForm(FlaskForm):
    name = StringField(
        "Nombre de la categoría",
        validators=[DataRequired(), Length(min=2, max=100)]
    )
    submit = SubmitField("Crear categoría")

class OptionForm(FlaskForm):
    name = StringField("Nombre de la opción", validators=[DataRequired()])
    category = SelectField("Categoría", coerce=int, validators=[DataRequired()])
    image = FileField("Imagen", validators=[Optional()])
    price_modifier = DecimalField(
        "Costo adicional",
        validators=[Optional(), NumberRange(min=0)],
        default=0
    )
    submit = SubmitField("Crear opción")

class ProductForm(FlaskForm):
    name = StringField("Nombre del producto", validators=[DataRequired(), Length(min=2, max=120)])
    description = TextAreaField("Descripción", validators=[Optional()])
    base_price = DecimalField("Precio base", validators=[DataRequired(), NumberRange(min=0)])
    image = FileField("Imagen del producto", validators=[Optional()])
    submit = SubmitField("Crear producto")

class SimpleSubmitForm(FlaskForm):
    submit = SubmitField("Confirmar")