from crewai.tools import BaseTool
from exa_py import Exa
import os
import logging
from dotenv import load_dotenv
from pathlib import Path
from pydantic import Field
from typing import Type, Optional
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class ExaSearchInput(BaseModel):
    query: str = Field(..., description="Specific query about ingredient - ex: 'fator correção batata' or 'preço carne bovina kg Brasil'. NEVER leave empty.")

class ExaSearchTool(BaseTool):
    name: str = "Exa Search Tool"
    description: str = """
    Specialized tool to search for information about culinary ingredients in Brazil.
    
    RETURNS:
    - Current prices in reais (R$) per kg/liter
    - Correction factors for preparation (losses in peeling, cleaning, cooking)
    - Market quotes like CEAGESP
    - Supplier and wholesale information
    
    HOW TO USE:
    Always provide a specific query with the desired ingredient.
    
    RECOMMENDED QUERIES:
    For correction factors: "fator correção [ingrediente]" 
    For prices: "preço [ingrediente] kg Brasil"
    For quotes: "cotação [ingrediente] CEAGESP atacado"
    
    NEVER use empty query. Always specify the ingredient you need to research.
    """
    args_schema: Type[BaseModel] = ExaSearchInput
    
    def __init__(self):
        # Load environment variables when tool is initialized
        load_dotenv(Path(__file__).parent.parent / '.env')
        super().__init__()
    
    def _run(self, query) -> str:
        """Executa busca no Exa com a query fornecida"""
        try:
            # Handle both string and dict input formats
            if isinstance(query, dict):
                search_query = str(query.get('query', '')).strip()
            else:
                search_query = str(query).strip()
            
            # Validate query
            if not self._validate_query(search_query):
                logger.warning(f"Invalid query received: '{search_query}'")
                return """Query vazia ou inválida. Para usar esta ferramenta, forneça uma consulta específica como:
                
Exemplos úteis:
• "fator de correção batata" - para fatores de correção
• "preço carne bovina kg" - para preços de ingredientes  
• "cotação tomate CEAGESP" - para preços de mercado
• "rendimento frango assado" - para dados de rendimento

Tente novamente com uma query mais específica sobre o ingrediente que você precisa."""
            
            # Get API key
            api_key = os.getenv("EXA_API_KEY")
            if not api_key or not api_key.strip():
                logger.warning("EXA_API_KEY not configured, using fallback response")
                return self._get_fallback_response(search_query)
            
            # Initialize Exa client
            exa = Exa(api_key=api_key.strip())
            logger.info(f"Executing Exa search for: '{search_query}'")
            
            # Enhance search query for better results
            enhanced_query = self._enhance_search_query(search_query)
            logger.debug(f"Enhanced query: '{enhanced_query}'")
            
            # Perform search
            results = exa.search(enhanced_query, num_results=5, use_autoprompt=True)
            
            if not results.results:
                logger.info(f"No results found for query: '{search_query}'")
                return f"Nenhum resultado encontrado para '{search_query}'. Tente termos mais específicos como 'preço [ingrediente] kg Brasil' ou 'fator correção [ingrediente] perda'."
            
            # Format results
            formatted_results = self._format_results(results.results[:3])
            logger.info(f"Successfully retrieved {len(results.results)} results")
            
            return "\n\n".join(formatted_results)
            
        except Exception as e:
            logger.error(f"Error in Exa search for '{query}': {e}")
            
            # Handle specific error types
            error_msg = str(e).lower()
            if any(term in error_msg for term in ['api', 'key', 'auth', 'unauthorized']):
                logger.warning("Authentication error with Exa API")
                return self._get_fallback_response(search_query)
            
            return f"ERRO na busca Exa: {e}"
    
    def _validate_query(self, query: str) -> bool:
        """Validate search query."""
        return (
            query and 
            query != '{}' and 
            query.lower() != 'none' and 
            len(query.strip()) >= 2
        )
    
    def _get_fallback_response(self, query: str) -> str:
        """Get fallback response when API is not available."""
        return f"""EXA_API_KEY não configurada. Resposta de fallback para: '{query}'
        
Fatores de correção típicos:
• Vegetais (batata, cenoura): 1.2 (20% perda)
• Carnes bovinas: 1.15 (15% perda)
• Frango: 1.1 (10% perda) 
• Cebola: 1.15 (15% perda)
• Grãos e cereais: 1.0-1.05 (0-5% perda)
• Peixes: 1.3-1.5 (30-50% perda)

Para dados atualizados, configure a EXA_API_KEY no arquivo .env"""
    
    def _format_results(self, results: list) -> list:
        """Format search results for display."""
        formatted_results = []
        for i, r in enumerate(results, 1):
            if r.text and r.text.strip():
                # Truncate text for readability
                text_preview = r.text[:250].replace('\n', ' ').strip()
                formatted_results.append(f"{i}. {r.title}\n   Conteúdo: {text_preview}...\n   Fonte: {r.url}")
            else:
                formatted_results.append(f"{i}. {r.title}\n   Fonte: {r.url}")
        return formatted_results
    
    def _enhance_search_query(self, original_query: str) -> str:
        """Melhora a query de busca para obter melhores resultados sobre preços e fatores de correção"""
        query_lower = original_query.lower()
        
        # Se já contém termos específicos, manter query original
        specific_terms = ['preço', 'cotação', 'brasil', 'kg', 'r$', 'real', 'ceagesp', 'atacado']
        if any(term in query_lower for term in specific_terms):
            return original_query
        
        # Se é busca por fator de correção, manter foco
        correction_terms = ['fator', 'correção', 'correction', 'perda', 'rendimento']
        if any(term in query_lower for term in correction_terms):
            return f"{original_query} Brasil nutrição culinária"
        
        # Se parece ser busca por ingrediente, adicionar contexto de preço
        common_ingredients = ['batata', 'carne', 'frango', 'tomate', 'cebola', 'arroz', 'feijão', 'leite', 'ovo', 'peixe', 'queijo']
        if any(ingrediente in query_lower for ingrediente in common_ingredients):
            return f"preço {original_query} kg Brasil mercado atacado varejo"
        
        # Query genérica - adicionar contexto brasileiro e culinário
        return f"{original_query} Brasil culinário ingredientes preços"