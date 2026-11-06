import sys
import time

CYAN = "\033[0;36m"
VERDE = "\033[0;32m"
VERMELHO = "\033[0;31m"
AMARELO = "\033[1;33m"
RESET = "\033[0m"


class RPGDev:

    def __init__(self):
        self.mana = 100

    def tutorial(self):
        print(f"{CYAN}{'='*55}{RESET}")
        print(
            f"{AMARELO}   🔮 O ORÁCULO DOS DADOS ANTIGOS (RPG ADS)         {RESET}"
        )
        print(f"{CYAN}{'='*55}{RESET}")
        print(f"\n{AMARELO}📜 GUIA RÁPIDO DE FEITIÇOS (TUTORIAL):{RESET}")
        print(f"  • {VERDE}POO:{RESET} Em Python, classes usam 'def __init__(self):' e métodos acessam 'self'.")
        print(
            f"  • {VERDE}SQL SELECT:{RESET} 'SELECT colunas FROM tabela WHERE condicao;'"
        )
        print(
            f"  • {VERDE}SQL INSERT:{RESET} 'INSERT INTO tabela (colunas) VALUES (valores);'"
        )
        print(
            f"  • {VERDE}SQLite Commit:{RESET} Modificações exigem 'conn.commit()' para persistir no disco.\n"
        )
        input("Pressione Enter para entrar no Templo...")

    def executar(self):
        self.tutorial()

        # Missão 1
        print(
            f"\n{AMARELO}--- CAPÍTULO I: O Despertar da Entidade (POO) ---{RESET}"
        )
        print(
            "Diante do altar, você precisa instanciar o guardião da classe 'Oraculo'."
        )
        print("Escreva o comando Python exato para criar o objeto 'bot' a partir da classe 'Oraculo()'.")

        while True:
            cmd = input(f"{CYAN}dev@oraculo:~$ {RESET}").strip()
            if cmd == "bot = Oraculo()":
                print(
                    f"{VERDE}✔ O autômato ganha consciência: 'Saudações, Mago dos Dados!'{RESET}\n"
                )
                break
            else:
                self.mana -= 25
                print(
                    f"{VERMELHO}✖ Sintaxe corrompida! Mana restante: {self.mana}/100{RESET}"
                )
                if self.mana <= 0:
                    print(
                        f"{VERMELHO}💀 Sua mana secou. O monólito desmoronou!{RESET}"
                    )
                    sys.exit(0)

        # Missão 2
        print(f"{AMARELO}--- CAPÍTULO II: A Busca no Santuário (SQL) ---{RESET}")
        print("O autômato pergunta: 'Como extrair todos os registros da tabela segredos onde status é igual a 'ativo'?'")
        print(
            "Digite a query SQL (em maiúsculas ou minúsculas, sem necessidade de ponto e vírgula):"
        )

        while True:
            cmd = input(f"{CYAN}sql@oraculo:~$ {RESET}").strip().rstrip(";")
            cmd_norm = " ".join(cmd.upper().split())
            if (
                cmd_norm
                == "SELECT * FROM SEGREDOS WHERE STATUS = 'ATIVO'"
                or cmd_norm == 'SELECT * FROM SEGREDOS WHERE STATUS = "ATIVO"'
            ):
                print(
                    f"{VERDE}✔ A câmara subterrânea se abre revelando as tabelas sagradas!{RESET}\n"
                )
                break
            else:
                self.mana -= 25
                print(
                    f"{VERMELHO}✖ Query inválida! O templo treme. Mana: {self.mana}/100{RESET}"
                )
                if self.mana <= 0:
                    print(f"{VERMELHO}💀 Mana esgotada. Fim de jogo!{RESET}")
                    sys.exit(0)

        # Missão 3
        print(
            f"{AMARELO}--- CAPÍTULO III: A Selagem do Destino (SQLite) ---{RESET}"
        )
        print("Você inseriu novos dados na tabela, mas as alterações continuam voláteis na memória RAM.")
        print(
            "Qual comando Python deve ser invocado sobre a conexão 'conn' para gravar no disco?"
        )

        while True:
            cmd = input(f"{CYAN}dev@oraculo:~$ {RESET}").strip()
            if cmd == "conn.commit()":
                print(
                    f"{VERDE}✔ As runas foram gravadas na pedra! O banco SQLite está seguro.{RESET}\n"
                )
                break
            else:
                self.mana -= 25
                print(
                    f"{VERMELHO}✖ Os dados começam a evaporar! Mana: {self.mana}/100{RESET}"
                )
                if self.mana <= 0:
                    print(
                        f"{VERMELHO}💀 Falha na transação. Rollback total!{RESET}"
                    )
                    sys.exit(0)

        print(f"\n{CYAN}{'='*55}{RESET}")
        print(
            f"{VERDE}🏆 VITÓRIA! Você restaurou o Oráculo com Mana Final: {self.mana}/100{RESET}"
        )
        print(f"{CYAN}{'='*55}{RESET}")
        input("\nPressione Enter para retornar ao menu principal.")


if __name__ == "__main__":
    jogo = RPGDev()
    jogo.executar()
