function passwordvalidation() {
  var x = document.forms["form"]["password"].value;
  if (x == "") {
    alert("Lösenordet innehåller inte kraven");
    return false;
  }
}
