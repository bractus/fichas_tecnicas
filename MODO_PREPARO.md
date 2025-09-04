# 📝 Modo de Preparo nas Fichas Técnicas

O sistema agora extrai e processa **completa e automaticamente** o modo de preparo das receitas.

## 🔧 **Funcionalidade Implementada**

### ✅ **Extração Obrigatória com Busca Web**
- **OBRIGATÓRIO**: Cada receita DEVE ter campo modo_preparo processado
- **Detecção inteligente**: Localiza automaticamente a seção de modo de preparo nas receitas
- **Busca web como fallback**: Se não encontrado na fonte, busca na web por "receita [nome] modo preparo"
- **Formatação padronizada**: Converte para lista numerada (1. Passo 1, 2. Passo 2, etc.)
- **Preservação de detalhes**: Mantém tempos, temperaturas e técnicas culinárias
- **Vazio se necessário**: Campo pode ficar vazio [] apenas se não encontrado em lugar nenhum

### 📊 **Estrutura de Dados**
```json
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
```

### 📋 **Geração no Excel**
- **Seção dedicada**: Uma seção "MODO DE PREPARO" em cada ficha técnica
- **Formatação profissional**: Passos numerados com quebra de linha automática
- **Layout otimizado**: Células mescladas para melhor visualização
- **Altura automática**: Ajuste da altura das linhas conforme o conteúdo

## 🎯 **Benefícios**

### ✨ **Para Usuários**
- **Fichas completas**: Inclui todos os aspectos da receita (ingredientes + preparo)
- **Padronização**: Formato consistente em todas as fichas
- **Profissionalismo**: Layout adequado para uso comercial
- **Facilidade**: Nenhuma configuração adicional necessária

### 🏭 **Para Cozinhas Comerciais**
- **Treinamento**: Facilita a capacitação de funcionários
- **Consistência**: Garante que o preparo seja sempre igual
- **Qualidade**: Mantém os padrões estabelecidos
- **Eficiência**: Reduz tempo de consulta e dúvidas

## 🔄 **Fluxo de Processamento**

1. **Leitura**: Sistema lê arquivos/URLs com receitas
2. **Extração Primária**: IA identifica seção de modo de preparo na fonte
3. **Busca Web (se necessário)**: Se não encontrado, busca na web:
   - "receita [nome] modo preparo passo a passo"
   - "[nome] receita como fazer"
4. **Formatação**: Converte para lista numerada padronizada
5. **Validação**: Verifica se está completo e coerente
6. **Consolidação**: Integra com ingredientes e preços
7. **Excel**: Gera planilha com seção dedicada ao modo de preparo

### 🔍 **Prioridade de Busca**
1. **🏅 PRIMÁRIO**: Conteúdo da fonte original (arquivo/URL)
2. **🔎 FALLBACK**: Busca web automática para receitas incompletas
3. **📝 FINAL**: Lista vazia [] se nenhuma fonte disponível

## 📖 **Exemplos de Processamento**

### ✅ Caso 1: Encontrado na Fonte
**Entrada no arquivo:**
```
MODO DE PREPARO:
Refogue a cebola no óleo.
Adicione a carne e tempere.
Acrescente o molho de tomate.
```
**Resultado:** Extração direta da fonte

### ✅ Caso 2: Lista Já Numerada
**Entrada no arquivo:**
```
PREPARO:
1. Aqueça o óleo em uma panela
2. Doure a cebola por 3 minutos
3. Junte a carne moída
```
**Resultado:** Mantém numeração existente

### 🔍 Caso 3: Não Encontrado na Fonte → Busca Web
**Entrada no arquivo:**
```
LASANHA À BOLONHESA
Ingredientes: massa, carne, queijo...
(sem modo de preparo)
```
**Ação:** Sistema busca automaticamente "receita lasanha bolonhesa modo preparo"
**Resultado:** Extrai modo de preparo dos resultados da web

### ⚠️ Caso 4: Não Encontrado em Lugar Nenhum
**Entrada no arquivo:**
```
RECEITA OBSCURA
Ingredientes: ingrediente1, ingrediente2...
```
**Ação:** Busca web não retorna resultados úteis
**Resultado:** `"modo_preparo": []`

## 📊 **Saída Padronizada**

Todos os formatos acima são convertidos para:
```json
"modo_preparo": [
  "1. Refogue a cebola e alho no óleo até dourar",
  "2. Adicione a carne moída e tempere com sal",
  "3. Acrescente o molho de tomate e cozinhe por 15 minutos"
]
```

## 🔧 **Configuração**

**Nenhuma configuração é necessária!** O sistema automaticamente:
- ✅ Detecta seções de modo de preparo
- ✅ Formata em lista numerada
- ✅ Integra ao Excel gerado
- ✅ Preserva todos os detalhes importantes

---

*O modo de preparo é agora parte integral das fichas técnicas, proporcionando receitas completas e profissionais.*