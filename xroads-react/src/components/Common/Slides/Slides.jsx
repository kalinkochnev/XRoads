import React from 'react';
import variables from '../Variables.scss';
import './Slides.scss';
// import Carousel, { slidesToShowPlugin, fastSwipe } from '@brainhubeu/react-carousel';
import Carousel, { slidesToShowPlugin } from '@brainhubeu/react-carousel';
import '@brainhubeu/react-carousel/lib/style.css';

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

class TextSlide extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            scaleAmount: 1,
        };
        this.slideContainer = React.createRef();
    }

    componentDidMount() {
        var height = this.slideContainer.current.offsetHeight;
        this.setState({
            scaleAmount: height / (variables.maxPageWidth.replace('px', '') / variables.slideAspectRatio)
        });
    }

    render() {
        return (
            <div ref={this.slideContainer} className="slide text-slide" style={{ backgroundColor: this.props.color }}>
                <div className="slide-content" style={{ transform: "scale(" + this.state.scaleAmount + ")" }}>
                    <div className="text-area">
                        <h1>{this.props.title}</h1>
                        <h2>{this.props.subtitle}</h2>
                        <p>{this.props.body}</p>
                    </div>
                </div>
            </div>
        );
    }
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
                <iframe title="slideshow-iframe" src={getEmbed(this.props.videoURL)} frameBorder="0" allow="encrypted-media; fullscreen;" allowFullScreen></iframe>
            </div>
        );
    }
}

export { Slideshow, SlideshowFiller, TextSlide, ImageSlide, VideoSlide };