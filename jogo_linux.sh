#!/bin/bash

VERDE='\033[0;32m'
VERMELHO='\033[0;31m'
CYAN='\033[0;36m'
AMARELO='\033[1;33m'
AZUL='\033[0;34m'
SEM_COR='\033[0m'

clear
echo -e "${AZUL}====================================================${SEM_COR}"
echo -e "${AMARELO}   🛡️  A FORTALEZA DOS SERVIDORES PERDIDOS (RPG)     ${SEM_COR}"
echo -e "${AZUL}====================================================${SEM_COR}"

echo -e "\n${CYAN}📖 TUTORIAL RÁPIDO DO REINO DO LINUX:${SEM_COR}"
echo -e "  * Para criar salas (pastas): ${VERDE}mkdir <nome>${SEM_COR} ou ${VERDE}mkdir -p <caminho>${SEM_COR}"
echo -e "  * Para forjar chaves/arquivos: ${VERDE}touch <arquivo>${SEM_COR}"
echo -e "  * Para encantar arquivos com execução: ${VERDE}chmod +x <arquivo>${SEM_COR}"
echo -e "  * Para purgar arquivos: ${VERDE}rm <arquivo>${SEM_COR}\n"
read -p "Pressione Enter para iniciar a jornada..."

HP=100

# ATO 1
clear
echo -e "${AMARELO}--- ATO 1: O Abrigo Subterrâneo ---${SEM_COR}"
echo "Você acorda em um terminal escuro. Uma tempestade de pacotes corrompidos se aproxima."
echo "Você precisa criar imediatamente um bunker chamado 'bunker_defesa'."
echo ""
while true; do
    read -p "sysadmin@fortaleza:~$ " CMD
    if [[ "$CMD" == "mkdir bunker_defesa" || "$CMD" == "mkdir -p bunker_defesa" ]]; then
        echo -e "${VERDE}✔ Sucesso! O diretório seguro foi erguido a tempo!${SEM_COR}\n"
        break
    else
        HP=$((HP-25))
        echo -e "${VERMELHO}✖ Comando inválido! O vento solar atinge seu terminal. HP: $HP/100${SEM_COR}"
        if [ $HP -le 0 ]; then
            echo -e "${VERMELHO}💀 Conexão perdida. Game Over!${SEM_COR}"
            exit 1
        fi
    fi
done

# ATO 2
echo -e "${AMARELO}--- ATO 2: O Cristal de Acesso ---${SEM_COR}"
echo "Dentro do bunker, você encontra um altar vazio onde falta o arquivo de chave 'chave.pem'."
echo "Crie o arquivo vazio para energizar o terminal."
echo ""
while true; do
    read -p "sysadmin@fortaleza:~$ " CMD
    if [[ "$CMD" == "touch chave.pem" || "$CMD" == "touch bunker_defesa/chave.pem" ]]; then
        echo -e "${VERDE}✔ O cristal brilha! O arquivo 'chave.pem' foi gerado.${SEM_COR}\n"
        break
    else
        HP=$((HP-25))
        echo -e "${VERMELHO}✖ Erro de sintaxe! Raios elétricos escapam do painel. HP: $HP/100${SEM_COR}"
        if [ $HP -le 0 ]; then
            echo -e "${VERMELHO}💀 Energia esgotada. Game Over!${SEM_COR}"
            exit 1
        fi
    fi
done

# ATO 3
echo -e "${AMARELO}--- ATO 3: A Barreira de Execução ---${SEM_COR}"
echo "O script de defesa da torre 'defesa.sh' está bloqueado pelo sistema."
echo "Conceda permissão de execução a ele antes que os invasores quebrem o portão."
echo ""
while true; do
    read -p "sysadmin@fortaleza:~$ " CMD
    if [[ "$CMD" == "chmod +x defesa.sh" || "$CMD" == "chmod 755 defesa.sh" || "$CMD" == "chmod 777 defesa.sh" ]]; then
        echo -e "${VERDE}✔ Defesas ativadas! Os escudos da Fortaleza foram restaurados.${SEM_COR}\n"
        break
    else
        HP=$((HP-25))
        echo -e "${VERMELHO}✖ Acesso negado! O portão sofreu dano. HP: $HP/100${SEM_COR}"
        if [ $HP -le 0 ]; then
            echo -e "${VERMELHO}💀 A fortaleza caiu. Game Over!${SEM_COR}"
            exit 1
        fi
    fi
done

echo -e "${AZUL}====================================================${SEM_COR}"
echo -e "${VERDE}🏆 PARABÉNS! Você dominou os comandos e salvou a Fortaleza!${SEM_COR}"
echo -e "HP Final: ${AMARELO}$HP/100${SEM_COR}"
echo -e "${AZUL}====================================================${SEM_COR}"
read -p "Pressione Enter para voltar ao menu principal."
