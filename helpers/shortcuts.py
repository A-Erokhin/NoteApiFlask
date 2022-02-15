from api import abort

def get_or_404(model, id):
    obj = model.query.get(id)
    if not obj:
        abort(404, error=f"{model.__name__} with id {id} not found")
    return obj