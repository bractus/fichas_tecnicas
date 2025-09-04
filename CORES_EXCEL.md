# 🎨 Personalização de Cores do Excel

A interface agora permite personalizar as cores das planilhas Excel geradas com diversas opções:

## 📋 Temas Predefinidos

Escolha entre 8 temas de cores predefinidos:

- **🔵 Azul (Padrão)**: Principal `#4472C4`, Secundária `#D9E1F2`
- **🟢 Verde**: Principal `#70AD47`, Secundária `#E2EFDA`
- **🔴 Vermelho**: Principal `#C5504B`, Secundária `#F2DCDB`
- **🟡 Amarelo**: Principal `#FFC000`, Secundária `#FFF2CC`
- **🟣 Roxo**: Principal `#7030A0`, Secundária `#E4DFEC`
- **🟠 Laranja**: Principal `#D26625`, Secundária `#FCE4D6`
- **⚫ Cinza**: Principal `#595959`, Secundária `#D9D9D9`
- **🩷 Rosa**: Principal `#E91E63`, Secundária `#FCE4EC`

## 🎨 Cores Personalizadas

### Opção 1: Color Picker Visual
- Use o seletor de cores visual para escolher qualquer cor
- Interface intuitiva com preview em tempo real

### Opção 2: Código Hexadecimal
- Digite diretamente o código hexadecimal (sem #)
- Validação automática dos códigos inseridos
- Formato: `4472C4` (6 caracteres)

## 👁️ Preview das Cores

- Visualização instantânea das cores selecionadas
- Exibição dos códigos hexadecimais
- Preview antes de gerar o Excel

## 🔧 Como Usar

1. **Via Interface Streamlit:**
   ```bash
   streamlit run streamlit_app.py
   ```
   - Acesse a seção "🎨 Personalização do Excel" na barra lateral
   - Escolha um tema predefinido ou selecione "Personalizado"
   - Para cores personalizadas: use o color picker ou digite o código hex

2. **Via Código Python:**
   ```python
   from main import fichas_tecnicas
   
   # Usando cores padrão
   result = fichas_tecnicas(sources=['receita.txt'])
   
   # Usando cores personalizadas
   result = fichas_tecnicas(
       sources=['receita.txt'],
       color1='70AD47',  # Verde
       color2='E2EFDA'   # Verde claro
   )
   ```

## 📊 Aplicação no Excel

As cores são aplicadas em:
- **Cor Principal**: Cabeçalhos, títulos, bordas principais
- **Cor Secundária**: Fundos alternados, bordas secundárias, destaque de células

## ✨ Benefícios

- **Identidade Visual**: Personalize de acordo com sua marca
- **Facilidade de Leitura**: Escolha combinações que facilitam a leitura
- **Flexibilidade**: Desde temas prontos até cores totalmente customizadas
- **Preview**: Veja exatamente como ficará antes de gerar

---

*As cores padrão (Azul) são otimizadas para melhor contraste e legibilidade.*