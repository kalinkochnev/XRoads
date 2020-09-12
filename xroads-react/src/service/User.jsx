import {Role} from './Roles'
import { Cookies } from "react-cookie";
import { sendRequest, removeAuthCookies } from '../service/xroads-api';
import { isInteger } from 'formik';


const detailFromData = (data) => {
    return {
        roles: data.permissions.map(item => Role.fromStr(item)),
        school: data.school,
        district: data.district,
        firstName: data.first_name,
        lastName: data.last_name,
        email: data.email,
        joinedClubs: data.joined_clubs
    }
}

const login = (responseData) => {
    return {...detailFromData(responseData.user)};
}

const logout = () => {
    removeAuthCookies();
}


const loggedIn = () => {
    let cookies = new Cookies();

    // Only need to check if Header Payload is null since js can't access the signature
    return cookies.get('JWT-HEADER-PAYLOAD') != null
}

const editableClubs = (roles) => {
    if (roles.length > 0 ) {
        let clubRoles = roles.filter(role => role.model.localeCompare('Club') == 0);
        return clubRoles.map(role => Number(role.id));
    }
    return [];
}

const joinClub = (joinedClubs, clubId) => {
    joinedClubs.push(clubId)
    return {joinedClubs: joinedClubs};
}

const leaveClub = (joinedClubs, clubId) => {
    return {joinedClubs: joinedClubs.filter(item => item !== clubId)};
}

const userReducer = (state, action) => {
    switch (action.type) {
        case 'logged in': 
            return {...state, ...loggedIn()}
        case 'load detail': 
            return {...state, ...detailFromData(action.payload)}
        case 'login':
            return {...state, ...login(action.payload)}
        case 'logout':
            return {...state, ...logout()}
        case 'join club': 
            return {...state, ...joinClub(state.joinedClubs, action.payload)};
        case 'leave club':
            return {...state, ...leaveClub(state.joinedClubs, action.payload)};
        default:
            return state;
    }
}

export { loggedIn, userReducer, detailFromData, editableClubs, logout};