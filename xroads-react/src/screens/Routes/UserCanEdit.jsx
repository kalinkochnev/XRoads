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
            render={(props) => {
                if (state.user.loggedIn() && Role.canEditModel(state.user, modelName, other.computedMatch.params.id)) {
                    return <Component {...props} />;
                } else {
                    return <Redirect to="/clubs" />;
                }
            }}
        />
    );
}

export { CanEditRoute };
