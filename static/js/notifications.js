/**
 * Sistema de Notificações estilo Ubuntu
 */

class UbuntuNotification {
  constructor(options = {}) {
    this.options = {
      title: options.title || 'Notificação',
      message: options.message || '',
      type: options.type || 'info', // info, success, warning, error
      icon: options.icon || this.getDefaultIcon(options.type || 'info'),
      duration: options.duration || 5000,
      actions: options.actions || [],
      onClose: options.onClose || null,
      onClick: options.onClick || null
    };
    
    this.element = null;
    this.progressTimer = null;
    this.closeTimer = null;
    this.init();
  }
  
  getDefaultIcon(type) {
    switch (type) {
      case 'success': return 'fa-check-circle';
      case 'error': return 'fa-exclamation-circle';
      case 'warning': return 'fa-exclamation-triangle';
      default: return 'fa-info-circle';
    }
  }
  
  init() {
    // Criar o container se não existir
    let container = document.querySelector('.ubuntu-notification-container');
    if (!container) {
      container = document.createElement('div');
      container.className = 'ubuntu-notification-container';
      document.body.appendChild(container);
    }
    
    // Criar a notificação
    this.element = document.createElement('div');
    this.element.className = `ubuntu-notification ${this.options.type}`;
    
    // Estrutura da notificação
    this.element.innerHTML = `
      <div class="ubuntu-notification-header">
        <div class="ubuntu-notification-app-icon">
          <i class="fas ${this.options.icon}"></i>
        </div>
        <div class="ubuntu-notification-title">${this.options.title}</div>
        <button class="ubuntu-notification-close">
          <i class="fas fa-times"></i>
        </button>
      </div>
      <div class="ubuntu-notification-progress">
        <div class="ubuntu-notification-progress-bar"></div>
      </div>
      <div class="ubuntu-notification-body">${this.options.message}</div>
      ${this.renderActions()}
    `;
    
    // Adicionar ao container
    container.appendChild(this.element);
    
    // Adicionar eventos
    this.addEventListeners();
    
    // Mostrar com animação
    setTimeout(() => {
      this.element.classList.add('show');
    }, 10);
    
    // Configurar timer para fechar
    if (this.options.duration > 0) {
      this.closeTimer = setTimeout(() => {
        this.close();
      }, this.options.duration);
    }
    
    return this;
  }
  
  renderActions() {
    if (!this.options.actions || this.options.actions.length === 0) {
      return '';
    }
    
    let actionsHtml = '<div class="ubuntu-notification-actions">';
    
    this.options.actions.forEach(action => {
      const className = action.primary ? 'ubuntu-notification-action primary' : 'ubuntu-notification-action';
      actionsHtml += `<button class="${className}" data-action-id="${action.id}">${action.text}</button>`;
    });
    
    actionsHtml += '</div>';
    return actionsHtml;
  }
  
  addEventListeners() {
    // Botão fechar
    const closeBtn = this.element.querySelector('.ubuntu-notification-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => this.close());
    }
    
    // Clique na notificação
    if (this.options.onClick) {
      this.element.addEventListener('click', (e) => {
        // Não disparar se clicou em botões de ação ou fechar
        if (!e.target.closest('.ubuntu-notification-action') && 
            !e.target.closest('.ubuntu-notification-close')) {
          this.options.onClick();
        }
      });
    }
    
    // Botões de ação
    const actionButtons = this.element.querySelectorAll('.ubuntu-notification-action');
    actionButtons.forEach(button => {
      button.addEventListener('click', () => {
        const actionId = button.getAttribute('data-action-id');
        const action = this.options.actions.find(a => a.id === actionId);
        if (action && action.onClick) {
          action.onClick();
        }
        if (action && action.closeOnClick !== false) {
          this.close();
        }
      });
    });
    
    // Pausar o timer ao passar o mouse
    this.element.addEventListener('mouseenter', () => {
      if (this.closeTimer) {
        clearTimeout(this.closeTimer);
        this.closeTimer = null;
        
        // Pausar a animação da barra de progresso
        const progressBar = this.element.querySelector('.ubuntu-notification-progress-bar');
        if (progressBar) {
          const computedStyle = window.getComputedStyle(progressBar);
          const width = computedStyle.getPropertyValue('transform');
          progressBar.style.animation = 'none';
          progressBar.style.transform = width;
        }
      }
    });
    
    // Retomar o timer ao tirar o mouse
    this.element.addEventListener('mouseleave', () => {
      if (!this.closeTimer && this.options.duration > 0) {
        this.closeTimer = setTimeout(() => {
          this.close();
        }, 2000); // Tempo reduzido após o hover
        
        // Retomar a animação da barra de progresso
        const progressBar = this.element.querySelector('.ubuntu-notification-progress-bar');
        if (progressBar) {
          progressBar.style.animation = 'progress-shrink 2s linear forwards';
          progressBar.style.transform = 'scaleX(1)';
        }
      }
    });
  }
  
  close() {
    if (!this.element) return;
    
    // Limpar timers
    if (this.closeTimer) {
      clearTimeout(this.closeTimer);
      this.closeTimer = null;
    }
    
    // Animar saída
    this.element.classList.remove('show');
    this.element.style.opacity = '0';
    this.element.style.transform = 'translateX(50px)';
    
    // Remover após animação
    setTimeout(() => {
      if (this.element && this.element.parentNode) {
        this.element.parentNode.removeChild(this.element);
        this.element = null;
        
        // Callback de fechamento
        if (typeof this.options.onClose === 'function') {
          this.options.onClose();
        }
      }
    }, 300);
  }
}

// Função global para criar notificações
window.showUbuntuNotification = function(options) {
  return new UbuntuNotification(options);
};

// Funções de conveniência
window.showSuccessNotification = function(message, title = 'Sucesso') {
  return new UbuntuNotification({
    title: title,
    message: message,
    type: 'success'
  });
};

window.showErrorNotification = function(message, title = 'Erro') {
  return new UbuntuNotification({
    title: title,
    message: message,
    type: 'error',
    duration: 8000 // Erros ficam visíveis por mais tempo
  });
};

window.showWarningNotification = function(message, title = 'Atenção') {
  return new UbuntuNotification({
    title: title,
    message: message,
    type: 'warning',
    duration: 6000
  });
};

window.showInfoNotification = function(message, title = 'Informação') {
  return new UbuntuNotification({
    title: title,
    message: message,
    type: 'info'
  });
};

// Integração com mensagens Django
document.addEventListener('DOMContentLoaded', function() {
  // Converter mensagens Django em notificações Ubuntu
  const djangoMessages = document.querySelectorAll('.toast');
  
  if (djangoMessages && djangoMessages.length > 0) {
    djangoMessages.forEach(message => {
      // Obter tipo da mensagem
      let type = 'info';
      if (message.classList.contains('bg-success')) type = 'success';
      if (message.classList.contains('bg-danger')) type = 'error';
      if (message.classList.contains('bg-warning')) type = 'warning';
      
      // Obter texto da mensagem
      const toastBody = message.querySelector('.toast-body');
      const messageText = toastBody ? toastBody.innerText.trim() : 'Notificação do sistema';
      
      // Criar notificação Ubuntu
      new UbuntuNotification({
        message: messageText,
        type: type
      });
      
      // Remover toast original
      message.remove();
    });
  }
});