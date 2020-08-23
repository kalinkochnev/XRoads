import React, {useState} from "react";

const AlertBar = (props) => {
    return (
        <div>{props.children}</div>
    );
};

// Same as props.type, props.children
const Message = ({type, children, dismissable=true}) => {
    const [dismissed, setDismissed] = useState(false);

    let dismissBtn = (<button className="dismiss-button" onClick={()=>setDismissed(true)}></button>);
    let msg = (
        <div className={`${type}-alert`}>
            <div className="alert-message">
                <h2>{children}</h2>
            </div>
            
            {dismissable ? dismissBtn : (<div className="empty-dismiss"></div>)}
        </div>
    );
    return !dismissed ? msg : null;
}


export { AlertBar, Message };
