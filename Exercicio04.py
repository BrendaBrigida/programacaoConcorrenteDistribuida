import matplotlib.pyplot as plt
import numpy as np
import random
import os
import threading

# Função para gerar fractais usando um Sistema de Funções Iteradas (IFS)
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

# Funções de geração de fractais
def sierpinski():
    transformacoes = [
        lambda x, y: (0.5 * x, 0.5 * y),
        lambda x, y: (0.5 * x + 0.5, 0.5 * y),
        lambda x, y: (0.5 * x + 0.25, 0.5 * y + 0.5)
    ]
    probabilidades = [1/3, 1/3, 1/3]
    pontos = gerar_fractal(transformacoes, probabilidades, iteracoes=100000)

    x_vals, y_vals = zip(*pontos)
    plt.figure()
    plt.scatter(x_vals, y_vals, s=0.1, color='black', marker='.')
    plt.title("Triângulo de Sierpinski")
    plt.axis('off')
    plt.savefig(os.path.join(os.path.expanduser("~"), "Desktop", "sierpinski.png"), bbox_inches='tight', dpi=300)
    plt.close()

def samambaia_barnsley():
    transformacoes = [
        lambda x, y: (0.0, 0.16 * y),
        lambda x, y: (0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6),
        lambda x, y: (0.2 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6),
        lambda x, y: (-0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44)
    ]
    probabilidades = [0.01, 0.85, 0.07, 0.07]
    pontos = gerar_fractal(transformacoes, probabilidades, iteracoes=100000)

    x_vals, y_vals = zip(*pontos)
    plt.figure()
    plt.scatter(x_vals, y_vals, s=0.1, color='green', marker='.')
    plt.title("Samambaia de Barnsley")
    plt.axis('off')
    plt.savefig(os.path.join(os.path.expanduser("~"), "Desktop", "samambaia_barnsley.png"), bbox_inches='tight', dpi=300)
    plt.close()

def mandelbrot(width=800, height=800, max_iter=100):
    x_min, x_max = -2.0, 1.0
    y_min, y_max = -1.5, 1.5
    image = np.zeros((height, width))

    for row in range(height):
        for col in range(width):
            c = complex(x_min + (x_max - x_min) * col / width,
                        y_min + (y_max - y_min) * row / height)
            z = 0.0j
            n = 0
            while abs(z) <= 2 and n < max_iter:
                z = z * z + c
                n += 1
            image[row, col] = n

    plt.figure()
    plt.imshow(image, extent=(x_min, x_max, y_min, y_max), cmap='hot', interpolation='bilinear')
    plt.title("Conjunto de Mandelbrot")
    plt.axis('off')
    plt.savefig(os.path.join(os.path.expanduser("~"), "Desktop", "mandelbrot.png"), bbox_inches='tight', dpi=300)
    plt.close()

def julia(c=-0.7 + 0.27015j, width=800, height=800, max_iter=100):
    x_min, x_max = -1.5, 1.5
    y_min, y_max = -1.5, 1.5
    image = np.zeros((height, width))

    for row in range(height):
        for col in range(width):
            z = complex(x_min + (x_max - x_min) * col / width,
                        y_min + (y_max - y_min) * row / height)
            n = 0
            while abs(z) <= 2 and n < max_iter:
                z = z * z + c
                n += 1
            image[row, col] = n

    plt.figure()
    plt.imshow(image, extent=(x_min, x_max, y_min, y_max), cmap='twilight_shifted', interpolation='bilinear')
    plt.title("Conjunto de Julia")
    plt.axis('off')
    plt.savefig(os.path.join(os.path.expanduser("~"), "Desktop", "julia.png"), bbox_inches='tight', dpi=300)
    plt.close()

# Função principal para executar as threads
def main():
    threads = []
    fractais = [sierpinski, samambaia_barnsley, mandelbrot, julia]

    for fractal in fractais:
        t = threading.Thread(target=fractal)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("Todos os fractais foram gerados.")

if __name__ == "__main__":
    main()
