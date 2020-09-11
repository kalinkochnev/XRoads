import React from "react";
import { Route, Redirect } from "react-router-dom";
import { useStateValue } from "../../service/State";

const AuthRoute = ({ component: Component, ...other }) => {
  const [state, dispatch] = useStateValue();

  return (
    <Route
      {...other}
      render={(props) => {
        if (state.user.loggedIn()) {
          return <Component {...props} />;
        } else {
          return <Redirect to="/login" />;
        }
      }}
    />
  );
};

export { AuthRoute };
