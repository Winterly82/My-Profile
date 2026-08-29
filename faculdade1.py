def calcular_probabilidades():
    print("=" * 70)
    print("ANALISADOR DE DEFEITOS EM APARELHOS DE TV")
    print("=" * 70)
    
    print("\n INSTRUÇÕES:")
    print("Digite os percentuais de cada categoria de defeito.")
    print("EXEMPLO: Se você digitar '2', será interpretado como 2%")
    print("Os valores devem estar entre 0 e 100")
    print("A soma total pode ser menor que 100% (o restante são aparelhos sem defeito)")
    print("-" * 70)
    
    print("\n INSIRA OS DADOS (EM PORCENTAGEM):")
    
    try:
        apenas_A = float(input("  Aparelhos com apenas defeitos críticos (A): "))
        apenas_B = float(input("  Aparelhos com apenas defeitos graves (B): "))
        apenas_C = float(input("  Aparelhos com apenas defeitos pequenos (C): "))
        A_e_B = float(input("  Aparelhos com defeitos críticos e graves (A∩B): "))
        A_e_C = float(input("  Aparelhos com defeitos críticos e pequenos (A∩C): "))
        B_e_C = float(input("  Aparelhos com defeitos graves e pequenos (B∩C): "))
        A_B_C = float(input("  Aparelhos com os três tipos de defeito (A∩B∩C): "))
        
        valores = [apenas_A, apenas_B, apenas_C, A_e_B, A_e_C, B_e_C, A_B_C]
        for val in valores:
            if val < 0 or val > 100:
                print(f"\n ERRO: O valor {val}% está fora do intervalo permitido (0 a 100)!")
                return
        
    except ValueError:
        print("\n ERRO: Por favor, digite apenas números válidos (ex: 2, 3.5, 10)!")
        return
    
    total = 100  
    
    soma_defeitos = apenas_A + apenas_B + apenas_C + A_e_B + A_e_C + B_e_C + A_B_C
    
    if soma_defeitos > 100:
        print(f"\n  ATENÇÃO: A soma dos defeitos é {soma_defeitos:.1f}%, que ultrapassa 100%!")
        print("   Isso é impossível na prática. Verifique seus dados.")
        continuar = input("\nDeseja continuar mesmo assim? (s/n): ").lower()
        if continuar != 's':
            return
    
    P_A = apenas_A + A_e_B + A_e_C + A_B_C
    P_B = apenas_B + A_e_B + B_e_C + A_B_C
    P_C = apenas_C + A_e_C + B_e_C + A_B_C
    
    P_A_e_B = A_e_B + A_B_C
    P_A_e_C = A_e_C + A_B_C
    P_B_e_C = B_e_C + A_B_C
    P_A_e_B_e_C = A_B_C
    
    P_uniao = P_A + P_B + P_C - P_A_e_B - P_A_e_C - P_B_e_C + P_A_e_B_e_C
    P_nenhum = total - P_uniao
    
    P_A_ou_B = P_A + P_B - P_A_e_B
    
    print("\n" + "=" * 70)
    print(" RESULTADOS DA ANÁLISE")
    print("=" * 70)
    
    print("\n DADOS INSERIDOS (em %):")
    print(f"  Apenas defeitos críticos (A):        {apenas_A:>6.1f}%")
    print(f"  Apenas defeitos graves (B):          {apenas_B:>6.1f}%")
    print(f"  Apenas defeitos pequenos (C):        {apenas_C:>6.1f}%")
    print(f"  Defeitos críticos e graves (A∩B):    {A_e_B:>6.1f}%")
    print(f"  Defeitos críticos e pequenos (A∩C):  {A_e_C:>6.1f}%")
    print(f"  Defeitos graves e pequenos (B∩C):    {B_e_C:>6.1f}%")
    print(f"  Os três tipos (A∩B∩C):               {A_B_C:>6.1f}%")
    print(f"  Soma dos defeitos informados:         {soma_defeitos:>6.1f}%")
    
    print("\n PROBABILIDADES INDIVIDUAIS (em %):")
    print(f"  P(A) = {P_A:>6.1f}%  (defeitos críticos)")
    print(f"  P(B) = {P_B:>6.1f}%  (defeitos graves)")
    print(f"  P(C) = {P_C:>6.1f}%  (defeitos pequenos)")
    
    print("\n RESPOSTAS:")
    print(f"  a) Fração sem nenhum defeito:           {P_nenhum:>6.1f}%")
    print(f"  b) Fração com defeitos críticos OU graves: {P_A_ou_B:>6.1f}%")
    
    soma_verificacao = soma_defeitos + P_nenhum
    print(f"\n Verificação: Soma total = {soma_verificacao:.1f}%")
    
    if abs(soma_verificacao - 100) > 0.01:
        diferenca = 100 - soma_verificacao
        print(f"  ATENÇÃO: Há uma diferença de {abs(diferenca):.1f}%")
        if diferenca > 0:
            print(f"   Isso pode indicar que {diferenca:.1f}% dos aparelhos estão em categorias não especificadas")
        else:
            print("   Os dados estão inconsistentes (soma > 100%)")
    
    print("\n" + "=" * 70)
    
    print("\n EXPLICAÇÃO PASSO A PASSO DOS CÁLCULOS:")
    print("-" * 70)
    print("a) Para calcular a fração sem defeitos:")
    print("   1. Usamos o Princípio da Inclusão-Exclusão para calcular P(A∪B∪C):")
    print(f"      P(A∪B∪C) = {P_A:.1f} + {P_B:.1f} + {P_C:.1f} - {P_A_e_B:.1f} - {P_A_e_C:.1f} - {P_B_e_C:.1f} + {A_B_C:.1f}")
    print(f"      P(A∪B∪C) = {P_uniao:.1f}%")
    print(f"   2. P(nenhum) = 100% - {P_uniao:.1f}% = {P_nenhum:.1f}%")
    
    print("\nb) Para calcular a fração com defeitos críticos OU graves:")
    print("   Usamos a fórmula para a união de dois eventos:")
    print(f"   P(A∪B) = P(A) + P(B) - P(A∩B)")
    print(f"   P(A∪B) = {P_A:.1f} + {P_B:.1f} - {P_A_e_B:.1f} = {P_A_ou_B:.1f}%")
    
    print("\n VISUALIZAÇÃO DOS DADOS:")
    print("-" * 70)
    print("Diagrama de Venn (representação simplificada):")
    print("")
    print("    ┌──────────────────────────────┐")
    print("    │        CONJUNTO UNIVERSAL    │")
    print("    │      (100% dos aparelhos)    │")
    print("    │                              │")
    print(f"    │  ┌───────┐   ┌───────┐      │")
    print(f"    │  │   A   │   │   B   │      │")
    print(f"    │  │  {P_A:>4.1f}%  │   │  {P_B:>4.1f}%  │      │")
    print(f"    │  │  ┌───┐│   │  │     │      │")
    print(f"    │  │  │{A_B_C:>3.1f}%││   │  │     │      │")
    print(f"    │  │  └───┘│   │  │     │      │")
    print(f"    │  └───────┘   └───┼─────┘      │")
    print(f"    │                  │            │")
    print(f"    │            ┌─────┴─────┐      │")
    print(f"    │            │     C     │      │")
    print(f"    │            │   {P_C:>4.1f}%   │      │")
    print(f"    │            └───────────┘      │")
    print(f"    │                              │")
    print(f"    │  Aparelhos sem defeito: {P_nenhum:>4.1f}%  │")
    print("    └──────────────────────────────┘")
    
    return {
        'apenas_A': apenas_A, 'apenas_B': apenas_B, 'apenas_C': apenas_C,
        'A_e_B': A_e_B, 'A_e_C': A_e_C, 'B_e_C': B_e_C, 'A_B_C': A_B_C,
        'P_A': P_A, 'P_B': P_B, 'P_C': P_C,
        'P_nenhum': P_nenhum,
        'P_A_ou_B': P_A_ou_B
    }

def main():
    print(" ANALISADOR DE DEFEITOS - VERSÃO INTERATIVA")
    print("=" * 70)
    print("Todos os números digitados serão interpretados como PORCENTAGEM")
    print("Exemplo: digite '2' para representar 2%")
    print("=" * 70)
    
    while True:
        print("\n" + " NOVA ANÁLISE")
        print("-" * 70)
        calcular_probabilidades()
        
        print("\n" + "=" * 70)
        continuar = input("\nDeseja fazer outra análise com dados diferentes? (s/n): ").lower()
        if continuar != 's':
            print("\n Obrigado por usar o Analisador de Defeitos!")
            break

if __name__ == "__main__":
    main()