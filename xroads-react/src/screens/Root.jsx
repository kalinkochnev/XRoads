import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import ScreenClubBrowser from "./Club/Browser";
import ScreenClubDetail from "./Club/Page";
import ScreenClubEdit from "./Club/Edit";

import ScreenNotFound from "./Generic/NotFound";
import ErrorOcurred from "./Generic/Error";

const ScreensRoot = () => {  
  return (
    <Router>
      <Switch>
        <Route exact path="/clubs/:id/edit/:code" component={ScreenClubEdit} />
        <Route exact path="/clubs/:id" component={ScreenClubDetail} />
        <Route exact path="/clubs" component={ScreenClubBrowser} />

        <Route exact path="/error" component={ErrorOcurred} />
        <Route component={ScreenNotFound} />
      </Switch>
    </Router>
  );
};

export default ScreensRoot;
