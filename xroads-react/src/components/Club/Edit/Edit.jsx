import React from 'react';

import { Slideshow, SlideshowFiller, TextSlide, ImageSlide, VideoSlide } from '../../Common/Slides/Slides';
import './Edit.scss';

import Carousel, { slidesToShowPlugin } from '@brainhubeu/react-carousel';
import '@brainhubeu/react-carousel/lib/style.css';

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
                    <label className="short" for="title">Club Name<br />
                        <input type="text" id="title" name="title" value={props.club.name} />
                    </label>

                    <label className="" for="join">How to join<br />
                        <input type="text" id="join" name="join" value={props.club.join} />
                    </label>

                    <label className="" for="description">Description<br />
                        <textarea type="textarea" id="title" name="title">{props.club.description}</textarea>
                    </label>
                </form>

                <h2>Slideshow</h2>
                <div className="slideshowSelect">
                    {
                        props.club.slides.map(slide => {
                            if (slide.img) {
                                return <div className="slideContain"> <ImageSlide key={slide.id} source={slide.img} caption={slide.text} scaleAmount={0.4}/> </div>
                            } else if (slide.video_url) {
                                return <div className="slideContain"> <VideoSlide key={slide.id} videoURL={slide.video_url} caption={slide.text} scaleAmount={0.4}/> </div>
                            } else {
                                return <div className="slideContain"> <TextSlide key={slide.id} title={slide.text} body={slide.text} color="lightblue" scaleAmount={0.4}/> </div>
                            }
                        })
                        
                    }
                    <div class="dummySpacer"></div>
                </div>
                <form className="clubEdit">
                    <label className="short" for="title">Slide Template<br />
                        <select id="title" name="title">
                            <option>Text</option>
                            <option>Image</option>
                            <option>Video</option>
                        </select>
                    </label>

                    <label className="" for="join">Title<br />
                        <input type="text" id="join" name="join"/>
                    </label>

                    <label className="" for="description">Body<br />
                        <textarea type="textarea" id="title" name="title"></textarea>
                    </label>

                </form>
            </div>
        </div>
    );
}

export default ClubEdit;