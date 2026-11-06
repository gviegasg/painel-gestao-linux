#!/bin/bash

# --- CONFIGURAÇÕES DE CORES ---
AZUL='\033[0;34m'
VERDE='\033[0;32m'
AMARELO='\033[1;33m'
VERMELHO='\033[0;31m'
CYAN='\033[0;36m'
SEM_COR='\033[0m'

# --- MÓDULOS / FUNÇÕES ---

iniciar_ambiente() {
    DATA=$(date +%Y-%m-%d)
    PASTA=~/Documentos/Estudos/$DATA
    mkdir -p "$PASTA"
    echo "🚀 Abrindo ambiente em: $PASTA"
    code "$PASTA" & brave-browser &
    sleep 2
}

manutencao_sistema() {
    echo "🧹 Executando manutenção..."
    sudo apt update && sudo apt upgrade -y && sudo apt autoremove -y
    read -p "Concluído. Pressione Enter para voltar."
}

saude_hardware() {
    echo "🛡️ Relatório de Hardware:"
    TEMP=$(cat /sys/class/thermal/thermal_zone0/temp)
    echo "🌡️ Temperatura CPU: $((TEMP/1000))°C"
    upower -i $(upower -e | grep 'BAT') | grep -E "percentage|capacity"
    free -h
    read -p "Pressione Enter para voltar."
}

perfil_energia() {
    echo "🔋 1.Performance | 2.Equilibrado | 3.Economia"
    read -p "Escolha: " MOD
    if [ "$MOD" == "1" ]; then powerprofilesctl set performance
    elif [ "$MOD" == "2" ]; then powerprofilesctl set balanced
    elif [ "$MOD" == "3" ]; then powerprofilesctl set power-saver
    fi
}

status_rede() {
    echo "🌐 Status de Rede:"
    ping -c 3 google.com
    echo "IP Local: $(hostname -I)"
    read -p "Pressione Enter para voltar."
}

monitor_processos() {
    echo "📊 Abrindo htop (Pressione 'q' para sair)..."
    sleep 1
    htop
    read -p "Pressione Enter para voltar."
}

executar_modulo_ads() {
    echo "🐍 Executando Módulo ADS (Python + SQL)..."
    python3 ~/.scripts/projeto_ads/main.py
    read -p "Pressione Enter para voltar."
}

guia_atalhos() {
    clear
    echo -e "${AMARELO}=== GUIA DE ATALHOS RÁPIDOS ===${SEM_COR}"
    echo -e "${VERDE}ls${SEM_COR}      : Lista arquivos da pasta atual."
    echo -e "${VERDE}cd [dir]${SEM_COR}: Entra em uma pasta."
    echo -e "${VERDE}pwd${SEM_COR}     : Mostra o caminho da pasta atual."
    echo -e "${VERDE}mkdir${SEM_COR}   : Cria uma pasta nova."
    echo -e "${VERDE}rm [arq]${SEM_COR}: Deleta um arquivo."
    echo -e "----------------------------------"
    read -p "Pressione Enter para voltar ao menu."
}

chat_ollama() {
    echo "🧠 Iniciando LLM Local via Ollama..."
    echo "💡 Dica: Digite /bye para encerrar o chat e voltar ao menu."
    echo "---------------------------------------------------------"
    ollama run llama3.2:1b
    read -p "Pressione Enter para voltar ao menu."
}

jogar_terminal_linux() {
    bash ~/.scripts/jogo_linux.sh
}

jogar_arena_dev() {
    python3 ~/.scripts/projeto_ads/jogo_dev.py
}

editar_proprio_script() {
    echo "📝 Abrindo o script no editor Nano..."
    sleep 1
    nano ~/.scripts/gestao.sh
}

iniciar_seek_and_fix() {
    python3 ~/.scripts/projeto_ads/seek_and_fix.py
    read -p "Pressione Enter para voltar ao menu."
}

