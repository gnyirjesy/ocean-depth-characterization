import axios from "axios";

export default axios.create({
  baseURL:
    "https://maps.googleapis.com/maps/api/staticmap?center=40%2C-60&zoom=3&scale=2&size=600x300&maptype=roadmap&format=png&key=AIzaSyDWNHa7bl41DeifSUFHFJlXfYSde2J1ZUk&markers=size:mid%7Ccolor:0xff0000%7Clabel:%7C40%2C-60",
});
