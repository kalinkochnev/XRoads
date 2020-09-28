import React, { useEffect } from "react";

import "./Edit.scss";

import RichEditor from "../../Common/RichEditor/RichEditor";
import { TextSlide, ImageSlide, VideoSlide } from "../../Common/Slides/Slides";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Field, Form, Formik } from "formik";
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
    let length = this.state.slides.length;
    this.state.slides.push({
      club: this.props.club.id,
      img: "",
      position: length + 1,
      template_type: type,
      text: "",
      body: "",
      video_url: ""
    });
    this.assignPositions();
    this.setState({ activeKey: length });
    this.forceUpdate();
  }

  deleteSlide = (position) => {
    if (this.state.slides.length == 1) {
      console.log("You can't remove all the slides")
    }
    else {
      this.state.slides.splice(position - 1, 1);
      this.setState({ activeKey: 0 });
      this.assignPositions();
      this.forceUpdate();
    }
  }

  moveSlide = (direction) => {
    let slides = this.state.slides;

    if (direction == -1 && this.state.activeKey > 0) {
      slides.splice(this.state.activeKey - 1, 0, slides.splice(this.state.activeKey, 1)[0]);
      this.setState({ activeKey: this.state.activeKey - 1 });
    }
    else if (direction == 1 && this.state.activeKey < slides.length - 1) {
      slides.splice(this.state.activeKey + 1, 0, slides.splice(this.state.activeKey, 1)[0]);
      this.setState({ activeKey: this.state.activeKey + 1 });
    }
    this.assignPositions();
    this.forceUpdate();
  }

  assignPositions = () => {
    let slides = this.state.slides;
    for (let i = 0; i < slides.length; i++) {
      slides[i].position = i + 1;
      console.log("hello");
      this.forceUpdate();
    }
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
              <div className="add" onClick={() => { this.addSlide(4) }}><FontAwesomeIcon icon={faFont} />Add text</div>
              <div className="add middle" onClick={() => { this.addSlide(1) }}><FontAwesomeIcon icon={faImage} />Add an image</div>
              <div className="add" onClick={() => { this.addSlide(3) }}><FontAwesomeIcon icon={faFilm} />Add a video</div>
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
                  return <TextSlide key={slide.id} title={slide.text} body={slide.body} color="lightblue" />
                }
              })()
            }
          </div>
          <form className="clubEdit">
            <div class="slideControls">
              <IconButton
                icon={"faAngleDoubleRight"}
                filled={true}
                color="gray"
                size="2x"
                customClickEvent={() => { this.moveSlide(1) }}
                tip="move right"
              />
              <IconButton
                icon={"faTrash"}
                filled={true}
                color="darkred"
                size="2x"
                customClickEvent={() => { this.deleteSlide(this.state.slides[this.state.activeKey].position) }}
                tip="delete slide"
              />
              <IconButton
                icon={"faAngleDoubleLeft"}
                filled={true}
                color="gray"
                size="2x"
                customClickEvent={() => { this.moveSlide(-1) }}
                tip="move left"
              />
            </div>
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
                        <input class="long" type="text" id="body" name="body" value={slide.body} onChange={(e) => { slide.body = e.target.value; this.forceUpdate() }} />
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
  let [editors, setEditors] = props.editors;
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
          setEditors([...editors].filter(item => item.email != editor.email))

          setDisplay(false);
          store.addNotification({
            title: "Success",
            message: `You removed ${name} from the club editors`,
            type: "success",
            insert: "top",
            container: "top-right",
            dismiss: {
              duration: 5000,
              onScreen: true,
            },
          });
        } else if (response.status == 403) {
          store.addNotification({
            title: "Permission Denied",
            message: "You don't have permission to remove this user",
            type: "danger",
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
        <p>{props.editor.perms.join(", ")}</p>
        {editor.email != user.email ? <IconButton
          icon={"faTimes"}
          filled={true}
          color="gray"
          size="2x"
          customClickEvent={removeEditor}
        /> : <p>(You)</p>}

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
  const [possPerms, setPerms] = useState([]);

  const onSubmit = (values, { setSubmitting, setFieldError }) => {
    let urlArgs = {
      districtId: user.district,
      schoolId: user.school,
      clubId: props.club.id,
    };
    sendRequest("add_editor", urlArgs, "POST", { ...values, permissions: [values.permissions] }).then((response) => {
      if (response.ok) {
        response.json().then(body => {
          console.log(body)
          setEditors([...editors].concat(body))

          // If the length is the same, that means it was updated instead
          let successMessage = `Your added ${values.email} as an editor!`;

          store.addNotification({
            title: "Success!",
            message: successMessage,
            type: "success",
            insert: "top",
            container: "top-right",
            dismiss: {
              duration: 5000,
              onScreen: true,
            },
          });
        })

      } else if (response.status == 403) {
        store.addNotification({
          title: "Permission Denied",
          message: "You don't have permission to change this user",
          type: "danger",
          insert: "top",
          container: "top-right",
          dismiss: {
            duration: 5000,
            onScreen: true,
          },
        });
      }
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
          setPerms(body.poss_perms);
          setEditors(body.admins);
        });
      }
    });
  }, [state.user]);

  return (
    <div className="editorManager">
      {editors.map((editor) => (
        <EditorCard user={user} editor={editor} club={club} editors={[editors, setEditors]} />
      ))}
      <div className="editorCard">
        <Formik
          initialValues={{ email: "", permissions: possPerms[0] }}
          validationSchema={Yup.object({
            email: Yup.string().email().required('Email must be provided'),
            permissions: Yup.string()
          })}
          onSubmit={onSubmit}
        >
          <Form className="addEditor">
            <div className="addForm editBody">
              <Field name="email" type="email" placeholder="User email"></Field>
              <Field name="permissions" as="select" >
                <option selected disabled default>Select one</option>
                {possPerms.map((perm) => <option value={perm}>{perm}</option>)}
              </Field>
              <button type="submit" className="addEditorButton">
                Add editor
              </button>
            </div>
          </Form>
        </Formik>
      </div>
    </div>
  );
};

export { GeneralEdit, SlideshowEdit, ManageQuestions, EditAccess };
