import React, { useState } from "react";
import DropDownPicker from "react-native-dropdown-picker";

const DateDropdown = () => {
  const [open, setOpen] = useState(false);
  const [value, setValue] = useState(null);
  const [items, setItems] = useState([
    { label: "March 1, 2022", value: "202231" },
    { label: "Sept 1, 2022", value: "202291" },
  ]);

  return (
    <DropDownPicker
      open={open}
      value={value}
      items={items}
      setOpen={setOpen}
      setValue={setValue}
      setItems={setItems}
      style={{ marginTop: open ? 50 : 10 }}
    />
  );
};

export default DateDropdown;
