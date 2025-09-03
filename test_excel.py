#!/usr/bin/env python3
"""
Teste para verificar se o generate_excel.py gera arquivos Excel válidos
"""

import json
import os
from tools.generate_excel import ExcelGeneratorTool

def test_excel_generation():
    """Testa a geração de arquivo Excel com dados de exemplo"""
    
    # Dados de teste
    test_data = {
        "fichas_tecnicas": [
            {
                "nome_preparacao": "Bolo de Chocolate",
                "rendimento_porcoes": 10,
                "preco_venda": 25.00,
                "ingredientes": [
                    {
                        "nome": "Farinha de Trigo",
                        "unidade": "kg",
                        "quantidade": 0.5,
                        "fator_correcao": 1.0,
                        "custo_unitario": 4.50
                    },
                    {
                        "nome": "Açúcar",
                        "unidade": "kg", 
                        "quantidade": 0.3,
                        "fator_correcao": 1.0,
                        "custo_unitario": 3.20
                    },
                    {
                        "nome": "Chocolate em Pó",
                        "unidade": "kg",
                        "quantidade": 0.2,
                        "fator_correcao": 1.0,
                        "custo_unitario": 15.00
                    }
                ],
                "modo_preparo": [
                    "Misture os ingredientes secos",
                    "Adicione os líquidos gradualmente",
                    "Asse em forno pré-aquecido a 180°C por 40 minutos"
                ]
            }
        ],
        "base_de_insumos": [
            {
                "ingrediente": "Farinha de Trigo",
                "unidade": "kg",
                "preco": 4.50,
                "fator_correcao": 1.0,
                "fornecedor": "Fornecedor A",
                "data_cotacao": "2024-01-15"
            },
            {
                "ingrediente": "Açúcar",
                "unidade": "kg",
                "preco": 3.20,
                "fator_correcao": 1.0,
                "fornecedor": "Fornecedor B", 
                "data_cotacao": "2024-01-15"
            },
            {
                "ingrediente": "Chocolate em Pó",
                "unidade": "kg",
                "preco": 15.00,
                "fator_correcao": 1.0,
                "fornecedor": "Fornecedor C",
                "data_cotacao": "2024-01-15"
            }
        ]
    }
    
    # Converter para JSON string
    json_data = json.dumps(test_data, ensure_ascii=False, indent=2)
    
    # Criar instância da ferramenta
    excel_tool = ExcelGeneratorTool()
    
    print("🧪 Testando geração de arquivo Excel...")
    print(f"📊 Dados de teste: {len(test_data['fichas_tecnicas'])} fichas, {len(test_data['base_de_insumos'])} insumos")
    
    # Executar a ferramenta
    resultado = excel_tool._run(json_data)
    
    print(f"📄 Resultado: {resultado}")
    
    # Verificar se o arquivo foi criado
    output_dir = "/Users/cairorocha/Documents/fichas_tecnicas1/output"
    if os.path.exists(output_dir):
        excel_files = [f for f in os.listdir(output_dir) if f.endswith('.xlsx')]
        if excel_files:
            print(f"✅ Arquivos Excel encontrados no diretório output:")
            for file in excel_files:
                filepath = os.path.join(output_dir, file)
                size = os.path.getsize(filepath) / 1024  # KB
                print(f"   📁 {file} ({size:.1f} KB)")
                
                # Tentar abrir o arquivo para verificar se é válido
                try:
                    import openpyxl
                    wb = openpyxl.load_workbook(filepath)
                    print(f"   📋 Planilhas: {[ws.title for ws in wb.worksheets]}")
                    wb.close()
                    print(f"   ✅ Arquivo válido!")
                except Exception as e:
                    print(f"   ❌ Erro ao abrir arquivo: {e}")
        else:
            print("❌ Nenhum arquivo Excel encontrado no diretório output")
    else:
        print("❌ Diretório output não existe")
    
    return resultado

if __name__ == "__main__":
    test_excel_generation()