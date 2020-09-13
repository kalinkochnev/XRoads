import React from "react";
import { Route, Redirect } from "react-router-dom";
import { Role } from "../../service/Roles";
import { useStateValue } from "../../service/State";
import { AuthRoute } from "./AuthenticatedRoute"

const CanEditRoute = ({ component: Component, modelName, ...other }) => {
    const [state, dispatch] = useStateValue();

    return (
        <Route
            {...other}
            render={(compProps) => <Component {...compProps} />}
        />
    );
}

export { CanEditRoute };
