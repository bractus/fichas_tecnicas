
from crewai.tools import BaseTool
from firecrawl import FirecrawlApp
import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class WebScrapingTool(BaseTool):
    name: str = "Web Scraping Tool"
    description: str = "Extracts web page content for recipe analysis using Firecrawl."

    def _run(self, url: str) -> str:
        try:
            # Load environment variables and initialize FirecrawlApp
            load_dotenv()
            api_key = os.getenv('FIRECRAWL_API_KEY')
            
            if not api_key:
                logger.error("FIRECRAWL_API_KEY not found in environment variables")
                return f"ERRO: FIRECRAWL_API_KEY não encontrada no arquivo .env"
            
            app = FirecrawlApp(api_key=api_key)
            logger.info(f"Starting web scraping for URL: {url}")
            
            result = app.scrape_url(
                url=url,
                params={
                    'formats': ['markdown', 'html'],
                    'includeTags': ['main', 'article', 'div.content', 'div.recipe', 'section.content'],
                    'excludeTags': ['nav', 'footer', 'header', 'sidebar', 'advertisement', 'script', 'style'],
                    'onlyMainContent': True,
                    'removeBase64Images': True
                }
            )
            
            if result['success']:
                content = result['data']['markdown'] or result['data']['content']
                final_content = content[:10000] if len(content) > 10000 else content
                logger.info(f"Successfully scraped {len(final_content)} characters from {url}")
                return final_content
            else:
                error_msg = result.get('error', 'Erro desconhecido')
                logger.error(f"Firecrawl scraping failed for {url}: {error_msg}")
                return f"Erro ao fazer scraping da URL {url}: {error_msg}"
            
        except Exception as e:
            logger.error(f"Exception during web scraping of {url}: {e}")
            return f"Erro ao fazer scraping da URL {url}: {e}"
