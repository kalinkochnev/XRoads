import React from 'react';
import './styles/_navBars.scss';
import './styles/_clubPage.scss';
import { Navbar } from './ClubBrowser';
import { Slideshow, TextSlide, ImageSlide, VideoSlide } from './Slideshow';

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
            <Slideshow>
                    <ImageSlide source="https://lh3.googleusercontent.com/pw/ACtC-3dTHcR7fGDF02Z4rAWarD_Jek_kbVPCL6WzU4iju57ePIN2W1bd-uhWUi8yVW4dStChrDK2fdSmTo7R7e4PTSi-aEV4PROwsf7eqp8sFiSOnuxQGaj2qCfr198pxY6H9TR0YpJw2RLXkBpz0Ec-jxjX7w=w1291-h969-no?authuser=0" caption="Our driving team and robot (bottom left) just before the begining of the match."></ImageSlide>
                    <TextSlide title="We compete in the FTC" body="Each year, more than 7,000 high school teams around the world go head to head in the First Tech Challenge. The competition changes each year, keeping teams on their toes." color="lightblue"></TextSlide>
                    <ImageSlide source="https://lh3.googleusercontent.com/Hh7-xwoD3hz1g6SZ_MXnCeuFveffb9IU0nc6R3eot76xFFNo6To2v6Jzy2vHsSbrA4K3aVQWkYXqk7BWsLks6DXn0ivb2KhKBRgQ9Q_56hXzqmkQWDUZIMgJLQ0_TEah6U6hIgb8yky_PXTERAE0XUAKyCmwzvOCYOzOIxmZr3_mFggYcNpFR9uKpOLEys3uBj68EC3RwRPrd5idynC-vOoFVsbuiasaN0Hl13NnR3gYB4ORmV0WzzNU-gPEhHFTDn4wqEkDWjZyfRlGdAp0em3jS02awHBXtti7t4bmY971Ldy0mN8OrkH4FWS1Qt1th87Tip2eh960IbsufQSU5zD5byrBkou_I30RAMYhQgPiGDMByc87Pq8hRGdKhuW2JVgApYncJxjGq3MMOTLlzCrGiRw5DAvSeqJDZw5PLu2VDQxV53c_DjP-FNrF95sZmLyb71x5B5H2ShXZK5GGnWx-WhRIAT9F86Z-S2c4qHCwdp04T_9DUZmUQDJ5mOtbPIY4xgl5X1OdxowM80q2HBQB5WPJOj7P6l1Fd11HF1LApipLBBnIhmVAMX6sAPzuhP7qrAtaaJYVRPGVwNeA1yYJSYUOU86P4WFN9xrAJvz0R0-jECciEeokyOXySLkBKiUypg_f5tlWVzHMXSrbkXQfaU6eTLFD39PVF7kgBN6xqWH1f6sX0kD0Bx_ntg=w1785-h1340-no?authuser=0
" caption="Sam describes his innovative duct tape and nylon cord intake to a skeptical team."></ImageSlide>
                    <TextSlide title="What we're about" body="Robotics is a great way to put all those STEM skills from class to a good use. But it's more than that too. It's about creative thinking and problem solving under pressure." color="#ffc4c4"></TextSlide>
                    <VideoSlide videoURL="https://www.youtube.com/watch?v=D2-CRBoGpJQ" caption="Here's our challenge kickoff from our past season."></VideoSlide>
            </Slideshow>
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
                <h1>Robotics Club</h1>
                <h2>Text @niskyrobot to 81010 to join</h2>
            </div>
            <div class="details">
            <p>
            <h2>What we do</h2>
            Robotics club is where all the action is at. We create robots and compete against other schools for the glory of having the best robot. We’re pretty good at what we do, and not to brag, but we qualified for the World Championships last year! That’s no joke!
            </p><p>
            The First Tech Challenge (FTC) is an international organization where about 7,000 highschool teams go head to head in a competition that changes every year. No person alone could take on such an amazing feat. Robotics is about banding together with your peers to create something awesome.
            </p><p>
            As a current club member, I can vouch and say that I have met some of the most creative, smart, funny and resourceful people ever. Robotics can be a rollercoaster of emotions sometimes. It definitely was last year. We were so happy that we qualified for worlds, but later disappointed when it was canceled because of COVID.
            </p><p>
            <h2>Who its for</h2>
            Robotics is probably the best opportunity you have in high school to take STEM to the next level. If you love engineering or coding, this is a great place to apply what you learn. If you want to learn coding or engineering, this is a great place to learn. If you don’t even like coding or engineering, but like tough problem solving and fierce competition, this is a ton of fun. What we’re trying to say is that there’s no reason not to join.
            </p><p>
            Building a robot takes a lot of time and that’s why we meet as much as we do, but it doesn’t mean that you can’t join if you’re a busy person. Members always welcome to pop in for whatever time they’re available for.
            </p><p>
            Robotics is all about being able to react as situations change. Sometimes we have a plan, but most of the time we’re winging it. Robotics is definitely going to be different this year due to COVID, but we have a plan (we’re totally winging it) and it’s gonna be more exciting than ever before.
            </p>
            <div class="clubHeading">
            <h1>FAQ</h1>
            </div>
                <p>
                    <h3>
                        Q: When do we meet?
                    </h3>
                    A: We meet twice a week, mondays and fridays under normal circumstances. Depending on what the situation is like, it may change so be sure to check back.
                </p>
                <p>
                    <h3>
                        Q: I don’t have a lot of experience, can I still join?
                    </h3>
                    A: Yeah anybody can join! You end up learning as you go. Even if you aren’t interested in STEM, there’s lots of other stuff you can do.
                </p>
                <p>
                    <h3>
                        Q: What language do you program your robots in?
                    </h3>
                    A: We use a set of two android phones as the brains of our robot. We write java to control the various motors and sensors on board.
                </p>
                <p>
                    <h3>
                        Q: What are your robots made of?
                    </h3>
                    A: We use all sorts of materials, but the main robot design is made from aluminum. We use 3D printed and custom parts all the time as well.
                </p>
            </div>
        </div>
        );
    }
}

export {ClubPage};