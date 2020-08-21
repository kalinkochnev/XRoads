


/**
 * Generates a Fetch confiugration object so we can share headers
 * @method generateFetchConfig
 * @param  {string}            method      HTTP verb
 * @param  {object}            [body=null] payload for post/put
 * @return {object}                        config
 */
function generateFetchConfig(method, body = null) {
    const upCasedMethod = method.toUpperCase();
    // const token = Cookies.get('xroads-token');

    const token = process.env.REACT_APP_XROADS_TEMP_TOKEN;
    const config = {
        method: upCasedMethod,
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': `Token ${token}`
        },
        credentials: 'same-origin'
    };
    if (['POST', 'PUT'].includes(upCasedMethod)) {
        config.body = JSON.stringify(body);
    }
    return config;
}

export function fetchClubs(districtId, schoolId) {
    return fetch(`${process.env.REACT_APP_XROADS_API_ENDPOINT}/district/${districtId}/school/${schoolId}/club/`, generateFetchConfig("GET"));
}

export function fetchClub(districtId, schoolId, clubId) {
    return fetch(`${process.env.REACT_APP_XROADS_API_ENDPOINT}/district/${districtId}/school/${schoolId}/club/${clubId}`, generateFetchConfig("GET"));
}