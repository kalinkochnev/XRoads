import React, { useEffect } from 'react';
import { Route, Switch, useRouteMatch } from 'react-router-dom';
import { SlideHelp } from '../../components/Help/Help';
import HelpNavigation from '../../components/Help/Navigation';


const HelpRoutes = ({ match: { params: { schoolId } } }) => {
    let { path, url } = useRouteMatch();

    return (
        <Switch>
            <Route exact path={path} component={HelpNavigation} />
            <Route exact path={`${path}/slides/`} component={SlideHelp} />
        </Switch>
    );
}

export default HelpRoutes;