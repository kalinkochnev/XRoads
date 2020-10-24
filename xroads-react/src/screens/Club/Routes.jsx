import React, { useEffect } from 'react';
import { Route, Switch, useRouteMatch } from 'react-router-dom';
import ClubCode from '../../components/Club/Edit/ClubCode';
import { useStateValue } from '../../service/State';
import ScreenClubBrowser from './Browser';
import ScreenClubEdit from './Edit';
import ScreenClubDetail from './Page';

const SchoolRoutes = ({ match: { params: { schoolId } } }) => {
    let { path, url } = useRouteMatch();
    const [state, dispatch] = useStateValue();

    useEffect(() => {
        dispatch({ type: 'set school', payload: schoolId })
    }, [])

    return (
        <Switch>
            <Route exact path={path} component={ScreenClubBrowser} />
            <Route exact path={`${path}/clubs/edit/`} component={ClubCode} />
            <Route exact path={`${path}/clubs/:clubId`} component={ScreenClubDetail} />
            <Route exact path={`${path}/clubs/:clubId/edit/:code`} component={ScreenClubEdit} />

        </Switch>
    );
}

export default SchoolRoutes;