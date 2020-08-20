


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

export function fetchClubs() {
    // var clubs = []
    // var clubs = [
    //     [1, "Robotics Club", "https://lh3.googleusercontent.com/pw/ACtC-3fIUy1uUAK3OgwH7h4WURxF4I6vpu1K35iwDZqzBpy_hII4ySNfhqLy7yeFC5Twv9a83Rn4UvdKeZar5dhtLbRjfTsQVNhczKUy4s-CtymhzR2D19tugouYi30BX0i954NKISlQh9qYhSaq27G9JV0kNQ=w1291-h970-no?authuser=0", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.", ["M","F"]],
    //     [2, "Drama Club", "https://unsplash.it/800/600?image=38", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.", ["W"]],
    //     [3, "Model UN", "https://unsplash.it/800/600?image=22", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.", ["W"]],
    //     [4, "Moddel UN", "https://unsplash.it/800/600?image=69", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.", ["TH"]],
    //     [5, "Model UN", "https://unsplash.it/800/600?image=666", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.", ["TU"]],
    //     [6, "Model UN", "https://unsplash.it/800/600?image=420", "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.", ["M","W","S"]],
    //   ];


    return fetch(`${process.env.REACT_APP_XROADS_API_ENDPOINT}/district/1/school/1/club/`, generateFetchConfig("GET"));
}