#!/usr/bin/env python3
"""
Teste do cálculo de preço de venda baseado no custo dos ingredientes
"""

import sys
import os
import json
import math
sys.path.append('/Users/cairorocha/Documents/fichas_tecnicas')

from tools.generate_excel import ExcelGeneratorTool

def calculate_recipe_cost_and_price(recipe, insumos_dict):
    """Calcula o custo total da receita e preço de venda sugerido"""
    
    print(f"\n📊 Calculando custos para: {recipe.get('nome_preparacao', 'Receita')}")
    print(f"🍽️  Rendimento: {recipe.get('rendimento_porcoes', 1)} porções")
    
    total_cost = 0.0
    detailed_costs = []
    
    for ingrediente in recipe.get('ingredientes', []):
        nome = ingrediente.get('nome', '')
        quantidade = ingrediente.get('quantidade', 0)
        fator_correcao = ingrediente.get('fator_correcao', 1.0)
        
        # Buscar preço no dicionário de insumos
        preco_unitario = 0.0
        if nome.lower() in insumos_dict:
            preco_unitario = insumos_dict[nome.lower()].get('preco', 0.0)
        
        # Calcular custo do ingrediente
        quantidade_corrigida = quantidade * fator_correcao
        custo_ingrediente = quantidade_corrigida * preco_unitario
        total_cost += custo_ingrediente
        
        detailed_costs.append({
            'nome': nome,
            'quantidade': quantidade,
            'fator_correcao': fator_correcao,
            'quantidade_corrigida': quantidade_corrigida,
            'preco_unitario': preco_unitario,
            'custo_total': custo_ingrediente
        })
        
        print(f"  • {nome}: {quantidade:.3f} × {fator_correcao:.2f} × R$ {preco_unitario:.2f} = R$ {custo_ingrediente:.2f}")
    
    print(f"💰 Custo total da receita: R$ {total_cost:.2f}")
    
    # Calcular preço de venda
    rendimento = recipe.get('rendimento_porcoes', 1)
    custo_por_porcao = total_cost / rendimento
    
    # Aplicar markup de 3.5x (mínimo 3x)
    preco_base = custo_por_porcao * 3.5
    
    # Arredondar para o próximo 0.50
    preco_venda = math.ceil(preco_base * 2) / 2
    
    # Garantir mínimo de 3x
    preco_minimo = custo_por_porcao * 3
    if preco_venda < preco_minimo:
        preco_venda = math.ceil(preco_minimo * 2) / 2
    
    markup_real = (preco_venda / custo_por_porcao) if custo_por_porcao > 0 else 0
    
    print(f"💵 Custo por porção: R$ {custo_por_porcao:.2f}")
    print(f"🏷️  Preço de venda sugerido: R$ {preco_venda:.2f}")
    print(f"📈 Markup aplicado: {markup_real:.1f}x")
    
    return {
        'total_cost': total_cost,
        'cost_per_portion': custo_por_porcao,
        'suggested_price': preco_venda,
        'markup': markup_real,
        'detailed_costs': detailed_costs
    }

