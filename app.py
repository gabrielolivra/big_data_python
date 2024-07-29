import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os


df = pd.read_csv('./data/produtos_eletronicos.csv')

def criar_pasta(pasta):
    if not os.path.exists(pasta):
        os.makedirs(pasta)
def garantir_pasta(pasta):
    if not os.path.exists(pasta):
        os.makedirs(pasta)

pasta_visualizations = './visualizations'
garantir_pasta(pasta_visualizations)


def recomendar_produtos(produto_nome, avaliacao_minima, preco_maximo):
   
    produtos_filtrados = df[
        (df['produto'].str.contains(produto_nome, case=False, na=False)) & 
        (df['avaliacao'] >= avaliacao_minima) &
        (df['preco'] <= preco_maximo)
    ]
    
    if produtos_filtrados.empty:
        print(f"Nenhum produto encontrado para '{produto_nome}' com avaliação mínima de {avaliacao_minima} e preço máximo de {preco_maximo}.")
        return
    
   
    produtos_recomendados = produtos_filtrados.sort_values(by='avaliacao', ascending=False)
    
    print(f"Produtos recomendados para {produto_nome.upper()} com avaliação mínima de {avaliacao_minima} e preço máximo de {preco_maximo}:")
    print(produtos_recomendados[['produto', 'marca', 'avaliacao', 'preco']])
    
    
    pasta_imagens = 'imagens'
    criar_pasta(pasta_imagens)
    
    
    fig, ax = plt.subplots(2, 1, figsize=(12, 14))
    
    ax[0].bar(produtos_recomendados['produto'] + ' (' + produtos_recomendados['marca'] + ')', produtos_recomendados['avaliacao'], color='skyblue')
    
    ax[0].set_ylabel('Avaliação', fontsize=14)
    ax[0].set_title(f'Avaliação dos Produtos Recomendados para {produto_nome.upper()}', fontsize=16, pad=20)
    ax[0].tick_params(axis='x', rotation=45, labelsize=12)
    ax[0].tick_params(axis='y', labelsize=12)
    
   
    ax[1].bar(produtos_recomendados['produto'] + ' (' + produtos_recomendados['marca'] + ')', produtos_recomendados['preco'], color='salmon')
    
    ax[1].set_ylabel('Preço', fontsize=14)
    ax[1].set_title(f'Preço dos Produtos Recomendados para {produto_nome.upper()}', fontsize=16, pad=20)
    ax[1].tick_params(axis='x', rotation=45, labelsize=12)
    ax[1].tick_params(axis='y', labelsize=12)
    
    
    plt.tight_layout()
    
    
    caminho_aval = os.path.join(pasta_imagens, 'grafico_avaliacoes.png')


    

    for caminho in [caminho_aval]:
        if os.path.isfile(caminho):
            os.remove(caminho)
    
   
    fig.savefig(caminho_aval, bbox_inches='tight', format='png')
    
    plt.close(fig)
    
  
    if not os.path.isfile(caminho_aval):
        print(f"Erro: A imagem '{caminho_aval}' não foi criada.")
        return
    
   
    pdf_filename = './visualizations/recomendacoes_produtos.pdf'
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter
    
 
    margem_x = 72
    margem_y = height - 72
    c.setFont("Helvetica", 14)

    c.drawString(margem_x, margem_y, f'Recomendações de Produtos para {produto_nome.upper()}')

    
   
    porcentagem_largura = 0.8
    img_width = width * porcentagem_largura
    img_height = 400
    c.drawImage(caminho_aval, 72, height - 72 - img_height, width=img_width, height=img_height)
    
    

    c.save()
    
    print(f"PDF '{pdf_filename}' gerado com sucesso!")


produto_nome = input("Digite o nome de um produto para obter recomendações: ")
produto_avaliacao = float(input("Digite o número de avaliação mínima (entre 1 e 5): "))
produto_preco = float(input("Digite o preço máximo que você pode pagar: "))

recomendar_produtos(produto_nome, produto_avaliacao, produto_preco)
