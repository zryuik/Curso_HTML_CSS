from datetime import datetime
import barcode
from barcode.writer import ImageWriter
import math
import os
import json # Importamos a biblioteca JSON

# --- Configurações ---
NOME_ESTACIONAMENTO = "Parque das Almas"
PRECO_POR_HORA = 5.00
ARQUIVO_DE_DADOS = 'estacionamento_dados.json' # Nome do nosso "banco de dados"

# --- Funções de Persistência ---

def carregar_dados():
    """Carrega os dados do arquivo JSON ao iniciar o programa."""
    try:
        with open(ARQUIVO_DE_DADOS, 'r') as f:
            dados_salvos = json.load(f)
            # JSON salva datetimes como strings. Precisamos convertê-las de volta.
            vagas_convertidas = {}
            for placa, data_str in dados_salvos.items():
                vagas_convertidas[placa] = datetime.fromisoformat(data_str)
            print("✔️ Dados carregados com sucesso!")
            return vagas_convertidas
    except FileNotFoundError:
        # Se o arquivo não existe, começamos com um dicionário vazio.
        print("ℹ️ Nenhum arquivo de dados encontrado. Iniciando um novo.")
        return {}
    except json.JSONDecodeError:
        print("❌ Erro ao ler o arquivo de dados. Iniciando um novo.")
        return {}


def salvar_dados(vagas):
    """Salva o dicionário de vagas no arquivo JSON."""
    # Para salvar datetimes em JSON, primeiro convertemos para string no formato ISO
    dados_para_salvar = {}
    for placa, data_obj in vagas.items():
        dados_para_salvar[placa] = data_obj.isoformat()
    
    with open(ARQUIVO_DE_DADOS, 'w') as f:
        json.dump(dados_para_salvar, f, indent=4)


# --- Funções do Sistema (com pequenas modificações) ---

def gerar_ticket(placa):
    """Gera uma imagem de código de barras para a placa."""
    try:
        Code128 = barcode.get_barcode_class('code128')
        codigo = Code128(placa, writer=ImageWriter())
        if not os.path.exists('tickets'):
            os.makedirs('tickets')
        nome_arquivo = f'tickets/ticket_{placa}'
        codigo.save(nome_arquivo)
        print(f"✔️ Ticket gerado e salvo como '{nome_arquivo}.png'")
    except Exception as e:
        print(f"❌ Erro ao gerar o código de barras: {e}")

def registrar_entrada(vagas):
    """Registra a entrada de um veículo no estacionamento."""
    placa = input("Digite a placa do carro: ").upper().strip()

    if not placa:
        print("❌ Placa inválida.")
        return

    if placa in vagas:
        print("❌ Atenção: Este carro já está no estacionamento!")
    else:
        vagas[placa] = datetime.now()
        salvar_dados(vagas)  # <<-- PONTO CHAVE: Salvamos os dados após a entrada
        print(f"\n🚗 Entrada registrada para o veículo de placa {placa}.")
        print(f"Horário de entrada: {vagas[placa].strftime('%d/%m/%Y %H:%M:%S')}")
        gerar_ticket(placa)
        print("\nSeja bem-vindo e aproveite o passeio!")

def registrar_saida(vagas):
    """Registra a saída de um veículo e calcula o valor a ser pago."""
    placa = input("Digite a placa do carro para registrar a saída: ").upper().strip()

    if placa in vagas:
        hora_entrada = vagas.pop(placa)
        salvar_dados(vagas) # <<-- PONTO CHAVE: Salvamos os dados após a saída
        hora_saida = datetime.now()
        duracao = hora_saida - hora_entrada
        
        total_segundos = duracao.total_seconds()
        horas_cobradas = math.ceil(total_segundos / 3600)
        if horas_cobradas == 0: horas_cobradas = 1
        valor_a_pagar = horas_cobradas * PRECO_POR_HORA
        
        print("\n--- Recibo de Saída ---")
        print(f"Veículo: {placa}")
        print(f"Entrada: {hora_entrada.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Saída  : {hora_saida.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Tempo total: {str(duracao).split('.')[0]}")
        print(f"Horas cobradas: {horas_cobradas}h")
        print("-----------------------")
        print(f"Valor a pagar: R$ {valor_a_pagar:.2f}")
        print("-----------------------")
        print("\nVolte sempre!")
    else:
        print("❌ Carro não encontrado. Verifique se a placa está correta.")

# --- Loop Principal do Programa ---

def main():
    """Função principal que executa o menu do sistema."""
    vagas = carregar_dados() # <<-- PONTO CHAVE: Carregamos os dados ao iniciar
    
    print(f"\n--- Bem-vindo ao Sistema do {NOME_ESTACIONAMENTO} ---")
    print(f"ℹ️ {len(vagas)} veículo(s) no pátio.")

    while True:
        print("\nEscolha uma opção:")
        print("1 - Registrar Entrada de Veículo")
        print("2 - Registrar Saída de Veículo")
        print("3 - Sair do Sistema")
        
        opcao = input("Opção: ")
        
        if opcao == '1':
            registrar_entrada(vagas)
        elif opcao == '2':
            registrar_saida(vagas)
        elif opcao == '3':
            print("Obrigado por usar o sistema. Até logo!")
            break
        else:
            print("❌ Opção inválida. Por favor, tente novamente.")

# Executa o programa
if __name__ == "__main__":
    main()