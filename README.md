# 🛠️ Painel de Gestão Linux & Seek and Fix (AI Auto-Repair)

![Linux](https://img.shields.io/badge/OS-Zorin_OS_%7C_Ubuntu-03A9F4?style=for-the-badge&logo=linux&logoColor=white)
![Bash](https://img.shields.io/badge/Shell-Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Ollama](https://img.shields.io/badge/AI-Ollama_Local-black?style=for-the-badge)

## 🎯 Objetivo do Projeto

Este projeto nasceu com dois grandes propósitos:
1. **Produtividade e Automação Real:** Centralizar em um único painel de terminal (CLI) a administração diária de um notebook Linux (Zorin OS / Ubuntu), permitindo diagnosticar e corrigir falhas de rede, bateria, memória RAM, áudio e pacotes **100% offline** e em poucos segundos.
2. **Laboratório Prático de Engenharia de Software (ADS):** Integrar na prática diferentes tecnologias fundamentais — *Shell Scripting (Bash)*, *Programação Orientada a Objetos (Python)*, *Banco de Dados Relacional (SQLite)* e *Agentes Locais de Inteligência Artificial (Ollama)* com travas de governança e segurança.

---

## ⚙️ Arquitetura e Módulos do Ecossistema

O sistema é dividido em módulos independentes orquestrados pelo script principal `gestao.sh`:

### 1. 🖥️ Painel de Gestão (`gestao.sh`)
Menu interativo em Bash que gerencia o fluxo de trabalho diário:
- Criação automática de pastas de estudo datadas e abertura do VS Code + Navegador.
- Manutenção automatizada do sistema (`apt update`, `upgrade` e limpeza).
- Monitoramento térmico da CPU, saúde física da bateria e consumo de memória RAM.
- Alternância rápida de perfis de energia (`performance`, `balanced`, `power-saver`).
- Integração nativa com o **GitHub CLI (`gh`)** para gestão de repositórios.

### 2. 🛠️ Seek and Fix v5.0 (`projeto_ads/seek_and_fix.py`)
Um assistente inteligente de **Auto-Diagnóstico e Auto-Reparo Offline**:
- **Leitura de Sensores Reais:** Antes de sugerir qualquer ação, o script coleta telemetria em tempo real do sistema (status de placas de rede, bloqueios `rfkill`, processos consumindo CPU/RAM, logs do kernel, estado do PipeWire e portas USB).
- **Cérebro Local com Ollama (`llama3.2:1b`):** Analisa a telemetria sem depender de internet e seleciona a ação corretiva ideal.
- **Firewall de Segurança (Whitelist + Matriz de Risco):** Nenhuma sugestão da IA é executada às cegas. O Python valida o comando contra uma Lista Branca homologada e exibe na tela o **Nível de Risco** e a **Consequência Prática** antes de pedir a confirmação (`s/n`) do usuário.

### 3. 🗄️ Módulo de Auditoria POO + SQL (`projeto_ads/main.py`)
Implementação em Python Orientado a Objetos (`SistemaAnalise`) conectada a um banco de dados **SQLite (`database.db`)**:
- Registra automaticamente todos os eventos e reparos realizados (ou bloqueados) pelo *Seek and Fix* com data e hora.
- Permite consultar o histórico recente de manutenções diretamente pelo terminal.

### 4. 🎮 Jogos Educacionais em RPG Textual
Para fixar conceitos de infraestrutura e programação de forma gamificada no terminal:
- **🛡️ A Fortaleza dos Servidores Perdidos (`jogo_linux.sh`):** RPG onde o jogador precisa digitar comandos reais de Linux (`mkdir`, `touch`, `chmod`) para restaurar as defesas de um servidor.
- **🔮 O Oráculo dos Dados Antigos (`projeto_ads/jogo_dev.py`):** RPG focado em desafios práticos de instanciação de classes em Python (POO), consultas `SELECT` em SQL e persistência transacional (`conn.commit()`).

---

## 🚀 Como Instalar e Executar

### Pré-requisitos
- Sistema Linux baseado em Debian/Ubuntu (Zorin OS, Ubuntu, Linux Mint, Pop!_OS).
- `python3` instalado.
- *(Opcional para o modo IA)* [Ollama](https://ollama.com/) instalado com o modelo leve:
  ```bash
  curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh
  ollama pull llama3.2:1b