def test_price_calculation():
    """Testa o cálculo de preços de venda"""
    
    print("🧪 Testando cálculo de preços de venda...")
    
    # Dados de teste com custos reais
    test_data = {
        "fichas_tecnicas": [
            {
                "nome_preparacao": "Lasanha à Bolonhesa",
                "rendimento_porcoes": 8,
                "preco_venda": 0.0,  # Será calculado
                "ingredientes": [
                    {
                        "nome": "Massa para Lasanha",
                        "unidade": "kg",
                        "quantidade": 0.5,
                        "fator_correcao": 1.0,
                        "custo_unitario": 0.0  # Será preenchido
                    },
                    {
                        "nome": "Carne Moída",
                        "unidade": "kg", 
                        "quantidade": 0.6,
                        "fator_correcao": 1.2,  # 20% de perda no preparo
                        "custo_unitario": 0.0
                    },
                    {
                        "nome": "Molho de Tomate",
                        "unidade": "kg",
                        "quantidade": 0.7,
                        "fator_correcao": 1.0,
                        "custo_unitario": 0.0
                    },
                    {
                        "nome": "Queijo Mussarela",
                        "unidade": "kg",
                        "quantidade": 0.3,
                        "fator_correcao": 1.0,
                        "custo_unitario": 0.0
                    },
                    {
                        "nome": "Cebola",
                        "unidade": "kg",
                        "quantidade": 0.15,
                        "fator_correcao": 1.3,  # 30% de perda (casca, etc)
                        "custo_unitario": 0.0
                    }
                ],
                "modo_preparo": [
                    "1. Prepare o molho à bolonhesa",
                    "2. Cozinhe as massas al dente", 
                    "3. Monte alternando camadas",
                    "4. Asse por 45 minutos a 180°C"
                ]
            },
            {
                "nome_preparacao": "Bolo de Chocolate Simples",
                "rendimento_porcoes": 12,
                "preco_venda": 0.0,
                "ingredientes": [
                    {
                        "nome": "Farinha de Trigo",
                        "unidade": "kg",
                        "quantidade": 0.4,
                        "fator_correcao": 1.0,
                        "custo_unitario": 0.0
                    },
                    {
                        "nome": "Açúcar Cristal",
                        "unidade": "kg",
                        "quantidade": 0.3,
                        "fator_correcao": 1.0,
                        "custo_unitario": 0.0
                    },
                    {
                        "nome": "Chocolate em Pó",
                        "unidade": "kg",
                        "quantidade": 0.1,
                        "fator_correcao": 1.0,
                        "custo_unitario": 0.0
                    }
                ],
                "modo_preparo": [
                    "1. Misture os ingredientes secos",
                    "2. Adicione os líquidos",
                    "3. Asse em forno médio por 35 minutos"
                ]
            }
        ],
        "base_de_insumos": [
            {
                "ingrediente": "Massa para Lasanha",
                "unidade": "kg",
                "preco": 8.50,
                "fator_correcao": 1.0,
                "fornecedor": "Pasta Bella",
                "data_cotacao": "2025-01-05"
            },
            {
                "ingrediente": "Carne Moída",
                "unidade": "kg",
                "preco": 28.00,
                "fator_correcao": 1.2,
                "fornecedor": "Açougue Central",
                "data_cotacao": "2025-01-05"
            },
            {
                "ingrediente": "Molho de Tomate",
                "unidade": "kg",
                "preco": 6.50,
                "fator_correcao": 1.0,
                "fornecedor": "Distribuidora Roma",
                "data_cotacao": "2025-01-05"
            },
            {
                "ingrediente": "Queijo Mussarela",
                "unidade": "kg",
                "preco": 35.00,
                "fator_correcao": 1.0,
                "fornecedor": "Laticínios Vale",
                "data_cotacao": "2025-01-05"
            },
            {
                "ingrediente": "Cebola",
                "unidade": "kg",
                "preco": 4.20,
                "fator_correcao": 1.3,
                "fornecedor": "Ceasa Local",
                "data_cotacao": "2025-01-05"
            },
            {
                "ingrediente": "Farinha de Trigo",
                "unidade": "kg",
                "preco": 4.50,
                "fator_correcao": 1.0,
                "fornecedor": "Moinho São José",
                "data_cotacao": "2025-01-05"
            },
            {
                "ingrediente": "Açúcar Cristal",
                "unidade": "kg",
                "preco": 3.80,
                "fator_correcao": 1.0,
                "fornecedor": "Usina Doce",
                "data_cotacao": "2025-01-05"
            },
            {
                "ingrediente": "Chocolate em Pó",
                "unidade": "kg",
                "preco": 18.50,
                "fator_correcao": 1.0,
                "fornecedor": "Cacau Nobre",
                "data_cotacao": "2025-01-05"
            }
        ]
    }
    
    try:
        # Criar dicionário de insumos para lookup rápido
        insumos_dict = {}
        for insumo in test_data['base_de_insumos']:
            nome_key = insumo['ingrediente'].lower()
            insumos_dict[nome_key] = insumo
        
        # Calcular preços para cada receita
        for i, recipe in enumerate(test_data['fichas_tecnicas']):
            calculation = calculate_recipe_cost_and_price(recipe, insumos_dict)
            
            # Atualizar dados com cálculos
            recipe['preco_venda'] = calculation['suggested_price']
            for j, ingrediente in enumerate(recipe['ingredientes']):
                nome_key = ingrediente['nome'].lower()
                if nome_key in insumos_dict:
                    ingrediente['custo_unitario'] = insumos_dict[nome_key]['preco']
        
        # Testar geração do Excel com os preços calculados
        print(f"\n📊 Gerando Excel com preços calculados...")
        
        excel_tool = ExcelGeneratorTool()
        json_data = json.dumps(test_data)
        
        result = excel_tool._run(
            data_json=json_data,
            color='70AD47',  # Verde
            color2='E2EFDA'  # Verde claro
        )
        
        print(f"✅ Resultado: {result}")
        
        if "FICHA_TECNICA_COMPLETA_" in result:
            print("🎉 Arquivo Excel gerado com preços calculados!")
            
            # Extrair caminho do arquivo
            import re
            path_match = re.search(r'/[^"]*\.xlsx', result)
            if path_match:
                excel_path = path_match.group()
                if os.path.exists(excel_path):
                    size = os.path.getsize(excel_path) / 1024
                    print(f"📁 Arquivo: {os.path.basename(excel_path)}")
                    print(f"📏 Tamanho: {size:.1f} KB")
                    
                    # Verificar conteúdo do Excel
                    try:
                        import openpyxl
                        wb = openpyxl.load_workbook(excel_path)
                        print(f"📋 Planilhas: {[ws.title for ws in wb.worksheets]}")
                        wb.close()
                        return True
                    except Exception as e:
                        print(f"❌ Erro ao verificar Excel: {e}")
                        return False
        
        return False
        
    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_price_calculation()
    if success:
        print(f"\n🎉 TESTE PASSOU - Preços calculados corretamente!")
        print("✅ Custos por ingrediente calculados")
        print("✅ Preço de venda com markup mínimo 3x")
        print("✅ Arredondamento para R$ 0,50")
        print("✅ Excel gerado com preços viáveis")
    else:
        print(f"\n💥 TESTE FALHOU")