const userReducer = (state, action) => {
    switch (action.type) {
        // case 'logged in': Example
        //     return {...state, ...loggedIn()}
        case 'set school': 
            return {...state, school: action.payload}
        default:
            return state;
    }
}

export { userReducer };