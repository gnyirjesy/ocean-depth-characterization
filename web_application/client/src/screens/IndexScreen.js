import React, { useState } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  TextInput,
  StyleSheet,
  Button,
} from "react-native";
import DatePicker from "../components/DatePicker";
import MapDisplay from "../components/MapDisplay";
import DateDropDown from "../components/DateDropdown";
import DropDownPicker from "react-native-dropdown-picker";

const IndexScreen = ({ navigation }) => {
  // const [date, setDate] = useState(new Date("March 1, 2022"));
  const [locData, setLocData] = useState({
    latitude: 40,
    longitude: -60,
  });

  const [open, setOpen] = useState(false);
  const [date, setDate] = useState("202231");
  const [items, setItems] = useState([
    { label: "March 1, 2022", value: "202231" },
    { label: "Sept 1, 2022", value: "202291" },
  ]);

  const [mapData, setMapData] = useState({
    mapLat: 40,
    mapLon: -60,
  });
  return (
    <View>
      <View style={styles.pageCont}>
        <View>
          <Text style={styles.inputLabel}>
            Please enter a date and location to begin:
          </Text>
          <View style={styles.dateInputCont}>
            <DropDownPicker
              open={open}
              value={date}
              items={items}
              setOpen={setOpen}
              setValue={setDate}
              setItems={setItems}
              style={{ marginTop: open ? 50 : 10 }}
            />
          </View>
          {/* LAT INPUT */}
          <Text style={styles.inputLabel}> latitude: </Text>
          <View style={styles.textInputCont}>
            <TextInput
              style={styles.inputCont}
              value={locData.latitude}
              onChangeText={(newLat) => {
                setLocData({ ...locData, latitude: newLat });
              }}
            />
          </View>

          {/* LON INPUT */}
          <Text style={styles.inputLabel}> longitude: </Text>
          <View style={styles.textInputCont}>
            <TextInput
              style={styles.inputCont}
              value={locData.longitude}
              onChangeText={(newLon) => {
                setLocData({ ...locData, longitude: newLon });
              }}
            />
          </View>
          <View style={styles.buttonCont}>
            <Button
              title="1. Show prediction location"
              onPress={() => {
                setMapData({
                  ...mapData,
                  mapLon: locData.longitude,
                  mapLat: locData.latitude,
                });
              }}
            />
          </View>
          <View style={styles.buttonCont}>
            <Button
              title="2. Continue to model prediction"
              onPress={() => {
                navigation.navigate("Model", {
                  satData: {
                    latitude: locData.latitude,
                    longitude: locData.longitude,
                    date: date,
                  },
                });
              }}
            />
          </View>
        </View>

        {/* MAP DISPLAY IMAGE */}
        <MapDisplay mapCoords={mapData} />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  inputCont: {
    borderWidth: 1,
    borderColor: "black",
    margin: 5,
  },
  inputLabel: {
    margin: 5,
  },
  buttonCont: {
    flexDirection: "row",
    justifyContent: "flex-start",
    margin: 5,
  },
  textInputCont: {
    flexDirection: "row",
    alignContent: "flex-start",
  },
  dateInputCont: {
    margin: 5,
    flexDirection: "row",
  },
  pageCont: {
    flexDirection: "row",
  },
});

export default IndexScreen;
