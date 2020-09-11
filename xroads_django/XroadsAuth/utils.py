from rest_framework import serializers

def get_parent_model(child, parent):
    """If a model instance has a many to many or many to one relationship 
    it will go up to the parent and return the model instance
    """
    # In District-1/School-3/  School-3 is the inner model, District-1 is the outer model
    m2m_query = f'{parent.__class__.__name__.lower()}__in'
    m2m_value = [parent]

    args = {
        'id': child.id,
        m2m_query: m2m_value,
    }

    return child.__class__.objects.get(**args)

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
