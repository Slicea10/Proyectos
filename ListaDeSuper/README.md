
ABOUT: 

Trabajé con un conjunto de datos de PROFECO llamado [Quien es Quien en los Precios](https://datos.gob.mx/busca/dataset/quien-es-quien-en-los-precios).  Usando estos datos reales de los diferentes precios de productos en tiendas de autoservicio en México hice un algoritmo para minimizar el costo de una lista del súper. El algoritmo toma como entrada la ubicación de la persona (en coordenadas de latitud y longitud), la lista de productos que desea comprar, y el tiempo máximo que se desea tardar en comprar los productos. Los tiempos de un lugar a otro se estimaron con la API de OpenStreetMap. El algoritmo regresa el recorrido de tiendas que se debe seguir para adquirir cada producto, el precio total (el más barato posible), y el tiempo que tomará el recorrido (menos del máximo establecido por el usuario). 

FILES:

- NotebookQuienEsQuie.ipynb: Aquí está todo el preprocesamiento de los datos explicado a detalle, una visualización del problema, y la implementación del algoritmo junto con un ejemplo de su implementación.
- DocumentacionTecnicaProyecto.pdf: Aquí se explica el modelo y la justificación matemática.
