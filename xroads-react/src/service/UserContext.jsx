import React from "react";
import { useState } from "react";
import { Cookies } from "react-cookie";

class User {
    constructor() {
        this.loggedIn = false;
        this.permissions = [];
        
        this.school = null;
        this.district = null;
        this.firstName = '';
        this.lastName = '';

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