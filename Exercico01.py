import random
import threading
import time

# Função principal do QuickSort

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[-1]
    left = [x for x in arr[:-1] if x <= pivot]  # Elementos menores ou iguais ao pivô
    right = [x for x in arr[:-1] if x > pivot]  # Elementos maiores que o pivô
    return quicksort(left) + [pivot] + quicksort(right)

# Função paralelizada do QuickSort

def parallel_quicksort(arr, result):
    if len(arr) <= 1:
        result.extend(arr)  # Adiciona diretamente ao resultado, pois já está ordenado
        return
    
    pivot = arr[-1]  # Escolhe o pivô
    left = [x for x in arr[:-1] if x <= pivot]  # Elementos menores ou iguais ao pivô
    right = [x for x in arr[:-1] if x > pivot]  # Elementos maiores que o pivô
    
    left_result = []
    right_result = []
    
    # Criação de threads para ordenar as sublistas
    left_thread = threading.Thread(target=parallel_quicksort, args=(left, left_result))
    right_thread = threading.Thread(target=parallel_quicksort, args=(right, right_result))
    
    # Inicia as threads
    left_thread.start()
    right_thread.start()
    

    left_thread.join()
    right_thread.join()
    
# Combina os resultados no array final
    result.extend(left_result + [pivot] + right_result)    


# Função para gerar números aleatórios

def gerar_numeros_aleatorios(n=100, min_val=1, max_val=200):
    return [random.randint(min_val, max_val) for _ in range(n)]

# Função principal para testar o QuickSort

if __name__ == "__main__":
    numeros = gerar_numeros_aleatorios()
    
    print("Primeiros 10 números antes da ordenação:", numeros)

    inicio_sequencial = time.time()
    numeros_ordenados = quicksort(numeros)    
    fim_sequencial = time.time()

    print("Primeiros 10 números após a ordenação:", numeros_ordenados)
    print(f"Tempo de execução sequencial: {fim_sequencial - inicio_sequencial:.2f} segundos")

    inicio_paralelo = time.time()
    numeros_ordenados_paralelo = []
    parallel_quicksort(numeros, numeros_ordenados_paralelo)
    fim_paralelo = time.time()
    print("Primeiros 10 números após ordenação paralela:", numeros_ordenados_paralelo[:10])
    print(f"Tempo de execução paralela: {fim_paralelo - inicio_paralelo:.2f} segundos")
