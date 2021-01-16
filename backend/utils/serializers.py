from typing import Callable

from rest_framework import serializers

class DynamicModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed. `exclude` indicates whether 
    the fields specified should be excluded or included.
    """


    @classmethod
    def to_serializer(cls, fields, exclude=False) -> Callable: 
        """An alternate constructor to be used in serializers member different fields"""
        def decorator(*args, **kwargs):
            return cls(fields=fields, exclude=exclude, *args, **kwargs)
        return decorator

    def __init__(self, *args, **kwargs:dict):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', False)
        
        # Instantiate the superclass normally
        super(serializers.ModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            specified_fields = set(fields)
            existing = set(self.fields)

            if exclude:
                for field_name in specified_fields:
                    self.fields.pop(field_name)
            else:
                for field_name in existing - specified_fields:
                    self.fields.pop(field_name)