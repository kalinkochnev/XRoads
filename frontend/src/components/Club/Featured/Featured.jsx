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

    // if (Object.keys(club).length == 0) {
    //     return null;
    // }
    if (club.description != null) {
        var description = club.description;
        if (club.description.length > 150) {
            description = club.description.substring(0, 5000).concat("...")
        }
    } else {
        var description = "";
    }
    return (


        <div className="featured-club">
            <Sticky label="Featured Club">
                <div className="featured-club-content">
                    <Slideshow singleSlide>
                        {club.slides != null ? club.slides.map(url => <AutoSlide url={url}></AutoSlide>) : null}
                    </Slideshow>
                    <div className="featured-club-details">
                        <Link to={`/${props.schoolSlug}/${props.club.slug}`}>
                            <h2>{club.name}</h2>
                            <p>{description}</p>
                            <div className="haze-bottom" />
                        </Link>
                    </div>
                </div>
            </Sticky>
        </div>
    );
}

const MeetingsSummary = (props) => {
    return (
        <div className="meetings">
            <Sticky label="Upcoming Events">
                <div className="meeting-list">
                    {props.children}
                </div>
            </Sticky>
        </div>
    )
}

export { FeaturedCard, MeetingsSummary };