function filterObject(c) {
  var x, i;
  x = document.getElementsByTagName("h1"); // Target <h1> elements
  if (c == "Type") c = "";
  // Add the "show" class (display:block) to the filtered elements, and remove the "show" class from the elements that are not selected
  for (i = 0; i < x.length; i++) {
    removeClass(x[i], "show");
    if (x[i].textContent.trim() === c) addClass(x[i], "show"); // Compare text content with the provided value
  }
}

function addClass(element, name) {
  var i, arr1, arr2;
  arr1 = element.className.split(" ");
  arr2 = name.split(" ");
  for (i = 0; i < arr2.length; i++) {
    if (arr1.indexOf(arr2[i]) == -1) {element.className += " " + arr2[i];}
  }
}

function removeClass(element, name) {
  var i, arr1, arr2;
  arr1 = element.className.split(" ");
  arr2 = name.split(" ");
  for (i = 0; i < arr2.length; i++) {while (arr1.indexOf(arr2[i]) > -1) {arr1.splice(arr1.indexOf(arr2[i]), 1);}}
  element.className = arr1.join(" ");
}