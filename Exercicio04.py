import matplotlib.pyplot as plt
import numpy as np
import random
import os
import threading
import time

def gerar_fractal(transformacoes, probabilidades, iteracoes=100000):
    if not abs(sum(probabilidades) - 1.0) < 1e-6:
        raise ValueError("As probabilidades devem somar 1.")
    
    x, y = 0.0, 0.0
    pontos = []

    for _ in range(iteracoes):
        r = random.random()
        acumulado = 0.0
        for i, prob in enumerate(probabilidades):
            acumulado += prob
            if r < acumulado:
                transformacao = transformacoes[i]
                break
        
        x, y = transformacao(x, y)
        pontos.append((x, y))
    
    return pontos

def sierpinski():
    transformacoes = [
        lambda x, y: (0.5 * x, 0.5 * y),
        lambda x, y: (0.5 * x + 0.5, 0.5 * y),
        lambda x, y: (0.5 * x + 0.25, 0.5 * y + 0.5)
    ]
    probabilidades = [1/3, 1/3, 1/3]
    pontos = gerar_fractal(transformacoes, probabilidades)
    salvar_imagem(pontos, "sierpinski.png")

def barnsley_fern():
    transformacoes = [
        lambda x, y: (0.0, 0.16 * y),
        lambda x, y: (0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6),
        lambda x, y: (0.2 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6),
        lambda x, y: (-0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44)
    ]
    probabilidades = [0.01, 0.85, 0.07, 0.07]
    pontos = gerar_fractal(transformacoes, probabilidades)
    salvar_imagem(pontos, "barnsley_fern.png")

def mandelbrot():
    pass  # Implementação do conjunto de Mandelbrot

def julia():
    pass  # Implementação do conjunto de Julia

def koch_curve():
    pass  # Implementação da Curva de Koch

def fractal_tree():
    pass  # Implementação da Árvore Fractal

def sierpinski_carpet():
    pass  # Implementação do Tapete de Sierpinski

def menger_sponge():
    pass  # Implementação da Esponja de Menger

def salvar_imagem(pontos, nome_arquivo):
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    caminho_arquivo = os.path.join(desktop, nome_arquivo)
    x_vals, y_vals = zip(*pontos)
    plt.scatter(x_vals, y_vals, s=0.2, color='black')
    plt.axis("off")
    plt.savefig(caminho_arquivo, dpi=300, bbox_inches='tight')
    plt.close()

def medir_tempo(funcao):
    inicio = time.time()
    funcao()
    fim = time.time()
    return fim - inicio

def executar_com_threads():
    threads = []
    funcoes = [sierpinski, barnsley_fern, mandelbrot, julia, koch_curve, fractal_tree, sierpinski_carpet, menger_sponge]
    
    for func in funcoes:
        thread = threading.Thread(target=func)
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

def executar_sem_threads():
    sierpinski()
    barnsley_fern()
    mandelbrot()
    julia()
    koch_curve()
    fractal_tree()
    sierpinski_carpet()
    menger_sponge()

def main():
    print("Executando sem threads...")
    tempo_sem_threads = medir_tempo(executar_sem_threads)
    print(f"Tempo sem threads: {tempo_sem_threads:.2f} segundos\n")
    
    print("Executando com threads...")
    tempo_com_threads = medir_tempo(executar_com_threads)
    print(f"Tempo com threads: {tempo_com_threads:.2f} segundos\n")
    
    print("Comparação de desempenho:")
    print(f"Tempo sem threads: {tempo_sem_threads:.2f} segundos")
    print(f"Tempo com threads: {tempo_com_threads:.2f} segundos")

if __name__ == "__main__":
    main()
