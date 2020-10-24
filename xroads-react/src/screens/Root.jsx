import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";

import ScreenClubBrowser from "./Club/Browser";
import ScreenClubDetail from "./Club/Page";
import ScreenClubEdit from "./Club/Edit";

import ScreenNotFound from "./Generic/NotFound";
import ErrorOcurred from "./Generic/Error";
import ClubCode from "../components/Club/Edit/ClubCode";

const ScreensRoot = () => {  
  return (
    <Router>
      <Switch>
        <Route exact path="/school/:schoolId" component={ScreenClubBrowser} />
        <Route exact path="/school/:schoolId/clubs/:clubId" component={ScreenClubDetail} />
        <Route exact path="/school/:schoolId/clubs/:clubId/edit/:code" component={ScreenClubEdit} />
        <Route exact path="/school/:schoolId/club/edit" component={ClubCode} />

        <Route exact path="/error" component={ErrorOcurred} />
        <Route component={ScreenNotFound} />
      </Switch>
    </Router>
  );
};

export default ScreensRoot;
