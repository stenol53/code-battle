const button = document.querySelector('.ready');
const tip = document.querySelector('.tip');
const tipText = document.querySelector('.tip-text');
const undoButton = document.querySelector('.undo');

const tips = [
	'Типо подсказка 1 (что-то мемное) Lorem, ipsum dolor sit amet consectetur adipisicing elit. Tenetur error atque, non placeat sequi assumendaenim quia magni natus optio aliquam facilis facere earum fugit nesciunt in sunt est a',
	'Типо подсказка 2 (что-то мемное) Lorem, ipsum dolor sit amet consectetur adipisicing elit. Tenetur error atque, non placeat sequi assumendaenim quia magni natus optio aliquam facilis facere earum fugit nesciunt in sunt est a',
	'Типо подсказка 3 (что-то мемное) Lorem, ipsum dolor sit amet consectetur adipisicing elit. Tenetur error atque, non placeat sequi assumendaenim quia magni natus optio aliquam facilis facere earum fugit nesciunt in sunt est a',
	'Типо подсказка 4 (что-то мемное) Lorem, ipsum dolor sit amet consectetur adipisicing elit. Tenetur error atque, non placeat sequi assumendaenim quia magni natus optio aliquam facilis facere earum fugit nesciunt in sunt est a',
];

function rand(max, min = 0) {
	let rand = min + Math.random() * (max - min);
	return Math.floor(rand);
}

document.querySelector('.ready').addEventListener('click', (e) => {
	e.preventDefault();
	button.style.opacity = 0;
	setTimeout(() => {
		// button.remove();
		button.style.display = 'none';
	}, 500);
	setTimeout(() => {
		tip.style.display = 'flex';
		tipText.textContent = tips[rand(tips.length - 1)];
		setTimeout(() => {
			tip.style.opacity = 1;
		}, 500);
	}, 500);
	setInterval(() => {
		tipText.textContent = tips[rand(tips.length - 1)];
	}, 10000);
});

undoButton.addEventListener('click', () => {
	setTimeout(() => {
		tip.style.opacity = 0;
		setTimeout(() => {
			tip.style.display = 'none';
			button.style.display = 'block';
			setTimeout(() => {
				button.style.opacity = 1;
			}, 500);
		}, 500);
	});
});
