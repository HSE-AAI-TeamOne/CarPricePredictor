// Configure a few settings and attach camera
Webcam.set({
  width: 500,
  height: 375,
  image_format: "jpeg",
  jpeg_quality: 90
});
Webcam.attach("#my_camera");

var file_path;
var raw_data;

function take_snapshot() {
  // take snapshot and get image data
  Webcam.snap(function(data_uri) {
    // TODO dieser jpg data string base 64 an flask übergeben
    raw_data = data_uri;
    console.log("in func ", data_uri);
    // display results in page
    document.getElementById("results").innerHTML = '<img src="' + data_uri + '"/>';

    document.getElementById("saveButton").setAttribute("href", data_uri);
    document.getElementById("my_camera").classList.toggle("hidden");
    document.getElementById("results").classList.toggle("hidden");
    document.getElementById("snapButton").value = "Neues Foto aufnehmen";
  });
}

function showSaveButton() {
  document.getElementById("saveButton").classList.toggle("hidden");
}

const sleep = milliseconds => {
  return new Promise(resolve => setTimeout(resolve, milliseconds));
};

function predict() {
  sleep(1000).then(() => {
    let fg = "C:/Users/David/Downloads/CarPricePredictorImage.jpg";
    if (fg) {
      console.log(raw_data);
    }
    $.post(
      "http://127.0.0.1:5000/",
      {
        //   C:/Users/David/Downloads/CarPricePredictorImage.jpg
        data_uri: raw_data
      },
      function(data) {
        console.log(data);
        document.getElementById("carType").classList.remove("hidden");
        document.getElementById("carType").innerHTML = "Cartype: " + data;
      }
    );
  });
}
