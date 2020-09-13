const { Role } = require("../../service/Roles");

const NOT_PERMITTED_EDIT = "User can't edit this object";
const SCHOOL_NOT_SELECTED = "User has not selected a school";
const NOT_AUTHENTICATED = "User has not authenticated";
const UNEXPECTED_ERROR = "An unexpected error occurred";

// ----------- Functions to be reused ---------------
const getCondRedirect = (reason) => {
    switch (reason) {
        case NOT_AUTHENTICATED:
            return '/login';
        case SCHOOL_NOT_SELECTED:
            return '/signup/school-select';
        case NOT_PERMITTED_EDIT:
            return '/clubs';
        case UNEXPECTED_ERROR:
        default:
            console.log(UNEXPECTED_ERROR);
            return '/error'
    }
}

const checkConditions = (conditions, args) => {
    try {
        for (let cond of conditions) {
            let [reason, allowed] = cond(args);
            if (!allowed) {
                return [reason, false];
            }
        }
    } catch (Error) {
        return [UNEXPECTED_ERROR,];
    }
}

// --------------------------------------------------


const isLoggedIn = ({state}) => {
    let allowed = state.user.loggedIn();
    return [NOT_AUTHENTICATED, allowed];
}

const userHasSchool = ({state}) => {
    let allowed = state.user.school != null
    return [SCHOOL_NOT_SELECTED, allowed]
}

const userCanEditClub = ({state, modelName, clubId}) => {
    let allowed = Role.canEditModel(state.user, modelName, clubId);
    return [NOT_PERMITTED_EDIT, allowed]
}

// Required args included: global state (included by default)
const userConditions = (args) => {
    const conditions = [
        isLoggedIn,
        userHasSchool
    ]

    return checkConditions(conditions, args)
}

export {userConditions, checkConditions, getCondRedirect}