import React from 'react';
import './styles/_navBars.scss';
import './styles/_clubPage.scss';
import { Navbar } from './ClubBrowser';
import variables from './styles/_variables.scss';

import Carousel, { slidesToShowPlugin, fastSwipe } from '@brainhubeu/react-carousel';
import '@brainhubeu/react-carousel/lib/style.css';

var scaleAmount

class ClubPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
        value: null,
        };
    }

    render() {
        return (
        <div>
            <Navbar>xroads</Navbar>
            <Slideshow></Slideshow>
            <ClubInfo></ClubInfo>
        </div>
        );
    }
}

class ClubInfo extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
        value: null,
        };
    }

    render() {
        return (
        <div class="clubDetails">
            <div class="clubHeading">
                <t>Drama Club</t>
                <h1>Meets Wednesday after school to 4 pm.</h1>
            </div>
            <div class="details">
            Once upon a time there were three little girls who went to the police academy. Two in Los Angeles. The other in San Francisco. And they were each assigned very hazardous duties. But I took them away from all that. And now they work for me. My name is Charlie.
            <br></br><br></br>
            Spiderman, Spiderman, does whatever a spider can. Spins a web, any size, catches thieves just like flies, look out! Here comes the Spiderman. Is he strong? Listen bud, he's got radioactive blood. Can he swing from a thread? Take a look overhead. Hey there, there goes the Spiderman. In the chill of night at the scene of a crime, like a streak of light he arrives just in time! Spiderman, Spiderman, friendly neighborhood Spiderman. Wealth and fame, He's ignored. Action is his reward. To him, life is a great big bang up. Whenever there's a hang up, you'll find the Spiderman!
            <br></br><br></br>
            Green Acres is the place to be. Farm livin' is the life for me. Land spreadin' out so far and wide. Keep Manhattan, just give me that countryside. New York is where I'd rather stay. I get allergic smelling hay. I just adore a penthouse view. Darling I love you but give me Park Avenue. The chores! The stores! Fresh air! Times Square! You are my wife. Good bye, city life. Green Acres we are there!
            <br></br><br></br>
            Gathered together from the cosmic reaches of the universe, here in this great Hall of Justice, are the most powerful forces of good ever assembled: Superman! Batman and Robin! Wonder Woman! Aquaman! And The Wonder Twins: Zan and Jayna, with their space monkey, Gleek! Dedicated to prove justice and peace for all mankind!
            </div>
        </div>
        );
    }
}

class Slideshow extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
        value: null,
        };
    }
    
    render() {
        var numSlides = (window.innerWidth)/variables.maxPageWidth.replace('px','');
        scaleAmount = (window.innerWidth)/variables.maxPageWidth.replace('px','');
        var slideshowHeight = variables.maxPageWidth.replace('px','')/variables.slideAspectRatio*scaleAmount;

        if(window.innerWidth < variables.maxPageWidth.replace('px','')){
            numSlides = 1;
        }
        else {
            scaleAmount = 1;
        }


        
        return (
            <div class="slideshow" style={{height: slideshowHeight}}>
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
                    <TextSlide title="a slide with a body" subtitle="and a subtitle" body="I'm not a witch. Oh! Come and see the violence inherent in the system! Help, help, I'm being repressed! We shall say 'Ni' again to you, if you do not appease us. No, no, no! Yes, yes. A bit. But she's got a wart. You don't vote for kings. Be quiet! Camelot! Shut up! Will you shut up?! I am your king. Why? We found them. No, no, no! Yes, yes. A bit. But she's got a wart. You don't frighten us, English pig-dogs! Go and boil your bottoms, sons of a silly person!" color="lightblue"></TextSlide>
                    <ImageSlide source="https://brainhubeu.github.io/react-carousel/static/mona-7a1ceae9bdb8c43272eb101c091c5408.jpg" caption="an image with a caption"></ImageSlide>
                    <TextSlide title="a slide with no body"></TextSlide>
                    <VideoSlide videoURL="https://vimeo.com/212103091"></VideoSlide>
                    <VideoSlide videoURL="https://www.youtube.com/watch?v=7LJIcrJKDI0"></VideoSlide>
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
        <div class="slide text-slide" style={{backgroundColor: this.props.color }}>
            <div class="slide-content" style={{transform: "scale("+scaleAmount+")"}}>
                <div class="text-area">
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
        <div class="slide image-slide">
            <div class="slide-content" style={{transform: "scale("+scaleAmount+")"}}>
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

            var noVideoEmbed = "https://player.vimeo.com/video/no-video";

            if(url != null && url.includes("youtu")){
                var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
                var match = url.match(regExp);
                return (match&&match[7].length==11)? ("https://www.youtube-nocookie.com/embed/"+match[7]) : noVideoEmbed;
            }

            else if(url != null && url.includes("vimeo")){
                var regExp = /(?:www\.|player\.)?vimeo.com\/(?:channels\/(?:\w+\/)?|groups\/(?:[^\/]*)\/videos\/|album\/(?:\d+)\/video\/|video\/|)(\d+)(?:[a-zA-Z0-9_\-]+)?/i
                var match = url.match(regExp);
                return (match&&match.length==2)? ("https://player.vimeo.com/video/"+match[1]) : noVideoEmbed;
            }
            else {
                return noVideoEmbed;
            }

        }
        
        var slideWidth = variables.maxPageWidth.replace('px','')*scaleAmount;
        var slideHeight = slideWidth/variables.slideAspectRatio;
        console.log(slideHeight);
        return (
        <div class="slide video-slide">
            <div class="slide-content">
                <iframe width={slideWidth} height={slideHeight} src={getEmbed(this.props.videoURL)} frameborder="0" allow="encrypted-media; fullscreen;" allowfullscreen></iframe>
            </div>
        </div>
        );
    }
}

export {ClubPage};