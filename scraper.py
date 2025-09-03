#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraper Robusto de Receitas - Contorna Bloqueios 403
Versão com múltiplas estratégias para evitar detecção

Instalar dependências:
pip install requests beautifulsoup4 lxml fake-useragent cloudscraper

Para usar:
python scraper_robusto.py
"""

import requests
from bs4 import BeautifulSoup
import time
import os
import zipfile
import re
import json
import random
from datetime import datetime
from urllib.parse import urljoin
import logging

# Imports opcionais para contornar proteções
try:
    from fake_useragent import UserAgent
    FAKE_UA_AVAILABLE = True
except ImportError:
    FAKE_UA_AVAILABLE = False

try:
    import cloudscraper
    CLOUDSCRAPER_AVAILABLE = True
except ImportError:
    CLOUDSCRAPER_AVAILABLE = False

class ScraperRobusto:
    def __init__(self):
        self.receitas = []
        self.base_url = 'https://www.tudogostoso.com.br'
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Pool de User Agents
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
        ]
        
        # Configurar sessões múltiplas
        self.sessoes = []
        self.configurar_sessoes()
        
        # URLs das receitas
        self.receitas_urls = [
            '/receita/23-bolo-de-cenoura.html',
            '/receita/114-brigadeiro.html', 
            '/receita/59-pure-de-batata.html',
            '/receita/2462-strogonoff-de-frango.html',
            '/receita/876-lasanha-de-carne-moida.html',
            '/receita/1282-torta-de-frango.html',
            '/receita/1363-coxinha-pratica-deliciosa.html',
            '/receita/2831-moqueca-de-peixe.html',
            '/receita/3158-acaraje.html',
            '/receita/2313-bolo-gelado.html',
            '/receita/302-pizza-de-pao-de-forma.html',
            '/receita/1443-pao-de-queijo.html',
            '/receita/2998-feijoada.html',
            '/receita/1154-baiao-de-dois.html',
            '/receita/112-bobo-de-camarao.html',
            '/receita/33269-caruru.html',
            '/receita/60592-vatapa-de-camarao-rapido.html',
            '/receita/60050-cuscuz-nordestino.html',
            '/receita/133817-moqueca-de-peixe-facil.html',
            '/receita/54052-caranguejo-ao-leite-de-coco.html',
            '/receita/13701-abara.html',
            '/receita/98437-beiju.html',
            '/receita/1444-cartola.html',
            '/receita/91253-mungunza.html',
            '/receita/68015-canjica-nordestina.html',
            '/receita/80343-bolo-baeta.html',
            '/receita/195644-pudim-de-tapioca.html',
            '/receita/35-pamonha-doce.html',
            '/receita/61618-torta-bulgara.html',
            '/receita/116740-bolo-de-aipim-com-coco.html',
            '/receita/15246-bolo-de-rolo-de-recife.html',
            '/receita/2753-cocada.html',
            '/receita/2620-bolo-souza-leao.html',
            '/receita/42565-lele-de-milho.html',
            '/receita/29124-bolo-simples.html',
            '/receita/15939-pave-de-chocolate.html',
            '/receita/6179-petit-gateau.html',
            '/receita/364-manjar-de-coco.html',
            '/receita/104383-torta-de-limao.html',
            '/receita/499-palha-italiana.html',
            '/receita/24104-pudim-de-leite.html',
            '/receita/97021-canjica-com-leite-condensado.html',
            '/receita/10592-arroz-doce-cremoso.html',
            '/receita/58-tabule.html',
            '/receita/28-arroz-a-grega.html',
            '/receita/38-molho-branco.html',
            '/receita/6662-creme-de-milho.html',
            '/receita/5887-molho-pesto.html',
            '/receita/42288-molho-bechamel.html',
            '/receita/128825-caipirinha-original.html'
        ]

    def configurar_sessoes(self):
        """Configura múltiplas sessões com diferentes configurações"""
        
        # Sessão 1: Requests padrão
        session1 = requests.Session()
        session1.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        })
        self.sessoes.append(('requests_padrao', session1))
        
        # Sessão 2: Com referer
        session2 = requests.Session()
        session2.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.google.com/',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        self.sessoes.append(('requests_referer', session2))
        
        # Sessão 3: CloudScraper (se disponível)
        if CLOUDSCRAPER_AVAILABLE:
            try:
                scraper = cloudscraper.create_scraper(
                    browser={
                        'browser': 'chrome',
                        'platform': 'windows',
                        'mobile': False
                    }
                )
                self.sessoes.append(('cloudscraper', scraper))
                self.logger.info("✅ CloudScraper configurado")
            except Exception as e:
                self.logger.warning(f"⚠️ Erro ao configurar CloudScraper: {e}")
        
        # Sessão 4: Com cookies simulados
        session4 = requests.Session()
        session4.headers.update({
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.tudogostoso.com.br/',
        })
        # Simular cookies de sessão
        session4.cookies.set('tudogostoso_session', 'simulated_session_' + str(random.randint(100000, 999999)))
        self.sessoes.append(('requests_cookies', session4))
        
        self.logger.info(f"🔧 {len(self.sessoes)} sessões configuradas")

    def obter_html_robusto(self, url, max_tentativas=3):
        """Obtém HTML usando múltiplas estratégias"""
        
        for tentativa in range(max_tentativas):
            # Rotacionar entre diferentes sessões
            nome_sessao, sessao = self.sessoes[tentativa % len(self.sessoes)]
            
            try:
                self.logger.info(f"Tentativa {tentativa + 1}/{max_tentativas} usando {nome_sessao}")
                
                # Rotacionar User-Agent se possível
                if hasattr(sessao, 'headers') and 'User-Agent' in sessao.headers:
                    if FAKE_UA_AVAILABLE:
                        try:
                            ua = UserAgent()
                            sessao.headers['User-Agent'] = ua.random
                        except:
                            sessao.headers['User-Agent'] = random.choice(self.user_agents)
                    else:
                        sessao.headers['User-Agent'] = random.choice(self.user_agents)
                
                # Fazer request
                response = sessao.get(url, timeout=20, allow_redirects=True)
                
                # Verificar status
                if response.status_code == 200:
                    self.logger.info(f"✅ Sucesso com {nome_sessao}")
                    return response.text
                elif response.status_code == 403:
                    self.logger.warning(f"🚫 403 Forbidden com {nome_sessao}")
                    # Aguardar mais tempo em caso de 403
                    time.sleep(random.uniform(3, 6))
                    continue
                else:
                    self.logger.warning(f"⚠️ Status {response.status_code} com {nome_sessao}")
                    continue
                    
            except requests.exceptions.RequestException as e:
                self.logger.error(f"❌ Erro de conexão com {nome_sessao}: {e}")
                time.sleep(random.uniform(2, 4))
                continue
            except Exception as e:
                self.logger.error(f"❌ Erro inesperado com {nome_sessao}: {e}")
                continue
        
        # Se todas as tentativas falharam, tentar método alternativo
        return self.obter_html_alternativo(url)

    def obter_html_alternativo(self, url):
        """Método alternativo usando curl ou wget se disponível"""
        self.logger.info("🔄 Tentando método alternativo...")
        
        try:
            import subprocess
            
            # Tentar com curl
            try:
                cmd = [
                    'curl', '-s', '-L',
                    '-H', f'User-Agent: {random.choice(self.user_agents)}',
                    '-H', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    '-H', 'Accept-Language: pt-BR,pt;q=0.9',
                    '-H', 'Referer: https://www.google.com/',
                    '--connect-timeout', '20',
                    url
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if result.returncode == 0 and result.stdout:
                    self.logger.info("✅ Sucesso com curl")
                    return result.stdout
            except Exception as e:
                self.logger.debug(f"Curl falhou: {e}")
            
            # Tentar com wget
            try:
                cmd = [
                    'wget', '-q', '-O', '-',
                    '--user-agent', random.choice(self.user_agents),
                    '--header', 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    '--header', 'Accept-Language: pt-BR,pt;q=0.9',
                    '--header', 'Referer: https://www.google.com/',
                    '--timeout', '20',
                    url
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                if result.returncode == 0 and result.stdout:
                    self.logger.info("✅ Sucesso com wget")
                    return result.stdout
            except Exception as e:
                self.logger.debug(f"Wget falhou: {e}")
                
        except ImportError:
            pass
        
        self.logger.error("❌ Todos os métodos falharam")
        return None

    def extrair_dados_receita(self, html, url):
        """Extrai dados da receita do HTML"""
        if not html:
            return None
            
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extrair título
            titulo = self.extrair_titulo(soup, url)
            
            # Extrair ingredientes
            ingredientes = self.extrair_ingredientes(soup)
            
            # Extrair modo de preparo
            preparo = self.extrair_preparo(soup)
            
            # Extrair metadados
            tempo = self.extrair_tempo(soup)
            porcoes = self.extrair_porcoes(soup)
            
            # Validar dados mínimos
            if not titulo or len(ingredientes) < 2:
                self.logger.warning(f"⚠️ Dados insuficientes para {url}")
                return None
            
            receita = {
                'titulo': titulo,
                'url': url,
                'ingredientes': ingredientes,
                'preparo': preparo,
                'tempo': tempo,
                'porcoes': porcoes,
                'coletado_em': datetime.now().isoformat()
            }
            
            return receita
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao processar HTML de {url}: {e}")
            return None

    def extrair_titulo(self, soup, url):
        """Extrai título da receita"""
        # Múltiplas estratégias
        selectors = [
            'h1',
            'title', 
            '.recipe-title',
            '[data-recipe-title]',
            '.entry-title'
        ]
        
        for selector in selectors:
            elemento = soup.select_one(selector)
            if elemento:
                titulo = elemento.get_text().strip()
                # Limpar título
                titulo = re.sub(r'\s*-\s*TudoGostoso.*', '', titulo, flags=re.I)
                titulo = re.sub(r'\s+', ' ', titulo)
                if titulo and len(titulo) > 3:
                    return titulo
        
        # Fallback: extrair do URL
        nome_url = url.split('/')[-1].replace('.html', '').replace('-', ' ')
        return nome_url.title()

    def extrair_ingredientes(self, soup):
        """Extrai lista de ingredientes"""
        ingredientes = []
        
        # Buscar por diferentes padrões
        patterns = [
            # Listas com classes específicas
            '.ingredients li',
            '.recipe-ingredients li', 
            '[data-ingredients] li',
            # Listas após títulos
            'h2:contains("Ingredientes") ~ ul li',
            'h3:contains("Ingredientes") ~ ul li',
            # Busca genérica
            'ul li',
            'ol li'
        ]
        
        for pattern in patterns:
            try:
                elementos = soup.select(pattern)
                temp_ingredientes = []
                
                for elem in elementos:
                    texto = elem.get_text().strip()
                    if self.eh_ingrediente_valido(texto):
                        temp_ingredientes.append(texto)
                
                if len(temp_ingredientes) >= 3:
                    ingredientes = temp_ingredientes[:15]  # Limitar
                    break
                    
            except Exception:
                continue
        
        return ingredientes

    def eh_ingrediente_valido(self, texto):
        """Verifica se texto é um ingrediente válido"""
        if not texto or len(texto) < 3:
            return False
        
        # Palavras que indicam ingredientes
        indicadores = [
            'xícara', 'colher', 'kg', 'g', 'ml', 'litro', 'l', 
            'dente', 'pitada', 'gosto', 'unidade', 'fatia', 
            'pedaço', 'lata', 'pacote', 'envelope', 'sache',
            'açúcar', 'sal', 'farinha', 'leite', 'ovo', 'manteiga',
            'óleo', 'cebola', 'alho', 'tomate'
        ]
        
        texto_lower = texto.lower()
        return any(ind in texto_lower for ind in indicadores)

    def extrair_preparo(self, soup):
        """Extrai modo de preparo"""
        passos = []
        
        # Padrões de busca
        patterns = [
            '.instructions li',
            '.recipe-instructions li',
            '.directions li',
            '[data-instructions] li',
            'h2:contains("Preparo") ~ ol li',
            'h3:contains("Preparo") ~ ol li',
            'h2:contains("Modo") ~ ol li',
            'ol li'
        ]
        
        for pattern in patterns:
            try:
                elementos = soup.select(pattern)
                temp_passos = []
                
                for i, elem in enumerate(elementos, 1):
                    texto = elem.get_text().strip()
                    if self.eh_passo_valido(texto):
                        if not re.match(r'^\d+\.', texto):
                            texto = f"{i}. {texto}"
                        temp_passos.append(texto)
                
                if len(temp_passos) >= 2:
                    passos = temp_passos[:12]  # Limitar
                    break
                    
            except Exception:
                continue
        
        return passos

    def eh_passo_valido(self, texto):
        """Verifica se texto é um passo válido"""
        if not texto or len(texto) < 10:
            return False
        
        verbos = [
            'misture', 'adicione', 'coloque', 'asse', 'cozinhe', 
            'frite', 'bata', 'mexa', 'tempere', 'corte', 'pique',
            'refogue', 'ferva', 'deixe', 'sirva', 'retire'
        ]
        
        return any(verbo in texto.lower() for verbo in verbos)

    def extrair_tempo(self, soup):
        """Extrai tempo de preparo"""
        texto_completo = soup.get_text()
        patterns = [
            r'(\d+)\s*min',
            r'(\d+)\s*minutos?',
            r'(\d+)\s*horas?',
            r'(\d+)h\s*(\d+)?m?'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, texto_completo, re.I)
            if match:
                return match.group(0)
        
        return ""

    def extrair_porcoes(self, soup):
        """Extrai número de porções"""
        texto_completo = soup.get_text()
        patterns = [
            r'(\d+)\s*porções?',
            r'(\d+)\s*pessoas?',
            r'rende\s*(\d+)',
            r'serve\s*(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, texto_completo, re.I)
            if match:
                return match.group(0)
        
        return ""

    def processar_receita(self, url_relativa):
        """Processa uma receita individual"""
        url_completa = urljoin(self.base_url, url_relativa)
        
        # Delay aleatório entre requests
        delay = random.uniform(2, 5)
        time.sleep(delay)
        
        html = self.obter_html_robusto(url_completa)
        receita = self.extrair_dados_receita(html, url_completa)
        
        return receita

    def salvar_receita(self, receita, pasta="receitas_robustas"):
        """Salva receita individual"""
        if not receita:
            return None
            
        os.makedirs(pasta, exist_ok=True)
        
        nome_arquivo = re.sub(r'[^\w\s-]', '', receita['titulo'])
        nome_arquivo = re.sub(r'\s+', '_', nome_arquivo)
        nome_arquivo = f"{nome_arquivo}.txt"
        
        caminho = os.path.join(pasta, nome_arquivo)
        
        with open(caminho, 'w', encoding='utf-8') as f:
            f.write(self.formatar_receita(receita))
        
        return caminho

    def formatar_receita(self, receita):
        """Formata receita para arquivo"""
        texto = f"# {receita['titulo']}\n\n"
        
        if receita.get('tempo'):
            texto += f"⏱️ **Tempo:** {receita['tempo']}\n"
        if receita.get('porcoes'):
            texto += f"🍽️ **Rendimento:** {receita['porcoes']}\n"
        texto += "\n"
        
        texto += "## 🥘 Ingredientes\n\n"
        for ingrediente in receita['ingredientes']:
            texto += f"- {ingrediente}\n"
        texto += "\n"
        
        texto += "## 👨‍🍳 Modo de Preparo\n\n"
        for passo in receita['preparo']:
            texto += f"{passo}\n\n"
        
        texto += "---\n"
        texto += f"**Fonte:** {receita['url']}\n"
        texto += f"**Coletado em:** {datetime.fromisoformat(receita['coletado_em']).strftime('%d/%m/%Y %H:%M')}\n"
        
        return texto

    def executar_coleta_completa(self):
        """Executa coleta completa com todas as proteções"""
        print("🛡️ SCRAPER ROBUSTO - ANTI-BLOQUEIO")
        print("=" * 50)
        print(f"🔧 CloudScraper: {'✅' if CLOUDSCRAPER_AVAILABLE else '❌'}")
        print(f"🔧 Fake UserAgent: {'✅' if FAKE_UA_AVAILABLE else '❌'}")
        print(f"📊 Total de receitas: {len(self.receitas_urls)}")
        print("=" * 50)
        
        sucessos = 0
        falhas = 0
        
        for i, url_relativa in enumerate(self.receitas_urls, 1):
            nome_receita = url_relativa.split('/')[-1].replace('.html', '').replace('-', ' ').title()
            
            print(f"[{i:02d}/{len(self.receitas_urls):02d}] {nome_receita[:30]:<30} ", end="", flush=True)
            
            try:
                receita = self.processar_receita(url_relativa)
                
                if receita and len(receita['ingredientes']) >= 2:
                    self.receitas.append(receita)
                    self.salvar_receita(receita)
                    print(f"✅ ({len(receita['ingredientes'])} ing.)")
                    sucessos += 1
                else:
                    print("❌ Dados insuficientes")
                    falhas += 1
                    
            except KeyboardInterrupt:
                print("\n\n⏸️ Interrompido pelo usuário")
                break
            except Exception as e:
                print(f"❌ Erro: {str(e)[:30]}")
                falhas += 1
                self.logger.error(f"Erro ao processar {url_relativa}: {e}")
        
        # Finalizar
        self.criar_arquivos_finais(sucessos, falhas)
        
        print("\n" + "=" * 50)
        print(f"🏁 COLETA FINALIZADA")
        print(f"✅ Sucessos: {sucessos}")
        print(f"❌ Falhas: {falhas}")
        print(f"📈 Taxa de sucesso: {sucessos/(sucessos+falhas)*100:.1f}%")
        print("=" * 50)

    def criar_arquivos_finais(self, sucessos, falhas):
        """Cria arquivos finais (ZIP e backup)"""
        # Backup JSON
        backup = {
            'metadados': {
                'data_coleta': datetime.now().isoformat(),
                'total_receitas': len(self.receitas),
                'sucessos': sucessos,
                'falhas': falhas,
                'versao': 'robusto_v1.0'
            },
            'receitas': self.receitas
        }
        
        with open('receitas_backup_robusto.json', 'w', encoding='utf-8') as f:
            json.dump(backup, f, ensure_ascii=False, indent=2)
        
        # Criar ZIP
        nome_zip = "Receitas_Brasileiras_Robusto.zip"
        
        with zipfile.ZipFile(nome_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # README
            readme = f"""# 🇧🇷 Receitas Brasileiras - Coleta Robusta

