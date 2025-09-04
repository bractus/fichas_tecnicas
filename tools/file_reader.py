from crewai.tools import BaseTool
import os
import logging
from pathlib import Path
from docx import Document
import PyPDF2
import pandas as pd
from typing import Optional

logger = logging.getLogger(__name__)


class MultiFormatFileReader(BaseTool):
    name: str = "Leitor Multi-formato"
    description: str = "Reads TXT, DOCX, PDF, XLSX files. For URLs, use WebScrapingTool."
    max_file_size: int = 50 * 1024 * 1024  # 50MB default

    def _run(self, source: str) -> str:
        try:
            # URLs não são suportadas - usar WebScrapingTool
            if source.startswith(('http://', 'https://')):
                return "ERRO: URLs não são suportadas. Use a WebScrapingTool para fazer scraping de páginas web."
            
            # Validar caminho do arquivo
            if not self._validate_file_path(source):
                return f"ERRO: Caminho de arquivo inválido ou inseguro: '{source}'"
            
            # Verificar se o arquivo existe
            if not os.path.exists(source):
                logger.error(f"File not found: {source}")
                return f"ERRO: O arquivo '{source}' não foi encontrado."
            
            # Verificar tamanho do arquivo
            if not self._check_file_size(source):
                return f"ERRO: Arquivo '{source}' é muito grande (máximo {self.max_file_size // (1024*1024)}MB)"
            
            file_path = Path(source)
            extension = file_path.suffix.lower()
            
            logger.info(f"Reading file: {source} (type: {extension})")
            
            if extension == '.txt':
                return self._read_txt(source)
            elif extension == '.docx':
                return self._read_docx(source)
            elif extension == '.pdf':
                return self._read_pdf(source)
            elif extension in ['.xlsx', '.xls']:
                return self._read_excel(source)
            else:
                logger.warning(f"Unsupported file format: {extension}")
                return f"ERRO: Formato de arquivo não suportado: {extension}. Formatos suportados: .txt, .docx, .pdf, .xlsx, .xls"
                
        except Exception as e:
            logger.error(f"Error reading source '{source}': {e}")
            return f"ERRO ao ler fonte '{source}': {e}"
    
    def _validate_file_path(self, file_path: str) -> bool:
        """Validate file path for security."""
        try:
            # Check for empty or None path
            if not file_path or not file_path.strip():
                return False
            
            file_path = file_path.strip()
            
            # Resolve to absolute path
            abs_path = os.path.abspath(file_path)
            original_cwd = os.getcwd()
            
            # Check for path traversal attempts that go outside safe directories
            if '..' in file_path:
                # Check if the resolved path tries to escape safe directories
                normalized = os.path.normpath(abs_path)
                
                # If relative path with .. doesn't resolve within current directory, reject
                if not os.path.isabs(file_path):
                    if not normalized.startswith(original_cwd):
                        return False
                
                # Additional check: if .. remains in normalized path, it's suspicious
                if '..' in normalized:
                    return False
            
            # Allow paths in system temp directories
            import tempfile
            temp_dir = tempfile.gettempdir()
            
            # Allow if:
            # 1. Within current working directory
            # 2. Within system temp directory
            # 3. Within user's home directory (for uploaded files)
            allowed_prefixes = [
                original_cwd,
                temp_dir,
                os.path.expanduser('~'),
                '/var/folders',  # macOS temp directories
                '/tmp',          # Unix temp directories
                'C:\\Users',     # Windows user directories
                'C:\\Temp'       # Windows temp directories
            ]
            
            for prefix in allowed_prefixes:
                if abs_path.startswith(prefix):
                    return True
            
            # If it's a relative path that resolves within current directory
            if not os.path.isabs(file_path):
                return abs_path.startswith(original_cwd)
            
            return False
        except Exception as e:
            logger.warning(f"Error validating file path {file_path}: {e}")
            return False
    
    def _check_file_size(self, file_path: str) -> bool:
        """Check if file size is within limits."""
        try:
            return os.path.getsize(file_path) <= self.max_file_size
        except Exception:
            return False
    
    def _read_txt(self, file_path: str) -> str:
        """Read text file with proper encoding detection."""
        encodings = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                    logger.info(f"Successfully read TXT file with {encoding} encoding")
                    return content
            except UnicodeDecodeError:
                continue
        
        logger.error(f"Could not decode TXT file {file_path}")
        return f"ERRO: Não foi possível decodificar o arquivo de texto {file_path}"
    
    def _read_docx(self, file_path: str) -> str:
        """Read DOCX file with error handling."""
        try:
            doc = Document(file_path)
            text = []
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():  # Skip empty paragraphs
                    text.append(paragraph.text.strip())
            
            result = '\n'.join(text)
            logger.info(f"Successfully read DOCX file: {len(text)} paragraphs")
            return result if result else "AVISO: Documento DOCX está vazio ou não contém texto legível"
        except Exception as e:
            logger.error(f"Error reading DOCX file {file_path}: {e}")
            return f"ERRO ao ler arquivo DOCX: {e}"
    
    def _read_pdf(self, file_path: str) -> str:
        """Read PDF file with error handling."""
        try:
            text = []
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                if len(reader.pages) == 0:
                    return "AVISO: Arquivo PDF não contém páginas"
                
                for page_num, page in enumerate(reader.pages):
                    try:
                        page_text = page.extract_text().strip()
                        if page_text:
                            text.append(f"--- Página {page_num + 1} ---\n{page_text}")
                    except Exception as e:
                        logger.warning(f"Error reading page {page_num + 1}: {e}")
                        continue
            
            result = '\n\n'.join(text)
            logger.info(f"Successfully read PDF file: {len(reader.pages)} pages")
            return result if result else "AVISO: Não foi possível extrair texto legível do PDF"
        except Exception as e:
            logger.error(f"Error reading PDF file {file_path}: {e}")
            return f"ERRO ao ler arquivo PDF: {e}"
    
    def _read_excel(self, file_path: str) -> str:
        """Read Excel file with error handling."""
        try:
            # Read all sheets
            dfs = pd.read_excel(file_path, sheet_name=None)
            
            if not dfs:
                return "AVISO: Arquivo Excel não contém planilhas"
            
            text_parts = []
            total_rows = 0
            
            for sheet_name, df in dfs.items():
                if df.empty:
                    text_parts.append(f"=== ABA: {sheet_name} === (vazia)")
                    continue
                    
                text_parts.append(f"=== ABA: {sheet_name} ===")
                # Convert DataFrame to text, limit rows for readability
                if len(df) > 100:
                    text_parts.append(f"(Mostrando primeiras 100 linhas de {len(df)} total)")
                    text_parts.append(df.head(100).to_string(index=False))
                else:
                    text_parts.append(df.to_string(index=False))
                text_parts.append("")
                total_rows += len(df)
            
            result = '\n'.join(text_parts)
            logger.info(f"Successfully read Excel file: {len(dfs)} sheets, {total_rows} total rows")
            return result
        except Exception as e:
            logger.error(f"Error reading Excel file {file_path}: {e}")
            return f"ERRO ao ler arquivo Excel: {e}"
    
