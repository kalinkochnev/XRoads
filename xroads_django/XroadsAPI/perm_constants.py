# Permission names
all_crud_district_perm = ('_district_all_crud_perm', 'Can modify all district data')
all_crud_school_perm = ('_school_all_crud_perm', 'Can modify all school data')
school_club_perm = ('_club_edit', 'Can modify club')


# Permissions associated with groups
district_group_permissions = [all_crud_district_perm]
school_group_permissions = [all_crud_school_perm]
club_group_permissions = [school_club_perm]

# Group Names
DISTRICT_MOD = 'district_super'
SCHOOL_MOD = 'school_super'
CLUB_EDITOR = 'club_editor'

# Groups and permission list mappings
district_permissions_group = {
    DISTRICT_MOD: district_group_permissions,
    SCHOOL_MOD: school_group_permissions,
    CLUB_EDITOR: club_group_permissions,
}
