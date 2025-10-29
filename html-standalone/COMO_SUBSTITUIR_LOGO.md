# COMO SUBSTITUIR A LOGO PELA SUA LOGO REAL

## Opção 1: Converter sua logo para Base64

1. Salve sua logo como PNG ou JPG
2. Use um conversor online (ex: base64-image.de)
3. Substitua o conteúdo entre aspas no src="..." por:
   data:image/png;base64,SUA_LOGO_AQUI

## Opção 2: Usar arquivo de imagem

1. Salve sua logo como logo-temvenda.png na pasta html-standalone/
2. Substitua as linhas:
   ```html
   <img src="data:image/svg+xml;base64,..." alt="Logo TEM VENDA" />
   ```
   Por:
   ```html
   <img src="logo-temvenda.png" alt="Logo TEM VENDA" />
   ```

## Opção 3: Me enviar a logo novamente

Se preferir, me envie a logo novamente e eu faço a conversão para você!

## Localizações da logo no código:

1. Header (linha ~887): `<div class="logo-icon">`
2. Footer (linha ~1116): `<div class="logo-icon">`

Ambas precisam ser substituídas pela mesma logo.
