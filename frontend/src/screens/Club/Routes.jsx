import React, { useEffect, useState } from 'react';
import { Route, Switch, useRouteMatch } from 'react-router-dom';
import ClubCode from '../../components/Club/Edit/ClubCode';
import { useStateValue } from '../../service/State';
import ScreenClubBrowser from './Browser';
import ScreenClubEdit from './Edit';
import ScreenClubDetail from './Page';

const ClubContext = React.createContext([{}, () => { }])
const ClubProvider = (props) => {
    const [club, setClub] = useState({});
    return (
        <ClubContext.Provider value={[club, setClub]}>
            {props.children}
        </ClubContext.Provider>
    );
}

const SchoolRoutes = ({ match: { params: { schoolSlug } } }) => {
    let { path, url } = useRouteMatch();
    const [state, dispatch] = useStateValue();

    useEffect(() => {
        dispatch({ type: 'set school', payload: schoolSlug })
    }, [])

    return (
        <Switch>
            <Route exact path={path} component={ScreenClubBrowser} />
            <ClubProvider>
                {/* TODO make this url set the code into state and redirect to edit page*/}
                <Route exact path={`${path}/edit-code/`} component={ClubCode} />
                <Route exact path={`${path}/:clubSlug/edit`} component={ScreenClubEdit} />
                <Route exact path={`${path}/:clubSlug/`} component={ScreenClubDetail} />

            </ClubProvider>
            

        </Switch>
    );
}

export { SchoolRoutes, ClubProvider, ClubContext };
