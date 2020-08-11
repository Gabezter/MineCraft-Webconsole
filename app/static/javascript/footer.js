baseHref = (document.getElementsByTagName("base")[0] || {}).href;

fetch(baseHref + "/partials/footer.html")
    .then((response) => {
        return response.text();
    })
    .then(data => {
        document.querySelector("footer").innerHTML = data;
    });