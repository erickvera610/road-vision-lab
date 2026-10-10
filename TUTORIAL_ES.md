# Tutorial en español: Road Vision Lab

## 1. Qué problema resuelve

La computadora recibe una imagen: una matriz de números de 0 a 255. Ahora el proyecto busca píxeles que podrían formar carriles; ya no recibe los puntos del carril como entrada.

## 2. Pruébalo primero

Abre https://erickvera610.github.io/road-vision-lab/ . La demo funciona en tu navegador. Cambia un control y compara la salida. Los datos ficticios no son usuarios reales; los ejemplos tampoco representan trabajo realizado para una empresa.

## 3. Instálalo paso a paso

1. Instala Python desde python.org y Git desde git-scm.com.
2. Abre PowerShell y escribe `python --version` y `git --version`.
3. Escribe `git clone https://github.com/erickvera610/road-vision-lab.git`.
4. Escribe `cd road-vision-lab`.
5. Escribe `python app.py` y mantén abierta la terminal.
6. Abre http://127.0.0.1:8000 y prueba los controles.
7. Detén el servidor con Ctrl+C.

## 4. La secuencia de trabajo

`Image pixels → grayscale ROI → gradients → RANSAC → line overlay`

**ROI** es la región de interés: aquí, la parte inferior de la imagen. Un **gradiente** mide cómo cambia el brillo entre vecinos; ayuda a localizar bordes. **RANSAC** propone muchas rectas usando pares de puntos y conserva la que reúne más puntos cercanos. Los **inliers** son esos puntos cercanos. Después ajustamos otra vez la recta con mínimos cuadrados. El error de ancho compara la estimación con el ancho conocido de la escena ficticia. En una fotografía subida no conocemos ese ancho: el programa debe mostrar “No ground truth”, no inventar una precisión.

Prueba la escena sintética, aumenta el ruido y después carga una fotografía. Si no detecta dos líneas, eso es un resultado válido. Detectar dos líneas tampoco garantiza que sean carriles.

## 5. Leer el código con calma

Empieza por `core.py` y busca `run`. Después abre el archivo especializado indicado en README. Sigue una sola entrada hasta su salida. Lee las pruebas: cada una describe un comportamiento concreto. Por último, revisa `enhanced.js` para comparar la versión del navegador.

## 6. Reproducir los resultados

```bash
python -m unittest discover -v
node test_enhanced.cjs
python benchmark.py
```

Abre `benchmark-results.json` y compara su resumen con `CASE_STUDY.md`. El reporte incluye una hora real de ejecución. Los experimentos con semillas repetidas muestran varios resultados; no escogemos solo el mejor. Las métricas sintéticas de JavaScript pueden diferir de Python.

## 7. Tu siguiente mejora personal

Añade escenas con sombras y curvas; registra cuándo falla en lugar de cambiar las imágenes para ocultarlo. Luego añade un dataset de imágenes con licencia y anotaciones, separando escenas de entrenamiento y prueba.

```bash
git switch -c feature/my-improvement
# Edita código y ejecuta las pruebas
git add .
git commit -m "Describe the actual behavior change"
git push -u origin feature/my-improvement
```

Abre un pull request y explica problema, solución, resultado y límite. Se usó asistencia de IA para construir esta base. En una entrevista distingue lo que recibiste, lo que estudiaste y lo que realmente cambiaste.

## 8. Practicar la entrevista

- What problem does this application solve?
- Which data are available when the prediction is made?
- What is the simplest baseline?
- How did you avoid data leakage or inconsistent state?
- Which result surprised you?
- What failure case remains?
- What did you personally improve?

Primero responde en español. Después prepara cuatro frases cortas en inglés: problema, método, resultado y limitación. Usa solo resultados documentados.
