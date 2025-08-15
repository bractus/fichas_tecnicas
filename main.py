import os
import json
import re
from datetime import datetime
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Carregar variáveis de ambiente
load_dotenv()

# --- Configuração do LLM ---
llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"), temperature=0.0)
web_search = SerperDevTool()

# --- FERRAMENTAS ---

class LocalFileReadTool(BaseTool):
    name: str = "Leitor de Arquivos Locais"
    description: str = "Lê o conteúdo completo de um arquivo de texto local."
    def _run(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return f"Erro: O arquivo '{file_path}' não foi encontrado."

class ExcelGeneratorTool(BaseTool):
    name: str = "Gerador de Planilha de Ficha Técnica e Base de Insumos"
    description: str = "Cria um arquivo Excel a partir de um JSON com 'fichas_tecnicas' e 'base_de_insumos'."

    def _run(self, dados_completos: dict) -> str:
        output_filename = "FICHA_TECNICA_COMPLETA.xlsx"
        workbook = openpyxl.Workbook()
        workbook.remove(workbook.active)

        fichas_tecnicas = dados_completos.get("fichas_tecnicas", [])
        base_de_insumos = dados_completos.get("base_de_insumos", [])

        # Estilos comuns
        font_titulo = Font(name='Arial', size=14, bold=True, color='FFFFFF')
        fill_titulo = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
        align_center = Alignment(horizontal='center', vertical='center')
        font_subtitulo = Font(name='Arial', size=11, bold=True)
        font_bold = Font(name='Arial', size=10, bold=True)
        fill_header_tabela = PatternFill(start_color='D9E1F2', end_color='D9E1F2', fill_type='solid')
        border_thin = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))

        # --- PARTE 1: Gerar abas para cada Ficha Técnica ---
        for ficha in fichas_tecnicas:
            sheet_name = ficha.get("nome_preparacao", "Ficha")[:31]
            sheet = workbook.create_sheet(title=sheet_name)

            # A. Cabeçalho Principal e Informações
            sheet.merge_cells('A1:E1')
            cell = sheet['A1']
            cell.value = "FICHA TÉCNICA DE PREPARAÇÃO"
            cell.font = font_titulo
            cell.fill = fill_titulo
            cell.alignment = align_center
            sheet.row_dimensions[1].height = 25
            sheet['A3'] = "NOME DA PREPARAÇÃO:"
            sheet['A3'].font = font_subtitulo
            sheet.merge_cells('B3:E3')
            sheet['B3'] = ficha.get("nome_preparacao", "").upper()
            sheet['B3'].font = font_subtitulo
            sheet['A4'] = "DEPARTAMENTO:"
            sheet['A4'].font = font_bold
            sheet['B4'] = "COZINHA"

            # B. Tabela de Ingredientes
            headers_tabela = ["INGREDIENTES", "UNIDADE", "QUANTIDADE", "CUSTO UNITÁRIO", "CUSTO TOTAL"]
            for col_num, header_text in enumerate(headers_tabela, 1):
                cell = sheet.cell(row=7, column=col_num, value=header_text)
                cell.font = font_bold; cell.fill = fill_header_tabela; cell.border = border_thin
            
            linha_atual = 8
            for ingrediente in ficha.get("ingredientes", []):
                sheet.cell(row=linha_atual, column=1, value=ingrediente[0])
                sheet.cell(row=linha_atual, column=2, value=ingrediente[1])
                sheet.cell(row=linha_atual, column=3, value=ingrediente[2])
                sheet.cell(row=linha_atual, column=4, value=ingrediente[3])
                sheet.cell(row=linha_atual, column=5, value=f'=C{linha_atual}*D{linha_atual}')
                for col in range(1, 6):
                    cell = sheet.cell(row=linha_atual, column=col)
                    cell.border = border_thin
                    if col == 3: cell.number_format = '0.000'
                    if col >= 4: cell.number_format = 'R$ #,##0.00'
                linha_atual += 1

            # C. Seção de Totais e Fórmulas
            primeira_linha_dados = 8
            ultima_linha_dados = linha_atual - 1
            linha_totais = linha_atual + 1
            linha_seguinte = linha_totais # Inicia a contagem para a proxima seção

            if ultima_linha_dados >= primeira_linha_dados:
                # Custo Total da Preparação
                sheet.cell(row=linha_totais, column=1, value="CUSTO TOTAL DA PREPARAÇÃO").font = font_bold
                custo_total_soma_cell = sheet.cell(row=linha_totais, column=5)
                custo_total_soma_cell.value = f'=SUM(E{primeira_linha_dados}:E{ultima_linha_dados})'
                custo_total_soma_cell.font = font_bold; custo_total_soma_cell.number_format = 'R$ #,##0.00'; custo_total_soma_cell.border = border_thin

                # Peso Total da Preparação
                sheet.cell(row=linha_totais + 1, column=1, value="PESO TOTAL DA PREPARAÇÃO (KG)").font = font_bold
                peso_total_soma_cell = sheet.cell(row=linha_totais + 1, column=3)
                peso_total_soma_cell.value = f'=SUM(C{primeira_linha_dados}:C{ultima_linha_dados})'
                peso_total_soma_cell.font = font_bold; peso_total_soma_cell.number_format = '0.000'; peso_total_soma_cell.border = border_thin

                # Custo por Kg
                sheet.cell(row=linha_totais + 2, column=1, value="CUSTO POR KG").font = font_bold
                custo_kg_cell = sheet.cell(row=linha_totais + 2, column=5)
                custo_kg_cell.value = f'={custo_total_soma_cell.coordinate}/{peso_total_soma_cell.coordinate}'
                custo_kg_cell.font = font_bold; custo_kg_cell.number_format = 'R$ #,##0.00'; custo_kg_cell.border = border_thin
                
                linha_seguinte = linha_totais + 3

                # D. Seção de Rendimento e Preço
                if "rendimento_porcoes" in ficha:
                    linha_adicionais = linha_seguinte + 1
                    rendimento = ficha["rendimento_porcoes"]
                    sheet.cell(row=linha_adicionais, column=1, value="RENDIMENTO (Nº DE PORÇÕES)").font = font_bold
                    sheet.cell(row=linha_adicionais, column=3, value=rendimento).font = font_bold
                    
                    sheet.cell(row=linha_adicionais + 1, column=1, value="PESO POR PORÇÃO (KG)").font = font_bold
                    peso_porcao_cell = sheet.cell(row=linha_adicionais + 1, column=3)
                    peso_porcao_cell.value = f'={peso_total_soma_cell.coordinate}/{rendimento}'
                    peso_porcao_cell.font = font_bold; peso_porcao_cell.number_format = '0.000'
                    
                    sheet.cell(row=linha_adicionais + 2, column=1, value="CUSTO POR PORÇÃO").font = font_bold
                    custo_porcao_cell = sheet.cell(row=linha_adicionais + 2, column=5)
                    custo_porcao_cell.value = f'={custo_total_soma_cell.coordinate}/{rendimento}'
                    custo_porcao_cell.font = font_bold; custo_porcao_cell.number_format = 'R$ #,##0.00'

                    if "preco_venda" in ficha:
                        preco_venda = ficha["preco_venda"]
                        sheet.cell(row=linha_adicionais + 3, column=1, value="PREÇO DE VENDA").font = font_bold
                        preco_venda_cell = sheet.cell(row=linha_adicionais + 3, column=5, value=preco_venda)
                        preco_venda_cell.font = font_bold; preco_venda_cell.number_format = 'R$ #,##0.00'

                        sheet.cell(row=linha_adicionais + 4, column=1, value="CMV (%)").font = font_bold
                        cmv_cell = sheet.cell(row=linha_adicionais + 4, column=5)
                        cmv_cell.value = f'={custo_porcao_cell.coordinate}/{preco_venda_cell.coordinate}'
                        cmv_cell.font = font_bold; cmv_cell.number_format = '0.00%'

                    linha_seguinte = linha_adicionais + 5

            # E. Seção Modo de Preparo
            if "modo_preparo" in ficha:
                linha_preparo = linha_seguinte + 2
                cell_titulo_preparo = sheet.cell(row=linha_preparo, column=1, value="MODO DE PREPARO")
                cell_titulo_preparo.font = font_subtitulo
                sheet.merge_cells(f'A{linha_preparo}:E{linha_preparo}')
                for i, passo in enumerate(ficha["modo_preparo"], 1):
                    passo_cell = sheet.cell(row=linha_preparo + i, column=1, value=passo)
                    passo_cell.alignment = Alignment(wrap_text=True, vertical='top')
                    sheet.merge_cells(f'A{linha_preparo + i}:E{linha_preparo + i}')

            # F. Ajuste da Largura das Colunas
            sheet.column_dimensions['A'].width = 35; sheet.column_dimensions['B'].width = 12
            sheet.column_dimensions['C'].width = 15; sheet.column_dimensions['D'].width = 18
            sheet.column_dimensions['E'].width = 18

        # --- PARTE 2: Gerar a aba "Base de Insumos" ---
        if base_de_insumos:
            sheet_base = workbook.create_sheet(title="Base de Insumos")
            headers_base = ["INGREDIENTE", "UNIDADE", "PREÇO UNITÁRIO", "FORNECEDOR", "DATA DE COTAÇÃO"]
            for col, (header, width) in enumerate(zip(headers_base, [35, 15, 18, 25, 20]), 1):
                cell = sheet_base.cell(row=1, column=col, value=header)
                cell.font = font_bold; cell.fill = fill_header_tabela; cell.border = border_thin
                sheet_base.column_dimensions[get_column_letter(col)].width = width
            
            for row, item in enumerate(base_de_insumos, 2):
                sheet_base.cell(row=row, column=1, value=item.get("ingrediente"))
                sheet_base.cell(row=row, column=2, value=item.get("unidade"))
                preco_cell = sheet_base.cell(row=row, column=3, value=item.get("preco"))
                preco_cell.number_format = 'R$ #,##0.00'
                sheet_base.cell(row=row, column=4, value=item.get("fornecedor"))
                sheet_base.cell(row=row, column=5, value=item.get("data_cotacao"))
                for col in range(1, 6):
                    sheet_base.cell(row=row, column=col).border = border_thin

        workbook.save(output_filename)
        return f"Arquivo Excel '{output_filename}' criado com sucesso."

