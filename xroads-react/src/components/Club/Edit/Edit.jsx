import React from 'react';

import './Edit.scss';

import RichEditor from '../../Common/RichEditor/RichEditor'
import { TextSlide, ImageSlide, VideoSlide } from '../../Common/Slides/Slides';


const ClubEdit = (props) => {
    return (
        <div className="centerContent">
            <div className="editBody">
                <div className="clubHeading">
                    <h2>Now Editing</h2>
                    <h1>{props.club.name}</h1>
                </div>

                <h2>General</h2>
                <form className="clubEdit">
                    <label for="title">Club Name<br />
                        <input class="medium" type="text" id="title" name="title" value={props.club.name} />
                    </label>

                    <label className="" for="join">How to join<br />
                        <input type="text" id="join" name="join" value={props.club.join} />
                    </label>

                    <label className="" for="description">Description<br />
                        <RichEditor />
                    </label>
                </form>

                <h2>Slideshow</h2>
                <div className="slideshowSelect">
                    {
                        props.club.slides.map(slide => {
                            if (slide.img) {
                                return <div className="slideContain"> <ImageSlide key={slide.id} source={slide.img} caption={slide.text}/> </div>
                            } else if (slide.video_url) {
                                return <div className="slideContain"> <VideoSlide key={slide.id} videoURL={slide.video_url} caption={slide.text}/> </div>
                            } else {
                                return <div className="slideContain"> <TextSlide key={slide.id} title={slide.text} body={slide.text} color="lightblue"/> </div>
                            }
                        })

                    }
                    <div className="slideContain addSlide">+</div>
                    <div className="spacer"></div>
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

export default ClubEdit;