/**
 * Mobile Menu Fullscreen - Viixen
 * Este script implementa um menu mobile que sai da lateral e ocupa a tela inteira
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elementos do menu
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (!navbarToggler || !navbarCollapse) return;
    
    // Criar botão de fechar para o menu mobile
    const closeButton = document.createElement('button');
    closeButton.classList.add('navbar-toggler-close');
    closeButton.innerHTML = '<i class="fas fa-times"></i>';
    closeButton.setAttribute('aria-label', 'Fechar menu');
    closeButton.style.display = 'none';
    
    // Adicionar botão de fechar ao menu
    navbarCollapse.prepend(closeButton);
    
    // Função para abrir o menu
    function openMobileMenu() {
        document.body.style.overflow = 'hidden'; // Impedir rolagem do body
        closeButton.style.display = 'block';
    }
    
    // Função para fechar o menu
    function closeMobileMenu() {
        document.body.style.overflow = ''; // Restaurar rolagem do body
        closeButton.style.display = 'none';
    }
    
    // Event listener para o botão de hambúrguer
    navbarToggler.addEventListener('click', function() {
        if (navbarCollapse.classList.contains('show')) {
            closeMobileMenu();
        } else {
            openMobileMenu();
        }
    });
    
    // Event listener para o botão de fechar
    closeButton.addEventListener('click', function() {
        navbarToggler.click(); // Simular clique no botão de hambúrguer para fechar o menu
    });
    
    // Fechar o menu ao clicar em um link
    const navLinks = navbarCollapse.querySelectorAll('.nav-link');
    navLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            if (window.innerWidth < 992 && navbarCollapse.classList.contains('show')) {
                navbarToggler.click();
            }
        });
    });
    
    // Fechar o menu ao redimensionar a janela para desktop
    window.addEventListener('resize', function() {
        if (window.innerWidth >= 992 && navbarCollapse.classList.contains('show')) {
            navbarToggler.click();
        }
    });
});