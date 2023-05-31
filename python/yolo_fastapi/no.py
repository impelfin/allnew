function getUsers() {
    const xhr = new XMLHttpRequest();
    const method = "GET";
    const url = "/users";
    xhr.open(method, url);
    xhr.setRequestHeader("content-type", "application/json");
    xhr.send();

    xhr.onload = () => {
        if (xhr.status === 200) {
            const res = JSON.parse(xhr.response);
            console.log(res);
            const element = document.getElementById("ss5");
            element.innerHTML = JSON.stringify(res);
        } else {
            console.log("HTTP error", xhr.status, xhr.statusText);
        }
    };
}