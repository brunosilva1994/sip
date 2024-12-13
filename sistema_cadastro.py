import curses
import datetime


# Listas globais para armazenar dados
tecnicos = []
veiculos = []


# Menu principal intuitivo com navegação usando setas
def menu_principal(stdscr):
    curses.curs_set(0)  # Ocultar o cursor
    menu_opcoes = [
        "Cadastrar Técnico",
        "Cadastrar Veículo",
        "Exibir Veículos",
        "Previsão de Custos de Viagem",
        "Sair"
    ]
    indice_selecionado = 0  # Índice da opção atualmente selecionada

    while True:
        # Limpar tela
        stdscr.clear()
        stdscr.addstr(0, 2, "--- MENU PRINCIPAL ---", curses.A_BOLD)

        # Desenhar o menu com destaque na opção selecionada
        for idx, opcao in enumerate(menu_opcoes):
            if idx == indice_selecionado:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(2 + idx, 4, opcao)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(2 + idx, 4, opcao)

        # Atualizar interface
        stdscr.refresh()

        # Capturar entrada do usuário
        tecla = stdscr.getch()

        if tecla == curses.KEY_DOWN:
            indice_selecionado = (indice_selecionado + 1) % len(menu_opcoes)
        elif tecla == curses.KEY_UP:
            indice_selecionado = (indice_selecionado - 1) % len(menu_opcoes)
        elif tecla in [10, 13]:  # Enter
            if indice_selecionado == 0:  # Cadastrar Técnico
                cadastrar_tecnico(stdscr)
            elif indice_selecionado == 1:  # Cadastrar Veículo
                cadastrar_veiculo(stdscr)
            elif indice_selecionado == 2:  # Exibir Veículos
                exibir_veiculos(stdscr)
            elif indice_selecionado == 3:  # Previsão de Custos
                previsao_custos_viagem(stdscr)
            elif indice_selecionado == 4:  # Sair
                break


# Função para cadastrar técnico
def cadastrar_tecnico(stdscr):
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 2, "--- CADASTRAR TÉCNICO ---")
    stdscr.addstr(2, 0, "Digite o nome do técnico: ")
    stdscr.refresh()
    nome_tecnico = stdscr.getstr(2, 30, 20).decode("utf-8").strip()
    tecnicos.append({"nome": nome_tecnico})
    curses.noecho()
    stdscr.addstr(4, 0, f"Técnico '{nome_tecnico}' cadastrado com sucesso!")
    stdscr.addstr(6, 0, "Pressione qualquer tecla para retornar ao menu principal.")
    stdscr.refresh()
    stdscr.getch()


# Função para cadastrar veículo
def cadastrar_veiculo(stdscr):
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 2, "--- CADASTRAR VEÍCULO ---")
    stdscr.addstr(2, 0, "Digite a placa do veículo: ")
    stdscr.refresh()
    placa = stdscr.getstr(2, 30, 10).decode("utf-8").strip()
    stdscr.addstr(4, 0, "Digite o modelo do veículo: ")
    stdscr.refresh()
    modelo = stdscr.getstr(4, 30, 20).decode("utf-8").strip()
    veiculos.append({"placa": placa, "modelo": modelo})
    curses.noecho()
    stdscr.addstr(6, 0, f"Veículo {modelo} com placa {placa} cadastrado com sucesso!")
    stdscr.addstr(8, 0, "Pressione qualquer tecla para retornar ao menu principal.")
    stdscr.refresh()
    stdscr.getch()


# Exibir veículos no menu
def exibir_veiculos(stdscr):
    stdscr.clear()
    stdscr.addstr(0, 2, "--- VEÍCULOS CADASTRADOS ---")
    if veiculos:
        for idx, veiculo in enumerate(veiculos, start=1):
            stdscr.addstr(2 + idx, 4, f"{idx}. {veiculo['modelo']} - {veiculo['placa']}")
    else:
        stdscr.addstr(2, 4, "Nenhum veículo cadastrado.")
    stdscr.addstr(6 + len(veiculos), 0, "Pressione qualquer tecla para retornar ao menu principal.")
    stdscr.refresh()
    stdscr.getch()


# Previsão de custos da viagem com base nas regras
def previsao_custos_viagem(stdscr):
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 2, "--- PREVISÃO DE CUSTOS DA VIAGEM ---")

    # Coletando informações
    stdscr.addstr(2, 0, "Digite a data de saída (AAAA-MM-DD): ")
    stdscr.refresh()
    data_saida = stdscr.getstr(2, 40, 10).decode("utf-8").strip()
    stdscr.addstr(3, 0, "Digite a data de chegada (AAAA-MM-DD): ")
    stdscr.refresh()
    data_chegada = stdscr.getstr(3, 40, 10).decode("utf-8").strip()
    stdscr.addstr(4, 0, "Digite o destino da viagem: ")
    stdscr.refresh()
    destino = stdscr.getstr(4, 30, 20).decode("utf-8").strip().lower()

    # Calculando o período da viagem
    inicio = datetime.datetime.strptime(data_saida, "%Y-%m-%d").date()
    fim = datetime.datetime.strptime(data_chegada, "%Y-%m-%d").date()
    dias_viagem = (fim - inicio).days

    # Custos
    custo_almoco = 37.50
    custo_janta = 30.00
    custo_outros = 50

    if destino == "ourilandia do norte":
        custo_total = dias_viagem * (custo_almoco + custo_janta)
    else:
        custo_total = dias_viagem * (custo_almoco + custo_janta + custo_outros)

    curses.noecho()
    stdscr.addstr(6, 0, f"Período: {dias_viagem} dias")
    stdscr.addstr(8, 0, f"Custo Almoço + Lanche da tarde: R${custo_almoco:.2f}")
    stdscr.addstr(9, 0, f"Custo Janta: R${custo_janta:.2f}")
    if destino != "ourilandia do norte":
        stdscr.addstr(10, 0, f"Custo Outros: R${custo_outros:.2f}")
    stdscr.addstr(12, 0, f"Custo Total: R${custo_total:.2f}")
    stdscr.addstr(14, 0, "Pressione qualquer tecla para retornar ao menu principal.")
    stdscr.refresh()
    stdscr.getch()


# Execução principal
if __name__ == "__main__":
    curses.wrapper(menu_principal)
