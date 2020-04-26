const timerBorder = document.querySelector('.timer');
const timer = document.querySelector('.timer > .time');

let START_MIN = 0;
let START_SEC = 30;

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

// Switch active problem

const problems = document.querySelectorAll('.problem');
const submitButton = document.querySelector('.task-answers-submit');

// Removes class=current from all who has it
function clearActive() {
    document.querySelectorAll('.current').forEach(el => {
        el.classList.remove('current');
    });
}

// Change color on click
problems.forEach(problem => {
    problem.addEventListener('click', () => {
        clearActive();
        problem.classList.add('current');
    });
});

let i = 3;
// Switch current task on submit click
submitButton.addEventListener('click', (e) => {
    e.preventDefault();

    // Здесь будет ajax запрос к серверу 
    // который вернет информацию о следующей задаче

    if (problems[i]) {
        clearActive();
        problems[i++].classList.add('current');
    }
});