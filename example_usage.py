#!/usr/bin/env python3
"""
Exemplo de uso da função fichas_tecnicas modificada.
"""

from main import fichas_tecnicas

def example_usage():
    """Exemplos de como usar a função modificada"""
    
    # Exemplo 1: Usando arquivos locais
    sources_arquivos = [
        './input_examples/receita1.txt',
        './input_examples/receita2.docx',
        './input_examples/planilha_receitas.xlsx'
    ]
    
    # Exemplo 2: Usando URLs
    sources_urls = [
        'https://tudogostoso.com.br/receita/123456-lasanha',
        'https://www.receitasnestle.com.br/receitas/bolo-chocolate'
    ]
    
    # Exemplo 3: Misturando arquivos e URLs
    sources_mistas = [
        './input_examples/receita1.txt',
        'https://tudogostoso.com.br/receita/123456-lasanha',
        './input_examples/receita2.docx'
    ]
    
    print("Exemplos de uso:")
    print("1. Com arquivos locais:")
    print(f"   fichas_tecnicas({sources_arquivos})")
    print()
    print("2. Com URLs:")
    print(f"   fichas_tecnicas({sources_urls})")
    print()
    print("3. Com fontes mistas:")
    print(f"   fichas_tecnicas({sources_mistas})")
    print()
    print("4. Com cores personalizadas:")
    print(f"   fichas_tecnicas({sources_arquivos}, color1='FF5733', color2='C4E1FF')")
    print()
    
    # Exemplo de validação - isso resultará em erro
    print("5. Exemplos que resultarão em erro:")
    print("   fichas_tecnicas([])  # Lista vazia - ValueError")
    print("   fichas_tecnicas(None)  # None - ValueError")
    
    print("6. Exemplo de ficha técnica com modo de preparo:")
    print("""
    {
        "nome_preparacao": "Lasanha à Bolonhesa",
        "rendimento_porcoes": 6,
        "preco_venda": 35.0,
        "modo_preparo": [
            "1. Refogue a cebola e alho no óleo até dourar",
            "2. Adicione a carne moída e tempere com sal",
            "3. Acrescente o molho de tomate e deixe cozinhar por 15 minutos",
            "4. Monte a lasanha alternando massa, molho e queijo",
            "5. Leve ao forno pré-aquecido a 180°C por 40 minutos"
        ],
        "ingredientes": [...]
    }
    """)
    
    # Executar um exemplo real (descomente para testar)
    # result = fichas_tecnicas(sources_arquivos)
    # print(f"Resultado: {result}")

if __name__ == "__main__":
    example_usage()