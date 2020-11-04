import React from 'react';
import { Carousel } from 'react-responsive-carousel';
import "react-responsive-carousel/lib/styles/carousel.min.css"; // requires a loader
import ReactPlayer from 'react-player';

class Slideshow extends React.Component {
    render() {
        return (
            <Carousel centerMode infiniteLoop> 
                {this.props.children}
            </Carousel>
        );
    }
}

const AutoSlide = ({ url }) => {
    if (url != null && url.includes("youtu")) {
        let regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
        let match = url.match(regExp);
        if (match) {
            return (<ReactPlayer width="100%" height="100%" url={url}></ReactPlayer>)
        }
    }
    return (<div><img src={url}></img></div>)
}

export { Slideshow, AutoSlide };