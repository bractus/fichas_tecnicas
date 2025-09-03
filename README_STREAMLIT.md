# 📋 Gerador de Fichas Técnicas - Interface Streamlit

Uma aplicação web moderna para gerar fichas técnicas culinárias automaticamente usando inteligência artificial.

## 🚀 Como Executar

### Método 1: Script Automático
```bash
# Ativar ambiente conda e executar
source activate ai_chefs
python run_streamlit.py
```

### Método 2: Comando Direto
```bash
# Ativar ambiente conda
source activate ai_chefs

# Executar Streamlit
streamlit run streamlit_app.py
```

A aplicação será aberta automaticamente em: **http://localhost:8501**

## 🔐 **Acesso à Aplicação**

A aplicação possui um sistema de login simples para proteger o acesso:

- **Usuário:** `admin`  
- **Senha:** `admin`

### Funcionalidades do Login:
- ✅ Proteção da interface principal
- 🔒 Sessão mantida durante o uso
- 🚪 Botão de logout no cabeçalho
- 🎨 Interface de login estilizada

## 🎯 Funcionalidades

### 📤 **Métodos de Entrada**

1. **📁 Upload de Arquivos**
   - Formatos: `.txt`, `.docx`, `.xlsx`, `.pdf`
   - Suporta múltiplos arquivos
   - Processamento automático

2. **✍️ Digite a Receita**
   - Interface de texto para colar receitas
   - Formato livre, mas estruturado
   - Exemplo fornecido na interface

3. **🌐 URLs de Receitas**
   - Adicionar URLs individuais
   - Lista de múltiplas URLs
   - Processamento web automático

### 🔄 **Processamento Inteligente**

1. **🔍 Análise das Fontes**
   - Extração de conteúdo de arquivos/URLs
   - Validação de fontes

2. **📝 Extração de Receitas**
   - Identificação de ingredientes e quantidades
   - Conversão para unidades padrão (kg/L)
   - Cálculo de porções

3. **⚖️ Fatores de Correção**
   - Consulta automática na base de conhecimento RAG
   - Pesquisa web para ingredientes não encontrados
   - Aplicação de fatores de perda/desperdício

4. **💰 Pesquisa de Preços**
   - Múltiplas consultas por ingrediente
   - Fontes: CEASA, supermercados, atacadistas
   - Preços regionalizados (Teresina/Nordeste)

5. **📊 Geração da Planilha**
   - Excel com múltiplas abas
   - Cálculos automáticos de custos
   - Base consolidada de insumos
   - Cálculo de CMV

### 📋 **Interface de Usuário**

- **Design Responsivo**: Funciona em desktop e mobile
- **Progress Bar**: Acompanhamento visual do progresso
- **Spinner Animado**: Feedback durante processamento
- **Download Direto**: Botão para baixar o Excel
- **Preview**: Visualização dos resultados
- **Tratamento de Erros**: Mensagens claras de erro

## 📊 **Estrutura do Excel Gerado**

### Abas Criadas:
1. **Ficha Técnica por Receita**
   - Nome da preparação
   - Lista de ingredientes com quantidades
   - Fatores de correção aplicados
   - Custos unitários e totais
   - Rendimento e preço de venda
   - Cálculo de CMV

2. **Base de Insumos**
   - Lista consolidada de todos os ingredientes
   - Preços de mercado atualizados
   - Fornecedores sugeridos
   - Data da cotação

### Cálculos Automáticos:
- **Peso Corrigido** = Quantidade × Fator de Correção
- **Custo Total** = Peso Corrigido × Custo Unitário
- **Custo por Porção** = Custo Total ÷ Rendimento
- **CMV** = (Custo por Porção ÷ Preço de Venda) × 100

## 🛠️ **Requisitos Técnicos**

### Dependências Python:
```
streamlit>=1.28.0
pandas>=2.0.0
pyyaml>=6.0
python-dotenv>=1.0.0
crewai>=0.x.x
```

### Variáveis de Ambiente (.env):
```bash
OPENAI_API_KEY=sua_chave_openai
GEMINI_API_KEY=sua_chave_gemini  
SERPER_API_KEY=sua_chave_serper
LANGFUSE_SECRET_KEY=sua_chave_langfuse
LANGFUSE_PUBLIC_KEY=sua_chave_langfuse_publica
EXA_API_KEY=sua_chave_exa
```

## 📝 **Como Usar**

1. **Prepare suas receitas**:
   - Arquivos com receitas estruturadas
   - URLs de sites de culinária
   - Ou digite diretamente na interface

2. **Acesse a aplicação**:
   - Execute o script ou comando Streamlit
   - Abra http://localhost:8501
   - **Faça login com: admin / admin**

3. **Carregue as receitas**:
   - Use uma das três opções de entrada
   - Verifique se as fontes foram carregadas

4. **Processe**:
   - Clique em "🔄 Gerar Fichas Técnicas"
   - Aguarde o processamento (pode levar alguns minutos)

5. **Download**:
   - Clique no botão de download
   - Abra o arquivo Excel gerado

## 🐛 **Solução de Problemas**

### Problemas Comuns:

1. **"No module named 'crewai'"**
   ```bash
   source activate ai_chefs
   pip install crewai
   ```

2. **"Erro no processamento"**
   - Verifique o arquivo `.env`
   - Confirme as chaves de API
   - Teste com uma receita simples primeiro

3. **"Nenhum arquivo Excel gerado"**
   - Verifique os logs na interface
   - Confirme que as receitas têm formato válido
   - Teste a conexão com a internet

4. **Preços zerados**
   - Problema comum: agentes podem não encontrar preços
   - Será corrigido em futuras iterações
   - Verifique a configuração das APIs de busca

### Logs:
- Logs detalhados em `fichas_tecnicas.log`
- Mensagens de erro na interface Streamlit
- Debug no console do navegador (F12)

## 🔮 **Melhorias Futuras**

- [ ] Cache de resultados para receitas já processadas
- [ ] Edição inline de ingredientes e preços
- [ ] Exportação para outros formatos (PDF, CSV)
- [ ] Histórico de processamentos
- [ ] Comparação de custos entre receitas
- [ ] Integração com APIs de supermercados
- [ ] Modo offline com preços pré-cadastrados

## 📞 **Suporte**

Para problemas ou dúvidas:
1. Consulte este README
2. Verifique os logs de erro
3. Teste com receitas simples primeiro
4. Confirme as configurações de ambiente