@echo off
:: Script para inicializar, adicionar, fazer commit e push para o repositório GitHub

:: Diretório do repositório
cd /d %~dp0

:: Verificar se é um repositório Git
git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
    echo "Repositório Git não encontrado. Inicializando..."
    git init
    git remote add origin https://github.com/GabrielSantosTerra/tcs_indicadores.git
)

:: Adicionando arquivos
echo Adicionando arquivos ao stage...
git add .

:: Mensagem de commit
set /p commit_message="Digite a mensagem de commit: "

:: Realizando o commit
git commit -m "%commit_message%"

:: Fazendo push para o repositório
echo Fazendo push para o repositório...
git push -u origin main

echo Operação concluída!
pause
