import React, { useState } from "react";
import { View, Text, TouchableOpacity, Button, StyleSheet } from "react-native";

import LoadingAnimation from "../components/LoadingAnimation";
import SatDataDisplay from "../components/SatDataDisplay";
import ModelOutput from "../components/ModelOutput";
import SpinningGlobe from "../components/SpinningGlobe";

import model from "../api/model";

const ModelScreen = ({ navigation }) => {
  const { latitude, longitude, date } = navigation.getParam("satData");

  const [satState, setSatState] = useState({
    sat_data: [],
    show_sat_data: false,
    currently_loading: false,
  });

  const [modelState, setModelState] = useState({
    model_output: [],
    show_model_output: false,
    currently_loading: false,
  });

  const getSatteliteData = (lat, lon, date) => {
    setSatState({ ...satState, currently_loading: true });
    model.get(`/sat_pull/${date}/${lat}/${lon}`).then((result) => {
      setSatState({
        ...satState,
        currently_loading: false,
        show_sat_data: true,
        sat_data: result.data.sat_data,
      });
    });
  };

  const runModel = () => {
    setModelState({ ...modelState, currently_loading: true });
    console.log(satState.sat_data);
    const lat = satState.sat_data[0].value;
    const lon = satState.sat_data[1].value;
    const pic = satState.sat_data[2].value;
    const date = satState.sat_data[3].value;
    const sst = satState.sat_data[4].value;
    const aph = satState.sat_data[5].value;
    const par = satState.sat_data[6].value;
    const chlor_a = satState.sat_data[7].value;
    model
      .get(
        `/run_model/${date}/${lat}/${lon}/${chlor_a}/${sst}/${pic}/${aph}/${par}`
      )
      .then((result) => {
        setModelState({
          ...modelState,
          currently_loading: false,
          model_output: result.data.model_data,
          show_model_output: true,
        });
      });
  };

  return (
    <View>
      <View style={styles.textCont}>
        <Text>
          In order to make prediction about ({latitude}, {longitude}) on {date},
          need to query NASA's sattelite data. Note: this process may take up to
          30 seconds.
        </Text>
      </View>

      <View style={styles.buttonCont}>
        <Button
          title="Get satellite data"
          onPress={() => getSatteliteData(latitude, longitude, date)}
        />
      </View>

      {satState.currently_loading ? (
        <SpinningGlobe loading_message="getting sat data" />
      ) : satState.show_sat_data ? (
        <SatDataDisplay sat_data={satState.sat_data} />
      ) : null}
      {satState.show_sat_data ? (
        <View style={styles.buttonCont}>
          <Button title="Run model" onPress={() => runModel()} />
        </View>
      ) : null}
      {modelState.show_model_output ? (
        <ModelOutput model_data={modelState.model_output} />
      ) : null}
    </View>
  );
};

const styles = StyleSheet.create({
  buttonCont: {
    flexDirection: "row",
    justifyContent: "flex-start",
    margin: 5,
  },
  textCont: {
    margin: 5,
  },
});

export default ModelScreen;
