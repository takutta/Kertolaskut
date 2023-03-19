from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, DecimalField, validators
from wtforms.validators import Optional, ValidationError
from flask import flash


class IndexForm(FlaskForm):
    pelaaja = RadioField("Pelaaja", validators=[Optional()])
    vanha = RadioField("Vanha", validators=[Optional()])
    # moodi = RadioField(
    #     "Moodi", choices=[("tasot", "Tasot"), ("seikkailu", "Seikkailu")]
    # )
    submit = SubmitField("Aloita")

    def validate(self, extra_validators=None):
        if not super(IndexForm, self).validate(extra_validators):
            return False

        if self.pelaaja.data is None and self.vanha.data is None:
            self.pelaaja.errors.append("Valitse pelaaja.")
            return False

        return True


class CalcForm(FlaskForm):
    answer = DecimalField(
        "Answer", validators=[validators.InputRequired(), validators.NumberRange(min=0)]
    )
    submit = SubmitField("Lähetä")
