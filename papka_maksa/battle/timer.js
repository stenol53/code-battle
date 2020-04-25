const timerBorder = document.querySelector('.timer');
const timer = document.querySelector('.timer > .time');

let START_MIN = 5;
let START_SEC = 0;

let interval = setInterval(() => {
    if (START_SEC == 0) {
        START_SEC = 59;
        START_MIN--;
    } else {
        START_SEC--;
    }

    timer.textContent = `${START_MIN}:${START_SEC > 9 ? START_SEC : '0' + START_SEC}`;

    if (START_MIN == 0 && START_SEC == 0) {
        clearInterval(interval);
        timer.style.color = 'red';
        timerBorder.style.borderColor = 'red';
    }
}, 1000);