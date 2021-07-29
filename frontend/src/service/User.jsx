import { Cookies } from 'react-cookie'

const userReducer = (state, action) => {
    switch (action.type) {
        // case 'logged in': Example
        //     return {...state, ...loggedIn()}
        case 'set school': 
            new Cookies().set('school', action.payload)
            return {...state, school: action.payload}
        // case 'set email': 
        //     new Cookies().set('email', action.payload)
        //     return {...state, email: action.payload}
        default:
            return state;
    }
}

export { userReducer };