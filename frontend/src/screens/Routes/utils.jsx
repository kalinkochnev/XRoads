// {schoolId: 1 } { schoolId: number } 
const checkURLParams = (params, expected, history) => {
    let checkFuncs = {
        number: (input) => !isNaN(input),
        string: (input) => typeof input == "string"
    }

    for (let i = 0; i < Object.keys(expected).length; i++) {
        let key = Object.keys(params)[i];

        if (!checkFuncs[expected[key]](params[key])) {
            history.push('/')
        }
    }
    return true;
}

export default checkURLParams;