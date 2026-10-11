# Road Vision Lab: fotografías reales y Python

## Abrir la demo desde GitHub

1. Abre https://codespaces.new/erickvera610/road-vision-lab e inicia sesión en GitHub.
2. Crea el Codespace y espera a que instale los paquetes.
3. El puerto 8000 debe abrirse automáticamente. Si no ocurre, entra a la pestaña Ports y selecciona Open in Browser para el puerto 8000.
4. Elige una de las seis fotografías y pulsa Analyze sample.
5. Para tu foto, escoge un PNG/JPEG y pulsa Analyze upload.

Codespaces usa tu cuenta y su cuota. La página pública de GitHub Pages muestra el ejercicio JavaScript y una galería; la nueva demo con Python se ejecuta en Codespaces o en tu equipo.

## Qué hace cada paso

- Máscara de color: selecciona píxeles blancos y amarillos que podrían pertenecer a las marcas de carretera.
- Bordes: identifica cambios de intensidad alrededor de esas marcas.
- Región de carretera: limita el análisis a un trapecio en la parte inferior de la foto.
- Hough: propone segmentos rectos a partir de los bordes.
- RANSAC: busca una línea apoyada por varios segmentos, tolerando puntos incorrectos.
- Comprobación geométrica: rechaza pares cruzados o que salen de la imagen.

La interfaz muestra las cuatro imágenes para que puedas inspeccionar cómo se tomó la decisión. El servidor procesa la foto en memoria y no la guarda. El ancho mostrado se mide en píxeles, no en metros.

## Cómo interpretar los resultados

El programa produjo un par geométrico en las seis fotos originales. Eso no significa 100% de exactitud: no contamos con etiquetas oficiales para afirmar que cada línea es correcta.

Al oscurecer las fotos a un 55% de brillo, no produjo un par en ninguna. Con desenfoque produjo un par en cinco de seis. Estos fallos muestran la sensibilidad del método. Las imágenes se usaron durante el desarrollo y no son una evaluación independiente.

Para repetir: instala requirements.txt, ejecuta `python real_benchmark.py` y abre real-results.json. Para las pruebas ejecuta `python -m unittest discover -v`.

## Explicación para entrevista

“I built a Python-backed demo that processes real road photographs. It combines color filtering, edge detection, Hough segments and RANSAC. I evaluated output availability under brightness and blur changes. The main limitation is sensitivity to lighting and curved lanes. The sample collection does not provide verified accuracy.”

Aprende a explicar por qué escogimos estos pasos y qué cambiarías. Distingue la ayuda de IA de las decisiones que comprendes y puedes defender.


## Mejoras del 11 de octubre de 2026

Añadimos una normalización de iluminación y la comparamos con la versión fija. En las seis fotos oscurecidas, la versión fija no apoyó pares y la adaptativa sí. Eso no significa exactitud de 100%: seguimos sin etiquetas oficiales de carriles. Usa el selector Lighting method y ejecuta lighting_benchmark.py.

La página evidence.html conecta resultados, pruebas y código para un revisor. RECRUITER_GUIDE.md relaciona capacidades demostradas con áreas de tus candidaturas y señala lo que estos proyectos todavía no demuestran.
