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
    // übergabe wert wird festgelegt
    raw_data = data_uri;
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
// gets the base 64 string and saves it
function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      raw_data = e.target.result;
    };
    reader.readAsDataURL(input.files[0]);
  }
}
//  jquery listener on file selecter
$("#imageInput").change(function() {
  readURL(this);
});

function predict() {
  $.post(
    "http://127.0.0.1:5000/predict",
    {
      //delivers the data to the python backend
      data_uri: raw_data
    },
    function(data) {
      document.getElementById("carType").classList.remove("hidden");
      document.getElementById("carType").innerHTML = "Cartype: " + data;
    }
  );
}
