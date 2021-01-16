import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import ScreenNotFound from "./Generic/NotFound";
import ErrorOcurred from "./Generic/Error";
import {SchoolRoutes} from "./Club/Routes";
import HelpRoutes from "./Generic/HelpRoutes";

const ScreensRoot = () => {  
  return (
    <Router>
      <Switch>
        <Route path="/:schoolSlug" component={SchoolRoutes} />
        <Route path="/help" component={HelpRoutes} />
        <Route exact path="/error" component={ErrorOcurred} />
        <Route component={ScreenNotFound} />
      </Switch>
    </Router>
  );
};

export default ScreensRoot;
