from XroadsAuth.permissions import Role
from XroadsAuth.models import HierarchyPerms

class TestPermissionSerializer:
    def test_highest_level_str(self, perm_const_override, create_test_prof, role_model_instances):
        prof = create_test_prof(1)
        district1, school1, club1 = role_model_instances()

        min_role = Role.from_start_model(school1)
        min_role.permissions.add('create-club')
        min_role.give_role(prof)

        hier_perm = HierarchyPerms.objects.get(perm_name=str(min_role))
        assert hier_perm.highest_level_str == 'School-1/perms=[create-club]'

    def test_serialize_permission(self, perm_const_override, create_test_prof, role_model_instances, role_test_data):
        district1, school1, club1 = role_model_instances()
        start_model = school1

        min_role = Role.from_start_model(start_model)
        min_role.permissions.add(*min_perms)

        # Case 6 -- Higher level access different district
        district_admin = create_test_prof(num=1)
        d2, s2, c1 = role_model_instances()

        invalid_role = Role.create(d2)
        invalid_role.give_role(district_admin)

        assert min_role.is_allowed(user=district_admin) is False