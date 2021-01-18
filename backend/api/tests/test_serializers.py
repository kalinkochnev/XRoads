import pytest
from utils.serializers import DynamicModelSerializer
from api.models import Club, School


class SerializerStub(DynamicModelSerializer):
    class Meta:
        model = Club
        fields = '__all__'


StubBasic = SerializerStub.sub_serializer(
    fields=['name', 'description'])
StubBasic2 = SerializerStub.sub_serializer(
    fields=['name'], exclude=True
)

class SubStub(DynamicModelSerializer):
    clubs = StubBasic(many=True)

    class Meta:
        model = School
        fields = ['clubs']


class TestDynamicSerializer:
    def test_include(self, create_club):
        c1 = create_club()
        expected = {
            'name': c1.name,
            'description': c1.description,
        }
        assert StubBasic(c1).data == expected

    def test_exclude(self, create_club):
        c1 = create_club()
        excluded_fields = ['name']
        
        result = StubBasic2(c1).data
        assert len(set(result.keys()).intersection(set(excluded_fields))) == 0


    # This tests that you can use this as a field serializer in a different serializer
    def test_callable_field(self, district_school_club, create_club):
        d1, s1, c1 = district_school_club()
        c2 = create_club()
        s1.add_club(c2)

        expected = {
            'clubs': [
                {
                    'name': c1.name,
                    'description': c1.description,
                },
                {
                    'name': c2.name,
                    'description': c2.description,
                }
            ]
        }

        assert SubStub(s1).data == expected
