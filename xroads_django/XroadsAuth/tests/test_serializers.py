from XroadsAuth.permissions import Role
from XroadsAuth.models import HierarchyPerms
from XroadsAuth.serializers import PermissionSerializer

class TestPermissionSerializer:
    def test_highest_level_str(self, perm_const_override, create_test_prof, role_model_instances):
        prof = create_test_prof(1)
        district1, school1, club1 = role_model_instances()

        role = Role.from_start_model(school1)
        role.permissions.add('create-club')
        role.give_role(prof)

        hier_perm = HierarchyPerms.objects.get(perm_name=str(role))
        assert hier_perm.highest_level_str == 'School-1/perms=[create-club]'

    def test_serialize_permission(self, perm_const_override, create_test_prof, role_model_instances):
        prof = create_test_prof(1)
        district1, school1, club1 = role_model_instances()

        role1 = Role.from_start_model(club1)
        role1.give_role(prof)
        hier_perm = HierarchyPerms.objects.get(perm_name=str(role1))

        
        """role2 = Role.from_start_model(school1)
        role1.give_role(prof)
        role3 = Role.from_start_model(district1)
        role1.give_role(prof)
        expected = [i.highest_level_str for i in prof.hierarchy_perms]"""

        expected = hier_perm.highest_level_str
        assert expected == PermissionSerializer(hier_perm).data