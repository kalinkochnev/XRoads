import React, { useEffect, useState } from "react";
import { AutoSlide, Slideshow } from "../../Common/Slides/Slides";
import ReactPlayer from "react-player";

const FeaturedCard = (props) => {
    let [club, setClub] = useState({});

    useEffect(() => {
        setClub(props.club)
    }, [props.club])

    if (Object.keys(club).length == 0) {
        return null;
    }

    return (
        <div>
            <h1>Featured Club!</h1>
            <h2>{club.name}</h2>
            <p>{club.description}</p>    
            <Slideshow>
                {club.slides != null ? club.slides.map(url => <AutoSlide url={url}></AutoSlide>) : null}
            </Slideshow>
            
        </div>
    );
}

export default FeaturedCard;