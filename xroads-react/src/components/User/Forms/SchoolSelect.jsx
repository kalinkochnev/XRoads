import React from "react";
import { Field, Formik } from "formik";
import * as Yup from "yup";
import "./SchoolSelect.scss";
import { signup } from "../../../service/xroads-api";

const SchoolSelectForm = ({ addAlert }) => {

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
      onSubmit={async (values, {}) => {
        //TODO: onsubmit for school selector
      }}
    >
      {(formik) => (
        <div class="accountLayout">
          <form onSubmit={formik.handleSubmit} className="accountForm">
            <div class="fields">
              <fieldset 
                class="school-select first-field last-field"
                {...formik.getFieldProps("school")}
              >

                <SchoolOption ID="1" name="Niskayuna HS" image="https://www.niskayunaschools.org/wp-content/uploads/2017/10/Niskayuna-HS-800x571.jpg"/>
                <SchoolOption ID="2" name="Iroquois MS" image="https://www.niskayunaschools.org/wp-content/uploads/2017/04/Iroquois-800x571.jpg"/>
                <SchoolOption ID="3" name="Van Antwerp MS" image="https://www.niskayunaschools.org/wp-content/uploads/2017/10/VanAntwerp-800x571.jpg"/>

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
          {this.props.name}
        </div>
      </label>
    );
  }
}



export default SchoolSelectForm;
