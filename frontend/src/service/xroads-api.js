/**
 @abstract
*/
class API {

}

class Endpoint {
    defaultIsSuccess = (response) => response.ok
    templates = {};

    fillUrl(template, ...urlArgs) {
        // This fills the template with the given args
        for (let [key, value] of Object.entries(urlArgs)) {
            template = template.replace(`:${key}`,value)
        }

        // Append the env domain
        return process.env.REACT_APP_XROADS_API_ENDPOINT + template;
    }

    /**
     * Generates a Fetch confiugration object so we can share headers
     * @method generateFetchConfig
     * @param  {string}            method      HTTP verb
     * @param  {object}            [body=null] payload for post/put
     * @return {object}                        config
    */
    generateFetchConfig(method, body = null) {
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

    async sendRequest(template, urlArgs, method, body = null, query_params = null) {
        let query = query_params != null ? "?" + new URLSearchParams(query_params) : ""
        return await fetch(fillUrl(template, urlArgs) + query, generateFetchConfig(method, body));
    }

    list(parentId, query_params={}) {
        return this.sendRequest(this.templates.list, {parentId: parentId}, 'GET', {}, query_params)
    }

    detail(id, query_params={}) {
        return this.sendRequest(this.templates.detail, {id: id}, 'GET', {}, query_params)
    }

    create(objectData) {
        return this.sendRequest(this.templates.create, {}, 'POST', objectData, {})
    }
}

class Club extends Endpoint {
    templates = {
        list: "/api/school/:parentId/",
        detail: "/api/club/:id/",
        action: {
            edit: "/api/club/:code/:id/",
            hide: "/api/club/:code/:clubId/toggle_hide/"
        }
    }
    hide() {
        return this.sendRequest()
    }

}

class School extends Endpoint {
    templates = {
        list: "/api/district/:parentId/",
        actions: {
            events: "/api/school/:id/events/",
        }
    }
}

class XroadsAPI extends API {
    constructor(districtId=-1, schoolId=-1, clubId=-1) {
        this.districtId = districtID;
        this.schoolId = schoolId;
        this.clubId = clubId;
    }

    endpoint_templates = {
    
        'toggle_hide_club': '',
        'check_code': '/api/school/:schoolId/club_code/',
        'club_email_info': '/api/club/:clubId/send_info/',
    
        'event_create': '/api/event/:clubId/:clubCode/',
        'event_edit': '/api/event/:clubId/:clubCode/:eventId/',
    
        'school_events': '',
        'event_info': '/api/events/:eventId/info/'
    };

    
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
