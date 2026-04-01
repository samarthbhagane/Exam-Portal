const timerElement = document.getElementById("timer");
const examForm = document.querySelector("form");

if (timerElement && examForm) {
    let time = Number(timerElement.dataset.duration || 300);
    let examSubmitted = false;
    let timerInterval = null;

    const renderTime = () => {
        const minutes = Math.floor(time / 60);
        const seconds = time % 60;
        timerElement.innerText = `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
    };

    const submitExam = () => {
        if (examSubmitted) {
            return;
        }

        examSubmitted = true;
        window.onbeforeunload = null;
        examForm.submit();
    };

    const startTimer = () => {
        renderTime();

        timerInterval = setInterval(() => {
            time -= 1;

            if (time <= 0) {
                clearInterval(timerInterval);
                timerElement.innerText = "00:00";
                alert("Time is up. Your test will be submitted automatically.");
                submitExam();
                return;
            }

            renderTime();
        }, 1000);
    };

    examForm.addEventListener("submit", () => {
        examSubmitted = true;
        window.onbeforeunload = null;

        if (timerInterval) {
            clearInterval(timerInterval);
        }
    });

    window.onbeforeunload = function () {
        if (!examSubmitted) {
            return "Exam is in progress!";
        }
    };

    renderTime();
    alert("You have 5 minutes to complete the test. Click OK to start.");
    startTimer();
}