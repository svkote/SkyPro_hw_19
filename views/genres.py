from flask import request
from flask_restx import Resource, Namespace

from dao.model.genre import GenreSchema
from implemented import genre_service
from helpers.decorators import auth_required,admin_required

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        data = request.json
        new_genre = genre_service.create(data)
        return '', 201, {'location': f'/genres/{new_genre.id}'}


@genre_ns.route('/<int:rid>')
class GenreView(Resource):
    @auth_required
    def get(self, rid):
        r = genre_service.get_one(rid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @admin_required
    def post(self, rid):
        data = request.json

        if 'id' not in data:
            data['id'] = rid

        new_genre = genre_service.update(data)
        return '', 201, {'location': f'/genres/{new_genre.id}'}

    @admin_required
    def delete(self, rid):
        genre_service.delete(rid)
        return '', 204
