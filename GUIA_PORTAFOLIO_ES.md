# Cómo entender y presentar este proyecto

1. Lee primero el problema y los datos en README.md.
2. Ejecuta la demo para entender las entradas y salidas.
3. Ejecuta las pruebas: `python -m unittest discover -v`.
4. Reproduce el experimento indicado abajo. Mira el resultado y compáralo con la referencia sencilla.
5. Explica qué datos se reservaron para prueba, qué decisiones se tomaron antes y en qué casos falla.

Ejecuta `python stress_benchmark.py`. El programa busca píxeles claros, calcula bordes y ajusta líneas tolerando puntos incorrectos. Detectó 30 de 45 escenas artificiales; las 15 de bajo contraste fallaron. Presenta también esos fallos: explican el límite del método. No se entrena una red neuronal en este proyecto.

Para una entrevista, prepara una explicación de dos minutos: problema → datos → método → comparación → resultado → límites. Identifica qué código te ayudó a generar IA y demuestra que entiendes cada decisión.
