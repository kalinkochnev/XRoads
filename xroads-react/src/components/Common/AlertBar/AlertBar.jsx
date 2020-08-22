import React from 'react';

const AlertBar = (props) => {
    return (
        <div className={`${props.alertType}-alert`}>
            <h2>{props.message}</h2>
        </div>
    );
}

const Alert = (props) => {

    return (
        <div className={`${props.alertType}-alert`}>
            <h2>{props.message}</h2>
        </div>
    );
}


export {Alert as AlertBar};