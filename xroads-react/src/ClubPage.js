import React from 'react';
import './styles/_navBars.scss';
import './styles/_clubPage.scss';
import { Navbar } from './ClubBrowser';

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
        return (
        <div class="slideshow">
            
        </div>
        );
    }
}

export {ClubPage};