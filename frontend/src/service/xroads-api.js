import { Cookies } from 'react-cookie';

// To have keyworded args use this format:   :keyword_arg
const endpoint_templates = {
    'club_list': '/api/school/:schoolSlug/',
    'club_detail': '/api/club/:clubSlug/',
    'club_edit': '/api/club/:code/:clubSlug/',
    
    'school_list': '/api/district/:districtId/',

    'toggle_hide_club': '/api/club/:code/:clubSlug/toggle_hide/',
    'check_code': '/api/school/:schoolSlug/club_code/',
    'club_email_info': '/api/club/:clubSlug/send_info/',

    'event_create': '/api/event/:clubSlug/:clubCode/',
    'event_edit': '/api/event/:clubSlug/:clubCode/:eventId/',

    'school_events': '/api/school/:schoolSlug/events/',
    'event_info': '/api/events/:eventId/info/'
};

function fillTemplate(urlName, urlArgs) {
    let template = endpoint_templates[urlName];
    for (var arg of Object.keys(urlArgs)) {
        template = template.replace(`:${arg}`, urlArgs[arg])
    }
    // console.log(template)
    return template;
}

function getUrl(urlName, urlArgs) {
    return "https://xroads.club/backend" + fillTemplate(urlName, urlArgs);
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
        credentials: 'same-origin',
        // mode: 'no-cors'
    };

    if (['POST', 'PUT', 'PATCH'].includes(upCasedMethod)) {
        // Get the CSRF token from the cookies
        config.headers['X-CSRFToken'] = new Cookies().get('csrftoken')
        config.body = JSON.stringify(body);
    }
    return config;
}

export async function sendRequest(urlName, urlArgs, method, body = null, query_params = null) {
    let query = query_params != null ? "?" + new URLSearchParams(query_params) : ""
    let result = await fetch(getUrl(urlName, urlArgs) + query, generateFetchConfig(method, body));
    // console.log(result);
    return result;
}

export function fetchClubs(schoolSlug) {
    return sendRequest('club_list', { 'schoolSlug': schoolSlug }, 'GET');
}

export function fetchClub(clubSlug) {
    return sendRequest('club_detail', { 'clubSlug': clubSlug }, 'GET');
}

export function fetchClubEdit(clubSlug, code) {
    return sendRequest('club_edit', { 'code': code, 'clubSlug': clubSlug }, 'GET');
}

export function updateClub(clubSlug, updatedClub, code) {
    // console.log(updatedClub);
    return sendRequest('club_edit', { 'clubSlug': clubSlug, 'code': code }, 'PATCH', updatedClub);
}
