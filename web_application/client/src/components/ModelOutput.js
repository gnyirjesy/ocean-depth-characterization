import React, { useState } from "react";
import useDownloader from "react-use-downloader";

import { View, Text, StyleSheet, Button } from "react-native";
import {
  VictoryChart,
  VictoryLine,
  VictoryTheme,
  VictoryAxis,
  VictoryLabel,
} from "victory";
import model from "../api/model";

const baseFileUrl = "http://127.0.0.1:105/getPlotCSV";
const filename = "model_output.csv";
const ModelOutput = ({ model_data }) => {
  const list_model_data = [];
  model_data.forEach((element) => {
    list_model_data.push(element.x, element.y);
  });

  const { download } = useDownloader({
    headers: {
      model_data: list_model_data,
    },
  });

  async function downloadData() {
    console.log(model_data);
    download(baseFileUrl, filename);
  }

  return (
    <View>
      <Text style={{ margin: 5 }}>Model Results:</Text>
      <View style={styles.chartCont}>
        <VictoryChart
          theme={VictoryTheme.material}
          animate={{ duration: 3000, easing: "linear" }}
          style={{
            data: { stroke: "green" },
          }}
          height={400}
          width={700}
        >
          <VictoryLine data={model_data} />
          <VictoryAxis
            dependentAxis
            label="Chlor_a Prediction"
            style={{
              grid: { stroke: "black", strokeWidth: 1 },
            }}
            axisLabelComponent={
              <VictoryLabel dy={-33} style={{ fontSize: 13, margin: 5 }} />
            }
          />
          <VictoryAxis
            style={{
              grid: { stroke: "black", strokeWidth: 1 },
            }}
            label="Normalized Depth"
            axisLabelComponent={
              <VictoryLabel dy={33} style={{ fontSize: 13, margin: 5 }} />
            }
          />
        </VictoryChart>
      </View>
      <View style={styles.buttonContCenter}>
        <Button
          title="download data as csv"
          onPress={() => {
            console.log("Download data");
            downloadData();
          }}
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  textCont: {
    margin: 5,
  },
  chartCont: {
    flexDirection: "row",
    alignContent: "center",
    borderColor: "black",
    borderWidth: 2,
    height: 500,
    width: 800,
    margin: 10,
  },
  buttonContCenter: {
    flexDirection: "row",
    justifyContent: "flex-start",
    margin: 5,
  },
});

export default ModelOutput;
