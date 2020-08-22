function InvalidKeysProvided(message) {
    const error = new Error(message);
    return error;
}

InvalidKeysProvided.prototype = Object.create(Error.prototype)