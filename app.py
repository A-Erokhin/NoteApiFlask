from api import api, app, docs
from api.resources.note import NoteResource, NotesListResource, NoteAddTagResource, NotesFilterResource
from api.resources.user import UserResource, UsersListResource
from api.resources.auth import TokenResource
from api.resources.tag import TagResourse, TagsListResource
from config import Config

# CRUD

# Create --> POST
# Read --> GET
# Update --> PUT
# Delete --> DELETE
api.add_resource(UsersListResource,
                 '/users')  # GET, POST
api.add_resource(UserResource,
                 '/users/<int:user_id>')  # GET, PUT, DELETE

api.add_resource(TokenResource,
                 '/auth/token')  # GET

api.add_resource(NotesListResource,
                 '/notes',  # GET, POST
                 )
api.add_resource(NoteResource,
                 '/notes/<int:note_id>',  # GET, PUT, DELETE
                 )
api.add_resource(NoteAddTagResource,
                 '/notes/<int:note_id>/tags',  # GET, PUT, DELETE
                 )
api.add_resource(NotesFilterResource,
                 '/notes/filter',  # GET
                 )
api.add_resource(TagsListResource,
                 '/tags', # GET, POST
                 )
api.add_resource(TagResourse,
                 '/tags/<int:tag_id>',  # GET, PUT, DELETE
                 )

docs.register(UserResource)
docs.register(UsersListResource)
docs.register(NoteResource)
docs.register(NotesListResource)
docs.register(NoteAddTagResource)
docs.register(NotesFilterResource)
docs.register(TagResourse)
docs.register(TagsListResource)

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
