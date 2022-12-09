import React from "react";
import { View, Text, StyleSheet, ActivityIndicator } from "react-native";

const LoadingAnimation = ({ loading_message }) => {
  return (
    <View style={styles.indicatorWrapper}>
      <ActivityIndicator size="large" stycle={styles.indicator} />
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
  indicatorText: {
    fontSize: 18,
    marginTop: 12,
  },
});

export default LoadingAnimation;
