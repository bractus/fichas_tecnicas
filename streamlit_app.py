import streamlit as st
import os
import tempfile
import time
from datetime import datetime
from main import fichas_tecnicas
import yaml
import json
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração da página
st.set_page_config(
    page_title="Gerador de Fichas Técnicas",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

def check_login():
    """Verifica se o usuário está autenticado."""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    return st.session_state.authenticated

def login_form():
    """Exibe o formulário de login."""    
    # Criar container centralizado para o login
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)  # Espaçamento superior
        
        with st.form("login_form"):
            st.markdown("### 🔐 Acesso ao Sistema")
            username = st.text_input("👤 Usuário")
            password = st.text_input("🔑 Senha", type="password")
            
            submit_button = st.form_submit_button("🚀 Entrar", type="primary", use_container_width=True)
            
            if submit_button:
                if username == "admin" and password == "admin":
                    st.session_state.authenticated = True
                    st.success("✅ Login realizado com sucesso!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Credenciais inválidas")

def logout():
    """Faz logout do usuário."""
    st.session_state.authenticated = False
    st.rerun()

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stFileUploader > div > div > div > div {
        border: 2px dashed #1f77b4;
        border-radius: 10px;
    }
    .success-box {
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #28a745;
        background-color: #d4edda;
        color: #155724;
        margin: 1rem 0;
    }
    .login-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .login-form {
        background: white;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        min-width: 400px;
    }
    .stForm > div > div {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        border: 1px solid #e9ecef;
    }
    .logout-btn {
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def save_temp_file(uploaded_file):
    """Salva arquivo temporário e retorna o caminho."""
    # Create a more secure temp file with proper naming
    temp_dir = tempfile.mkdtemp(prefix="fichas_tecnicas_")
    
    # Sanitize filename
    safe_filename = "".join(c for c in uploaded_file.name if c.isalnum() or c in (' ', '.', '_', '-')).rstrip()
    if not safe_filename:
        safe_filename = f"uploaded_file_{int(time.time())}"
    
    temp_path = os.path.join(temp_dir, safe_filename)
    
    try:
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Log the file creation for debugging
        logger.info(f"Temporary file created: {temp_path}")
        logger.info(f"File size: {os.path.getsize(temp_path)} bytes")
        
        return temp_path
    except Exception as e:
        logger.error(f"Error saving temporary file: {e}")
        # Try to clean up on failure
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            os.rmdir(temp_dir)
        except:
            pass
        raise e

def save_text_as_temp_file(text_content, filename="receita_manual.txt"):
    """Salva texto como arquivo temporário."""
    temp_dir = tempfile.mkdtemp(prefix="fichas_tecnicas_text_")
    
    # Sanitize filename
    safe_filename = "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_', '-')).rstrip()
    if not safe_filename:
        safe_filename = f"receita_manual_{int(time.time())}.txt"
    
    temp_path = os.path.join(temp_dir, safe_filename)
    
    try:
        with open(temp_path, "w", encoding='utf-8') as f:
            f.write(text_content)
        
        # Log the file creation for debugging
        logger.info(f"Temporary text file created: {temp_path}")
        logger.info(f"File size: {len(text_content)} characters")
        
        return temp_path
    except Exception as e:
        logger.error(f"Error saving temporary text file: {e}")
        # Try to clean up on failure
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            os.rmdir(temp_dir)
        except:
            pass
        raise e

def update_sources_config(sources_list):
    """Atualiza o arquivo sources.yaml com as novas fontes."""
    sources_config = {
        'sources': sources_list
    }
    
    config_path = "config/sources.yaml"
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(sources_config, f, default_flow_style=False, allow_unicode=True)
    
    return config_path

def cleanup_temp_files(sources_list):
    """Limpa arquivos temporários após o processamento."""
    for source in sources_list:
        try:
            if source and os.path.exists(source) and 'fichas_tecnicas' in source:
                # Remove the file
                os.remove(source)
                # Try to remove the directory if it's empty
                temp_dir = os.path.dirname(source)
                try:
                    os.rmdir(temp_dir)
                except OSError:
                    pass  # Directory not empty or other issue
                logger.info(f"Cleaned up temporary file: {source}")
        except Exception as e:
            logger.warning(f"Could not clean up temporary file {source}: {e}")

def process_recipes(sources_list, color1='4472C4', color2='D9E1F2'):
    """Processa receitas usando os agentes CrewAI."""
    temp_files_created = []
    try:
        # Log the sources being processed
        logger.info(f"Processing {len(sources_list)} sources:")
        for i, source in enumerate(sources_list, 1):
            logger.info(f"  {i}. {source}")
            if '/tmp' in source or 'fichas_tecnicas' in source:
                temp_files_created.append(source)
        
        # Executar processo principal com fontes e cores customizadas
        result = fichas_tecnicas(sources=sources_list, color1=color1, color2=color2)
        
        # Verificar se o resultado é válido
        if isinstance(result, dict) and result.get('success'):
            excel_file = result.get('excel_file')
            if excel_file and os.path.exists(excel_file):
                return True, excel_file, result.get('result')
            else:
                return False, None, "Arquivo Excel não foi encontrado."
        else:
            error_msg = result.get('result', "Erro desconhecido no processamento") if isinstance(result, dict) else str(result)
            return False, None, error_msg
            
    except Exception as e:
        logger.error(f"Erro no processamento: {str(e)}")
        return False, None, str(e)
    finally:
        # Clean up temporary files
        if temp_files_created:
            cleanup_temp_files(temp_files_created)

def main():
    # Verificar autenticação
    if not check_login():
        login_form()
        return
    
    # Header com botão de logout
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown('<h1 class="main-header">📋 Gerador de Fichas Técnicas Culinárias</h1>', unsafe_allow_html=True)
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)  # Espaçamento
        if st.button("🚪 Logout", type="secondary"):
            logout()
    
    # Sidebar com informações
    with st.sidebar:
        st.header("👤 Usuário Logado")
        st.info("🔐 **Usuário autenticado**")
        
        st.header("ℹ️ Informações")
        st.markdown("""
        **Formatos aceitos:**
        - 📄 Arquivos de texto (.txt)
        - 📝 Documentos Word (.docx)
        - 📋 Planilhas Excel (.xlsx)
        - 📄 Arquivos PDF (.pdf)
        - 🌐 URLs de receitas
        
        **Funcionalidades:**
        - ✅ Extração automática de ingredientes
        - ⚖️ Cálculo de fatores de correção
        - 💰 Pesquisa de preços de mercado
        - 📊 Geração de planilha Excel completa
        - 🧮 Cálculo de CMV (Custo da Mercadoria Vendida)
        """)
        
        st.header("🎨 Personalização do Excel")
        st.markdown("**Escolha as cores do Excel:**")
        
        # Cores predefinidas
        predefined_colors = {
            "Azul (Padrão)": {"primary": "#4472C4", "secondary": "#D9E1F2"},
            "Verde": {"primary": "#70AD47", "secondary": "#E2EFDA"},
            "Vermelho": {"primary": "#C5504B", "secondary": "#F2DCDB"},
            "Amarelo": {"primary": "#FFC000", "secondary": "#FFF2CC"},
            "Roxo": {"primary": "#7030A0", "secondary": "#E4DFEC"},
            "Laranja": {"primary": "#D26625", "secondary": "#FCE4D6"},
            "Cinza": {"primary": "#595959", "secondary": "#D9D9D9"},
            "Rosa": {"primary": "#E91E63", "secondary": "#FCE4EC"},
            "Personalizado": None
        }
        
        # Seletor de tema de cores
        color_theme = st.selectbox(
            "Escolha um tema de cores:",
            list(predefined_colors.keys()),
            help="Selecione um tema predefinido ou 'Personalizado' para definir suas próprias cores"
        )
        
        # Se personalizado, mostrar color pickers
        if color_theme == "Personalizado":
            col_color1, col_color2 = st.columns(2)
            with col_color1:
                color1 = st.color_picker(
                    "Cor Principal",
                    value="#4472C4",
                    help="Cor principal para cabeçalhos e destaque"
                )
            with col_color2:
                color2 = st.color_picker(
                    "Cor Secundária", 
                    value="#D9E1F2",
                    help="Cor secundária para fundos e bordas"
                )
            
            # Opção de inserir hex manualmente
            st.markdown("**Ou insira códigos hexadecimais:**")
            col_hex1, col_hex2 = st.columns(2)
            with col_hex1:
                hex_input1 = st.text_input(
                    "Hex Cor Principal",
                    value=color1.lstrip('#'),
                    max_chars=6,
                    help="Digite o código hexadecimal sem # (ex: 4472C4)"
                )
                if len(hex_input1) == 6:
                    try:
                        int(hex_input1, 16)
                        color1 = f"#{hex_input1}"
                    except ValueError:
                        st.warning("Código hex inválido para cor principal")
            
            with col_hex2:
                hex_input2 = st.text_input(
                    "Hex Cor Secundária",
                    value=color2.lstrip('#'),
                    max_chars=6,
                    help="Digite o código hexadecimal sem # (ex: D9E1F2)"
                )
                if len(hex_input2) == 6:
                    try:
                        int(hex_input2, 16)
                        color2 = f"#{hex_input2}"
                    except ValueError:
                        st.warning("Código hex inválido para cor secundária")
        else:
            # Usar cores predefinidas
            color1 = predefined_colors[color_theme]["primary"]
            color2 = predefined_colors[color_theme]["secondary"]
        
        # Preview das cores selecionadas
        st.markdown(f"""
        **Preview das cores - {color_theme}:**
        <div style="display: flex; gap: 15px; margin: 15px 0; align-items: center;">
            <div style="display: flex; flex-direction: column; align-items: center;">
                <div style="width: 60px; height: 40px; background-color: {color1}; border: 2px solid #ccc; border-radius: 8px; margin-bottom: 5px;"></div>
                <small style="color: #666;">Principal</small>
                <small style="color: #666; font-family: monospace;">{color1}</small>
            </div>
            <div style="display: flex; flex-direction: column; align-items: center;">
                <div style="width: 60px; height: 40px; background-color: {color2}; border: 2px solid #ccc; border-radius: 8px; margin-bottom: 5px;"></div>
                <small style="color: #666;">Secundária</small>
                <small style="color: #666; font-family: monospace;">{color2}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Armazenar cores no session_state
        st.session_state.excel_color1 = color1.lstrip('#')
        st.session_state.excel_color2 = color2.lstrip('#')
        
        st.header("🔧 Status do Sistema")
        if os.path.exists(".env"):
            st.success("✅ Configurações carregadas")
        else:
            st.warning("⚠️ Arquivo .env não encontrado")

    # Área principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📤 Entrada de Dados")
        
        # Tabs para diferentes métodos de entrada
        tab1, tab2, tab3 = st.tabs(["📁 Upload de Arquivos", "✍️ Digite a Receita", "🌐 URLs"])
        
        sources_list = []
        
        with tab1:
            st.markdown("**Faça upload de arquivos com receitas:**")
            uploaded_files = st.file_uploader(
                "Escolha os arquivos",
                type=['txt', 'docx', 'xlsx', 'pdf'],
                accept_multiple_files=True,
                help="Selecione um ou mais arquivos contendo receitas culinárias"
            )
            
            if uploaded_files:
                st.success(f"✅ {len(uploaded_files)} arquivo(s) carregado(s)")
                for uploaded_file in uploaded_files:
                    temp_path = save_temp_file(uploaded_file)
                    sources_list.append(temp_path)
                    st.write(f"📄 {uploaded_file.name}")
        
        with tab2:
            st.markdown("**Digite ou cole suas receitas:**")
            recipe_text = st.text_area(
                "Conteúdo da receita",
                height=300,
                placeholder="""
Exemplo:
LASANHA À BOLONHESA

INGREDIENTES:
- 500g massa para lasanha
- 500g carne moída
- 700ml molho de tomate
- 150g cebola
- 10g alho
- 30ml óleo
- 5g sal
- 2g temperos
- 300g queijo mussarela
- 50g queijo parmesão

MODO DE PREPARO:
1. Refogue a cebola e alho no óleo
2. Adicione a carne moída e temperos
3. ...

RENDIMENTO: 6 porções
                """,
                help="Cole aqui o texto da receita com ingredientes e modo de preparo"
            )
            
            if recipe_text.strip():
                temp_path = save_text_as_temp_file(recipe_text)
                sources_list.append(temp_path)
                st.success("✅ Receita digitada pronta para processamento")
        
        with tab3:
            st.markdown("**Adicione URLs de receitas da web:**")
            url_input = st.text_input(
                "URL da receita",
                placeholder="https://example.com/receita-lasanha",
                help="Cole aqui o link de uma receita online"
            )
            
            urls_list = st.text_area(
                "Ou adicione múltiplas URLs (uma por linha):",
                height=150,
                placeholder="""https://tudogostoso.com.br/receita/123-lasanha
https://example.com/receita-strogonoff
https://site.com/receita-bolo""",
                help="Adicione várias URLs, uma em cada linha"
            )
            
            # Processar URLs
            if url_input.strip():
                sources_list.append(url_input.strip())
                st.success("✅ URL adicionada")
            
            if urls_list.strip():
                urls = [url.strip() for url in urls_list.split('\n') if url.strip()]
                sources_list.extend(urls)
                st.success(f"✅ {len(urls)} URL(s) adicionada(s)")
    
    with col2:
        st.subheader("🚀 Processamento")
        
        if sources_list:
            st.markdown("**Fontes prontas para processamento:**")
            for i, source in enumerate(sources_list, 1):
                if source.startswith('http'):
                    st.write(f"{i}. 🌐 {source}")
                elif 'temp' in source:
                    filename = os.path.basename(source)
                    st.write(f"{i}. 📄 {filename}")
                else:
                    st.write(f"{i}. 📁 {source}")
        
        # Botão de processamento
        process_button = st.button(
            "🔄 Gerar Fichas Técnicas",
            type="primary",
            disabled=len(sources_list) == 0,
            help="Clique para iniciar o processamento das receitas"
        )
        
        if process_button and sources_list:
            # Container para o processo
            process_container = st.container()
            
            with process_container:
                # Progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Spinner personalizado
                with st.spinner("🔄 Processando receitas..."):
                    status_text.text("🔍 Iniciando análise das fontes...")
                    progress_bar.progress(10)
                    time.sleep(1)
                    
                    status_text.text("📝 Extraindo receitas e ingredientes...")
                    progress_bar.progress(30)
                    time.sleep(2)
                    
                    status_text.text("⚖️ Consultando fatores de correção...")
                    progress_bar.progress(50)
                    time.sleep(2)
                    
                    status_text.text("💰 Pesquisando preços de mercado...")
                    progress_bar.progress(70)
                    time.sleep(2)
                    
                    status_text.text("📊 Gerando planilha Excel...")
                    progress_bar.progress(90)
                    
                    # Processar receitas com cores personalizadas
                    colors1 = st.session_state.get('excel_color1', '4472C4')
                    colors2 = st.session_state.get('excel_color2', 'D9E1F2')
                    success, excel_file, result = process_recipes(sources_list, colors1, colors2)
                    
                    progress_bar.progress(100)
                
                # Resultado do processamento
                if success:
                    status_text.text("✅ Processamento concluído com sucesso!")
                    
                    # Box de sucesso
                    st.markdown("""
                    <div class="success-box">
                        <h4>🎉 Fichas Técnicas Geradas com Sucesso!</h4>
                        <p>Todas as receitas foram processadas e a planilha Excel está pronta para download.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Informações do arquivo
                    if excel_file and os.path.exists(excel_file):
                        file_size = os.path.getsize(excel_file) / 1024  # KB
                        modification_time = datetime.fromtimestamp(os.path.getmtime(excel_file))
                        
                        st.markdown(f"""
                        **📋 Detalhes do Arquivo:**
                        - 📁 **Nome:** {os.path.basename(excel_file)}
                        - 📏 **Tamanho:** {file_size:.1f} KB
                        - 🕐 **Criado:** {modification_time.strftime('%d/%m/%Y %H:%M:%S')}
                        """)
                        
                        # Botão de download
                        with open(excel_file, 'rb') as f:
                            file_data = f.read()
                        
                        st.download_button(
                            label="📥 Download Planilha Excel",
                            data=file_data,
                            file_name=os.path.basename(excel_file),
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            type="primary"
                        )
                        
                        # Preview das informações
                        with st.expander("👀 Preview das Informações Processadas"):
                            st.code(str(result), language="text")
                    
                else:
                    status_text.text("❌ Erro no processamento!")
                    st.error(f"**Erro:** {result}")
                    
                    st.markdown("""
                    **Possíveis soluções:**
                    - Verifique se as variáveis de ambiente estão configuradas (.env)
                    - Certifique-se de que os arquivos contêm receitas válidas
                    - Verifique sua conexão com a internet para pesquisa de preços
                    - Consulte os logs para mais detalhes do erro
                    """)
        
        elif not sources_list:
            st.info("👆 Adicione pelo menos uma receita para começar o processamento")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        💡 <strong>Dica:</strong> Para melhores resultados, use receitas com ingredientes bem especificados e quantidades claras.
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()