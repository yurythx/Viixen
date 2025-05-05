import axios from 'axios';

// Crie uma instância do Axios para personalizar as configurações
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',  // API base URL
});

// Adicionando interceptador para adicionar o token JWT nas requisições
api.interceptors.request.use(
  (config) => {
    // Só tentar acessar o localStorage no lado do cliente
    if (typeof window !== "undefined") {
      const token = localStorage.getItem('access_token');
      if (token) {
        // Se o token existir, adiciona no cabeçalho Authorization
        config.headers['Authorization'] = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export { api };