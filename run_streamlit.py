#!/usr/bin/env python3
"""
Script para executar a aplicação Streamlit com o ambiente correto.
"""
import os
import sys
import subprocess

def run_streamlit():
    """Executa a aplicação Streamlit."""
    try:
        # Mudar para o diretório do projeto
        project_dir = "/Users/cairorocha/Documents/fichas_tecnicas"
        os.chdir(project_dir)
        
        print(f"📂 Executando a partir de: {project_dir}")
        print(f"🐍 Python: {sys.executable}")
        print("🚀 Iniciando aplicação Streamlit...")
        
        # Executar Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "streamlit_app.py",
            "--server.port=8501",
            "--server.address=localhost",
            "--browser.gatherUsageStats=false"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Aplicação encerrada pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar Streamlit: {e}")

if __name__ == "__main__":
    run_streamlit()