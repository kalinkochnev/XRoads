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

/* This will list alerts and append them
let [alerts, setAlert] = useState([]);

  function addAlert(type, message, dismissable = true) {
    // WARNING do not modify the order of the array or else you should not be using this key value!
    setAlert((oldAlerts) => {
      let msgComponent = (<Message key={oldAlerts.length + 1} type={type} dismissable={dismissable}>{message}</Message>)
      return oldAlerts.concat([msgComponent])
    })
  }
  
  <div>
      <Navbar></Navbar>
      <AlertBar>
        {alerts.map((item) => item)}
      </AlertBar>
      <LoginForm key="1" addAlert={addAlert}></LoginForm>
    </div>
*/


export { AlertBar, Message };
