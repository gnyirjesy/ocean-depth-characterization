import { createAppContainer } from "react-navigation";
import { createStackNavigator } from "react-navigation-stack";

import IndexScreen from "./src/screens/IndexScreen";
import ModelScreen from "./src/screens/ModelScreen";

const navigator = createStackNavigator(
  {
    Index: IndexScreen,
    Model: ModelScreen,
  },
  {
    initialRouteName: "Index",
    defaultNavigationOptions: {
      title: "Extending Satellite Data Observations",
      headerStyle: { backgroundColor: "#bfbfbf" },
      cardStyle: { backgroundColor: "#FFFFFF" },
    },
  }
);

export default createAppContainer(navigator);
