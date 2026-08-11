document.addEventListener('DOMContentLoaded', () => {
    const reportButtons = document.querySelectorAll('[href="#"]');

    reportButtons.forEach((link) => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
        });
    });

    const cards = document.querySelectorAll('.equipment-card');
    cards.forEach((card) => {
        card.addEventListener('click', () => {
            const details = card.querySelector('p:nth-of-type(3)')?.textContent || '';
            console.log('Ver más equipo:', details);
        });
    });
});
