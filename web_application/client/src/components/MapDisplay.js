import React from "react";
import { StyleSheet, Text, View, Dimensions, Image } from "react-native";
// import staticmap from "../api/staticmap";

const MapDisplay = ({ mapCoords }) => {
  const mapkey = "AIzaSyBRsCTzlHWb89XJ5hKzPmtvSD9jofrzCFM";
  return (
    <View style={styles.mapContainer}>
      <Image
        source={{
          uri: `https://maps.googleapis.com/maps/api/staticmap?center=${mapCoords.mapLat}%2C${mapCoords.mapLon}&zoom=2&scale=2&size=600x300&maptype=roadmap&format=png&key=${mapkey}&markers=size:mid%7Ccolor:0xff0000%7Clabel:%7C${mapCoords.mapLat}%2C${mapCoords.mapLon}`,
        }}
        style={styles.magImage}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  mapContainer: {
    flexDirection: "row",
    justifyContent: "center",
    margin: 10,
  },
  mapView: {
    alignSelf: "center",
  },
  magImage: {
    width: 400,
    height: 400,
  },
});

export default MapDisplay;
