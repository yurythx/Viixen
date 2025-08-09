# Script para ativar ambiente virtual e executar Django
Write-Host "Ativando ambiente virtual..." -ForegroundColor Green

# Ativar ambiente virtual
& ".\venv\Scripts\Activate.ps1"

Write-Host "Executando servidor Django..." -ForegroundColor Green

# Executar servidor Django
python manage.py runserver

Write-Host "Servidor encerrado." -ForegroundColor Yellow
Read-Host "Pressione Enter para continuar..."
