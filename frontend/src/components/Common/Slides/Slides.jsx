import React from 'react';
import { Carousel } from 'react-responsive-carousel';
import "react-responsive-carousel/lib/styles/carousel.min.css"; // requires a loader
import ReactPlayer from 'react-player';
import './Slides.scss';

class Slideshow extends React.Component {
    render() {
        let centered = true;
        if (this.props.singleSlide) {
            centered = false;
        }
        let centerSlidePercentage = Math.min((1000 / window.innerWidth) * 100, 100);

        return (
            <Carousel
                centerMode={centered}
                infiniteLoop
                swipeable
                showThumbs={false}
                showIndicators={false}
                showStatus={false}
                centerSlidePercentage={ centerSlidePercentage }
                renderArrowPrev={(onClickHandler, hasPrev, label) =>
                    hasPrev && (
                        <button className="slide-arrow" type="button" onClick={onClickHandler} title={label} style={{ left: 15 }}>&lt;</button>
                    )
                }
                renderArrowNext={(onClickHandler, hasNext, label) =>
                    hasNext && (
                        <button className="slide-arrow" type="button" onClick={onClickHandler} title={label} style={{ right: 15 }}>&gt;</button>
                    )
                }
            >
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