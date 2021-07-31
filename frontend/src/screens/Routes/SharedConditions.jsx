
const UNEXPECTED_ERROR = "An unexpected error occurred";

// ----------- Functions to be reused ---------------
const getCondRedirect = (reason) => {
    switch (reason) {
        case UNEXPECTED_ERROR:
        default:
            // console.log(UNEXPECTED_ERROR);
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
        return ['', true]
    } catch (Error) {
        return [UNEXPECTED_ERROR,];
    }
}

export { checkConditions, getCondRedirect }