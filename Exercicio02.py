import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from threading import Thread, Lock

def buscar_palavra_na_pagina(url_atual, palavra, resultados, urls_visitados, lock):
   """
    Busca recursivamente uma palavra específica em todas as páginas de um site.

    Parâmetros:
        url_inicial (str): A URL inicial do site.
        palavra (str): A palavra a ser buscada.
        profundidade_maxima (int): A profundidade máxima de navegação (padrão: 3).

    Retorna:
        dict: Um dicionário onde as chaves são URLs e os valores indicam se a palavra foi encontrada.
    """
    # Estruturas para armazenar resultados e evitar loops
   
    with lock:
        if url_atual in urls_visitados:
            return
        urls_visitados.add(url_atual)

    try:
        print(f"Buscando em: {url_atual}")
        response = requests.get(url_atual, timeout=10)
        response.raise_for_status()  # Lança exceção para erros HTTP

        soup = BeautifulSoup(response.text, 'html.parser')
        conteudo = soup.get_text().lower()
        palavra_encontrada = palavra.lower() in conteudo

        with lock:
            resultados[url_atual] = palavra_encontrada
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url_atual}: {e}")

# Função gerencia threads e buscar palavras no site

def buscar_palavra_no_site(url_inicial, palavra, profundidade_maxima=3):
    urls_visitados = set()
    resultados = {}
    lock = Lock()
    threads = []

    def buscar_recursivo(url_atual, profundidade_atual):
        if profundidade_atual > profundidade_maxima:
            return

        try:
            response = requests.get(url_atual, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)

            for link in links:
                url_completa = urljoin(url_inicial, link['href'])

                if url_completa.startswith(url_inicial):
                    thread = Thread(target=buscar_palavra_na_pagina, args=(
                        url_completa, palavra, resultados, urls_visitados, lock
                    ))
                    threads.append(thread)
                    thread.start()

                    buscar_recursivo(url_completa, profundidade_atual + 1)

        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar {url_atual}: {e}")

    buscar_recursivo(url_inicial, profundidade_atual=1)

    for thread in threads:
        thread.join()

    return resultados

# Função principal
if __name__ == "__main__":
    url_inicial = input("Digite a URL inicial do site (ex.: https://www.exemplo.com): ")
    palavra = input("Digite a palavra a ser buscada: ")

    resultados = buscar_palavra_no_site(url_inicial, palavra)

    print("\nResultados da busca:")
    for url, encontrada in resultados.items():
        status = "Encontrada" if encontrada else "Não encontrada"
        print(f"{url}: Palavra '{palavra}' {status}")