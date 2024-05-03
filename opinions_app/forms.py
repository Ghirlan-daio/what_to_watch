from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, Optional


class OpinionForm(FlaskForm):
    """Форма для добавления пользователями новых мнений."""
    title = StringField(
        "Введите название фильма",
        validators=[DataRequired(message="Обязательное поле"),
                    Length(1, 128)]
    )
    text = TextAreaField(
        "Добавьте мнение о фильме",
        validators=[DataRequired(message="Обязательно поле")]
    )
    source = URLField(
        "Добавьте ссылку на подробный разбор фильма",
        validators=[Length(1, 256), Optional()]
    )
    submit = SubmitField("Добавить")
