document.addEventListener('DOMContentLoaded', () => {
    // Encontra TODOS os botões que abrem um modal
    const abrirModalBtns = document.querySelectorAll('[data-modal-target]');
    
    // Encontra TODOS os botões que fecham um modal
    const fecharModalBtns = document.querySelectorAll('[data-modal-close]');
    
    // Encontra TODOS os overlays de modal
    const overlays = document.querySelectorAll('.modal-overlay');

    abrirModalBtns.forEach(button => {
        button.addEventListener('click', () => {
            const modal = document.querySelector(button.dataset.modalTarget);
            abrirModal(modal);
        });
    });

    fecharModalBtns.forEach(button => {
        button.addEventListener('click', () => {
            const modal = button.closest('.modal-overlay');
            fecharModal(modal);
        });
    });

    overlays.forEach(overlay => {
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                fecharModal(overlay);
            }
        });
    });

    function abrirModal(modal) {
        if (modal == null) return;
        modal.classList.add('visivel');
    }

    function fecharModal(modal) {
        if (modal == null) return;
        modal.classList.remove('visivel');
    }
});