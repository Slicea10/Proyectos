
ABOUT: 

Trabajé con un conjunto de datos de PROFECO llamado Quien es [Quien en los Precios](https://www.profeco.gob.mx/precios/canasta/default.aspx).

Usé datos reales de los diferentes precios de una gran gama de productos que se ofrecen en tiendas de autoservicio en México. Con estos datos hice un algoritmo para minimizar el costo de una lista del súper. El algoritmo toma como entrada la ubicación de la persona (en coordenadas de latitud y longitud), la lista de productos que desea comprar, y el tiempo máximo que se desea tardar en "hacer su súper". Fue necesario establecer el tiempo máximo pues de otra forma el algoritmo sólo buscaría las tiendas en las que se ofrece cada producto al menor precio sin importar qué tan lejos estén. Los tiempos de un lugar a otro se estimaron con una API llamada OpenStreetMap.
El algoritmo regresa el recorrido de tiendas que se debe seguir para adquirir cada producto, el precio total (el más barato posible), y el tiempo que tomará el recorrido (menos del máximo establecido por el usuario). 


FILES:
- Notebook .ipynb del preprocesamiento de los datos y del algoritmo junto con un ejemplo de su implementación.
- Documento pdf donde se explica el modelo matemático.
