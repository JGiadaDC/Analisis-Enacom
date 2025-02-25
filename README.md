# Analisis de datos ENACOM
## _Proyecto individual de analisis de datos de Telecomunicaciones_

![Alt Text](https://github.com/JGiadaDC/Analisis-Enacom/raw/main/Logo_enacom.png)

Para este proyecto se proporcionaron unas tablas de datos de la empresa de telecomunicaciones argentina (ENACOM) con el objetivo de realizar un analisis completo del sector, con un particular enfoque en el acceso a internet.  El análisis busca identificar oportunidades de crecimiento, mejorar la calidad del servicio y proponer soluciones personalizadas a posibles clientes.
El proceso completo incluyo:

- ETL y EDA de los datos
- Analisis y calculo de los KPI
- Creacion de Dashboard interactivo
- Conclusiones y medidas de implementacion

## Requerimentos

- python correctamente instalado 
- streamlit 

Puedes emcontrar mas informaciiones sobre [streamlit] en [https://streamlit.io/][df1]

> Streamlit es una interesante libreria de python 
> que permite crear dashnoards interactivos
> para la visualizaciones de datos


### Contenidos del Repositorio
 
- ETL-EDA.ipynb: Análisis Exploratorio de Datos detallado, incluyendo gráficos, análisis de valores faltantes, outliers y registros duplicados.
- KPI.ipynb: analisis de los Kpi graficados
- data/: Datos limpios utilizados para el análisis
- sttreamlit.py file py de streamlit para la visualizaciones

## Etapas de analisis
> IMPORTANTE
> Primero hay que explorar los datos "crudos" en formato Excel proporcionados por la empresa, para tener una idea mas clara de cuales de todos los datos utilizar efectivamente para el analisis. 

### ETL-EDA
El notebook de EDA (ETL-EDA.ipynb) incluye:

-Búsqueda de valores faltantes: Identificación y tratamiento de datos incompletos.
-Detección de valores atípicos: Análisis de outliers y su impacto en el dataset.
-Registros duplicados: Identificación y eliminación de registros redundantes.
-Visualizaciones: Gráficos coherentes según la tipología de variables (histogramas, box plots, scatter plots, etc.).
-Conclusiones: Comentarios y análisis en celdas Markdown.

Se importan las librerias necesarias y el file excel proporcionado, con todas sus hojas, imprimendo los nombres de cada una 
```sh
all_sheets = pd.read_excel('Internet.xlsx', sheet_name=None)

print("Nombre de las hojas:", all_sheets.keys())
```
para luego convertrir las hojas que se consideren relevantes en dataframes separados y poder analizar los datos. 
```sh
# Ahora `all_sheets` es un diccionario donde la
for sheet_name, df in all_sheets.items():
    print(f"Foglio: {sheet_name}")
    print(df.head())

# Creamos variables separadas para cada DF, por ejemplo
vel_perc = all_sheets['Velocidad % por prov']
```

**vel_perc:** nos brinda datos sobre la media de descarga por provincia, por ano. 
Utilizando los graficos adecuados se pueden notar muchos outliers, o sea valores que difieren de la media de bajada. Esto podria ser por las zonas mas remotas donde el internet no accede bien. 
Seria interesante notar cuales son estas zonas:
Para este proposito se crea un grafico que ponga en relacion media de bajada y provincia. 

Veremos, como esperado, que en capital federal la media de bajada destaca respecto a otras provincias  como Santa Cruz o Tierra del Fuego. Que se podria hacer para llegar a una buena media en estas zonas? 

**penetracion:** es un df que une los accesos por cada 100 hogares con los de 100 habitantes.
De estos graficos se notan la cantidad de outliers. Podria significar que el acceso a internet no tiene un valor medio a nivel nacional, sino cambia mucho de zona a zona. hay que destacar, pero, que a pesar del descostarse de los valores de la media, parecen seguir una tendencia comun o sea suben, lo que nos hace entender que en general el acceso va mejorando.

**ingresos:** se explora el df ingresos y lo primero que se nota es que las eentradas son en Pesos Argentino.  
Esto es un aspecto importante a considerar, a la hora de graficar y calcular eventuales KPI, ya que la inflacion ha afectado notevolmente el Pais en estos anos. Se decide actuar una medida de proporcionalidad, dolarizando los ingresos.
```sh
# Calcular los ingresos en USD usando la columna 'Ingresos (miles de pesos)' y 'Tipo de cambio'
ingresos_usd['Ingresos (USD)'] = ingresos_usd['Ingresos (miles de pesos)'] / ingresos_usd['Cambio']
```
***Importante --*** se decidio tomar en cuenta como cambio el proedio del ano y no el cambio efectivo. Esto afectara un poco los valores y las graficas que se sacaran.

**acc_vel:** info sobre las velocidades en cada Provincia, por periodo.
Podemos ver cuales son las provincias que tienen las velocidades de conexion mas bajas, para evenyualmente implementar acciones con el objetivo de proporcionar una velocidad mas alta en estas zonas.

**acc_tec:** de estos datos se puede entender cuales son las tecnologias mas usadas en las varias provincias.
El uso de Fibra optica es un punto interesante a evaluar en este contexto, ya que suele representar la tecnologia mas avanzada deseable para los accesos a internet, debido a su velocidad y estabilidad.
Por esto se podria crear un nuevo KPI.

### Dashboard Interactivo
El dashboard <streamlit.py> permite:
Exploración de datos: Filtros interactivos para detallar la información.
Visualización clara: Gráficos adecuados para cada tipo de variable.
Estética y funcionalidad: Diseño limpio y fácil de interpretar.

### Análisis de KPIs
El análisis de KPIs (KPI_analysis.ipynb) incluye:

-KPI propuesto: Aumento del 2% en el acceso al servicio de internet para el próximo trimestre por cada 100 hogares, por provincia.
KPIs adicionales:
- Incremento de la media de bajada para alcanzar la media nacional en 2025.
- Incremento en el uso de la fibra optica.
Cada KPI es medido, graficado y analizado.

#### Calculo del KPI propuesto: 
Aumentar en un 2% el acceso al servicio de internet para el próximo trimestre, cada 100 hogares, por provincia

```sh
# Calcular el nuevo acceso proyectado
penetracion['Nuevo_Acceso_por_100_hogares'] = penetracion['Accesos por cada 100 hogares'] * 1.02
```

#### Conclusiones Basadas en el KPI Calculado:
- Evaluación del Cumplimiento del Objetivo:

Cumplimiento del Objetivo del 2%: Si la mayoría de las provincias han alcanzado o superado el aumento del 2% en acceso a internet, se puede concluir que las estrategias implementadas están siendo efectivas.
Incumplimiento del Objetivo: Si varias provincias no han alcanzado el aumento del 2%, se debe investigar qué factores están impidiendo el crecimiento esperado.

- Identificación de Áreas con Mayor y Menor Crecimiento:

Áreas con Mayor Crecimiento: Provincias que muestran un crecimiento significativamente mayor al 2% pueden estar beneficiándose de mejoras en infraestructura, políticas locales favorables, o una mayor demanda de servicios de internet. Estas áreas representan oportunidades de expansión y desarrollo continuo.
Áreas con Menor Crecimiento o Decrecimiento: Provincias que no alcanzan el 2% de crecimiento o incluso muestran un decrecimiento necesitan atención especial. Pueden estar enfrentando desafíos como falta de infraestructura, problemas económicos, o baja adopción tecnológica.

- Comparación Interprovincial:

Comparación entre Provincias: Analizar cómo se comparan las provincias entre sí puede revelar desigualdades en el acceso a internet. Provincias con acceso significativamente menor pueden necesitar estrategias personalizadas para mejorar la penetración del servicio.

- Tendencias y Patrones:

Tendencias Generales: Observar tendencias generales en el acceso a internet puede ayudar a identificar patrones. Por ejemplo, si ciertas regiones geográficas muestran consistentemente bajo crecimiento, esto puede indicar una necesidad de enfoques regionales específicos.

#### KPI 2
Incrementar la media de bajada en el proximo ano, hasta la media nacional, en las provincias que no llegan a la media. 

Calculo: calcular la media de bajada nacional por el ano 2023 y establecerla como meta para el 2025. Se tomo en cuenta un plazo de tiempo largo para tener suficiente tiempo para monitorar  implemetar medidas, ya que muchas provincias estan mucho por debajo de la media todavia. Luego calcular las provincias que no alcanzan la media y graficarlas.

Descripción: Incrementar la velocidad de bajada promedio en las provincias que, al 2023, no alcanzan la media nacional de 77.78 Mbps. El objetivo es que todas las provincias por debajo de esta media la alcancen para el año 2025.
Provincias como Catamarca, Chaco, y Chubut tienen velocidades de bajada significativamente menores que la media nacional. Estas provincias necesitarán aumentar su velocidad de bajada en varios Mbps para alcanzar la meta establecida para 2025.
Provincias por Debajo de la Media Nacional en 2023

Estrategias para Alcanzar el KPI
-Inversiones en Infraestructura: Desarrollar y mejorar la infraestructura de red en las provincias identificadas.
-Actualización Tecnológica: Implementar tecnologías más avanzadas como la fibra óptica.
-Programas de Incentivos: Ofrecer incentivos a proveedores locales para mejorar sus servicios.
-Colaboración con Autoridades Locales: Trabajar con gobiernos locales para facilitar el despliegue de infraestructura.
-Periodicidad: Monitorear trimestralmente el progreso de la velocidad de bajada en las provincias objetivo.
-Herramientas: Utilizar dashboards interactivos para visualizar el progreso y ajustar estrategias según sea necesario.
-Indicadores Complementarios: Evaluar también otros indicadores como la satisfacción del cliente y la tasa de penetración del mercado.

-Implementar programas de subsidios para apoyar la mejora de la infraestructura de Internet en regiones desfavorecidas.
Estos subsidios pueden estar dirigidos tanto a proveedores de servicios de Internet como a los consumidores finales.

- Educación y concienciación:
Lanzar campañas de educación y concienciación para informar a las comunidades sobre los beneficios de mejorar la infraestructura de Internet.
Involucrar a las comunidades locales en el proceso de planificación y mejora de las conexiones.

#### KPI 3:
Incremento percentual en el uso de fibra optica en el proximo trimestre

Del EDA se nota que a parte Buenos Aires, el acceso a la fibra optica no esta muy bien 
distribuido en el Pais, en general es bastante bajo. Se podria incrementar el uso 
de esta tecnologia? Como?

Implementación del KPI de Incremento en el Uso de la Fibra Óptica
El KPI del incremento en el uso de la fibra óptica puede calcularse como el 
porcentaje de crecimiento de los accesos de fibra óptica de un periodo a otro.
Para el calculo de este KPI, primero voy a medir el incremento en el ano pasado (2022-2023)

```sh
aumento_percentuale = ((fibra_2023 - fibra_2022) / fibra_2022) * 100
```

Hay que remarcar que se excluyo Buenos Aires del calculo, ya que tiene muy buen acceso, y afectaria el valor de aumento percentual real.

```sh
internet['Acceso proyectado fibra optica'] = internet['Accesos fibra optica'] * 1.13
```

Calcular el incremento trimestral 
(1+R)=(1+r) ^ 4 donde R = incremento anual y r = incremento trimestral

incremento_anual = 46% = 0.4601
incremento_trimestral = [((1 + 0,4601) / 100) ** (1/4)] - 1 = 0.99 = 9,9%

#### Conclusiones 
Crecimiento Sostenido: Un aumento del 9.9% indica un crecimiento sólido en la adopción de fibra óptica. Esto sugiere que más usuarios o entidades están optando por esta tecnología, lo cual podría estar impulsado por una mayor demanda de conexiones de alta velocidad y mayor ancho de banda.

Inversión en Infraestructura: Es posible que los proveedores de servicios estén invirtiendo en expandir y mejorar la infraestructura de fibra óptica para satisfacer la creciente demanda. Este tipo de inversión es crucial para mantener y mejorar la calidad del servicio y la capacidad de respuesta a las necesidades del mercado.

Tendencia hacia Conexiones de Alta Velocidad: Un aumento significativo en la adopción de fibra óptica también puede indicar una tendencia creciente hacia conexiones de Internet de alta velocidad. Esto es importante en un contexto donde las aplicaciones y servicios en línea requieren cada vez más capacidad de banda ancha.

Impacto en la Competitividad: Las empresas y regiones que invierten en infraestructura de fibra óptica pueden experimentar beneficios en términos de competitividad económica y digital. La conectividad de alta velocidad es crucial para la innovación, la eficiencia empresarial y el acceso equitativo a recursos digitales.

Desafíos y Oportunidades: Aunque un crecimiento del 9.9% es positivo, también puede plantear desafíos en términos de gestionar la expansión de la red y asegurar que todos los usuarios tengan acceso equitativo. Esto podría presentar oportunidades para mejorar políticas públicas y regulaciones que promuevan la inversión en infraestructura digital.
