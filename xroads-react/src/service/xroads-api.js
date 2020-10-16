
// To have keyworded args use this format:   :keyword_arg
const endpoint_templates = {
    'club_list': '/api/school/:schoolId',
    'club_detail': '/api/club/:clubId',
    'club_edit': '/api/club/:code/:clubId',
    'school_list': '/api/district/:districtId',

    'toggle_hide_club': '/api/admin/district/:districtId/school/:schoolId/club/:clubId/toggle_hide/',
    'admin_club_detail': '/api/admin/district/:districtId/school/:schoolId/club/:clubId',
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

export function fetchClubs(schoolId) {
    return sendRequest('club_list', { 'schoolId': schoolId }, 'GET');
}

export function fetchClub(clubId) {
    return sendRequest('club_detail', { 'clubId': clubId }, 'GET');
}

export function fetchClubEdit(clubId, code) {
    return sendRequest('club_edit', { 'code': code, 'clubId': clubId }, 'GET');
}

export function updateClub(clubId, updatedClub) {
    return sendRequest('admin_club_detail', { 'clubId': clubId }, 'PUT', updatedClub);
}
