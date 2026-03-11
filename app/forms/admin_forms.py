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
    submit = SubmitField("Crear opción")


class ProductForm(FlaskForm):
    name = StringField("Nombre del producto", validators=[DataRequired(), Length(min=2, max=120)])
    description = TextAreaField("Descripción", validators=[Optional()])
    base_price = DecimalField("Precio base", validators=[DataRequired(), NumberRange(min=0)])
    image_url = StringField("URL de imagen", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Crear producto")