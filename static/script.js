// script.js - CÓDIGO FINAL DE FUNCIONAMENTO DO MODAL

// A função document.addEventListener('DOMContentLoaded', ...) garante que o script só rode depois que todo o HTML for carregado.
document.addEventListener('DOMContentLoaded', () => {
    
    // 1. SELECIONA OS ELEMENTOS IMPORTANTES
    const verMaisButtons = document.querySelectorAll('.btn-vermais');
    const closeButtons = document.querySelectorAll('.close-button');


    // ===================================================
    // FUNÇÕES DE ABRIR E FECHAR
    // ===================================================

    function openModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            // Adiciona a classe 'active' (display: flex) para mostrar o modal
            modal.classList.add('active'); 
            // Adiciona a classe para impedir a rolagem do body
            document.body.classList.add('modal-open');
        }
    }

    function closeModal(modalElement) {
        if (modalElement) {
            // Remove a classe 'active' (display: none) para esconder o modal
            modalElement.classList.remove('active'); 
            // Remove a classe para restaurar a rolagem do body
            document.body.classList.remove('modal-open');
        }
    }


    // 2. LIGA O BOTÃO "VER MAIS" (ABRIR)
    verMaisButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault(); 
            
            // Pega o ID do modal do atributo data-modal-target
            const modalId = button.getAttribute('data-modal-target'); 
            
            openModal(modalId);
        });
    });


    // 3. LIGA OS BOTÕES DE FECHAR ('x')
    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Encontra o ancestral mais próximo que tem a classe '.modal'
            const modal = button.closest('.modal');
            closeModal(modal);
        });
    });

    // 4. FECHAR O MODAL CLICANDO FORA (NO OVERLAY ESCURO)
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (event) => {
            // Verifica se o clique foi exatamente no fundo (elemento com a classe 'modal')
            if (event.target.classList.contains('modal')) {
                closeModal(modal);
            }
        });
    });

    // 5. FECHAR AO PRESSIONAR A TECLA ESC
    document.addEventListener('keydown', (event) => {
        const activeModal = document.querySelector('.modal.active');
        if (event.key === 'Escape' && activeModal) {
            closeModal(activeModal);
        }
    });

}); // <-- AQUI FECHA O document.addEventListener('DOMContentLoaded')


const timeline = document.querySelector(".timeline");
const btnLeft = document.querySelector(".timeline-nav.left");
const btnRight = document.querySelector(".timeline-nav.right");

const scrollAmount = 350; // distância por clique (ajuste se quiser)

btnRight.addEventListener("click", () => {
    timeline.scrollBy({
        left: scrollAmount,
        behavior: "smooth"
    });
});

btnLeft.addEventListener("click", () => {
    timeline.scrollBy({
        left: -scrollAmount,
        behavior: "smooth"
    });
});