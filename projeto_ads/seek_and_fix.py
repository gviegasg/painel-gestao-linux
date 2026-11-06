import datetime
import json
import os
import sqlite3
import subprocess
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "llama3.2:1b"
DB_PATH = os.path.expanduser("~/.scripts/projeto_ads/database.db")

CYAN = "\033[0;36m"
VERDE = "\033[0;32m"
AMARELO = "\033[1;33m"
VERMELHO = "\033[0;31m"
AZUL = "\033[0;34m"
RESET = "\033[0m"

# MATRIZ DE SEGURANÇA OFICIAL (Whitelist + Riscos e Consequências)
CATALOGO_SEGURO = {
    "powerprofilesctl set power-saver": {
        "risco": "NULO (100% Seguro)",
        "consequencia": "Reduz a frequência máxima da CPU para economizar bateria e diminuir a temperatura. O notebook pode ficar ligeiramente mais lento em tarefas pesadas até você voltar para o modo 'balanced'.",
    },
    "sudo systemctl restart NetworkManager": {
        "risco": "BAIXO (Queda temporária de conexão)",
        "consequencia": "Desconecta o Wi-Fi e a rede cabeada por cerca de 3 a 5 segundos enquanto o serviço reinicia. Downloads ativos ou chamadas de vídeo podem sofrer uma breve interrupção.",
    },
    "sudo rfkill unblock all": {
        "risco": "NULO (100% Seguro)",
        "consequencia": "Apenas remove bloqueios lógicos de software das antenas Wi-Fi e Bluetooth. Não afeta arquivos nem conexões ativas.",
    },
    "sudo systemctl restart bluetooth": {
        "risco": "BAIXO (Desconexão momentânea)",
        "consequencia": "Fones de ouvido, mouses ou caixas de som Bluetooth conectados serão desconectados imediatamente e reconectarão após alguns segundos.",
    },
    "sudo resolvectl flush-caches": {
        "risco": "NULO (100% Seguro)",
        "consequencia": "Apaga a tabela temporária de nomes de sites (DNS). Não derruba a conexão atual e força o sistema a buscar endereços atualizados.",
    },
    "sudo sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'": {
        "risco": "NULO (100% Seguro)",
        "consequencia": "Salva dados pendentes no disco (sync) e limpa apenas o cache ocioso da memória RAM. Nenhum programa aberto será fechado e nenhum arquivo será perdido.",
    },
    "systemctl --user restart pipewire wireplumber": {
        "risco": "BAIXO (Corte rápido no som)",
        "consequencia": "O áudio e o microfone ficarão mudos por 1 a 2 segundos. Vídeos abertos no navegador podem pausar ou precisar que você dê 'play' novamente.",
    },
    "sudo dpkg --configure -a": {
        "risco": "BAIXO (Manutenção de pacotes)",
        "consequencia": "Retoma e conclui instalações que foram interrompidas no meio do caminho. Pode levar de 10 segundos a 2 minutos dependendo do pacote preso.",
    },
    "sudo apt clean && sudo journalctl --vacuum-size=100M": {
        "risco": "NULO (100% Seguro)",
        "consequencia": "Apaga instaladores antigos já usados do cache do APT e reduz arquivos de log do sistema para 100 MB. Não apaga nenhum documento ou programa seu.",
    },
    "sudo udevadm control --reload-rules && sudo udevadm trigger": {
        "risco": "BAIXO (Piscada em periféricos)",
        "consequencia": "Recarrega todos os drivers de portas USB. O mouse, teclado externo ou pendrive pode parar de responder por 1 segundo enquanto é reidentificado.",
    },
    "sudo systemctl start ollama": {
        "risco": "NULO (100% Seguro)",
        "consequencia": "Inicia o servidor local do Ollama em segundo plano.",
    },
}

