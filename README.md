# RIWS
Traballo RIWS
Instalar dependencias con 

```
 pip install -r requirements.txt
```
Instalar dependencias página web react (react_website)
```
npm install @elastic/search-ui @elastic/react-search-ui @elastic/react-search-ui-views
npm install --save moment
npm install --save @elastic/search-ui-elasticsearch-connector
npm install react-icons --save
```
Antes de poder executar elasticsearch é importante configurar este para o seu correcto funcionamento esto farase no archivo *elasticsearch.yml*. 
Engadir as liñas, para activar Cors:
```
http.cors.enabled: true
http.cors.allow-credentials: true
http.cors.allow-origin: "*"
http.cors.allow-methods: OPTIONS, HEAD, GET, POST, PUT, DELETE
http.cors.allow-headers: "*"
```
Desabilitar autenticación:
```
xpack.security.enabled: false
xpack.security.enrollment.enabled: false
```
Unha vez modificado este archivo, pódese executar elastisearch e crear o índice con datos. Esto farase accedendo ao archivo *example.py*:
```
cd Crawler/crawler/crawler/spiders
scrapy runspider example.py
```

# Libros


1. Título
2. Autor
3. Editorial
4. Año de edicion
5. Idioma
6. Paginas
7. Imagen
8. Sinopsis
9. Categorias
11. "Precio"

## Postman
https://earlyrisk.postman.co/workspace/New-Team-Workspace~899a528d-733b-406e-a679-577f7f9cabc3/collection/1262116-52dcf7a2-4f26-43ea-b4ea-a11cce96ca60?action=share&creator=29656879
