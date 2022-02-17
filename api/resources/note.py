from api import auth, abort, g, Resource, reqparse, db
from api.models.note import NoteModel
from api.models.tag import TagModel
from api.schemas.note import note_schema, notes_schema, NoteSchema
from flask_apispec import marshal_with, use_kwargs, doc
from flask_apispec.views import MethodResource
from webargs import fields
from sqlalchemy import or_
from helpers.shortcuts import get_or_404

@doc(description='Api for notes.', tags=['Notes'])
class NoteResource(MethodResource):
    @doc(security=[{"basicAuth": []}])
    @marshal_with(NoteSchema)
    @auth.login_required
    def get(self, note_id):
        """
        Пользователь может получить ТОЛЬКО свою заметку
        """
        author = g.user
        # note = get_or_404(NoteModel, note_id)
        note = NoteModel.not_archived().get(note_id)
        if note.author != author:
            abort(403, error=f"Forbidden")
        if note is None:
            abort(404)
        return note, 200

    @doc(security=[{"basicAuth": []}])
    @auth.login_required
    def put(self, note_id):
        """
        Пользователь может редактировать ТОЛЬКО свои заметки
        """
        author = g.user
        parser = reqparse.RequestParser()
        parser.add_argument("text", required=True)
        parser.add_argument("private", type=bool)
        note_data = parser.parse_args()
        # note = NoteModel.query.get(note_id)
        # if not note:
        #     abort(404, error=f"note {note_id} not found")
        note = get_or_404(NoteModel, note_id)
        if note.author != author:
            abort(403, error=f"Forbidden")
        note.text = note_data["text"]

        if note_data.get("private") is not None:
            note.private = note_data.get("private")

        note.save()
        return note_schema.dump(note), 200


    @doc(summary="Delete note", description="Note to archive")
    @doc(security=[{"basicAuth": []}])
    @auth.login_required
    def delete(self, note_id):
        auth_user = g.user  # Пользователь может удалять ТОЛЬКО свои заметки
        note = get_or_404(NoteModel, note_id)
        if auth_user != note.author:
            abort(403)
        note.delete()
        return {}, 204 # no content
    #
    # def to_archive(self, note_id):
    #     note = NoteModel.query.get(note_id)
    #     if note is None:
    #         return f"Note with id {note_id} not found", 404
    #     note = get_or_404(NoteModel, note_id)
    #     note.archived = True
    #     note.save()
    #     return f"Note with id {note_id} send to archive", 200

@doc(description='Api for notes.', tags=['Notes'])
class NoteRestoreResourse(MethodResource):

    # @auth.login_required
    @doc(summary="Recovery note from archive")
    @marshal_with(NoteSchema)
    def put(self, note_id):
        note = get_or_404(NoteModel, note_id)
        note.restore()
        return note, 200


@doc(description='Api for notes.', tags=['Notes'])
class NotesListResource(MethodResource):
    def get(self):
        notes = NoteModel.not_archived().query.all()
        return notes_schema.dump(notes), 200

    @doc(security=[{"basicAuth": []}])
    @auth.login_required
    def post(self):
        author = g.user
        parser = reqparse.RequestParser()
        parser.add_argument("text", required=True)
        # Подсказка: чтобы разобраться с private="False",
        #   смотрите тут: https://flask-restful.readthedocs.io/en/latest/reqparse.html#request-parsing
        parser.add_argument("private", type=bool, required=True)
        note_data = parser.parse_args()
        note = NoteModel(author_id=author.id, **note_data)
        note.save()
        return note_schema.dump(note), 201


@doc(tags=["Notes"])
class NoteAddTagResource(MethodResource):
    @doc(summary="Add tags to note")
    @use_kwargs({"tags": fields.List(fields.Int())})
    def put(self, note_id, **kwargs):
        # print("kwargs = ", kwargs)
        note = NoteModel.query.get(note_id)
        # TagModel.query.filter(TagModel.id.in_((2, 3))).all()
        for tag_id in kwargs["tags"]:
            tag = TagModel.query.get(tag_id)
            note.tags.append(tag)
        note.save()
        return {}



@doc(tags=["Notes"])
class NotesFilterResource(MethodResource):
    @doc(summary="Get notes by tags")
    @use_kwargs({"tags": fields.List(fields.Str())}, location=("query"))
    @marshal_with(NoteSchema, code=200)
    def get(self, **kwargs):
        notes = NoteModel.query.join(NoteModel.tags).filter(TagModel.name.in_(kwargs["tags"])).all()
        return notes, 200