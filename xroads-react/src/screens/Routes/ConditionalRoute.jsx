import React, { useEffect, useState } from "react";
import { Route, Redirect, useHistory } from "react-router-dom";
import { useStateValue } from "../../service/State";
import { getCondRedirect } from "./SharedConditions";

// This took a very long time to figure out. And could still use a lot of work. Freaking state and rerender issues
// that apparently nobody in the history of the world has ever dealt with. 

const ConditionalRoute = ({ component: Component, condition, conditionArgs = {}, ...other }) => {
    const [state, dispatch] = useStateValue();
    // This is used to see if there is a difference in state from the original load (initial state value)
    // to the current state value
    const [originalState, setState] = useState(state);
    
    conditionArgs.state = state;


    useEffect(() => {

    }, [state.user])

        
    return (
        <Route
            {...other}
            render={(props) => {
                // condition() is used to check if the user can access that page. On the initial load
                // This will always return false. We check that the original and new state are different
                // so we know the data (user state) has been loaded. Once that is the case, then we can redirect
                // without any issues. However, if the user is not logged in, current state never changes. 
                // We check that they are logged in (this does not rely on user state), if they are not, 
                // and they are not allowed to access the page, they are redirected anyways

                conditionArgs.match = props.match;
                let [reason, isAllowed] = condition(conditionArgs)
                if (isAllowed) {
                    return <Component {...props} />;

                } else if (state.user.email != "" || !state.user.loggedIn()) {
                    return <Redirect to={getCondRedirect(reason)}/>;
                }
            }}
        />
    );
    
};

export { ConditionalRoute };
