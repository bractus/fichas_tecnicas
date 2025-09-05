#!/usr/bin/env python3
"""
Teste do FileReader para verificar se está lendo corretamente os arquivos fornecidos
"""

import sys
import os
sys.path.append('/Users/cairorocha/Documents/fichas_tecnicas')

from tools.file_reader import MultiFormatFileReader

def test_file_reader():
    """Testa se o file reader está lendo corretamente os arquivos fornecidos"""
    
    print("🧪 Testando MultiFormatFileReader...")
    
    # Instanciar a ferramenta
    file_reader = MultiFormatFileReader()
    
    # Arquivo de teste
    test_file = "/Users/cairorocha/Documents/fichas_tecnicas/input_examples/receita1.txt"
    
    print(f"📁 Testando arquivo: {test_file}")
    
    # Verificar se arquivo existe
    if not os.path.exists(test_file):
        print(f"❌ ERRO: Arquivo não existe: {test_file}")
        return False
    
    try:
        # Ler o arquivo usando a ferramenta
        result = file_reader._run(test_file)
        
        print(f"\n📄 CONTEÚDO LIDO:")
        print("=" * 50)
        print(result)
        print("=" * 50)
        
        # Verificar se o conteúdo foi lido corretamente
        if result.startswith("ERRO"):
            print(f"❌ ERRO ao ler arquivo: {result}")
            return False
        
        # Verificar se contém ingredientes esperados
        expected_ingredients = ["lulas", "azeite", "alho", "tomate", "arroz", "camarão"]
        content_lower = result.lower()
        
        missing_ingredients = []
        for ingredient in expected_ingredients:
            if ingredient not in content_lower:
                missing_ingredients.append(ingredient)
        
        if missing_ingredients:
            print(f"⚠️  AVISO: Ingredientes esperados não encontrados: {missing_ingredients}")
        else:
            print("✅ Todos os ingredientes esperados foram encontrados no conteúdo")
        
        # Verificar se não está vazio
        if len(result.strip()) == 0:
            print("❌ ERRO: Conteúdo lido está vazio")
            return False
        
        print(f"📊 ESTATÍSTICAS:")
        print(f"   - Tamanho do conteúdo: {len(result)} caracteres")
        print(f"   - Número de linhas: {len(result.splitlines())}")
        print(f"   - Contém 'Ingredientes': {'Ingredientes' in result}")
        
        # Verificar se há informações estruturadas
        lines = result.splitlines()
        ingredient_lines = [line for line in lines if line.strip() and not line.strip().lower() == 'ingredientes']
        
        print(f"   - Linhas de ingredientes: {len(ingredient_lines)}")
        
        if len(ingredient_lines) > 0:
            print("✅ Arquivo lido corretamente!")
            print(f"\n🔍 PRIMEIRAS LINHAS DE INGREDIENTES:")
            for i, line in enumerate(ingredient_lines[:5], 1):
                print(f"   {i}. {line.strip()}")
            return True
        else:
            print("❌ ERRO: Nenhuma linha de ingrediente encontrada")
            return False
            
    except Exception as e:
        print(f"❌ ERRO durante teste: {e}")
        return False

if __name__ == "__main__":
    success = test_file_reader()
    if success:
        print(f"\n🎉 TESTE PASSOU - FileReader está funcionando corretamente!")
    else:
        print(f"\n💥 TESTE FALHOU - Há problemas no FileReader")