import React from 'react';
import letiables from '../Variables.scss';
import './Slides.scss';
// import Carousel, { slidesToShowPlugin, fastSwipe } from '@brainhubeu/react-carousel';
import Carousel, { slidesToShowPlugin } from '@brainhubeu/react-carousel';
import '@brainhubeu/react-carousel/lib/style.css';

let scaleAmount

class Slideshow extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
        value: null,
        };
    }
    
    render() {
        let numSlides = (window.innerWidth)/letiables.maxPageWidth.replace('px','');
        scaleAmount = (window.innerWidth)/letiables.maxPageWidth.replace('px','');
        let slideshowHeight = letiables.maxPageWidth.replace('px','')/letiables.slideAspectRatio*scaleAmount;

        if(window.innerWidth < letiables.maxPageWidth.replace('px','')){
            numSlides = 1;
        }
        else {
            scaleAmount = 1;
        }

        return (
            <div className="slideshow" style={{height: slideshowHeight}}>
                <div className="haze left-haze"></div>
                <div className="haze right-haze"></div>
                <Carousel
                plugins={[
                    'centered',
                    'infinite',
                    'arrows',
                    'fastSwipe',
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

class TextSlide extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
        value: null,
        };
    }

    render() {
        return (
        <div className="slide text-slide" style={{backgroundColor: this.props.color }}>
            <div className="slide-content" style={{transform: "scale("+scaleAmount+")"}}>
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
        value: null,
        };
    }

    render() {
        return (
        <div className="slide image-slide">
            <div className="slide-content" style={{transform: "scale("+scaleAmount+")"}}>
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
        value: null,
        };
    }

    render() {
        function getEmbed(url){

            let noVideoEmbed = "https://player.vimeo.com/video/no-video";

            if(url != null && url.includes("youtu")){
                let regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
                let match = url.match(regExp);
                return (match&&match[7].length===11)? ("https://www.youtube-nocookie.com/embed/"+match[7]) : noVideoEmbed;
            }

            else if(url != null && url.includes("vimeo")){
                let regExp = /(?:www\.|player\.)?vimeo.com\/(?:channels\/(?:\w+\/)?|groups\/(?:[^\/]*)\/videos\/|album\/(?:\d+)\/video\/|video\/|)(\d+)(?:[a-zA-Z0-9_\-]+)?/i
                let match = url.match(regExp);
                return (match&&match.length===2)? ("https://player.vimeo.com/video/"+match[1]) : noVideoEmbed;
            }
            else {
                return noVideoEmbed;
            }

        }
        
        let slideWidth = letiables.maxPageWidth.replace('px','')*scaleAmount;
        let slideHeight = slideWidth/letiables.slideAspectRatio-65*scaleAmount;

        console.log(slideHeight);
        return (
        <div className="slide video-slide">
            <iframe title="slideshow-iframe" width={slideWidth} height={slideHeight} src={getEmbed(this.props.videoURL)} frameBorder="0" allow="encrypted-media; fullscreen;" allowFullScreen></iframe>
            <div className="slide-content" style={{transform: "scale("+scaleAmount+")"}}>
                <p>{this.props.caption}</p>
            </div>
        </div>
        );
    }
}

export {Slideshow, TextSlide, ImageSlide, VideoSlide};