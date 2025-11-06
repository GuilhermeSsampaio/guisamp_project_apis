import time
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from google import genai
import os
from urllib.parse import urlparse
import cloudscraper


load_dotenv()

# Configure a API do Gemini
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def scrap_recipe(url):
    """
    Scrape a recipe from the given URL and return its content.
    """
    # timer inicializado para medir o tempo de execução
    parsed_url = urlparse(url)
    font_of_url = parsed_url.netloc
    # print(font_of_url)
    start_time = time.time()
    # print(f"Starting to scrape the recipe from {url}...")
    scraper = cloudscraper.create_scraper()
    try:
        # Faz a requisição HTTP
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        # response = requests.get(url, headers=headers, timeout=10)
        response = scraper.get(url, headers=headers, timeout=10)
        print(f"HTTP request completed with status code {response.status_code}.")
        # print(f"Response content: {response.text[:500]}...")  # Print first 500 characters of the response
        response.raise_for_status() # Raise an error for bad status codes
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        # print("soup: ", soup.prettify()[:500])  # Print first 500 characters of the prettified soup
        # Remove tags de script e style
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Extrai o texto
        text = soup.get_text(separator='\n', strip=True)
        # print(f"extracted text (first 500 chars): {text[:500]}...")
        conversion_time = time.time() - start_time
        print(f"Tempo de conversão: {conversion_time:.2f} segundos")
        
        # define o comportamenteo do gemini
        prompt = f"""
        Resuma essa receita, passando os ingredientes, tempo de forno e o modo de preparo:

        {text}
        
        Caso não tenha o tempo de forno indique o recomendado.
        Use títulos de seção para separar os ingredientes do modo de preparo.
        O título da receita deve ser o primeiro item do resumo e deve usar heading 1.
        Abaixo do titulo, coloque a fonte da receita (site) e o link. Pode utilizar a váriavel {font_of_url} para isso.
        Traduza para o português.
        """
        
        # inicia o timer para medir o tempo de resposta do modelo
        model_start_time = time.time()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        model_time = time.time() - model_start_time
        print(f"Tempo de processamento do modelo: {model_time:.2f} segundos")
        
        total_time = time.time() - start_time
        print(f"Tempo total de execução: {total_time:.2f} segundos")
        print(f"Receita extraída: {response.text}")  # Print first 500 characters of the response
        return response.text
        
    except Exception as error:
        return {"error": f"Failed to scrape recipe from {url}: {error}"}
    
    
# url_teste = "https://www.tudogostoso.com.br/receita/23-bolo-de-cenoura.html"    
# # url_teste = "https://www.receitasnestle.com.br/receitas/bolo-de-limao-de-liquidificador"    
# scrap_recipe(url_teste)