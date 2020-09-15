import React, { useEffect, useState } from "react";
import { Field, Formik } from "formik";
import * as Yup from "yup";
import "./SchoolSelect.scss";
import { sendRequest, signup } from "../../../service/xroads-api";
import { useStateValue } from "../../../service/State";
import { displayFormHelp, defaultFail } from '../../../components/User/Forms/helper';
import { useHistory } from "react-router-dom";

const SchoolSelectForm = ({ setAlert }) => {
  const [schools, setSchools] = useState([])
  const [state, dispatch] = useStateValue();
  let history = useHistory();

  useEffect(() => {
    sendRequest('school_list', {'districtId': state.user.district}, 'GET').then(response => {
      if (response.ok) {
        response.json().then(body => {
          setSchools(body);
        })
      } else {
        setAlert('warning', 'An error occurred while getting the schools')
      }
    })
  }, [state.user.district])

  const onSubmit = (values, { setSubmitting, setFieldError }) => {
    console.log(values)
    sendRequest('join_school', {'districtId': state.user.district, 'schoolId': values.school}, 'POST').then(response => {
      console.log(response);
      let successCallback = (response, functions, data) => {
        functions.setAlert("success", "You selected a school successfully!", true);
        console.log(state.user)
        dispatch({ type: 'join school', payload: Number(values.school) });
        console.log(state.user)
        history.push('/clubs');
      }

      let funcs = {
        'setAlert': setAlert
      }

      displayFormHelp(response, { 'values': values }, funcs, successCallback, defaultFail)
    })
    setSubmitting(false);
  }


  function showOneError(formik) {
    let touched = Object.keys(formik.touched);
    for (var t_field of touched) {
      let error = formik.errors[t_field];
      if (error) {
        return <div class="error-box"><p>{error}</p></div>;
      }
    }
  }

  return (

    <Formik
      initialValues={{
        school: "",
      }}
      validationSchema={Yup.object({
        school: Yup.string()
          .required("Select your school")
      })}
      onSubmit={onSubmit}
    >
      {(formik) => (
        <div class="accountLayout">
          <form onSubmit={formik.handleSubmit} className="accountForm">
            <div class="fields">
              <fieldset 
                class="school-select first-field last-field"
                {...formik.getFieldProps("school")}
              >
                { schools.map(school => <SchoolOption key={school.id} ID={school.id} name={school.name} image={school.img} />)}

              </fieldset>

              <button type="submit" id="account-submit">
                Start browsing
              </button>

            </div>
            {showOneError(formik)}
          </form>
        </div>
      )}

    </Formik>
  );
};

class SchoolOption extends React.Component {
  render() {
    return(
      <label class="school-option">
        <input name="school" type="radio" value={this.props.ID}/>
        <div class="option-content">
          <img src={this.props.image}/>
          <h3>{this.props.name}</h3>
        </div>
      </label>
    );
  }
}



export default SchoolSelectForm;
