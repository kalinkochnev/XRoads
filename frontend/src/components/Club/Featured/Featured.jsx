import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { AutoSlide, Slideshow } from "../../Common/Slides/Slides";
import Sticky from '../../Common/StickyCard/StickyCard';
import './Featured.scss';

const FeaturedCard = (props) => {
    let [club, setClub] = useState({});

    useEffect(() => {
        setClub(props.club)
    }, [props.club])

    if (Object.keys(club).length == 0) {
        return null;
    }

    var description = club.description;
    if (club.description.length > 150) {
        description = club.description.substring(0, 5000).concat("...")
    }

    return (
        <div class="featured-container">
            <MeetingsSummary />
            <div className="featured-club">
                <Sticky label="Featured Club">
                    <div className="featured-club-content">
                        <Slideshow singleSlide>
                            {club.slides != null ? club.slides.map(url => <AutoSlide url={url}></AutoSlide>) : null}
                        </Slideshow>
                        <div className="featured-club-details">
                            <Link to={`/school/${club.school}/clubs/${club.id}`}>
                                <h2>{club.name}</h2>
                                <p>{description}</p>
                                <div className="haze-bottom" />
                            </Link>
                        </div>
                    </div>
                </Sticky>
            </div>
        </div>
    );
}

const MeetingsSummary = (props) => {
    return (
        <div className="meetings">
            <Sticky label="Upcoming Events">
                <div className="meeting-list">
                    <h3>Today</h3>
                    <p>Robotics Club · 3 pm</p>
                    <p>Model UN · 3:30 pm</p>
                    <p>Badminton Club · 4 pm</p>

                    <h3>Upcoming</h3>
                    <p>Robotics Club · Jan 6 · 4 pm</p>
                </div>
            </Sticky>
        </div>
    )
}

export default FeaturedCard;