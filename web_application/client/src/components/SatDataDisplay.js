import React from "react";

import { Text, View, StyleSheet, FlatList } from "react-native";

const SatDataDisplay = ({ sat_data }) => {
  console.log("Render Sat Display");
  console.log(sat_data);
  return (
    <View>
      <Text style={styles.titleText}> Matched Satellite Data: </Text>
      <FlatList
        data={sat_data}
        renderItem={({ item }) => {
          return (
            <View style={{ margin: 5 }}>
              <Text>
                {item.var}: {item.value}
              </Text>
            </View>
          );
        }}
        keyExtractor={(item) => item.var}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  titleText: {
    fontWeight: "bold",
    fontSize: 18,
    borderBottomWidth: 1,
    borderColor: "black",
    margin: 5,
  },
});

export default SatDataDisplay;
