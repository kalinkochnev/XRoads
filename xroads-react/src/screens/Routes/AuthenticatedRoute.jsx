import React from "react";
import { Route, useHistory, Redirect } from "react-router-dom";
import { useEffect } from "react";
import { useContext } from "react";
import { UserContext } from "../../service/UserContext";

const AuthRoute = ({ component: Component, ...other }) => {
  let [user, setUser] = useContext(UserContext);

  return (
    <Route
      {...other}
      render={(props) => {
        if (user.loggedIn) {
          return <Component {...props} />;
        } else {
          return <Redirect to="/login" />;
        }
      }}
    />
  );
};

export { AuthRoute };
