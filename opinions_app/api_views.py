from flask import jsonify, request

from . import app, db
from .models import Opinion
from .views import random_opinion
from .error_handlers import InvalidAPIUsage


@app.route("/api/opinions/<id>/", methods=["GET"])
def get_opinion(id: int):
    opinion = Opinion.query.get(id)
    if opinion is None:
        raise InvalidAPIUsage("Мнение с указанным id не найдено", 404)
    return jsonify({"opinion": opinion.to_dict()}), 200


@app.route("/api/opinions/<id>/", methods=["PATCH"])
def update_opinion(id: int):
    data = request.get_json()

    if (
        "text" in data
        and Opinion.query.filter_by(text=data["text"]).first() is not None
    ):
        raise InvalidAPIUsage("Такое мнение уже есть в Базе.")

    opinion = Opinion.query.get(id)
    if opinion is None:
        raise InvalidAPIUsage("Мнение с указанным id не найдено", 404)
    opinion.title = data.get("title", opinion.title)
    opinion.text = data.get("text", opinion.text)
    opinion.source = data.get("source", opinion.source)
    opinion.added_by = data.get("added_by", opinion.added_by)
    db.session.commit()
    return jsonify({"opinion": opinion.to_dict()}), 201


@app.route("/api/opinions/<id>/", methods=["DELETE"])
def delete_opinion(id: int):
    opinion = Opinion.query.get(id)
    if opinion is None:
        raise InvalidAPIUsage("Мнение с указанным id не найдено", 404)
    db.session.delete(opinion)
    db.session.commit()
    return "", 204


@app.route("/api/opinions/", methods=["GET"])
def get_all_opinions():
    opinions = Opinion.query.all()
    opinions_list = [opinion.to_dict() for opinion in opinions]
    return jsonify({"opinions": opinions_list}), 200


@app.route("/api/opinions/", methods=["POST"])
def add_opinion():
    data = request.get_json()

    if "title" not in data or "text" not in data:
        raise InvalidAPIUsage("В запросе отсутствуют обязательные поля.")

    if Opinion.query.filter_by(text=data["text"]).first() is not None:
        raise InvalidAPIUsage("Такое мнение уже есть в Базе.")

    opinion = Opinion()
    opinion.from_dict(data)
    db.session.add(opinion)
    db.session.commit()
    return jsonify({"opinion": opinion.to_dict()}), 201


@app.route("/api/get-random-opinion/", methods=["GET"])
def get_random_opinion():
    opinion = random_opinion()
    if opinion is not None:
        return jsonify({"opinion": opinion.to_dict()}), 200
    raise InvalidAPIUsage("В Базе нет мнений", 404)
