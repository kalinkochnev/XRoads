import pytest
from XroadsAuth.models import InvitedUser, Profile, RoleModel
from XroadsAuth.permissions import Role

class TestInvitedModel:
    def test_create(self, db, role_model_instances):
        d1, s1, c1 = role_model_instances()
        r1 = Role.from_start_model(c1)
        r1_model = RoleModel.from_role(r1)

        invited = InvitedUser.create("test@email.com", roles=[r1])
        assert invited.email == "test@email.com"
        assert list(invited.roles.all()) == [r1_model]

    def test_user_create_from_invited(self, role_model_instances):
        d1, s1, c1 = role_model_instances()
        d2, s2, c2 = role_model_instances()
        r1 = Role.from_start_model(c1)
        r2 = Role.from_start_model(c2)
        r1_model = RoleModel.from_role(r1)
        r2_model = RoleModel.from_role(r2)

        invited = InvitedUser.create(email="test@gmail.com", roles=[r1, r2])
        invited_roles = list(invited.roles.all())

        user = Profile.create_profile(email="test@gmail.com", password="password", first="a", last="b")
        assert invited_roles == list(user.roles.all())

        # Make sure the invited user model is deleted
        assert not InvitedUser.objects.filter(email="test@gmail.com").exists()
