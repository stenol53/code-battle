const button = document.querySelector('.ready');
const tip = document.querySelector('.tip');
const tipText = document.querySelector('.tip-text');
const undoButton = document.querySelector('.undo');

const tips = [
	'Подсказка 1: Lorem, ipsum dolor sit amet consectetur adipisicing elit. Tenetur error atque, non placeat sequi assumendaenim quia magni natus optio aliquam facilis facere earum fugit nesciunt in sunt est a',
	'Подсказка 2: Tenetur error atque, non placeat sequi assumendaenim quia magni natus optio aliquam facilis facere earum fugit nesciunt in sunt est a',
	'Подсказка 3: Proin in elit quis ligula gravida vestibulum. Proin condimentum neque nec enim placerat pellentesque.',
	'Подсказка 4: Quisque vehicula dapibus est, eget rhoncus purus. Phasellus egestas dolor vel lectus gravida maximus. Proin id ligula semper mi vehicula blandit.',
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
