import React from "react";
import { View, Text, StyleSheet, Image } from "react-native";

import globeSpin from "../assets/globeLoad.gif";

const SpinningGlobe = ({ loading_message }) => {
  return (
    <View style={styles.indicatorWrapper}>
      <Image style={styles.loadingImg} source={{ uri: globeSpin }} />
      <Text style={styles.indicatorText}>{loading_message}...</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  indicatorWrapper: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    margin: 5,
  },
  loadingImg: {
    height: 200,
    width: 200,
  },
  indicatorText: {
    fontSize: 18,
    marginTop: 12,
  },
});

export default SpinningGlobe;
