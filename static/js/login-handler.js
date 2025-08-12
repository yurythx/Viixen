/**
 * Login Handler - Gerencia o processo de login no frontend
 */

document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    
    if (loginForm) {
        const loginButton = document.getElementById('loginButton');
        const loginButtonText = document.getElementById('loginButtonText');
        const loginSpinner = document.getElementById('loginSpinner');
        
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault(); // Impedir o envio padrão do formulário
            
            // Mostrar feedback visual
            loginButton.disabled = true;
            loginButtonText.textContent = 'Entrando...';
            loginSpinner.classList.remove('d-none');
            
            // Mostrar notificação
            showInfoNotification('Processando login...', 'Autenticação');
            
            // Obter os dados do formulário
            const formData = new FormData(loginForm);
            
            // Enviar requisição AJAX para o endpoint de login AJAX
            fetch('/accounts/ajax-login/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                credentials: 'same-origin'
            })
            .then(response => {
                if (response.redirected) {
                    // Se o servidor redirecionou, significa que o login foi bem-sucedido
                    showSuccessNotification('Login realizado com sucesso!', 'Autenticação');
                    window.location.href = response.url; // Redirecionar para a URL fornecida pelo servidor
                    return;
                }
                
                // Se não houve redirecionamento, verificar o status da resposta
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Falha na autenticação');
                }
            })
            .then(data => {
                if (data && data.error) {
                    // Exibir mensagem de erro do servidor
                    showErrorNotification(data.error, 'Erro de Autenticação');
                    resetLoginForm();
                } else if (data && data.success) {
                    // Login bem-sucedido com resposta JSON
                    showSuccessNotification('Login realizado com sucesso!', 'Autenticação');
                    window.location.href = data.redirect_url || '/';
                }
            })
            .catch(error => {
                console.error('Erro no login:', error);
                showErrorNotification('Ocorreu um erro ao tentar fazer login. Por favor, tente novamente.', 'Erro de Autenticação');
                resetLoginForm();
            });
        });
        
        function resetLoginForm() {
            // Restaurar o estado do botão
            loginButton.disabled = false;
            loginButtonText.textContent = 'Entrar';
            loginSpinner.classList.add('d-none');
        }
    }
});

// Funções auxiliares para notificações
function showInfoNotification(message, title = 'Informação') {
    if (typeof UbuntuNotification !== 'undefined') {
        new UbuntuNotification({
            title: title,
            message: message,
            type: 'info'
        });
    } else {
        console.log(`${title}: ${message}`);
    }
}

function showSuccessNotification(message, title = 'Sucesso') {
    if (typeof UbuntuNotification !== 'undefined') {
        new UbuntuNotification({
            title: title,
            message: message,
            type: 'success'
        });
    } else {
        console.log(`${title}: ${message}`);
    }
}

function showErrorNotification(message, title = 'Erro') {
    if (typeof UbuntuNotification !== 'undefined') {
        new UbuntuNotification({
            title: title,
            message: message,
            type: 'error'
        });
    } else {
        console.log(`${title}: ${message}`);
    }
}