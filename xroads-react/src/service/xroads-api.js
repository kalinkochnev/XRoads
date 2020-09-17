import InvalidKeysProvided from '../utils/exceptions';
import {isEqual} from '../utils/arrays';
import { Cookies } from 'react-cookie';

// To have keyworded args use this format:   :keyword_arg
const endpoint_templates = {
    'login': '/auth/login/',
    'logout': '/auth/logout/',
    'signup': '/auth/registration/',
    'club_list': '/api/district/:districtId/school/:schoolId/club/',
    'club_detail': '/api/district/:districtId/school/:schoolId/club/:clubId',
    'user_detail': '/auth/user/',
    'join_club': '/api/district/:districtId/school/:schoolId/club/:clubId/join_club/',
    'leave_club': '/api/district/:districtId/school/:schoolId/club/:clubId/leave_club/',
    'school_list': '/api/district/:districtId/school/',
    'join_school': '/api/district/:districtId/school/:schoolId/join_school/',
    'ask_question': '/api/district/:districtId/school/:schoolId/club/:clubId/ask_question/',

    'answer_question': '/api/admin/district/:districtId/school/:schoolId/club/:clubId/answer_question/',
    'toggle_hide_club': '/api/admin/district/:districtId/school/:schoolId/club/:clubId/toggle_hide/',
    'admin_club_detail': '/api/admin/district/:districtId/school/:schoolId/club/:clubId',
    'get_questions': '/api/admin/district/:districtId/school/:schoolId/club/:clubId/questions/',
};

function fillTemplate(urlName, urlArgs) {
    let template = endpoint_templates[urlName];

    let items = template.split("/");
    let urlFragments = [];
    for (var item of items) {
        if (item !== '') {
            urlFragments.push(item)
        }
    }

    let newUrl = "";
    for (var part of urlFragments) {
        if (part.charAt(0) === ":") {
            newUrl += "/" + urlArgs[part.substring(1, part.length)];
        } else {
            newUrl += "/" + part;
        }
    }
    return newUrl + '/';
}

function getUrl(urlName, urlArgs) {
    return process.env.REACT_APP_XROADS_API_ENDPOINT + fillTemplate(urlName, urlArgs);
}


/**
 * Generates a Fetch confiugration object so we can share headers
 * @method generateFetchConfig
 * @param  {string}            method      HTTP verb
 * @param  {object}            [body=null] payload for post/put
 * @return {object}                        config
 */
function generateFetchConfig(method, body = null) {
    const upCasedMethod = method.toUpperCase();

    let config = {
        method: upCasedMethod,
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        credentials: 'same-origin'
    };

    if (['POST', 'PUT'].includes(upCasedMethod)) {
        // Get the CSRF token from the cookies
        // config.headers = new Cookies().get('')
        config.body = JSON.stringify(body);
    }
    return config;
}

export async function sendRequest(urlName, urlArgs, method, body = null) {
    return await fetch(getUrl(urlName, urlArgs), generateFetchConfig(method, body));
}

export function fetchClubs(districtId, schoolId) {
    return sendRequest('club_list', { 'districtId': districtId, 'schoolId': schoolId }, 'GET');
}

export function fetchClub(districtId, schoolId, clubId) {
    return sendRequest('club_detail', { 'districtId': districtId, 'schoolId': schoolId, 'clubId': clubId }, 'GET');
}

export function signup(formData) {
    let requiredKeys = ['email', 'first_name', 'last_name', 'password1', 'password2']
    if (!isEqual(Object.keys(formData), requiredKeys)) {
        throw InvalidKeysProvided('The signup form did not have the right values')
    }
    return sendRequest('signup', {}, 'POST', formData, false);
}

export function updateClub(districtId, schoolId, clubId, updatedClub) {
    return sendRequest('admin_club_detail', { 'districtId': districtId, 'schoolId': schoolId, 'clubId': clubId }, 'PUT', updatedClub);
}

export function removeAuthCookies() {
    let cookies = new Cookies();
    cookies.remove('JWT-SIGNATURE', { path: '/' });
    cookies.remove('JWT-HEADER-PAYLOAD', { path: '/' });
}

export function login(formData) {
    removeAuthCookies();
    
    let requiredKeys = ['email', 'password', 'remember_me']
    if (!isEqual(Object.keys(formData), requiredKeys)) {
        throw InvalidKeysProvided('The login form did not have the right keys')
    }
    return sendRequest('login', {}, 'POST', formData);
}
