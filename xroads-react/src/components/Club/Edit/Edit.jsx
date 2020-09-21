import React from 'react';

import './Edit.scss';

import RichEditor from '../../Common/RichEditor/RichEditor'
import { TextSlide, ImageSlide, VideoSlide } from '../../Common/Slides/Slides';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faFilm, faFont, faImage, faImages, faTextHeight, faVideo } from '@fortawesome/free-solid-svg-icons'
import { useState } from 'react'
import { sendRequest, updateClub } from '../../../service/xroads-api'
import { useStateValue } from '../../../service/State'
import ReactTooltip from 'react-tooltip';

import { store } from 'react-notifications-component';



const GeneralEdit = (props) => {
    let [clubDescriptionMd, setClubDescription] = useState(props.club.description);
    let [clubName, setClubName] = useState(props.club.name)
    let [clubJoinPromo, setClubJoinPromo] = useState(props.club.join_promo)
    const [state, dispatch] = useStateValue();
    const [isVisible, setVisibility] = useState(props.club.is_visible);



    const handleClubDescription = (clubDescMd) => {
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
        updateClub(districtId, props.club.school, props.club.id, updatedClub).then(res => {
            res.json().then(updatedClub => {
                console.log("Updated club", updateClub);
                store.addNotification({
                    title: "Saved",
                    message: "Club details successfully saved",
                    type: "success",
                    insert: "top",
                    container: "top-right",
                    dismiss: {
                        duration: 5000,
                        onScreen: true
                    }
                });
            });
        });
    }

    // FIXME this will not work if someone has edit access but has a different school
    const toggleHide = () => {
        let user = state.user;
        let urlArgs = {
            'districtId': user.district,
            'schoolId': user.school,
            'clubId': props.club.id
        }
        sendRequest("toggle_hide_club", urlArgs, 'POST', {}).then(response => {
            if (response.ok) {
                setVisibility(!isVisible)
                console.log('The club is now ' + isVisible.toString())
                store.addNotification({
                    title: "Club " + (isVisible ? "Visible" : "Hidden"),
                    message: "The club is now visible to " + (isVisible ? "all users" : "club editors only"),
                    type: "success",
                    insert: "top",
                    container: "top-right",
                    dismiss: {
                        duration: 5000,
                        onScreen: true
                    }
                });
            }
        })
    }

    return (
        <div className="centerContent">
            <div className="editBody">
                <form className="clubEdit">

                    <label className="" htmlFor="join">Hide club</label>
                    <label class="switch">
                        <input type="checkbox" onClick={toggleHide} checked={!isVisible} />
                        <span class="slider round"></span>
                    </label>
                    <ReactTooltip place="right" effect="solid" />

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

class SlideshowEdit extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            slides: this.props.club.slides,
            activeKey: 0
        };
    }

    slideClick = (pos) => {
        this.setState({ activeKey: pos - 1 });
    }

    addSlide = (type) => {
        let length = this.props.state.length;        
        this.state.slides.push({
            club: this.props.club.id,
            img: null,
            position: length+1,
            template_type: type,
            text: null,
            video_url: null
        });
    }



    render() {
        console.log(this.props.club.slides)
        return (
            <div className="centerContent">
                <div className="editBody">
                    <div className="slideshowSelect">
                        {
                            this.state.slides.map(slide => {
                                if (slide.template_type == 1 || slide.template_type == 2) {
                                    return <div className="slideContain" onClick={() => { this.slideClick(slide.position) }}> <ImageSlide key={slide.id} source={slide.img} caption={slide.text} /> </div>
                                } else if (slide.template_type == 3) {
                                    return <div className="slideContain" onClick={() => { this.slideClick(slide.position) }}> <VideoSlide key={slide.id} videoURL={slide.video_url} caption={slide.text} /> </div>
                                } else {
                                    return <div className="slideContain" onClick={() => { this.slideClick(slide.position) }}> <TextSlide key={slide.id} title={slide.text} body={slide.text} color="lightblue" /> </div>
                                }
                            })

                        }
                        <div className="slideContain addSlide">
                            <div className="add"><FontAwesomeIcon icon={faFont} />Add text</div>
                            <div className="add middle"><FontAwesomeIcon icon={faImage} />Add an image</div>
                            <div className="add"><FontAwesomeIcon icon={faFilm} />Add a video</div>
                        </div>
                        <div className="spacer"></div>
                    </div>
                    <div className="slideshowPreview">
                        {
                            (() => {
                                let slide = this.state.slides[this.state.activeKey];
                                if (slide.template_type == 1 || slide.template_type == 2) {
                                    return <ImageSlide key={slide.id} source={slide.img} caption={slide.text} />
                                } else if (slide.template_type == 3) {
                                    return <VideoSlide key={slide.id} videoURL={slide.video_url} caption={slide.text} />
                                } else {
                                    return <TextSlide key={slide.id} title={slide.text} body={slide.text} color="lightblue" />
                                }
                            })()
                        }
                    </div>
                    <form className="clubEdit">
                        {
                            (() => {
                                let slide = this.state.slides[this.state.activeKey];
                                if (slide.template_type == 1 || slide.template_type == 2) {
                                    return (
                                        <div>
                                            <label className="" for="image">Image Url<br />
                                                <input class="medium" type="text" id="title" name="image" value={slide.img} onChange={(e) => { slide.img = e.target.value; this.forceUpdate() }} />
                                            </label>

                                            <label className="" for="caption">Caption<br />
                                                <input class="long" type="text" id="body" name="caption" value={slide.text} onChange={(e) => { slide.text = e.target.value; this.forceUpdate() }} />
                                            </label>
                                        </div>
                                    )

                                } else if (slide.template_type == 3) {
                                    return (
                                        <div>
                                            <label className="" for="video_url">YouTube or Vimeo Link<br />
                                                <input class="medium" type="text" id="title" name="video_url" value={slide.video_url} onChange={(e) => { slide.video_url = e.target.value; this.forceUpdate() }} />
                                            </label>
                                        </div>
                                    )
                                } else {
                                    return (
                                        <div>
                                            <label className="" for="title">Title<br />
                                                <input class="medium" type="text" id="title" name="title" value={slide.text} onChange={(e) => { slide.text = e.target.value; this.forceUpdate() }} />
                                            </label>

                                            <label className="" for="body">Body<br />
                                                <input class="long" type="text" id="body" name="body" value={slide.text} onChange={(e) => { slide.text = e.target.value; this.forceUpdate() }} />
                                            </label>
                                        </div>
                                    )
                                }
                            })()
                        }
                    </form>
                </div>
            </div>
        );
    }
}

export { GeneralEdit, SlideshowEdit };