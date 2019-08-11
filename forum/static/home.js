var newRequest = new XMLHttpRequest();

newRequest.open('GET', jsonURL);
newRequest.onload = function () {
    console.log(newRequest.responseText);
};

newRequest.send()