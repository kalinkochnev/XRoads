import React from "react";
import { useState } from "react";

class User {
    constructor() {
        this.loggedIn = false;
        this.permissions = [];
        
        
        this.school = null;
        this.district = null;
        this.followed_clubs = [];
        console.log(this);
    }

    logIn() {
        this.loggedIn = true;
    }

    logout() {
        this.loggedIn = false;
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