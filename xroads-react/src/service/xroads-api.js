
// To have keyworded args use this format:   :keyword_arg
const endpoint_templates = {
    'club_list': '/api/school/:schoolId/',
    'club_detail': '/api/club/:clubId/',
    'club_edit': '/api/club/:code/:clubId/',
    'school_list': '/api/district/:districtId/',

    'toggle_hide_club': '/api/club/:code/:clubId/toggle_hide/',
    'check_code': '/api/school/:schoolId/club_code/',
    'club_email_info': '/api/club/:clubId/send_info/',

    'event_create': '/api/event/:clubId/:clubCode/',
    'event_edit': '/api/edit/event/:clubId/:clubCode/:eventId/',

    'school_events': '/api/school/:schoolId/events/',
    'event_info': '/api/events/:eventId/info/'
};

function fillTemplate(urlName, urlArgs) {
    let template = endpoint_templates[urlName];
    for (var arg of Object.keys(urlArgs)) {
        template = template.replace(`:${arg}`, urlArgs[arg])
    }
    console.log(template)
    return template;
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

export async function sendRequest(urlName, urlArgs, method, body = null, query_params = null) {
    let query = query_params != null ? "?" + new URLSearchParams(query_params) : ""
    return await fetch(getUrl(urlName, urlArgs) + query, generateFetchConfig(method, body));
}

export function fetchClubs(schoolId) {
    return sendRequest('club_list', { 'schoolId': schoolId }, 'GET');
}

export function fetchClub(clubId) {
    return sendRequest('club_detail', { 'clubId': clubId }, 'GET');
}

export function fetchClubEdit(clubId, code) {
    return sendRequest('club_edit', { 'code': code, 'clubId': clubId }, 'GET');
}

export function updateClub(clubId, updatedClub, code) {
    return sendRequest('club_edit', { 'clubId': clubId, 'code': code }, 'PUT', updatedClub);
}
