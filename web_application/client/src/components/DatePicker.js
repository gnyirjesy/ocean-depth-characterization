import React, { useState, createElement } from "react";

const DatePicker = ({ value, onChange }) => {
  return createElement("input", {
    type: "date",
    value: value,
    onInput: onChange,
  });
};

export default DatePicker;
