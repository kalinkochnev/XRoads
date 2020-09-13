import React, { createContext, useContext, useEffect, useReducer, useState } from 'react';
import { logout, loggedIn, detailFromData, userReducer, editableClubs } from './User'
import { sendRequest } from './xroads-api';

export const StateContext = createContext();
export const StateProvider = ({ reducer, initialState, children }) => {
    let [state, dispatch] = useReducer(reducer, initialState);
    useEffect( () => {
        const loadUser = async () => {
            if (state.user.loggedIn()) {
                let response = await sendRequest('user_detail', {}, 'GET');
                if (response.ok) {
                    let body = await response.json();
                    dispatch({type: 'load detail', payload: body})
                } else if (response.status == 401) {
                    dispatch({type: 'logout'})
                }
            }
            
        }
        loadUser()
        
    }, []);
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
            joinedClubs: [],
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