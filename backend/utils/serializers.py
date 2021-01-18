from typing import Callable

from rest_framework import serializers

class DynamicModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed. `exclude` indicates whether 
    the fields specified should be excluded or included.
    """


    @classmethod
    def sub_serializer(cls, fields, exclude=False) -> Callable: 
        """An alternate constructor that creates a serializer that is uninstantiated."""
        
        
        original_fields = cls().fields.keys()
        new_fields = set(fields)
        # Drop any fields that are not specified in the `fields` argument.

        if exclude:
            new_fields = original_fields - set(fields)

        class SubSerializer(cls):
            class Meta(cls.Meta):
                model = cls.Meta.model
                fields = list(new_fields)

        return SubSerializer
    

    def __init__(self, *args, **kwargs):
        """
        An initializer that takes an additional `fields` argument that
        controls which fields should be displayed.
        """
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(serializers.ModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)