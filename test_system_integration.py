#!/usr/bin/env python3
"""
Teste de integração completo do sistema para verificar se não está inventando receitas
"""

import sys
import os
sys.path.append('/Users/cairorocha/Documents/fichas_tecnicas')

from main import fichas_tecnicas
import tempfile

def test_system_integration():
    """Testa o sistema completo com arquivo real para verificar se não inventa receitas"""
    
    print("🧪 Testando sistema completo (sem inventar receitas)...")
    
    # Usar o arquivo de receita existente
    test_sources = ["/Users/cairorocha/Documents/fichas_tecnicas/input_examples/receita1.txt"]
    
    print(f"📁 Usando fontes: {test_sources}")
    
    # Verificar se arquivo existe
    for source in test_sources:
        if not os.path.exists(source):
            print(f"❌ ERRO: Fonte não existe: {source}")
            return False
    
    try:
        # Executar o sistema com cores padrão
        print("🚀 Executando sistema...")
        result = fichas_tecnicas(
            sources=test_sources, 
            color1='4472C4', 
            color2='D9E1F2'
        )
        
        print(f"✅ Sistema executado com sucesso!")
        print(f"📄 Resultado: {result}")
        
        # Verificar se foi gerado arquivo
        output_dir = "/Users/cairorocha/Documents/fichas_tecnicas/output"
        if os.path.exists(output_dir):
            excel_files = [f for f in os.listdir(output_dir) if f.endswith('.xlsx')]
            if excel_files:
                latest_file = max([os.path.join(output_dir, f) for f in excel_files], key=os.path.getmtime)
                print(f"📊 Arquivo Excel gerado: {latest_file}")
                
                # Verificar tamanho do arquivo
                size = os.path.getsize(latest_file) / 1024
                print(f"📁 Tamanho: {size:.1f} KB")
                
                return True
            else:
                print("❌ ERRO: Nenhum arquivo Excel gerado")
                return False
        else:
            print("❌ ERRO: Diretório de saída não existe")
            return False
            
    except Exception as e:
        print(f"❌ ERRO durante execução: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_system_integration()
    if success:
        print(f"\n🎉 TESTE PASSOU - Sistema está funcionando sem inventar receitas!")
    else:
        print(f"\n💥 TESTE FALHOU - Há problemas no sistema")