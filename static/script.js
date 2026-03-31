let time = 20 * 60;

setInterval(() => {
    let m = Math.floor(time / 60);
    let s = time % 60;

    document.getElementById("timer").innerText =
        m + ":" + (s < 10 ? "0" : "") + s;

    time--;

    if (time < 0) {
        alert("Time up!");
        document.querySelector("form").submit();
    }
}, 1000);

window.onbeforeunload = function () {
    return "Exam is in progress!";
};