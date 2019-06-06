Webcam.set({
  width: 400,
  height: 300,
  image_format: "jpeg",
  jpeg_quality: 90
});
// für backend als base 64 string
var data_uri;
// variablen
var webcam_is_allowed = false;
var webcam_is_active = true;
var webcam_button = document.getElementById("webcam_button");
var webcam_snap = document.getElementById("webcam_snap");
// button für webcam enable, foto machen
function enable_webcam() {
  webcam_snap.setAttribute("class", "hidden");
  // fragt nach erlaubnis
  if (!webcam_is_allowed) {
    Webcam.attach("#webcam_preview");
    webcam_is_allowed = true;
  } else {
    if (webcam_is_active) {
      Webcam.freeze();
      take_snapshot();
      webcam_button.innerHTML = "Neues Auto aufnehmen";
      webcam_is_active = false;
    } else {
      Webcam.unfreeze();
      webcam_button.innerHTML = "Auto aufnehmen";
      webcam_is_active = true;
    }
  }
  // wenn webcam läuft
  Webcam.on("live", function() {
    webcam_button.innerHTML = "Auto aufnehmen";
  });
}

// coole lambda funktion, speichert webcam snapshot als base 64 in data_uri
function take_snapshot() {
  Webcam.snap(img_snap => (data_uri = img_snap));
}
function previewFile() {
  var file = document.querySelector("input[type=file]").files[0];
  var reader = new FileReader();

  reader.onloadend = function() {
    // TODO src festlegen im HTML <img>
    webcam_snap.src = reader.result;
    // legt die data uri fest
    data_uri = reader.result;
    webcam_snap.removeAttribute("class", "hidden");
  };

  if (file) {
    reader.readAsDataURL(file); //reads the data as a URL
  } else {
    webcam_snap.src = "";
  }
}
