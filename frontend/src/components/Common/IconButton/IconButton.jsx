import React from "react";
import "./IconButton.scss";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import * as Icons from '@fortawesome/free-regular-svg-icons'
import * as IconsFilled from '@fortawesome/free-solid-svg-icons'
import { Link } from "react-router-dom";

class IconButton extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            value: null,
        };
    }

    static defaultProps = {
        link: "#",
        size: '1x',
    };

    render() {
        var IconRef = Icons;
        if (this.props.filled) {
            IconRef = IconsFilled;
        }
        return (
            <Link to={this.props.link}>
                <div className="iconButton" style={{ color: this.props.color }} onClick={this.props.customClickEvent}>
                    <FontAwesomeIcon icon={IconRef[this.props.icon]} size={this.props.size} />
                </div>
            </Link>
        );

    }
}

export default IconButton;