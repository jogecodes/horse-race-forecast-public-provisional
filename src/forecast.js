(() => {
  const playground = document.getElementById('forecast-playground');
  if (!playground) return;
  const names = ['Prior Belief', 'Bayes Factor', 'Posterior Favourite'];
  const sliders = names.map((_, i) => document.getElementById(`forecast-${i}`));
  let probabilities = [50, 30, 20];
  let winner = 2;
  const setText = (id, text) => { document.getElementById(id).textContent = text; };
  function render() {
    const terms = probabilities.map((p, i) => (p / 100 - Number(i === winner)) ** 2);
    const score = terms.reduce((sum, term) => sum + term, 0);
    probabilities.forEach((p, i) => {
      sliders[i].value = p;
      // Explain the linked controls to screen-reader users on each adjustment.
      sliders[i].setAttribute('aria-valuetext', `${p} percent; other horses ${probabilities.filter((_, j) => j !== i).join(' and ')} percent; total 100 percent`);
      setText(`probability-${i}`, `${p}%`);
      setText(`brier-label-${i}`, `${names[i]} · ${i === winner ? 'won' : 'did not win'}`);
      setText(`brier-formula-${i}`, `(${(p / 100).toFixed(2)} − ${Number(i === winner)})²`);
      setText(`brier-term-${i}`, terms[i].toFixed(4));
    });
    setText('forecast-total', `${probabilities.reduce((a, b) => a + b, 0)}%`);
    setText('forecast-score', score.toFixed(4));
    setText('posterior-joke', winner === 2
      ? `Posterior Favourite wins at ${probabilities[2]}%. Particularly appropriate.`
      : `Posterior Favourite loses at ${probabilities[2]}%. A posterior revision is in order.`);
    setText('brier-winner', `The same invented race / ${names[winner]} wins`);
    setText('brier-outcome', `(${names.map((_, i) => Number(i === winner)).join(', ')})`);
    setText('brier-calculation', `${terms.map(t => t.toFixed(4)).join(' + ')} = ${score.toFixed(4)}`);
  }
  sliders.forEach((slider, index) => slider.addEventListener('input', () => {
    const value = Number(slider.value);
    const others = [0, 1, 2].filter(i => i !== index);
    const remaining = 100 - value;
    const previousTotal = probabilities[others[0]] + probabilities[others[1]];
    const first = Math.round(remaining * (previousTotal ? probabilities[others[0]] / previousTotal : 0.5));
    probabilities[index] = value;
    probabilities[others[0]] = first;
    probabilities[others[1]] = remaining - first;
    render();
  }));
  playground.querySelectorAll('[name="race-winner"]').forEach(radio => radio.addEventListener('change', () => {
    winner = Number(radio.value);
    render();
  }));
  document.getElementById('forecast-reset').addEventListener('click', () => {
    probabilities = [50, 30, 20];
    winner = 2;
    playground.querySelector('[name="race-winner"][value="2"]').checked = true;
    render();
  });
  playground.disabled = false;
  render();
})();