# TRADUTOR DE ATALHOS PARA EVITAR ERROS DE DIGITAÇÃO DA IA 1B
MAPA_IA_COMANDOS = {
    "CMD_BATERIA": "powerprofilesctl set power-saver",
    "power-saver": "powerprofilesctl set power-saver",
    "CMD_REDE": "sudo systemctl restart NetworkManager",
    "NetworkManager": "sudo systemctl restart NetworkManager",
    "CMD_RFKILL": "sudo rfkill unblock all",
    "rfkill": "sudo rfkill unblock all",
    "CMD_BLUETOOTH": "sudo systemctl restart bluetooth",
    "bluetooth": "sudo systemctl restart bluetooth",
    "CMD_DNS": "sudo resolvectl flush-caches",
    "flush-caches": "sudo resolvectl flush-caches",
    "CMD_RAM": "sudo sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'",
    "drop_caches": "sudo sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'",
    "CMD_AUDIO": "systemctl --user restart pipewire wireplumber",
    "pipewire": "systemctl --user restart pipewire wireplumber",
    "CMD_APT": "sudo dpkg --configure -a",
    "dpkg": "sudo dpkg --configure -a",
    "CMD_DISCO": "sudo apt clean && sudo journalctl --vacuum-size=100M",
    "CMD_USB": "sudo udevadm control --reload-rules && sudo udevadm trigger",
}


