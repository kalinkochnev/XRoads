import React from "react";


import './Body.scss';

// TODO eventually we should not have this component existing and just have it directly in the equivalent screen

const ClubBodyDetail = () => {
  return (
    <div class="clubDetails">
      <div class="clubHeading">
        <h1>Robotics Club</h1>
        <h2>Text @niskyrobot to 81010 to join</h2>
      </div>
      <div class="details">
        <p>
          <h2>What we do</h2>
          Robotics club is where all the action is at. We create robots and
          compete against other schools for the glory of having the best robot.
          We’re pretty good at what we do, and not to brag, but we qualified for
          the World Championships last year! That’s no joke!
        </p>
        <p>
          The First Tech Challenge (FTC) is an international organization where
          about 7,000 highschool teams go head to head in a competition that
          changes every year. No person alone could take on such an amazing
          feat. Robotics is about banding together with your peers to create
          something awesome.
        </p>
        <p>
          As a current club member, I can vouch and say that I have met some of
          the most creative, smart, funny and resourceful people ever. Robotics
          can be a rollercoaster of emotions sometimes. It definitely was last
          year. We were so happy that we qualified for worlds, but later
          disappointed when it was canceled because of COVID.
        </p>
        <p>
          <h2>Who its for</h2>
          Robotics is probably the best opportunity you have in high school to
          take STEM to the next level. If you love engineering or coding, this
          is a great place to apply what you learn. If you want to learn coding
          or engineering, this is a great place to learn. If you don’t even like
          coding or engineering, but like tough problem solving and fierce
          competition, this is a ton of fun. What we’re trying to say is that
          there’s no reason not to join.
        </p>
        <p>
          Building a robot takes a lot of time and that’s why we meet as much as
          we do, but it doesn’t mean that you can’t join if you’re a busy
          person. Members always welcome to pop in for whatever time they’re
          available for.
        </p>
        <p>
          Robotics is all about being able to react as situations change.
          Sometimes we have a plan, but most of the time we’re winging it.
          Robotics is definitely going to be different this year due to COVID,
          but we have a plan (we’re totally winging it) and it’s gonna be more
          exciting than ever before.
        </p>
        <div class="clubHeading">
          <h1>FAQ</h1>
        </div>
        <p>
          <h3>Q: When do we meet?</h3>
          A: We meet twice a week, mondays and fridays under normal
          circumstances. Depending on what the situation is like, it may change
          so be sure to check back.
        </p>
        <p>
          <h3>Q: I don’t have a lot of experience, can I still join?</h3>
          A: Yeah anybody can join! You end up learning as you go. Even if you
          aren’t interested in STEM, there’s lots of other stuff you can do.
        </p>
        <p>
          <h3>Q: What language do you program your robots in?</h3>
          A: We use a set of two android phones as the brains of our robot. We
          write java to control the various motors and sensors on board.
        </p>
        <p>
          <h3>Q: What are your robots made of?</h3>
          A: We use all sorts of materials, but the main robot design is made
          from aluminum. We use 3D printed and custom parts all the time as
          well.
        </p>
      </div>
    </div>
  );
};

export default ClubBodyDetail;
