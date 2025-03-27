from PIL import Image
from tkinter import Tk, filedialog
from threading import Thread

def processar_faixa(imagem, faixa, largura, imagem_preto_branco):
    for x in faixa:
        for y in range(largura):
            r, g, b = imagem.getpixel((x, y))
            luminancia = int(0.299 * r + 0.587 * g + 0.114 * b)
            imagem_preto_branco.putpixel((x, y), luminancia)

def converter_para_preto_e_branco_manual():
    try:
        root = Tk()
        root.withdraw()

        caminho_imagem = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp *.gif"), ("Todos os arquivos", "*.*")]
        )

        if not caminho_imagem:
            print("Nenhuma imagem foi selecionada.")
            return

        imagem = Image.open(caminho_imagem)
        imagem = imagem.convert("RGB")  #garante que a imagem esteja no modo RGB
        largura, altura = imagem.size
        imagem_preto_branco = Image.new("L", (largura, altura))

        #numero de threads
        num_threads = 4
        threads = []
        largura_faixa = altura // num_threads

        for i in range(num_threads):
            inicio_faixa = i * largura_faixa
            fim_faixa = altura if i == num_threads - 1 else (i + 1) * largura_faixa
            faixa = range(inicio_faixa, fim_faixa)

            thread = Thread(target=processar_faixa, args=(imagem, faixa, largura, imagem_preto_branco))
            threads.append(thread)
            thread.start()

        #aguarda todas as threads terminarem
        for thread in threads:
            thread.join()

        caminho_saida = filedialog.asksaveasfilename(
            title="Salvar imagem em preto e branco",
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("Todos os arquivos", "*.*")]
        )

        if not caminho_saida:
            print("Operação de salvamento cancelada.")
            return

        imagem_preto_branco.save(caminho_saida)
        print(f"Imagem convertida com sucesso! Salva em: {caminho_saida}")

    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")

if __name__ == "__main__":
    converter_para_preto_e_branco_manual()
