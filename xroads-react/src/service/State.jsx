import React, { createContext, useContext, useEffect, useReducer } from 'react';
import { logout, loggedIn, getUserDetail, userReducer, editableClubs } from './User'
import { sendRequest } from './xroads-api';

export const StateContext = createContext();
export const StateProvider = ({ reducer, initialState, children }) => {
    let [state, dispatch] = useReducer(reducer, initialState)

    console.log('State provider was used!')
    return (
        <StateContext.Provider value={[state, dispatch]}>
            {children}
        </StateContext.Provider>
    );

}

export const useStateValue = () => useContext(StateContext);


const AppState = ({children}) => {
    let initialState = {
        user: {
            loggedIn: () => loggedIn(),
            roles: [],
            school: null,
            district: null,
            firstName: '',
            lastName: '',
            email: '',
            editableClubs: (roles) => editableClubs(roles)
        }
    };

    const mainReducer = ({user}, action) => ({
        user: userReducer(user, action),
    });

    return (
        <StateProvider initialState={initialState} reducer={mainReducer}>
            {children}
        </StateProvider>
    );
}

export default AppState;