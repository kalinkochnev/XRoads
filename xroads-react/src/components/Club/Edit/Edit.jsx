import React from 'react';

import './Edit.scss';

import RichEditor from '../../Common/RichEditor/RichEditor'
import { TextSlide, ImageSlide, VideoSlide } from '../../Common/Slides/Slides';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faFilm, faFont, faImage, faImages, faQuestion, faTextHeight, faVideo } from '@fortawesome/free-solid-svg-icons'


const GeneralEdit = (props) => {
    return (
        <div className="centerContent">
            <div className="editBody">
                <form className="clubEdit">
                    <label className="" for="join">How to join<br />
                        <input type="text" id="join" name="join" value={props.club.join_promo} />
                    </label>

                    <label className="" for="description">Description<br />
                        <RichEditor />
                    </label>
                </form>
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