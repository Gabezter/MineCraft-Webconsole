baseHref = (document.getElementsByTagName('base')[0] || {}).href;

fetch(baseHref + "/partials/header.html")
    .then(response => {
        return response.text()
    })
    .then(data => {
        document.querySelector("header").innerHTML = data;
    });