def registrar_no_sqlite(acao_executada):
    """Conecta ao database.db do Módulo ADS (Opção 7) e grava o histórico do reparo."""
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs_acesso (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                evento TEXT NOT NULL
            )
        """)
        agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mensagem = f"[Seek & Fix] {acao_executada}"
        cursor.execute(
            "INSERT INTO logs_acesso (data, evento) VALUES (?, ?)",
            (agora, mensagem),
        )
        conn.commit()
        conn.close()
        print(
            f"💾 {CYAN}Registro salvo no banco SQLite (Módulo ADS): '{mensagem}'{RESET}"
        )
    except Exception as e:
        print(f"{VERMELHO}Erro ao gravar log no SQLite: {e}{RESET}")


def rodar_sensor(comando):
    """Executa comandos de leitura no sistema para coletar telemetria real."""
    try:
        res = subprocess.run(
            comando, shell=True, capture_output=True, text=True, timeout=5
        )
        saida = res.stdout.strip() or res.stderr.strip()
        return saida[:450] if saida else "Nenhum erro ou dado retornado."
    except Exception as e:
        return f"Erro ao ler sensor: {e}"


def coletar_telemetria(problema_usuario):
    """Coleta dados reais do Zorin OS dependendo da categoria do problema."""
    print(f"{CYAN}🔍 [Seek and Fix] Escaneando sensores do ThinkPad X280...{RESET}")
    dados = {}
    prob = problema_usuario.lower()

    if any(
        p in prob
        for p in [
            "bateria",
            "descarregando",
            "energia",
            "quente",
            "esquentando",
            "cooler",
        ]
    ):
        dados["Perfil_Energia"] = rodar_sensor("powerprofilesctl get")
        dados["Status_Bateria"] = rodar_sensor(
            "upower -i $(upower -e | grep 'BAT') | grep -E 'state|percentage|energy-rate|capacity'"
        )
        dados["Top_CPU"] = rodar_sensor(
            "ps -eo comm,%cpu --sort=-%cpu | grep -v 'ps' | head -n 5"
        )

    elif any(
        p in prob for p in ["bluetooth", "fone", "parear", "caixa de som"]
    ):
        dados["Servico_Bluetooth"] = rodar_sensor(
            "systemctl is-active bluetooth"
        )
        dados["Bloqueio_RFKill"] = rodar_sensor("rfkill list bluetooth")

    elif any(
        p in prob
        for p in ["usb", "pendrive", "mouse", "teclado", "porta", "hd externo"]
    ):
        dados["Dispositivos_USB"] = rodar_sensor("lsusb")
        dados["Ultimos_Eventos_USB"] = rodar_sensor(
            "dmesg | grep -i usb | tail -n 5"
        )

    elif any(
        p in prob
        for p in [
            "rede",
            "internet",
            "wifi",
            "wi-fi",
            "ethernet",
            "cabo",
            "conexão",
            "conexao",
            "dns",
        ]
    ):
        dados["Interfaces_Rede"] = rodar_sensor("nmcli device status")
        dados["Bloqueio_Antena"] = rodar_sensor("rfkill list wifi")
        dados["Ping_Externo"] = rodar_sensor("ping -c 1 -W 2 8.8.8.8")
        dados["Teste_DNS"] = rodar_sensor("ping -c 1 -W 2 google.com")

    elif any(
        p in prob
        for p in [
            "memoria",
            "memória",
            "ram",
            "lento",
            "travando",
            "congelando",
            "pesado",
        ]
    ):
        dados["Uso_Memoria_RAM"] = rodar_sensor("free -h")
        dados["Top_Consumo_RAM"] = rodar_sensor(
            "ps -eo pid,comm,%mem --sort=-%mem | head -n 6"
        )

    elif any(
        p in prob for p in ["som", "audio", "áudio", "mudo", "microfone", "volume"]
    ):
        dados["Servicos_Audio"] = rodar_sensor(
            "systemctl --user is-active pipewire pulseaudio"
        )
        dados["Dispositivos_Som"] = rodar_sensor("aplay -l | grep 'card'")

    elif any(
        p in prob
        for p in [
            "disco",
            "espaço",
            "espaco",
            "cheio",
            "apt",
            "atualizar",
            "pacote",
            "erro",
        ]
    ):
        dados["Uso_Disco_SSD"] = rodar_sensor("df -h /")
        dados["Tamanho_Logs"] = rodar_sensor("journalctl --disk-usage")
        dados["Processos_APT"] = rodar_sensor(
            "ps aux | grep -E 'apt|dpkg' | grep -v grep"
        )

    else:
        dados["Resumo_RAM"] = rodar_sensor("free -h")
        dados["Resumo_SSD"] = rodar_sensor("df -h /")
        dados["Erros_Recentes_Kernel"] = rodar_sensor(
            "journalctl -p 3 -n 4 --no-pager"
        )

    return dados


def normalizar_comando(cmd_bruto):
    """Traduz códigos curtos ou comandos parciais da IA para o comando completo da lista branca."""
    cmd_limpo = cmd_bruto.strip().strip("`").strip("'").strip('"')
    if cmd_limpo in CATALOGO_SEGURO:
        return cmd_limpo
    for chave, comando_oficial in MAPA_IA_COMANDOS.items():
        if chave.lower() in cmd_limpo.lower():
            return comando_oficial
    return cmd_limpo


def consultar_cerebro(problema, telemetria):
    """Envia a telemetria para o Ollama escolher um código de comando simples."""
    resumo_sensores = "\n".join([f"- {k}: {v}" for k, v in telemetria.items()])

    prompt = (
        "Você é o Seek and Fix, assistente técnico do Linux Zorin OS.\n"
        f"PROBLEMA RELATADO: {problema}\n\n"
        f"LEITURA DOS SENSORES:\n{resumo_sensores}\n\n"
        "ESCOLHA APENAS UM CÓDIGO DE REPARO ABAIXO:\n"
        "- Para bateria, energia ou aquecimento: CMD_BATERIA\n"
        "- Para Wi-Fi ou rede caindo: CMD_REDE\n"
        "- Para antena Wi-Fi/Bluetooth bloqueada: CMD_RFKILL\n"
        "- Para problema no Bluetooth: CMD_BLUETOOTH\n"
        "- Para internet conectada mas sem abrir sites (DNS): CMD_DNS\n"
        "- Para memória RAM cheia ou PC lento: CMD_RAM\n"
        "- Para som/áudio mudo: CMD_AUDIO\n"
        "- Para erro de pacotes/atualização apt: CMD_APT\n"
        "- Para disco cheio: CMD_DISCO\n"
        "- Para falha em USB/mouse/pendrive: CMD_USB\n\n"
        "Responda EXATAMENTE em 2 linhas neste formato:\n"
        "DIAGNOSTICO: <explique o que os sensores mostram em 1 frase curta em português>\n"
        "COMANDO: <escreva apenas o código CMD_ escolhido acima>"
    )

    payload = {
        "model": MODELO,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.05},
    }
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            return res["response"].strip()
    except Exception as e:
        return f"DIAGNOSTICO: O motor do Ollama não respondeu ({e}).\nCOMANDO: sudo systemctl start ollama"


def executar_com_avaliacao_risco(comando_bruto, origem="Manual"):
    """Normaliza o comando, exibe o risco/consequência, executa e salva no SQLite."""
    comando = normalizar_comando(comando_bruto)

    if comando in CATALOGO_SEGURO:
        info = CATALOGO_SEGURO[comando]
        print(
            f"\n{AZUL}========================================================={RESET}"
        )
        print(f"🔒 {VERDE}COMANDO VERIFICADO NA LISTA BRANCA:{RESET}")
        print(f"   {AMARELO}{comando}{RESET}")
        print(f"\n⚠️  {AMARELO}NÍVEL DE RISCO:{RESET} {info['risco']}")
        print(f"📋 {CYAN}CONSEQUÊNCIA PRÁTICA:{RESET}\n   {info['consequencia']}")
        print(
            f"{AZUL}========================================================={RESET}"
        )

        confirma = (
            input(f"\nDeseja prosseguir e executar esta ação? (s/n): ")
            .strip()
            .lower()
        )
        if confirma == "s":
            print(f"\n{CYAN}🚀 Executando correção...{RESET}\n")
            subprocess.run(comando, shell=True)
            print(f"\n{VERDE}✔ Operação finalizada com sucesso.{RESET}")
            registrar_no_sqlite(f"Reparo ({origem}): {comando}")
        else:
            print(f"\n{AMARELO}🛑 Operação cancelada pelo usuário.{RESET}")
            registrar_no_sqlite(f"Cancelado pelo usuário ({origem}): {comando}")
    else:
        print(f"\n{VERMELHO}🛡️ [BLOQUEIO DE SEGURANÇA ATIVADO]{RESET}")
        print(f"A IA sugeriu o comando: [{AMARELO}{comando_bruto}{RESET}]")
        print(
            "Risco: ALTO (Comando fora do catálogo homologado / possível alucinação)."
        )
        print(
            "Consequência: Execução bloqueada automaticamente para proteger seu Zorin OS."
        )
        registrar_no_sqlite(f"BLOQUEIO DE SEGURANÇA (IA): {comando_bruto}")


def reparo_conexoes():
    print(f"\n{AMARELO}🌐 [Seek and Fix] Reparo de Conexões{RESET}")
    print("1) Reiniciar Rede Wi-Fi / Ethernet")
    print("2) Reiniciar Bluetooth")
    print("3) Desbloquear Antenas (RFKill)")
    print("4) Limpar Cache de DNS")
    op = input("\nEscolha (1-4): ").strip()
    mapa = {
        "1": "sudo systemctl restart NetworkManager",
        "2": "sudo systemctl restart bluetooth",
        "3": "sudo rfkill unblock all",
        "4": "sudo resolvectl flush-caches",
    }
    if op in mapa:
        executar_com_avaliacao_risco(mapa[op], origem="Menu Conexões")


def reparo_bateria():
    print(f"\n{AMARELO}🔋 [Seek and Fix] Diagnóstico de Bateria e CPU{RESET}")
    print("\nTop 5 processos exigindo do processador agora:")
    print(
        rodar_sensor("ps -eo comm,%cpu --sort=-%cpu | grep -v 'ps' | head -n 6")
    )
    executar_com_avaliacao_risco(
        "powerprofilesctl set power-saver", origem="Menu Bateria"
    )


def reparo_memoria():
    print(f"\n{AMARELO}🧠 [Seek and Fix] Diagnóstico de Memória RAM{RESET}")
    print(rodar_sensor("free -h"))
    print("\nTop 5 programas consumindo mais memória:")
    print(rodar_sensor("ps -eo pid,comm,%mem --sort=-%mem | head -n 6"))

    print("\nOpções:")
    print("1) Limpar Cache de Memória RAM (Seguro)")
    print("2) Encerrar um programa travado pelo número PID")
    op = input("\nEscolha (1-2): ").strip()

    if op == "1":
        executar_com_avaliacao_risco(
            "sudo sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'",
            origem="Menu RAM",
        )
    elif op == "2":
        pid = input(
            "\nDigite o número PID do programa que deseja fechar: "
        ).strip()
        if pid.isdigit():
            nome_proc = rodar_sensor(f"ps -p {pid} -o comm=")
            print(f"\n{VERMELHO}⚠️  ATENÇÃO - RISCO MÉDIO:{RESET}")
            print(
                f"   Você está prestes a forçar o fechamento imediato (kill -9) do processo [{AMARELO}{nome_proc} (PID: {pid}){RESET}]."
            )
            print(
                "   Consequência: Qualquer trabalho não salvo aberto nesse programa será perdido imediatamente."
            )
            conf = (
                input("\nTem certeza que deseja encerrar este processo? (s/n): ")
                .strip()
                .lower()
            )
            if conf == "s":
                subprocess.run(f"kill -9 {pid}", shell=True)
                print(f"{VERDE}✔ Processo {pid} ({nome_proc}) encerrado.{RESET}")
                registrar_no_sqlite(
                    f"Processo encerrado (kill -9): PID {pid} ({nome_proc})"
                )


def reparo_sistema_audio_disco():
    print(
        f"\n{AMARELO}🛠️ [Seek and Fix] Manutenção de Áudio, USB, Pacotes e Disco{RESET}"
    )
    print("1) Reiniciar Áudio/Microfone (PipeWire)")
    print("2) Recarregar portas USB (Mouse/Pendrive não reconhecido)")
    print("3) Destravar Atualizações (dpkg quebrado)")
    print("4) Limpar Logs Antigos e Cache de Disco (Liberar SSD)")
    sub = input("\nEscolha a ação (1-4): ").strip()
    mapa = {
        "1": "systemctl --user restart pipewire wireplumber",
        "2": "sudo udevadm control --reload-rules && sudo udevadm trigger",
        "3": "sudo dpkg --configure -a",
        "4": "sudo apt clean && sudo journalctl --vacuum-size=100M",
    }
    if sub in mapa:
        executar_com_avaliacao_risco(mapa[sub], origem="Menu Sistema")


if __name__ == "__main__":
    print(
        f"{CYAN}========================================================={RESET}"
    )
    print(
        f"{AMARELO}     🛠️  SEEK AND FIX v5.0 - DIAGNÓSTICO E AUTO-REPARO     {RESET}"
    )
    print(
        f"{CYAN}========================================================={RESET}"
    )
    print("1) Descrever problema para Diagnóstico Inteligente (IA + Sensores)")
    print("2) Auto-Reparo: Conexões (Wi-Fi, Ethernet, Bluetooth e DNS)")
    print("3) Auto-Reparo: Bateria e Aquecimento (Modo Eco + Checagem CPU)")
    print("4) Auto-Reparo: Memória RAM e Travamentos (Limpar Cache + Matar PID)")
    print("5) Auto-Reparo: Áudio, Portas USB, Disco Cheio e APT Travado")
    print("0) Voltar ao Menu Principal")

    escolha = input("\nEscolha o módulo: ").strip()

    if escolha == "2":
        reparo_conexoes()
    elif escolha == "3":
        reparo_bateria()
    elif escolha == "4":
        reparo_memoria()
    elif escolha == "5":
        reparo_sistema_audio_disco()
    elif escolha == "1":
        problema = input(
            "\nDescreva o problema (ex: bluetooth não conecta, pc lento, sem som): "
        )
        telemetria = coletar_telemetria(problema)

        print(f"\n{CYAN}📊 Telemetria coletada pelos sensores:{RESET}")
        for chave, valor in telemetria.items():
            print(f"  • {AMARELO}{chave}:{RESET}\n    {valor}\n")

        print(f"{CYAN}🧠 Analisando telemetria com {MODELO}...{RESET}\n")
        resposta_ia = consultar_cerebro(problema, telemetria)

        print(f"{VERDE}--- DIAGNÓSTICO DA IA ---{RESET}")
        print(resposta_ia)
        print(f"{VERDE}-------------------------{RESET}")

        comando_sugerido = ""
        for linha in resposta_ia.split("\n"):
            if "COMANDO:" in linha.upper():
                comando_sugerido = linha.split(":", 1)[1].strip()

        if comando_sugerido:
            executar_com_avaliacao_risco(comando_sugerido, origem="IA")
