import React, { useEffect } from "react";

import "./Edit.scss";

import RichEditor from "../../Common/RichEditor/RichEditor";

import { useState } from "react";
import { sendRequest, updateClub } from "../../../service/xroads-api";
import { useStateValue } from "../../../service/State";
import ReactTooltip from "react-tooltip";

import { store } from "react-notifications-component";

import "react-confirm-alert/src/react-confirm-alert.css"; // Import css for alert

const GeneralEdit = (props) => {
  let [clubDescriptionMd, setClubDescription] = useState(
    props.club.description
  );
  let [clubName, setClubName] = useState(props.club.name);
  let [clubJoinPromo, setClubJoinPromo] = useState(props.club.join_promo);
  const [state, dispatch] = useStateValue();
  const [isVisible, setVisibility] = useState(props.club.is_visible);

  const handleClubDescription = (clubDescMd) => {
    setClubDescription(clubDescMd);
  };

  const saveClubDetails = () => {
    // FIXME : pull the district ID from whereever it lives in the context
    const updatedClub = {
      ...props.club,
      description: clubDescriptionMd,
      name: clubName,
      // join_promo: clubJoinPromo, TODO fix
    };

    console.log("Updated club would be", updatedClub);
    updateClub(props.club.id, updatedClub, props.code).then(
      (res) => {
        res.json().then((updatedClub) => {
          console.log("Updated club", updateClub);
          store.addNotification({
            title: "Saved",
            message: "Club details successfully saved",
            type: "success",
            insert: "top",
            container: "top-right",
            dismiss: {
              duration: 5000,
              onScreen: true,
            },
          });
        });
      }
    );
  };

  const toggleHide = () => {
    let user = state.user;
    let urlArgs = {
      clubId: props.club.id,
      code: props.code
    };
    sendRequest("toggle_hide_club", urlArgs, "POST", {}).then((response) => {
      if (response.ok) {
        setVisibility(!isVisible);
        console.log("The club is now " + isVisible.toString());
        store.addNotification({
          title: "Club " + (isVisible ? "Hidden" : "Visible"),
          message:
            "The club is now visible to " +
            (isVisible ? "club editors only" : "all users"),
          type: "success",
          insert: "top",
          container: "top-right",
          dismiss: {
            duration: 5000,
            onScreen: true,
          },
        });
      }
    });
  };

  return (
    <div className="centerContent">
      <div className="editBody">
        <form className="clubEdit">
          <label className="" htmlFor="join">
            Hide club
          </label>
          <label class="switch">
            <input type="checkbox" onClick={toggleHide} checked={!isVisible} />
            <span className="slider round"></span>
          </label>
          <ReactTooltip place="right" effect="solid" />

          <label className="" htmlFor="join">
            How to join
            <br />
            <input
              type="text"
              id="join"
              name="join"
              value={clubJoinPromo}
              onChange={(e) => setClubJoinPromo(e.target.value)}
            />
          </label>

          <label className="" htmlFor="description">
            Description
            <br />
            <RichEditor
              mdContent={clubDescriptionMd}
              onChange={handleClubDescription}
            />
          </label>
        </form>
        <button type="submit" id="club-submit" onClick={saveClubDetails}>
          Save
        </button>
      </div>
    </div>
  );
};


export { GeneralEdit };
