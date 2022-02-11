from api import Resource, abort, reqparse, auth
from api.models.tag import TagModel
from api.schemas.user import user_schema, users_schema, UserSchema, UserRequestSchema
from api.schemas.tag import TagSchema, TagRequestSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from webargs import fields

@doc(description='Api for notes.', tags=['Tags'])
class TagResourse(MethodResource):
    @marshal_with(TagSchema, code=200)
    @doc(summary="Get tag by id")
    def get(self, tag_id):
        tag = TagModel.query.get(tag_id)
        if tag is None:
            abort(404, error=f"Tag with id={tag_id} not found")
        return tag, 200

    @use_kwargs(UserRequestSchema, location=('json'))
    @marshal_with(TagSchema, code=201)
    def put(self, tag_id, **kwargs):
        tag_data = TagModel(**kwargs)
        tag = TagModel.query.get(tag_id)
        if tag is None:
            abort(404, error=f"Tag with id={tag_id} not found")
        tag.name = tag_data.name
        tag.save()
        return tag, 200

    def delete(self, tag_id):
        ...


@doc(description='Api for notes.', tags=['Tags'])
class TagsListResource(MethodResource):
    @marshal_with(TagSchema(many=True))
    def get(self):
        tags = TagModel.query.all()
        return tags, 200

    @doc(summary="Create new tag")
    @use_kwargs({"name": fields.Str(required=True)})
    # @use_kwargs(TagRequestSchema, location=('json'))
    @marshal_with(TagRequestSchema)
    def post(self, **kwargs):
        tag = TagModel(**kwargs)
        tag.save()
        return tag, 201

