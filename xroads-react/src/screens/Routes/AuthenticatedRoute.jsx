import React from "react"
import {Route, useHistory} from "react-router-dom"

const AuthRoute = ({component: Component, authenticated: auth, ...other}) => {
    let history = useHistory();

    if (!auth) {
        history.replace('/login')
        return null;
    }
    return (<Route {...other} render={props => (<Component {...props} />)} ></Route>)
}

export {AuthRoute};