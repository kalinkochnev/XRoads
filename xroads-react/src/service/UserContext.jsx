import React from "react";
import { useState } from "react";
import { Cookies } from "react-cookie";
import { sendRequest, removeAuthCookies } from '../service/xroads-api';
import { useEffect } from "react";


class Permissions {
    constructor(permissions) {
        this.permissions = permissions
    }

    static fromStr(permStr) {
        let perms = permStr.split('=')[1].replace('[', '').replace(']', '').split(',')
        return new Permissions(perms);
    }

}

class Role {
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

}

class User {
    constructor() {
        this.loggedIn = false;
        this.roles = [];
        
        this.school = null;
        this.district = null;
        this.firstName = '';
        this.lastName = '';
        this.email = '';

        this.checkLoggedIn();
    }

    checkLoggedIn() {
        let cookies = new Cookies();
        // Only need to check if Header Payload is null since js can't access the signature
        if (cookies.get('JWT-HEADER-PAYLOAD') == null) {
            this.loggedIn = false;
        } else {
            this.loggedIn = true;
        }

        if (this.loggedIn) {
            this.getUserDetail()
        }
    }

    getUserDetail() {
        sendRequest('user_detail', {}, 'GET').then(response => {
            if (response.ok) {
                response.json().then(body => {
                    this.loadUserDetail(body);
                });
            } else if (response.status == 401) {
                this.logout()
            }
        });
    }

    get editableClubs() {
        if (this.roles.length > 0 ) {
            let clubRoles = this.roles.filter(role => role.model.localeCompare('Club') == 0);
            return clubRoles.map(role => Number(role.id));
        }
        return [];
    }

    logIn(response) {
        this.loggedIn = true;
        response.json().then(body => {
            this.loadUserDetail(body.user);
        });
    }

    logout() {
        this.loggedIn = false;
        removeAuthCookies();
    }

    loadUserDetail(data) {
        this.roles = data.permissions.map(item => Role.fromStr(item));
        this.school = data.school;
        this.district = data.district;
        this.firstName = data.first_name;
        this.lastName = data.last_name;
        this.email = data.email;
    }

}

const UserContext = React.createContext();

const UserProvider = (props) => {
    const [user, setUser] = useState(new User());

    useEffect(() => {
        user.checkLoggedIn();
    }, [user])

    return (
        <UserContext.Provider value={[user, setUser]}>
            {props.children}
        </UserContext.Provider>
    )
}
export {User, UserProvider, UserContext};