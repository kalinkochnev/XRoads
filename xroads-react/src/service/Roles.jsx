export class Permissions {
    constructor(permissions) {
        this.permissions = permissions
    }

    static fromStr(permStr) {
        let perms = permStr.split('=')[1].replace('[', '').replace(']', '').split(',')
        return new Permissions(perms);
    }

}

export class Role {
    constructor(model, id) {
        this.permissions = new Permissions()
        this.model = model;
        this.id = id;
    }

    static fromStr(roleStr) {
        let chunks = roleStr.split('/');
        let modelChunks = chunks[0].split('-');

        let model = modelChunks[0];
        let id = modelChunks[1];
        let role = new Role(model, id);
        role.permissions = Permissions.fromStr(chunks[1]);
        return role;
    }

    static canEditModel(user, modelName, instanceId) {
        let roles = user.roles;
        if (roles.length > 0 ) {
            for (let role of roles) {
                if (role.model.localeCompare(modelName) == 0 && role.id == instanceId) {
                    return true;
                }
            }
        }
        return false;
    }

}


export default {Role, Permissions};