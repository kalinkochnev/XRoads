import React from 'react';

import './Edit.scss';

import RichEditor from '../../Common/RichEditor/RichEditor'
import { TextSlide, ImageSlide, VideoSlide } from '../../Common/Slides/Slides';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faFilm, faFont, faImage, faImages, faTextHeight, faVideo } from '@fortawesome/free-solid-svg-icons'
import { useState } from 'react'
import { updateClub } from '../../../service/xroads-api'

import ReactTooltip from 'react-tooltip';



const GeneralEdit = (props) => {
    let [clubDescriptionMd, setClubDescription] = useState(props.club.description);
    let [clubName, setClubName] = useState(props.club.name)
    let [clubJoinPromo, setClubJoinPromo] = useState(props.club.join_promo)

    const handleClubDescription = (clubDescMd) => {
        // console.log("Updated club description", clubDescMd);
        setClubDescription(clubDescMd);
    }

    const saveClubDetails = () => {
        // FIXME : pull the district ID from whereever it lives in the context
        const districtId = 1;
        const updatedClub = {
            ...props.club,
            description: clubDescriptionMd,
            name: clubName,
            join_promo: clubJoinPromo
        };
        console.log("Updated club would be", updatedClub);
        const saveRes = updateClub(districtId, props.club.school, props.club.id, updatedClub);
        console.log("Save club result", saveRes);
    }

    return (
        <div className="centerContent">
            <div className="editBody">
                <form className="clubEdit">
                    
                    <label className="" htmlFor="join">Hide this club</label>
                    <label class="switch">
                        <input type="checkbox" />
                        <span class="slider round"></span>
                    </label>
                    <ReactTooltip place="right" effect="solid"/>

                    <label className="" htmlFor="join">How to join<br />
                        <input type="text" id="join" name="join" value={clubJoinPromo} onChange={(e) => setClubJoinPromo(e.target.value)} />
                    </label>

                    <label className="" htmlFor="description">Description<br />
                        <RichEditor mdContent={clubDescriptionMd} onChange={handleClubDescription} />
                    </label>
                </form>
                <button type="submit" id="club-submit" onClick={saveClubDetails}>Save</button>
            </div>
        </div>
    );
}

const SlideshowEdit = (props) => {
    return (
        <div className="centerContent">
            <div className="editBody">
                <div className="slideshowSelect">
                    {
                        props.club.slides.map(slide => {
                            if (slide.img) {
                                return <div className="slideContain"> <ImageSlide key={slide.id} source={slide.img} caption={slide.text} /> </div>
                            } else if (slide.video_url) {
                                return <div className="slideContain"> <VideoSlide key={slide.id} videoURL={slide.video_url} caption={slide.text} /> </div>
                            } else {
                                return <div className="slideContain"> <TextSlide key={slide.id} title={slide.text} body={slide.text} color="lightblue" /> </div>
                            }
                        })

                    }
                    <div className="slideContain addSlide">
                        <div className="add"><FontAwesomeIcon icon={faFont} />Add a text slide</div>
                        <div className="add middle"><FontAwesomeIcon icon={faImage} />Add an image slide</div>
                        <div className="add"><FontAwesomeIcon icon={faFilm} />Add a video slide</div>
                    </div>
                    <div className="spacer"></div>
                </div>
                <div className="slideshowPreview">
                    {
                        (function () {
                            let slide = props.club.slides[0];
                            if (slide.img) {
                                return <div className="slideContain"> <ImageSlide key={slide.id} source={slide.img} caption={slide.text} /> </div>
                            } else if (slide.video_url) {
                                return <div className="slideContain"> <VideoSlide key={slide.id} videoURL={slide.video_url} caption={slide.text} /> </div>
                            } else {
                                return <div className="slideContain"> <TextSlide key={slide.id} title={slide.text} body={slide.text} color="lightblue" /> </div>
                            }
                        })()
                    }
                </div>
                <form className="clubEdit">
                    <label for="title">Slide Template<br />
                        <select class="short" id="title" name="title">
                            <option>Text</option>
                            <option>Image</option>
                            <option>Video</option>
                        </select>
                    </label>

                    <label className="" for="title">Title<br />
                        <input class="medium" type="text" id="title" name="title" />
                    </label>

                    <label className="" for="body">Body<br />
                        <input class="long" type="text" id="body" name="body"></input>
                    </label>

                </form>
            </div>
        </div>
    );
}

export { GeneralEdit, SlideshowEdit };