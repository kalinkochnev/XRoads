import React, { createContext, useContext, useEffect, useReducer, useState } from 'react';
import { userReducer } from './User';
import { Cookies } from 'react-cookie'

export const StateContext = createContext();
export const StateProvider = ({ reducer, initialState, children }) => {
    let [state, dispatch] = useReducer(reducer, initialState);
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
            school: new Cookies().get("school"),
            // email: new Cookies().get('email')
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