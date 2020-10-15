import React, { createContext, useContext, useEffect, useReducer, useState } from 'react';

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
            school: null,
            district: null,
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