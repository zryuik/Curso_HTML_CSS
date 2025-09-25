
senha_correta = 123456
valor_disponivel = 5000

def caixa_eletronico():

    print("Iniciaalizando sistema...")
    senha_digitada = int(input("Digite sua senha: "))

    if senha_digitada != senha_correta:
        print("Senha incorreta ")
        print("Finalizando o sistema ")
    else:
        print("Senha correta ")
        oprecao = input("Escolha uma operação (saque): ")
        if oprecao  != "saque":
            print("Finalizando o sistema ")
        else:
            valor_escolhido = int(input("Digite o valor: "))
            if valor_escolhido > valor_disponivel:
                print("Valor indisponivel, finalizando sistema... ")
            else:
                print("Atualizando o saldo... ")
                print("Por favor, retire o dinheiro")
                recibo = input("Deseja rebido da operação? S/N ")
                if recibo == "N":
                    print("Finalizando sistema")
                else:
                    print("Imprimindo recibo")
                    print("Finalizando sistema...")


while True:
    print("\n--- CAIXA ELETRONICO ---")
    print("[0] SAQUE")
    print("[1] DEPOSITO")
    print("[3] CONSULTA A SALDO")
    print("[4] SAIR")



    
   
        


