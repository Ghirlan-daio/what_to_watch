from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import OpinionForm
from .models import Opinion


def random_opinion():
    quantity = Opinion.query.count()
    if quantity:
        offset_value = randrange(quantity)
        opinion = Opinion.query.offset(offset_value).first()
        return opinion


@app.route("/")
def index_view():
    """Главный экран. Демонстрирует случайное мнение о фильме."""
    opinion = random_opinion()
    if opinion is not None:
        return render_template("opinion.html", opinion=opinion)
    abort(404)


@app.route("/add", methods=["GET", "POST"])
def add_opinion_view():
    """Страница добавления мнения."""
    form = OpinionForm()
    if form.validate_on_submit():
        text = form.text.data
        if Opinion.query.filter_by(text=text).first() is not None:
            flash("Такое мнение уже было оставлено ранее!")
            return render_template("add_opinion.html", form=form)
        opinion = Opinion(
            title=form.title.data,
            text=form.text.data,
            source=form.source.data
        )
        db.session.add(opinion)
        db.session.commit()
        # Переход на страницу добавленного мнения.
        return redirect(url_for("opinion_view", id=opinion.id))
    return render_template("add_opinion.html", form=form)


@app.route("/opinions/<int:id>")
def opinion_view(id):
    """Позволяет сформировать ссылку на мнение."""
    opinion = Opinion.query.get_or_404(id)
    return render_template("opinion.html", opinion=opinion)