# --- Agentes e Tarefas (O resto do código permanece o mesmo) ---

# 1. Ferramentas
file_reader_tool = LocalFileReadTool()
excel_generator_tool = ExcelGeneratorTool()

# 2. Agentes
file_reader_agent = Agent(role='Leitor de Arquivo', goal='Ler o conteúdo de um arquivo de texto', backstory='Especialista em ler arquivos de texto.', tools=[file_reader_tool], verbose=True, llm=llm)
data_extractor_agent = Agent(role='Analista de Dados Culinários', goal='Analisar texto de receita, buscar preços online e extrair dados em JSON.', backstory='Mestre em NLP, capaz de extrair múltiplas fichas e encontrar informações na web.', tools=[web_search], verbose=True, llm=llm)
excel_writer_agent = Agent(role='Gerador de Planilhas', goal='Receber um JSON e criar um arquivo Excel formatado com múltiplas abas.', backstory='Especialista em automação de planilhas que transforma dados brutos em relatórios Excel.', tools=[excel_generator_tool], verbose=True, llm=llm)

# 3. Tarefas
task_read_file = Task(agent=file_reader_agent, description='Leia o conteúdo do arquivo localizado em "{recipe_file_path}".', expected_output='O texto completo da receita.')

task_extract_data = Task(
    agent=data_extractor_agent,
    description=f'''Analise o texto da receita e crie um ÚNICO objeto JSON com DUAS chaves: "fichas_tecnicas" e "base_de_insumos".

    IMPORTANTE: Para CADA ingrediente, se o preço não for fornecido, **use a busca na web para encontrar um preço de mercado realista em Reais (BRL)**.

    1.  **Chave "fichas_tecnicas"**: Uma LISTA de dicionários. Cada dicionário é uma receita com a estrutura:
        -   `nome_preparacao`: (string) O nome da receita.
        -   `rendimento_porcoes`: (number) O número de porções que a receita rende.
        -   `preco_venda`: (number) O preço de venda da porção.
        -   `ingredientes`: Uma LISTA de listas `[NOME, UNIDADE, QUANTIDADE, CUSTO_UNITARIO]`.
        -   `modo_preparo`: (Opcional) Uma LISTA de strings com os passos.

    2.  **Chave "base_de_insumos"**: Uma LISTA de dicionários. Cada dicionário é um insumo com a estrutura:
        -   `ingrediente`, `unidade`, `preco`, `fornecedor`, `data_cotacao` (hoje é {datetime.now().strftime('%Y-%m-%d')}).

    Exemplo de formato de saída esperado:
    ```json
    {{
        "fichas_tecnicas": [
            {{
                "nome_preparacao": "FRANGO GRELHADO COM ARROZ",
                "rendimento_porcoes": 1,
                "preco_venda": 79.90,
                "ingredientes": [
                    ["Frango (sassami)", "Kg", 0.180, 21.90],
                    ["Arroz", "Kg", 0.150, 8.50]
                ],
                "modo_preparo": ["1. Grelhe o frango.", "2. Cozinhe o arroz."]
            }}
        ],
        "base_de_insumos": [
            {{
                "ingrediente": "Frango (sassami)", "unidade": "Kg", "preco": 21.90,
                "fornecedor": "Açougue Local", "data_cotacao": "{datetime.now().strftime('%Y-%m-%d')}"
            }},
            {{
                "ingrediente": "Arroz", "unidade": "Kg", "preco": 8.50,
                "fornecedor": "Supermercado Pão de Açúcar", "data_cotacao": "{datetime.now().strftime('%Y-%m-%d')}"
            }}
        ]
    }}
    ```
    ''',
    context=[task_read_file],
    expected_output='Um JSON único com as chaves "fichas_tecnicas" e "base_de_insumos", com preços pesquisados na web.'
)

