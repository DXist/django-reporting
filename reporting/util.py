from django.db.models.sql.constants import LOOKUP_SEP

def get_model_from_relation(field):
    if isinstance(field, models.related.RelatedObject):
        return field.model
    elif getattr(field, 'rel'): # or isinstance?
        return field.rel.to
    else:
        raise NotRelationField

def get_fields_from_path(model, path):
    """ Return list of Fields given path relative to model.

    e.g. (ModelX, "user__groups__name") -> [
        <django.db.models.fields.related.ForeignKey object at 0x...>,
        <django.db.models.fields.related.ManyToManyField object at 0x...>,
        <django.db.models.fields.CharField object at 0x...>,
    ]
    """
    pieces = path.split(LOOKUP_SEP)
    fields = []
    for piece in pieces:
        if fields:
            parent = get_model_from_relation(fields[-1])
        else:
            parent = model
        fields.append(parent._meta.get_field_by_name(piece)[0])
    return fields

