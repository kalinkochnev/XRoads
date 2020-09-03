import React from "react";


export function showOneError(formik) {
    let touched = Object.keys(formik.touched);
    for (var t_field of touched) {
      let error = formik.errors[t_field];
      if (error) {
        return <div class="error-box"><p>{error}</p></div>;
      }
    }
  }
  
export async function defaultFail(response, functions, data) {
    let body = await response.json();
    if (Object.keys(body).includes("non_field_errors")) {
        functions.setAlert("warning", body.non_field_errors[0], false);
    }
    for (var field of Object.keys(body)) {
        if (Object.keys(data.values).includes(field)) {
            functions.setFieldError(field, body[field][0])
        }
    }
}

export async function defaultOk(response, functions, data) {
    functions.setAlert("success", "Success!", false)
}

export function displayFormHelp(response, data, functions, okCallback, failCallback) {
    if (response.ok) {
        okCallback(response, functions, data)
    } else {
        failCallback(response, functions, data)
    }
}