task_generate_excel = Task(
    agent=excel_writer_agent,
    description='''Pegue o JSON completo da tarefa anterior. Use a ferramenta "Gerador de Planilha de Ficha Técnica e Base de Insumos" para criar o arquivo Excel final.''',
    context=[task_extract_data],
    expected_output='Mensagem de confirmação da criação do arquivo Excel.'
)

# 4. Montagem da Crew
final_crew = Crew(
    agents=[file_reader_agent, data_extractor_agent, excel_writer_agent],
    tasks=[task_read_file, task_extract_data, task_generate_excel],
    process=Process.sequential, memory=False, verbose=True
)

# --- Execução ---
if __name__ == '__main__':
    # try:
    #     with open("receita.txt", "w", encoding="utf-8") as f:
    #         f.write("""
    #         FICHA TÉCNICA: FRANGO GRELHADO COM ARROZ

    #         Rendimento (Nº de Porções): 1
    #         Preço de Venda: 79.90

    #         Ingredientes:
    #         - Frango sassami: 180g
    #         - Arroz: 150g
    #         - Azeite: 10ml
    #         - Sal: a gosto (considere 5g)

    #         Modo de Preparo:
    #         1. Tempere o frango com sal.
    #         2. Aqueça o azeite em uma frigideira e grelhe o frango até dourar.
    #         3. Cozinhe o arroz em água fervente.
    #         4. Sirva o frango ao lado do arroz.
    #         """)
    # except Exception as e:
    #     print(f"Não foi possível criar o arquivo de receita de exemplo: {e}")

    inputs = {'recipe_file_path': 'receita.txt'}
    print("🚀 Iniciando o processo completo de geração da Ficha Técnica...")
    result = final_crew.kickoff(inputs=inputs)

    print("\n\n✅ Processo Finalizado!")
    print("--------------------------------------------------")
    print("Resultado da Execução:", result, sep='\n')
    print("--------------------------------------------------")