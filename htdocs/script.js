function deleteReq(){
  var request = new XMLHttpRequest();

  doc = document.getElementById("url");

  file = doc.value;

  console.log(file);

  url = "http://localhost:8080/" + file;

  request.open("DELETE",file);

  console.log("delete");

  request.send();
}