📦 Coletado com scraper anti-bloqueio
🗓️ Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
📊 Receitas: {len(self.receitas)}
💪 Taxa de sucesso: {sucessos/(sucessos+falhas)*100:.1f}%

## 🍽️ Receitas Coletadas

{chr(10).join([f"- {r['titulo']}" for r in self.receitas])}

## 🛡️ Tecnologias Anti-Bloqueio

- Múltiplas sessões HTTP
- Rotação de User-Agents
- CloudScraper (Cloudflare bypass)
- Rate limiting inteligente
- Fallback com curl/wget
- Headers realistas

---
Coletado do TudoGostoso.com.br
"""
            
            zipf.writestr("README.md", readme)
            
            # Adicionar receitas
            pasta = "receitas_robustas"
            if os.path.exists(pasta):
                for arquivo in os.listdir(pasta):
                    if arquivo.endswith('.txt'):
                        zipf.write(os.path.join(pasta, arquivo), f"receitas/{arquivo}")
            
            # Adicionar backup
            zipf.write('receitas_backup_robusto.json', 'backup.json')
        
        print(f"📦 ZIP criado: {nome_zip} ({os.path.getsize(nome_zip)/1024:.1f} KB)")
        print(f"💾 Backup salvo: receitas_backup_robusto.json")

def main():
    print("🚀 Iniciando Scraper Robusto...")
    
    # Verificar dependências opcionais
    if not CLOUDSCRAPER_AVAILABLE:
        print("⚠️ CloudScraper não disponível. Instale com: pip install cloudscraper")
    
    if not FAKE_UA_AVAILABLE:
        print("⚠️ Fake UserAgent não disponível. Instale com: pip install fake-useragent")
    
    scraper = ScraperRobusto()
    scraper.executar_coleta_completa()

if __name__ == "__main__":
    main()