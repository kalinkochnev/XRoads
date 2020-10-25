import React, { useEffect, useState } from "react";
import { ImageSlide, Slideshow } from "../../Common/Slides/Slides";

const FeaturedCard = (props) => {
    let [club, setClub] = useState({});
    console.log(club)

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
                {club.slides.map(url => <ImageSlide source={url}></ImageSlide>)}
            </Slideshow>
            
        </div>
    );
}

export default FeaturedCard;