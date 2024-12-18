---
layout: post
title: "Curso de IA generativa de Kaggle y Google"
date: 2024-12-16 10:00:00
author: teresa
lang: es
categories: ia
tags: ia, LLM, Google, Kaggle, Gemini
header-image: 2024-12-16-genai-course/header.png
---


Desde Kaggle y Google han lanzado un curso de IA generativa que cubre los siguientes aspectos:
- Introducción a Large Language Models (LLMs), los modelos fundacionales
- Prompt Engineering
- Embeddings
- RAG
- Agentes
- LLMs de ámbito específico (*i.e.*, seguridad informática y ámbito médico)
- MLOps en el contexto de IA generativa

El curso se compone principalmente de *whitepapers* de Google y podcasts derivados de estos mismos, *notebooks* de Kaggle que se pueden ejecutar a través de nuestra cuenta de Kaggle o exportar como jupyter notebooks o a Google Colab, y cinco videos de Youtube en los que se hace un resumen de los *notebooks* y se discuten temas relacionados con los *whitepapers* con expertos en el área. Se han creado también podcasts que resumen los *whitepapers*. Como apunte de interés, los podcasts han sido generados con IA, a través de Notebook LM.

A pesar de que este curso se planteó como un curso en vivo de cinco días, los materiales se encuentran ya en abierto y se pueden encontrar en [Kaggle](https://www.kaggle.com/learn-guide/5-day-genai). Hay también un hilo específico en su canal de Discord en el que se pueden consultar dudas o solicitar más información.

Durante el curso, el LLM empleado es Gemini de Google, por lo que para ejecutar los *notebooks* es necesario obtener una API Key gratuita. Sin embargo, si se desease, el conocimiento obtenido de los *notebooks* se puede aplicar facilmente a otras LLMs adaptando los métodos.

Si tienes interés en el mundo de las LLMs y sus usos actuales, este curso te va a permitir tanto iniciarte en el tema como empezar a profundizar en el estado del arte de la IA generativa. Los *whitepapers* son una introducción teórica interesante y los *notebooks* permiten explorar una implementación básica de los aspectos abordados en el curso. Los *whitepapers* de los primeros tres días son imprescindibles para aportarnos una introducción al estado de arte de las LLMs. No recomiendo centrarse en exceso en el código de ejemplo que aparece en estos ya que para ello recomiendo ir a los *notebooks*, que proporcionan un desarrollo más detallado.  Si se dispone de más tiempo o se desea más información, recomiendo recurrir a los videos de Youtube. Los podcasts, al ser resúmenes, son lo más prescindible pero nos pueden ayudar a entender conceptos que encontremos particularmente complicados. Es también posible, una vez entendidos los conceptos correspondientes al día 1 centrarse en el tema en concreto que nos interese ya que los *whitepapers* y *notebooks* tratan temas independientes. Sin embargo, recomiendo no pasar por alto el día 3, pues es especialmente relevante porque se centra en el uso de agentes. Este es un tema candente que está permitiendo llevar más allá a las LLMs. Consiste en asignar roles específicos a varias LLMs y combinar estos modelos para realizar tareas complejas que no se podrían haber resuelto con *prompt engineering* únicamente.