modulo_github_cli() {
    clear
    echo -e "${CYAN}=== 🐙 CENTRAL GITHUB CLI (gh) ===${SEM_COR}"
    echo -e "${VERDE}1)${SEM_COR} Status da Conta (gh auth status)"
    echo -e "${VERDE}2)${SEM_COR} Listar Meus Repositórios (gh repo list)"
    echo -e "${VERDE}3)${SEM_COR} Criar Novo Repositório Remoto"
    echo -e "${VERDE}4)${SEM_COR} Visualizar Issues / Tarefas Abertas"
    echo -e "${VERMELHO}0)${SEM_COR} Voltar ao Menu Principal"
    echo -e "-----------------------------------"
    read -p "Selecione uma opção do GitHub: " GH_OP

    case $GH_OP in
        1)
            gh auth status
            ;;
        2)
            gh repo list --limit 10
            ;;
        3)
            read -p "Nome do novo repositório: " NOME_REPO
            read -p "Público ou Privado? (public/private): " TIPO_REPO
            gh repo create "$NOME_REPO" --"$TIPO_REPO" --confirm
            ;;
        4)
            gh issue list
            ;;
        0)
            return
            ;;
        *)
            echo "Opção inválida."
            ;;
    esac
    echo ""
    read -p "Pressione Enter para voltar ao painel."
}

# --- LOOP PRINCIPAL DO MENU ---

while true; do
    clear
    echo -e "${AZUL}=========================================="
    echo -e "       PAINEL DE GESTÃO - ZORIN OS        "
    echo -e "          Analista: gviegasg              "
    echo -e "==========================================${SEM_COR}"
    echo -e "${VERDE}1)${SEM_COR} Iniciar Ambiente (Brave + VS Code)"
    echo -e "${VERDE}2)${SEM_COR} Manutenção (Update + Limpeza)"
    echo -e "${VERDE}3)${SEM_COR} Saúde do Sistema (CPU, Bateria, RAM)"
    echo -e "${VERDE}4)${SEM_COR} Perfil de Energia (Performance/Eco)"
    echo -e "${VERDE}5)${SEM_COR} Status de Rede e IP"
    echo -e "${VERDE}6)${SEM_COR} Monitor de Processos (htop)"
    echo -e "${CYAN}7)${SEM_COR} Módulo ADS (Python + SQL)"
    echo -e "${AMARELO}8)${SEM_COR} Guia de Atalhos Rápidos"
    echo -e "${CYAN}9)${SEM_COR} Chat com LLM Local (Ollama Llama 3.2)"
    echo -e "${AMARELO}10)${SEM_COR} RPG: A Fortaleza dos Servidores (Linux)"
    echo -e "${AMARELO}11)${SEM_COR} RPG: O Oráculo dos Dados (Python/SQL)"
    echo -e "${CYAN}12)${SEM_COR} Editar este Menu (Nano)"
    echo -e "${VERDE}13)${SEM_COR} GitHub CLI (Repositórios e Status)"
    echo -e "${AMARELO}14)${SEM_COR} Seek and Fix (Auto-Diagnóstico e Reparo IA)"
    echo -e "${VERMELHO}0)${SEM_COR} Sair"
    echo -e "${AZUL}==========================================${SEM_COR}"
    read -p "Selecione uma opção: " OPCAO

    case $OPCAO in
        1) iniciar_ambiente ;;
        2) manutencao_sistema ;;
        3) saude_hardware ;;
        4) perfil_energia ;;
        5) status_rede ;;
        6) monitor_processos ;;
        7) executar_modulo_ads ;;
        8) guia_atalhos ;;
        9) chat_ollama ;;
        10) jogar_terminal_linux ;;
        11) jogar_arena_dev ;;
        12) editar_proprio_script ;;
        13) modulo_github_cli ;;
	14) iniciar_seek_and_fix ;;
        0) echo "Encerrando painel..."; exit 0 ;;
        *) echo "Opção inválida."; sleep 1 ;;
    esac
done
