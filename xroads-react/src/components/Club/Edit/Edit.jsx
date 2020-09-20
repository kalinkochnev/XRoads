import React, { useEffect } from "react";

import "./Edit.scss";

import RichEditor from "../../Common/RichEditor/RichEditor";
import { TextSlide, ImageSlide, VideoSlide } from "../../Common/Slides/Slides";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Formik } from "formik";
import * as Yup from "yup";

import {
  faFilm,
  faFont,
  faImage,
  faImages,
  faTextHeight,
  faVideo,
} from "@fortawesome/free-solid-svg-icons";
import { useState } from "react";
import { sendRequest, updateClub } from "../../../service/xroads-api";
import { useStateValue } from "../../../service/State";
import ReactTooltip from "react-tooltip";

import { store } from "react-notifications-component";
import IconButton from "../../Common/IconButton/IconButton";

import { confirmAlert } from "react-confirm-alert";
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
    const districtId = 1;
    const updatedClub = {
      ...props.club,
      description: clubDescriptionMd,
      name: clubName,
      join_promo: clubJoinPromo,
    };
    console.log("Updated club would be", updatedClub);
    updateClub(districtId, props.club.school, props.club.id, updatedClub).then(
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

  // FIXME this will not work if someone has edit access but has a different school
  const toggleHide = () => {
    let user = state.user;
    let urlArgs = {
      districtId: user.district,
      schoolId: user.school,
      clubId: props.club.id,
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
            <span class="slider round"></span>
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

const SlideshowEdit = (props) => {
  return (
    <div className="centerContent">
      <div className="editBody">
        <div className="slideshowSelect">
          {props.club.slides.map((slide) => {
            if (slide.img) {
              return (
                <div className="slideContain">
                  {" "}
                  <ImageSlide
                    key={slide.id}
                    source={slide.img}
                    caption={slide.text}
                  />{" "}
                </div>
              );
            } else if (slide.video_url) {
              return (
                <div className="slideContain">
                  {" "}
                  <VideoSlide
                    key={slide.id}
                    videoURL={slide.video_url}
                    caption={slide.text}
                  />{" "}
                </div>
              );
            } else {
              return (
                <div className="slideContain">
                  {" "}
                  <TextSlide
                    key={slide.id}
                    title={slide.text}
                    body={slide.text}
                    color="lightblue"
                  />{" "}
                </div>
              );
            }
          })}
          <div className="slideContain addSlide">
            <div className="add">
              <FontAwesomeIcon icon={faFont} />
              Add a text slide
            </div>
            <div className="add middle">
              <FontAwesomeIcon icon={faImage} />
              Add an image slide
            </div>
            <div className="add">
              <FontAwesomeIcon icon={faFilm} />
              Add a video slide
            </div>
          </div>
          <div className="spacer"></div>
        </div>
        <div className="slideshowPreview">
          {(function () {
            let slide = props.club.slides[0];
            if (slide.img) {
              return (
                <div className="slideContain">
                  {" "}
                  <ImageSlide
                    key={slide.id}
                    source={slide.img}
                    caption={slide.text}
                  />{" "}
                </div>
              );
            } else if (slide.video_url) {
              return (
                <div className="slideContain">
                  {" "}
                  <VideoSlide
                    key={slide.id}
                    videoURL={slide.video_url}
                    caption={slide.text}
                  />{" "}
                </div>
              );
            } else {
              return (
                <div className="slideContain">
                  {" "}
                  <TextSlide
                    key={slide.id}
                    title={slide.text}
                    body={slide.text}
                    color="lightblue"
                  />{" "}
                </div>
              );
            }
          })()}
        </div>
        <form className="clubEdit">
          <label for="title">
            Slide Template
            <br />
            <select class="short" id="title" name="title">
              <option>Text</option>
              <option>Image</option>
              <option>Video</option>
            </select>
          </label>

          <label className="" for="title">
            Title
            <br />
            <input class="medium" type="text" id="title" name="title" />
          </label>

          <label className="" for="body">
            Body
            <br />
            <input class="long" type="text" id="body" name="body"></input>
          </label>
        </form>
      </div>
    </div>
  );
};

const QuestionCard = (props) => {
  const [answer, setAnswer] = useState(props.answer);
  const [display, setDisplay] = useState(false);
  let user = props.user;

  let replyClick = () => {
    setDisplay(!display);
  };

  let replyForm = (questionId) => {
    let onSubmit = (values, { setSubmitting, setFieldError }) => {
      let urlArgs = {
        districtId: user.district,
        schoolId: user.school,
        clubId: props.club.id,
      };
      let body = {
        question: questionId,
        answer: values.answer,
      };
      sendRequest("answer_question", urlArgs, "POST", body).then((response) => {
        if (response.ok) {
          setDisplay(false);
          console.log(values.answer);
          setAnswer(values.answer);
          store.addNotification({
            title: "Success!",
            message: "Your answer should be delivered shortly!",
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
      <Formik
        initialValues={{ quanswerestion: "" }}
        validationSchema={Yup.object({
          answer: Yup.string().required("Answer is required"),
        })}
        onSubmit={onSubmit}
      >
        {(formik) => (
          <form onSubmit={formik.handleSubmit}>
            <div className="editBody" style={{ marginTop: "20px" }}>
              <textarea
                placeholder="A very helpful answer..."
                {...formik.getFieldProps("answer")}
              ></textarea>
            </div>
            <button
              type="submit"
              id="account-submit"
              style={{ marginTop: "20px", marginBottom: "0px" }}
            >
              Answer
            </button>
          </form>
        )}
      </Formik>
    );
  };

  return (
    <div className="questionCard">
      <h3>{props.question}</h3>
      {answer == null ? (
        <IconButton
          icon={"faReply"}
          filled={true}
          color="gray"
          size="2x"
          customClickEvent={replyClick}
        ></IconButton>
      ) : (
          <p>
            <i>Answer: </i> {answer}
          </p>
        )}
      {display ? replyForm(props.id) : null}
    </div>
  );
};

const ManageQuestions = (props) => {
  let [{ user }, dispatch] = props.stateValue;
  let [questions, setQuestions] = useState([]);

  let showUnansweredFirst = (questions) => {
    let newOrder = [];
    for (let question of questions) {
      if (question.answer == null) {
        newOrder.splice(0, 0, question);
      } else {
        newOrder.push(question);
      }
    }
    return newOrder;
  };

  useEffect(() => {
    let urlArgs = {
      districtId: user.district,
      schoolId: user.school,
      clubId: props.club.id,
    };
    sendRequest("get_questions", urlArgs, "get").then((response) => {
      if (response.ok) {
        response.json().then((body) => {
          setQuestions(showUnansweredFirst(body));
        });
      }
    });
  }, [user]);

  return (
    <div className="centerContent">
      <label class="switch">
        <span class="slider round"></span>
      </label>
      <div className="editBody">
        {questions.map((question) => {
          return (
            <QuestionCard
              user={user}
              club={props.club}
              id={question.id}
              question={question.question}
              answer={question.answer}
            />
          );
        })}
      </div>
    </div>
  );
};

const EditorCard = (props) => {
  let editor = props.editor.profile;
  let name = editor.first_name + " " + editor.last_name;
  let user = props.user;
  const [display, setDisplay] = useState(true);

  // TODO If you are a club advisor remove the x from yourself

  const removeEditor = () => {
    const sendRemove = () => {
      let urlArgs = {
        districtId: user.district,
        schoolId: user.school,
        clubId: props.club.id,
      };
      sendRequest("remove_editor", urlArgs, "POST", {
        email: editor.email,
      }).then((response) => {
        if (response.ok) {
          setDisplay(false);
        }
      });
    };

    confirmAlert({
      title: "Confirm removal",
      message: `Are you sure you want to remove ${editor.email}?`,
      buttons: [
        { label: "Yes", onClick: sendRemove },
        { label: "No", onClick: () => null },
      ],
    });
  };

  if (!display) {
    return null;
  }

  return (
    <div className="editorCard">
      <div className="editorInfo">
        <h2>{name}</h2>
        <p>{editor.email}</p>
      </div>
      <div className="modify">
        <p>{props.editor.perms}</p>
        <IconButton
          icon={"faTimes"}
          filled={true}
          color="gray"
          size="2x"
          customClickEvent={removeEditor}
        />
      </div>
    </div>
  );
};
const EditAccess = (props) => {
  const [state, dispatch] = props.stateValue;
  let user = state.user;
  let club = props.club;
  const [editors, setEditors] = useState([]);
  const [displayAdd, setDisplay] = useState(false);

  const onSubmit = (values, { setSubmitting, setFieldError }) => {
    let urlArgs = {
      districtId: user.district,
      schoolId: user.school,
      clubId: props.club.id,
    };
    sendRequest("add_editor", urlArgs, "POST", {email: values.email, permissions: []}).then((response) => {
      if (response.ok) {
        response.json().then(body => {
          setEditors(editors.concat(body))
          store.addNotification({
            title: "Success!",
            message: `Your added ${values.email} as an editor!`,
            type: "success",
            insert: "top",
            container: "top-right",
            dismiss: {
              duration: 5000,
              onScreen: true,
            },
          });
        })
        
      };
    });

    setSubmitting(false);

  };

  useEffect(() => {
    let urlArgs = {
      districtId: user.district,
      schoolId: user.school,
      clubId: club.id,
    };
    sendRequest("list_editors", urlArgs, "GET").then((response) => {
      if (response.ok) {
        response.json().then((body) => {
          console.log(body);
          setEditors(body);
        });
      }
    });
  }, [state.user]);

  return (
    <div className="editorManager">
      {editors.map((editor) => (
        <EditorCard user={user} editor={editor} club={club} />
      ))}
      <div className="editorCard">
        <Formik
          initialValues={{ email: "", permission: "" }}
          validationSchema={Yup.object({
            email: Yup.string().email().required('Email must be provided'),
            permission: Yup.string()
          })}
          onSubmit={onSubmit}
        >
          {(formik) => (
            <form onSubmit={formik.handleSubmit} className="addEditor">
              <div className="addForm editBody">
              <input placeholder="User email address" {...formik.getFieldProps("email")}></input>
              <button type="submit" className="addEditorButton">
                Add editor
              </button>
              </div>
              
            </form>
          )}
        </Formik>
      </div>
    </div>
  );
};

export { GeneralEdit, SlideshowEdit, ManageQuestions, EditAccess };
