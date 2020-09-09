import React from "react";
import { useState } from "react";

class User {
    constructor() {
        this.loggedIn = false;
        this.permissions = [];
        
        this.school = null;
        this.district = null;
        this.firstName = '';
        this.lastName = '';
    }

    logIn(response) {
        this.loggedIn = true;
        response.json().then(body => {
            this.loadUserDetail(body.user);
        });
    }

    logout() {
        this.loggedIn = false;
    }

    loadUserDetail(data) {
        this.permissions = data.permissions;
        this.school = data.school;
        this.district = data.district;
        this.firstName = data.first_name;
        this.lastName = data.last_name;
    }

}

const UserContext = React.createContext();

const UserProvider = (props) => {
    const [user, setUser] = useState(new User());
    return (
        <UserContext.Provider value={[user, setUser]}>
            {props.children}
        </UserContext.Provider>
    )
}
export {User, UserProvider, UserContext};