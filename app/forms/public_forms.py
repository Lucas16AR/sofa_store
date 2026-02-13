from flask_wtf import FlaskForm
from wtforms import SubmitField


class ConfiguratorForm(FlaskForm):
    submit = SubmitField("Guardar Configuración")