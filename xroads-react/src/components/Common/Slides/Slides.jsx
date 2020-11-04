import React from 'react';
import variables from '../Variables.scss';
import './Slides.scss';
// import Carousel, { slidesToShowPlugin, fastSwipe } from '@brainhubeu/react-carousel';
import Carousel, { slidesToShowPlugin } from '@brainhubeu/react-carousel';
import '@brainhubeu/react-carousel/lib/style.css';

function getEmbed(url) {

    if (url != null && url.includes("youtu")) {
        let regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
        let match = url.match(regExp);
        return (match && match[7].length === 11) ? ("https://www.youtube-nocookie.com/embed/" + match[7]) : null;
    }

    // else if (url != null && url.includes("vimeo")) {
    //     let regExp = /(?:www\.|player\.)?vimeo.com\/(?:channels\/(?:\w+\/)?|groups\/(?:[^\/]*)\/videos\/|album\/(?:\d+)\/video\/|video\/|)(\d+)(?:[a-zA-Z0-9_\-]+)?/i
    //     let match = url.match(regExp);
    //     return (match && match.length === 2) ? ("https://player.vimeo.com/video/" + match[1]) : null;
    // }
    
    return null;

}

class Slideshow extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            scaleAmount: 1,
        };
    }

    render() {
        let numSlides = (window.innerWidth) / variables.maxPageWidth.replace('px', '');
        let scaleAmount = (window.innerWidth) / variables.maxPageWidth.replace('px', '');
        let slideshowHeight = variables.maxPageWidth.replace('px', '') / variables.slideAspectRatio * scaleAmount;

        if (window.innerWidth < variables.maxPageWidth.replace('px', '')) {
            numSlides = 1;
        }
        else {
            scaleAmount = 1;
        }

        this.state.scaleAmount = scaleAmount;

        return (
            <div className="slideshow" style={{ height: slideshowHeight }}>
                <div className="haze left-haze"></div>
                <div className="haze right-haze"></div>
                <Carousel
                    onChange={console.log(this.props.value)}
                    plugins={[
                        'centered',
                        'infinite',
                        'arrows',
                        'fastSwipe',
                        'clickToChange',
                        {
                            resolve: slidesToShowPlugin,
                            options: {
                                numberOfSlides: numSlides
                            }
                        }
                    ]}
                >
                    {this.props.children}
                </Carousel>
            </div>
        );
    }
}

class SlideshowFiller extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            value: null,
        };
    }

    render() {
        let slideshowHeight = variables.maxPageWidth.replace('px', '') / variables.slideAspectRatio * this.props.scaleAmount;
        return (
            <div className="slideshow" style={{ height: slideshowHeight }}>
                <div className="haze left-haze"></div>
                <div className="haze right-haze"></div>

            </div>
        );
    }
}

const AutoSlide = (props) => {

    let embed = getEmbed(props.url)
    if (embed == null) {
        return (
            <ImageSlide source={props.url}></ImageSlide>
        ); 
    }
    return (<VideoSlide videoURL={props.url}></VideoSlide>);

    
}

class ImageSlide extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            scaleAmount: 1,
        };
        this.slideContainer = React.createRef();
    }

    componentDidMount() {
        var height = this.slideContainer.current.offsetHeight;
        console.log("Slidewidth is: " + height);
        this.setState({
            scaleAmount: height / (variables.maxPageWidth.replace('px', '') / variables.slideAspectRatio)
        });
    }

    render() {
        return (
            <div ref={this.slideContainer} className="slide image-slide">
                <div className="slide-content" style={{ transform: "scale(" + this.state.scaleAmount + ")" }}>
                    <img src={this.props.source}></img>
                    <p>{this.props.caption}</p>
                </div>
            </div>
        );
    }
}

class VideoSlide extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            scaleAmount: 1,
        };
        this.slideContainer = React.createRef();
    }

    componentDidMount() {
        var height = this.slideContainer.current.offsetHeight;
        console.log("Slidewidth is: " + height);
        this.setState({
            scaleAmount: height / (variables.maxPageWidth.replace('px', '') / variables.slideAspectRatio)
        });
    }

    render() {
        function getEmbed(url) {

            let noVideoEmbed = "https://player.vimeo.com/video/no-video";

            if (url != null && url.includes("youtu")) {
                let regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
                let match = url.match(regExp);
                return (match && match[7].length === 11) ? ("https://www.youtube-nocookie.com/embed/" + match[7]) : noVideoEmbed;
            }

            else if (url != null && url.includes("vimeo")) {
                let regExp = /(?:www\.|player\.)?vimeo.com\/(?:channels\/(?:\w+\/)?|groups\/(?:[^\/]*)\/videos\/|album\/(?:\d+)\/video\/|video\/|)(\d+)(?:[a-zA-Z0-9_\-]+)?/i
                let match = url.match(regExp);
                return (match && match.length === 2) ? ("https://player.vimeo.com/video/" + match[1]) : noVideoEmbed;
            }
            else {
                return noVideoEmbed;
            }

        }

        return (
            <div ref={this.slideContainer} className="slide video-slide">
                <iframe title="slideshow-iframe" width={"100%"} height={"100%"} src={getEmbed(this.props.videoURL)} frameBorder="0" allow="encrypted-media; fullscreen;" allowFullScreen></iframe>
            </div>
        );
    }
}

export { Slideshow, SlideshowFiller, ImageSlide, VideoSlide, AutoSlide };