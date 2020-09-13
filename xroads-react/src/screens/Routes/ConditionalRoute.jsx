import React from "react";
import { Route, Redirect } from "react-router-dom";
import { useStateValue } from "../../service/State";
import { getCondRedirect } from "./SharedConditions";

const ConditionalRoute = ({ component: Component, condition, conditionArgs = {}, ...other }) => {
    const [state, dispatch] = useStateValue();
    conditionArgs.state = state;

    if (state != null) {
        return (
            <Route
                {...other}
                render={(props) => {
                    let [reason, isAllowed] = condition(conditionArgs);
                    if (isAllowed) {
                        return <Component {...props} />;
                    } else {
                        return <Redirect to={getCondRedirect(reason)} />;
                    }
                }}
            />
        );
    }
    return null;
    
};

export { ConditionalRoute };
