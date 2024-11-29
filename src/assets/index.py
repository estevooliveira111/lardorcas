from PIL import Image

imagem = Image.open('/home/estevoo/Documentos/GitHub/lardorcas/src/assets/Logo_para_papel_Branco.jpg')

caixa = (100, 100, 400, 400)

# imagem_recortada = imagem.crop(caixa)

# imagem_recortada.save('/home/estevoo/Documentos/GitHub/lardorcas/src/assets/imagem_recortada.jpg')

imagem_recortada.show()