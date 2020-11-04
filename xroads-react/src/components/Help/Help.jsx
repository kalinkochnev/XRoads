import React from 'react';

const SlideHelp = () => {
    return (
        <div>
            <h1>FAQ</h1>

            <hr></hr>
            <h1>Browser</h1>
            <h2 id="featured-notification">When is my club going to be featured?</h2>
            <p>If your school allows you to input a club email, you would be notified by email 1 week before you are featured.
                You also receive an email once your club is currently being featured. New clubs are featured every week.
            </p>

            <h2 id="not-featured">I received an email that my club was going to be featured, but it's not showing up!</h2>
            <p>It's possible that your club is not showing up when it was scheduled to be featured. This is probably because the club is currently being hidden from viewing, so the next club up in line is shown instead.
            </p>

            <hr></hr>
            <h1>Edit Page</h1>
            <h2>My club code was lost <u>or</u> somebody who wasn't supposed to have the code is now in possesion!</h2>
            <p>If you require a new club code due to a variety of reasons, please contact support@xroads.club</p>

            <h2>How can I change my club name?</h2>
            <p>Currently the only way to change your club name is by contacting us at support@xroads.club</p>

            <h2>Help! Somebody messed up my club page!</h2>
            <p>It is not possible at the moment to "undo" what was done. We would recommend making your club invisible until your page gets fixed. 
                If your page was messed up because of somebody who wasn't supposed to access it, there is nothing we can do about it currently. 
                We would suggest keeping your club code limited to a few club members so only the people who need access know it. 
            </p>

            <hr></hr>
            <h1>Slideshow</h1>
            <h2 id="slideshow-setup">How do I setup my slideshow?</h2>
            <p>It's actually pretty simple!</p>
            <ol>
                <li>Create or open a presentation in Google Slides</li>
                <li>Click on "Share"</li>
                <li>Underneath "Get Link", click on "Copy Link"</li>
                <li>Go back to your edit page and paste that link under where it says "Presentation link"</li> 
            </ol>
            <p>If that doesn't work, that probably means that the link you pasted in was an editor link. Make sure the link you paste in is meant for viewing only</p>

            <h2 id="slides-not-appearing">Why is my slideshow not appearing?</h2>
            <p>
                There could be several different issues, but the most likely reason is that you put in an invalid slideshow link. <br></br>
                <a href="#slideshow-setup">Take me there!</a>
                <br></br>
                If many other clubs' slideshows are not working either, that probably means the site is undergoing maintenance.
            </p>

            <h2 id="video-only">Why is only my video appearing? I had other stuff on the same slide!!!</h2>
            <p>
                Don't worry! This is intentional!
                <br></br>
                Due to limitations of the site, we can only display an embedded video by taking up the entire slide. In other words, when you put a video in a slide, that should be the only thing on that slide.
            </p>

            <h2 id="no-video">Why is my video not appearing</h2>
            <p>Xroads currently only supports YouTube videos that are embedded</p>
        </div>
    );
}

export {SlideHelp};