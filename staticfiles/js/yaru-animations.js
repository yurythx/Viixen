// Animações e Interações Yaru Theme
document.addEventListener('DOMContentLoaded', function() {
    
    // ===== LOADING OVERLAY =====
    function showLoading() {
        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay show';
        overlay.innerHTML = `
            <div class="text-center text-white">
                <div class="ubuntu-loader"></div>
                <p class="mt-3">Carregando...</p>
            </div>
        `;
        document.body.appendChild(overlay);
        return overlay;
    }
    
    function hideLoading(overlay) {
        if (overlay) {
            overlay.classList.remove('show');
            setTimeout(() => overlay.remove(), 300);
        }
    }
    
    // ===== VALIDAÇÃO DE FORMULÁRIOS COM ANIMAÇÃO =====
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const invalidFields = form.querySelectorAll('.is-invalid');
            
            // Remove animação anterior
            invalidFields.forEach(field => {
                field.classList.remove('shake-animation');
            });
            
            // Adiciona animação de shake para campos inválidos
            setTimeout(() => {
                invalidFields.forEach(field => {
                    field.classList.add('shake-animation');
                });
            }, 10);
        });
        
        // Validação em tempo real
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid')) {
                    validateField(this);
                }
            });
        });
    });
    
    function validateField(field) {
        // Remove classes de validação anteriores
        field.classList.remove('is-valid', 'is-invalid');
        
        // Validação básica
        if (field.hasAttribute('required') && !field.value.trim()) {
            field.classList.add('is-invalid');
            showFieldError(field, 'Este campo é obrigatório');
        } else if (field.type === 'email' && field.value && !isValidEmail(field.value)) {
            field.classList.add('is-invalid');
            showFieldError(field, 'Email inválido');
        } else {
            field.classList.add('is-valid');
            hideFieldError(field);
        }
    }
    
    function showFieldError(field, message) {
        let errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'invalid-feedback';
            field.parentNode.appendChild(errorDiv);
        }
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    }
    
    function hideFieldError(field) {
        const errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.style.display = 'none';
        }
    }
    
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    // ===== ANIMAÇÕES DE CARDS =====
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // ===== MODAIS COM ANIMAÇÃO =====
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('show.bs.modal', function() {
            this.querySelector('.modal-dialog').style.transform = 'scale(0.8)';
            setTimeout(() => {
                this.querySelector('.modal-dialog').style.transform = 'scale(1)';
            }, 10);
        });
        
        modal.addEventListener('hide.bs.modal', function() {
            this.querySelector('.modal-dialog').style.transform = 'scale(0.8)';
        });
    });
    
    // ===== TOASTS AUTOMÁTICOS =====
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        const bsToast = new bootstrap.Toast(toast, {
            autohide: true,
            delay: 5000
        });
        bsToast.show();
    });
    
    // ===== LOADING EM LINKS E FORMULÁRIOS =====
    const actionButtons = document.querySelectorAll('.btn-action, [type="submit"]');
    actionButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (this.type === 'submit') {
                const form = this.closest('form');
                if (form && form.checkValidity()) {
                    showButtonLoading(this);
                }
            } else if (this.href) {
                showButtonLoading(this);
            }
        });
    });
    
    function showButtonLoading(button) {
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Carregando...';
        button.disabled = true;
        
        // Restaurar depois de 3 segundos (fallback)
        setTimeout(() => {
            button.innerHTML = originalText;
            button.disabled = false;
        }, 3000);
    }
    
    // ===== NAVEGAÇÃO POR TECLADO =====
    document.addEventListener('keydown', function(e) {
        // ESC fecha modais
        if (e.key === 'Escape') {
            const openModals = document.querySelectorAll('.modal.show');
            openModals.forEach(modal => {
                const bsModal = bootstrap.Modal.getInstance(modal);
                if (bsModal) bsModal.hide();
            });
        }
        
        // CTRL + / abre busca (se existir)
        if (e.ctrlKey && e.key === '/') {
            e.preventDefault();
            const searchInput = document.querySelector('[type="search"], .search-input');
            if (searchInput) {
                searchInput.focus();
            }
        }
    });
    
    // ===== SMOOTH SCROLL =====
    const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');
    smoothScrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // ===== LAZY LOADING PARA IMAGENS =====
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
    
    // ===== TOOLTIPS AUTOMÁTICOS =====
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // ===== CONFIRMAÇÃO DE AÇÕES DESTRUTIVAS =====
    const deleteButtons = document.querySelectorAll('.btn-danger, [data-confirm]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.dataset.confirm || 'Tem certeza que deseja realizar esta ação?';
            if (!confirm(message)) {
                e.preventDefault();
                return false;
            }
        });
    });

    // ===== TROCA DE TEMA (DARK/LIGHT) =====
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = themeToggle ? themeToggle.querySelector('i') : null;
    
    // Função para aplicar tema
    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        
        if (themeIcon) {
            if (theme === 'dark') {
                themeIcon.className = 'fas fa-sun';
                themeToggle.title = 'Alternar para tema claro';
            } else {
                themeIcon.className = 'fas fa-moon';
                themeToggle.title = 'Alternar para tema escuro';
            }
        }
    }
    
    // Detectar tema inicial
    function initTheme() {
        const savedTheme = localStorage.getItem('theme');
        const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        const initialTheme = savedTheme || systemTheme;
        applyTheme(initialTheme);
    }
    
    // Inicializar tema
    initTheme();
    
    // Event listener para o botão de troca de tema
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            // Animação de transição suave
            document.documentElement.style.transition = 'background-color 0.3s ease, color 0.3s ease';
            applyTheme(newTheme);
            
            // Remove a transição após a animação
            setTimeout(() => {
                document.documentElement.style.transition = '';
            }, 300);
        });
    }
    
    // Detectar mudanças no tema do sistema
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
        if (!localStorage.getItem('theme')) {
            applyTheme(e.matches ? 'dark' : 'light');
        }
    });
});
