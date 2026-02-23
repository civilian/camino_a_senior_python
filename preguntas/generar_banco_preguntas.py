#!/usr/bin/env python3
"""
Genera un banco de preguntas de entrevista Senior Python a partir de
habilidades_python.md y plantillas, con el objetivo de llegar a ~10.000 preguntas.
"""

import re
from pathlib import Path

HABILIDADES_PATH = Path(__file__).resolve().parent.parent / "habilidades_python.md"
OUTPUT_DIR = Path(__file__).resolve().parent / "banco_partes"
PREGUNTAS_POR_ARCHIVO = 100

# Plantillas de preguntas: {concept} se reemplaza por el concepto
PLANTILLAS = [
    "¿Qué es {concept}?",
    "¿Cómo funciona {concept} en Python?",
    "¿Cuándo usarías {concept}?",
    "¿Cuándo no usarías {concept}?",
    "Explica {concept} con un ejemplo.",
    "¿Qué ventajas tiene {concept}?",
    "¿Qué desventajas o limitaciones tiene {concept}?",
    "¿Cómo implementarías {concept} en un proyecto real?",
    "Diferencia entre {concept} y alternativas típicas.",
    "¿Qué errores comunes se cometen al usar {concept}?",
    "¿Cómo depurarías problemas relacionados con {concept}?",
    "¿Cómo testearías código que usa {concept}?",
    "¿Qué consideraciones de rendimiento tiene {concept}?",
    "¿Qué consideraciones de seguridad tiene {concept}?",
    "¿Cómo escalarías un sistema que usa {concept}?",
    "¿Qué patrones de diseño se relacionan con {concept}?",
    "¿Qué alternativas existen a {concept} y cuándo elegirías cada una?",
    "¿Cómo documentarías el uso de {concept} en un equipo?",
    "¿Qué dependencias suele tener {concept} en el ecosistema Python?",
    "¿Qué versiones de Python soportan {concept} o sus librerías típicas?",
    "¿Qué es el anti-patrón más común al usar {concept}?",
    "¿Cómo integrarías {concept} en un pipeline CI/CD?",
    "¿Qué métricas o observabilidad aplicarías a {concept}?",
    "¿Cómo manejarías fallos o reintentos con {concept}?",
    "¿Qué convenciones o mejores prácticas existen para {concept}?",
    "¿Cómo migrarías un proyecto legacy a usar {concept}?",
    "¿Qué impacto tiene {concept} en la mantenibilidad del código?",
    "¿Cómo combinarías {concept} con otros conceptos del ecosistema Python?",
    "¿Qué preguntas harías en una entrevista sobre {concept}?",
    "¿Qué recursos (docs, libros, cursos) recomendarías para dominar {concept}?",
    "¿Qué decisiones de diseño tomarías al adoptar {concept}?",
    "¿Cómo explicarías {concept} a un desarrollador junior?",
    "¿Qué trade-offs implica elegir {concept}?",
    "¿Cómo garantizarías consistencia o idempotencia al usar {concept}?",
    "¿Qué configuración típica usarías para {concept} en producción?",
    "¿Cómo monitorizarías una aplicación que usa {concept}?",
    "¿Qué problemas de concurrencia o threading puede introducir {concept}?",
    "¿Cómo usarías {concept} en un contexto de microservicios?",
    "¿Qué impacto tiene {concept} en la latencia o el throughput?",
    "¿Cómo harías rollback o recuperación ante fallos con {concept}?",
    "¿Qué requisitos de infraestructura suele tener {concept}?",
    "¿Cómo modelarías datos o dominios al usar {concept}?",
    "¿Qué estándares o RFCs se relacionan con {concept}?",
    "¿Cómo evitarías sobrecarga o abuso al usar {concept}?",
    "¿Qué controles de acceso o permisos aplicarías a {concept}?",
    "¿Cómo versionarías APIs o contratos que usan {concept}?",
    "¿Qué estrategia de caché usarías con {concept}?",
    "¿Cómo diseñarías tests de integración que involucren {concept}?",
    "¿Qué logging o trazabilidad aplicarías a {concept}?",
    "¿Cómo desplegarías en Kubernetes una aplicación que usa {concept}?",
    "¿Qué harías para reducir la deuda técnica al usar {concept}?",
    "¿Cómo priorizarías tareas en un proyecto que adopta {concept}?",
    "¿Qué riesgos típicos hay al adoptar {concept} y cómo mitigarlos?",
    "¿Cómo evaluarías si {concept} es la solución correcta para un problema?",
    "¿Qué preguntas de diseño harías en una entrevista sobre {concept}?",
    "¿Cómo explicarías el flujo de datos cuando se usa {concept}?",
    "¿Qué alternativas open source existen para {concept}?",
    "¿Qué costes operativos puede tener {concept}?",
    "¿Cómo asegurarías alta disponibilidad con {concept}?",
    "¿Qué formación recomendarías a un equipo que va a usar {concept}?",
    "¿Cómo compararías {concept} con soluciones en otros lenguajes?",
]

# Plantillas de respuesta (mismo orden que PLANTILLAS). {concept} y {seccion}. Respuestas largas y con contexto.
RESPUESTAS = [
    """**Respuesta:** {concept} forma parte del área «{seccion}» en el ecosistema Python. Puede ser un paradigma, una librería, un protocolo o una práctica de desarrollo. Conocer su definición exacta te permite explicarlo en una entrevista y decidir cuándo aplicarlo en un proyecto.

Para una definición precisa y ejemplos de uso, consulta siempre la documentación oficial del término. El archivo [preguntas_respuestas_entrevista_senior_python.md](preguntas_respuestas_entrevista_senior_python.md) incluye respuestas desarrolladas para temas relacionados del mismo ámbito, con más detalle y contexto práctico.""",
    """**Respuesta:** En Python, {concept} se implementa normalmente mediante la biblioteca estándar o paquetes de la comunidad (PyPI). El comportamiento concreto depende del tipo de concepto: si es una librería, hay que revisar su API y su documentación; si es un patrón o una práctica, conviene buscar ejemplos en la documentación o en el archivo de respuestas desarrolladas.

La documentación oficial es siempre la fuente de verdad: ahí se explica el contrato, las opciones de configuración y las versiones soportadas. En entrevistas, demostrar que sabes dónde buscar esta información da buena imagen de madurez técnica.""",
    """**Respuesta:** Conviene usar {concept} cuando el problema que tienes encaja con lo que resuelve: por ejemplo, cuando necesitas sus ventajas de estructura, rendimiento o integración y no existe una alternativa más simple que cubra el caso de uso. Antes de adoptarlo, revisa la documentación y las mejores prácticas del área «{seccion}» para no aplicarlo donde no aporta valor real.

En un contexto senior, se valora que sepas justificar la decisión: explicar por qué este concepto (y no otro) es adecuado para el requisito, y qué criterios has usado para descartar alternativas. Documentar esta decisión en el proyecto ayuda al equipo y a futuras revisiones.""",
    """**Respuesta:** No es recomendable usar {concept} cuando el requisito no lo justifica, cuando existen alternativas más sencillas que bastan para el caso, o cuando el equipo no tiene experiencia y el coste de adopción (formación, complejidad operativa) es alto. En esos casos, es preferible valorar primero soluciones más acotadas y documentar por qué se descarta {concept}, para que el contexto quede claro para todo el equipo.

Adoptar una tecnología o patrón “por moda” o sin evaluar el coste real suele generar deuda técnica y frustración. Un senior propone alternativas más simples cuando el problema no requiere toda la potencia (o complejidad) de {concept}.""",
    """**Respuesta:** Un ejemplo concreto de {concept} en Python suele encontrarse en la documentación oficial o en tutoriales del ecosistema. En [preguntas_respuestas_entrevista_senior_python.md](preguntas_respuestas_entrevista_senior_python.md) hay respuestas con ejemplos para temas del mismo ámbito («{seccion}»), que puedes usar como referencia para preparar la entrevista o para explicar el concepto en equipo.

Si {concept} es una librería, su repositorio en GitHub o la página en PyPI suelen incluir snippets de uso y ejemplos mínimos. Replicar uno de esos ejemplos en local y luego adaptarlo a tu caso es una forma práctica de aprender y de validar que encaja con tu problema.""",
    """**Respuesta:** Las ventajas de {concept} dependen del contexto: suelen incluir mejor estructura del código, rendimiento, mantenibilidad o integración con el resto del stack. Para concretar en tu caso, revisa la documentación y las guías de la comunidad; en el archivo de respuestas desarrolladas hay explicaciones más largas para conceptos del área «{seccion}» que detallan beneficios y cuándo se notan.

En una entrevista, es importante no limitarse a listar ventajas genéricas: intenta relacionar cada ventaja con un problema real que hayas resuelto o con un requisito concreto del proyecto. Eso demuestra experiencia aplicada y no solo conocimiento teórico.""",
    """**Respuesta:** Las limitaciones típicas suelen ser: mayor complejidad, dependencias adicionales, curva de aprendizaje o requisitos de infraestructura. Es fundamental evaluar estos trade-offs antes de adoptar {concept} y documentar la decisión para que el equipo entienda los riesgos y las condiciones bajo las que se eligió.

Si en tu contexto el coste supera el beneficio (por ejemplo, plazos muy ajustados o equipo pequeño), considera alternativas más ligeras o un enfoque incremental: adoptar solo una parte del concepto o introducirlo en un módulo acotado antes de extenderlo.""",
    """**Respuesta:** En un proyecto real, al implementar {concept} conviene seguir un orden claro: (1) acotar su alcance y responsabilidades para no mezclarlo con otras capas del sistema; (2) integrarlo de forma coherente con el resto del stack (configuración, logging, tests); (3) documentar cómo se usa, cuándo y qué decisiones de diseño se tomaron; y (4) añadir tests que cubran los flujos críticos y los casos de error.

Puedes apoyarte en patrones y ejemplos descritos en [preguntas_respuestas_entrevista_senior_python.md](preguntas_respuestas_entrevista_senior_python.md). En entrevistas, explicar que has implementado algo similar en un proyecto anterior (con qué restricciones y qué resultado) suele ser más convincente que solo describir los pasos teóricos.""",
    """**Respuesta:** {concept} se diferencia de otras opciones del ecosistema en alcance, modelo de uso (API, configuración) o en el tipo de problemas que resuelve. Para comparar con alternativas concretas, consulta la documentación oficial y, si existe, alguna comparativa o guía de elección en el área «{seccion}».

En un diseño senior, la elección entre varias opciones se justifica con criterios explícitos: requisitos funcionales, rendimiento, mantenimiento a largo plazo y experiencia del equipo. Tener una tabla o documento corto que resuma “cuándo usamos A frente a B” ayuda a mantener coherencia en el proyecto.""",
    """**Respuesta:** Errores frecuentes al usar {concept} incluyen: usar la API de forma incorrecta o incompleta (por ejemplo, no cerrar recursos o no manejar excepciones), no contemplar casos límite o fallos (timeouts, datos inválidos), e ignorar el impacto en rendimiento o seguridad. Para evitarlos, sigue la documentación y las guías de buenas prácticas, y revisa el código en equipo.

En code reviews, conviene tener una checklist que incluya estos puntos cuando el código toca {concept}. Si un error se repite, documentarlo (por ejemplo en el README o en un ADR) para que el resto del equipo no caiga en lo mismo.""",
    """**Respuesta:** Para depurar problemas relacionados con {concept} sigue un orden claro: (1) reproducir el fallo de forma estable, idealmente con un test o un script mínimo que no dependa del resto del sistema; (2) usar logging y, si hace falta, breakpoints (pdb) para seguir el flujo y ver el estado en el punto de fallo; (3) aislar el componente que usa {concept} y verificar su configuración y dependencias. Revisa también los logs de la aplicación y del propio {concept} si los expone.

En entornos de producción, la reproducibilidad puede ser difícil; en ese caso, los logs estructurados (con request_id, usuario, etc.) y las trazas distribuidas son fundamentales para reconstruir el escenario sin tener que adivinar.""",
    """**Respuesta:** Para testear código que usa {concept} combina varios niveles: tests unitarios que mockeen dependencias externas cuando convenga, para ir rápido y aislar la lógica; tests de integración con instancias reales o contenedores para los flujos críticos; y cobertura de casos de error (timeouts, datos inválidos, fallos de red). La sección de Testing en [preguntas_respuestas_entrevista_senior_python.md](preguntas_respuestas_entrevista_senior_python.md) amplía estrategias, herramientas (pytest, fixtures, coverage) y cuándo usar mocks frente a integración real.

Un senior no se limita a “tener tests”: asegura que los tests sean mantenibles, que fallen cuando algo se rompe y que den confianza para refactorizar. Documentar cómo ejecutar los tests y qué entorno necesitan (variables, servicios) es parte del trabajo.""",
    """**Respuesta:** Al usar {concept}, ten en cuenta el uso de CPU, memoria, I/O y la latencia que introduce. Mide con profiling y métricas antes y después de cambios; define objetivos de rendimiento (por ejemplo p95 de latencia o throughput máximo) y vigila que no se degraden con nuevas versiones o más carga. En sistemas con mucha carga, las decisiones de diseño alrededor de {concept} pueden ser críticas para cumplir los SLOs.

Herramientas como cProfile, memory_profiler o tracemalloc ayudan a localizar cuellos de botella. En producción, métricas exportadas (Prometheus, etc.) y dashboards permiten detectar regresiones sin tener que reproducir manualmente.""",
    """**Respuesta:** Desde el punto de vista de seguridad al usar {concept}: validar y sanitizar todas las entradas que afecten a {concept} (evitar inyección, datos malformados); no exponer datos sensibles en logs o respuestas; aplicar el principio de menor privilegio en permisos y configuración; y revisar dependencias (por ejemplo con bandit, pip-audit o safety) para vulnerabilidades conocidas.

En una entrevista senior se valora que menciones no solo “validar entradas” sino también aspectos como secretos (no hardcodear, usar gestores de secretos), rate limiting si aplica, y qué harías ante un incidente de seguridad (containment, análisis, comunicación).""",
    """**Respuesta:** Para escalar un sistema que usa {concept} hay que identificar primero el cuello de botella: CPU, memoria, I/O o red. Según dónde esté el límite, se escala de forma horizontal (más instancias) o vertical (más recursos por instancia). Según el caso, pueden ser necesarias colas, caché, particionamiento de datos o réplicas. La documentación de {concept} y las guías del área «{seccion}» suelen dar pistas para patrones de escalado típicos.

Antes de escalar, conviene medir: no asumir que “más instancias” resuelve todo si el problema es un cuello de botella compartido (por ejemplo una base de datos o un servicio externo). Diseñar para escalar desde el principio (estado externo, idempotencia) suele ser más barato que refactorizar después.""",
    """**Respuesta:** Los patrones de diseño que se relacionan con {concept} dependen del dominio: por ejemplo repositorio, factory, estrategia, observer, CQRS. Para ver cómo se aplican en el ecosistema Python y en el área «{seccion}», consulta la sección de Arquitectura en [preguntas_respuestas_entrevista_senior_python.md](preguntas_respuestas_entrevista_senior_python.md), donde se explican varios patrones con contexto y cuándo usarlos.

En un diseño senior, los patrones no se aplican “por lista”: se eligen en función del problema (desacoplamiento, testabilidad, escalabilidad) y se documenta por qué ese patrón y no otro en el contexto del proyecto.""",
    """**Respuesta:** Las alternativas a {concept} son otras librerías o enfoques del mismo ámbito. La elección debe basarse en requisitos funcionales, rendimiento medido cuando sea posible, mantenimiento del proyecto (¿quién mantiene la librería?, ¿hay releases recientes?) y experiencia del equipo. La documentación oficial y las comparativas en la comunidad (blogs, repos, benchmarks) ayudan a decidir con criterio.

Mantener una tabla o documento interno de “cuándo usamos X frente a Y” evita que cada desarrollador tome decisiones distintas y facilita el onboarding. Revisar esa decisión de vez en cuando (por ejemplo cuando sale una versión mayor) es buena práctica.""",
    """**Respuesta:** Documenta el uso de {concept} en el README o en la documentación del proyecto: para qué se usa, cómo se configura (variables de entorno, archivos), ejemplos mínimos de uso y enlaces a la documentación oficial. Mantén esta documentación actualizada cuando cambie la versión o la forma de uso, y compártela con el equipo en onboarding y en revisiones de código.

En equipos senior se suele complementar con ADRs (Architecture Decision Records) que explican por qué se eligió {concept}, qué alternativas se consideraron y bajo qué condiciones se revisaría la decisión. Eso evita que, con el tiempo, nadie recuerde el contexto original.""",
    """**Respuesta:** Las dependencias de {concept} suelen ser otras librerías Python (declaradas en requirements.txt o pyproject.toml), servicios externos (bases de datos, APIs, colas) o requisitos de sistema (versión de Python, librerías nativas). Revisa el proyecto o el paquete en PyPI para listar dependencias directas e indirectas y evaluar su mantenimiento (¿actualizaciones recientes?) y seguridad (pip-audit, safety).

En proyectos con muchas dependencias, es recomendable fijar versiones (o rangos) y tener un proceso para actualizar de forma controlada, probando que no se introduzcan regresiones o vulnerabilidades.""",
    """**Respuesta:** Para saber qué versiones de Python soporta {concept} (o sus librerías típicas), revisa el changelog y la documentación oficial; en PyPI suele indicarse en los metadatos del paquete (Programming Language :: Python :: 3.x). Muchas librerías actuales soportan al menos Python 3.8 o 3.9 en adelante; verifica antes de fijar la versión del proyecto para no bloquear futuras migraciones.

Si estás en un proyecto legacy con Python 2 o 3.6, ten en cuenta que muchas librerías modernas ya no soportan esas versiones; en ese caso puede ser necesario buscar alternativas o planificar una actualización del runtime.""",
    """**Respuesta:** Un anti-patrón habitual al usar {concept} es aplicarlo en todos los casos sin valorar si aporta valor (“porque sí” o “porque lo usa todo el mundo”), no escribir tests para el código que lo usa, o acoplar demasiado el código a detalles de implementación de {concept}, lo que dificulta cambiar de tecnología después. Para más anti-patrones y buenas prácticas del área «{seccion}», consulta el archivo de respuestas desarrolladas.

En code reviews, conviene estar atento a estos anti-patrones y proponer alternativas más simples cuando el problema no justifica la complejidad. Documentar “qué no hacer” en el README o en la guía del equipo ayuda a mantener coherencia.""",
    """**Respuesta:** Para integrar {concept} en un pipeline CI/CD: ejecutar tests (incluidos los que usan {concept}) en cada commit o pull request; ejecutar lint (flake8, black, mypy, etc.) y, si aplica, comprobaciones de seguridad (bandit, pip-audit); y desplegar solo si todo pasa. La configuración de CI debe reflejar el entorno esperado (variables de entorno, servicios auxiliares como bases de datos o colas) para que los tests sean fiables y no fallen solo en CI por diferencias con local.

Un pipeline bien configurado reduce la deuda técnica y da confianza para refactorizar: si algo se rompe, el pipeline lo detecta antes de llegar a producción. Documentar cómo ejecutar el pipeline en local y qué hace cada etapa facilita el trabajo en equipo.""",
    """**Respuesta:** Aplica métricas y observabilidad relevantes para {concept}: por ejemplo latencia, throughput, tasa de error y uso de recursos (CPU, memoria). Exportar métricas en formato estándar (por ejemplo Prometheus) y usar dashboards (Grafana) para detectar degradación o anomalías. La sección de Observabilidad en el archivo de respuestas desarrolladas amplía opciones (logs estructurados, trazas distribuidas, alertas).

En producción, definir SLOs (por ejemplo “p99 de latencia < X ms”) y alertas que se disparen cuando no se cumplan permite actuar antes de que los usuarios se quejen. Revisar periódicamente qué métricas se usan y cuáles se pueden retirar evita el ruido.""",
    """**Respuesta:** Para manejar fallos y reintentos con {concept}: definir una política de reintentos (cuántos intentos, con qué backoff exponencial o lineal) y timeouts para no bloquear indefinidamente; valorar un circuit breaker si el fallo es persistente (evitar saturar un servicio caído); y, si aplica, fallbacks o respuestas degradadas para que el sistema siga siendo útil. Librerías como tenacity o backoff pueden simplificar la implementación. En el archivo de respuestas hay preguntas sobre resiliencia con más detalle.

En sistemas distribuidos, los fallos son inevitables; un diseño senior asume que las dependencias fallarán y diseña para degradar de forma controlada en lugar de caer en cascada. Documentar la política de reintentos y los criterios de fallback ayuda al equipo de operaciones.""",
    """**Respuesta:** Sigue las convenciones y mejores prácticas del ecosistema: guías de estilo como PEP 8, convenciones acordadas en el equipo (nombres, estructura de carpetas) y la documentación oficial de {concept}. Incluye revisión de código para alinear criterios entre el equipo y documenta las excepciones cuando no se siga una práctica estándar, para que no parezca un descuido.

Tener un linter y formateador configurados (black, isort, flake8) y ejecutados en CI asegura que el estilo se mantenga sin depender solo de la disciplina individual. En equipos grandes, una guía de estilo compartida reduce fricción y facilita que cualquiera pueda leer y modificar el código.""",
    """**Respuesta:** Para migrar un proyecto legacy a {concept} conviene planificar por fases (por ejemplo por módulo o por flujo de negocio), usar feature flags si hace falta para desplegar sin activar todo de golpe, hacer migración gradual y tener siempre un plan de rollback. Documenta el proceso y comunícalo al equipo para reducir riesgos y alinear expectativas.

Cada fase debería dejar el sistema en un estado estable y desplegable. Medir y revisar después de cada fase (incidencias, rendimiento, tiempo de desarrollo) permite ajustar el plan. En proyectos grandes, un equipo dedicado o un “squad” de migración puede ser más eficiente que repartir el trabajo sin foco.""",
    """**Respuesta:** Un uso adecuado de {concept} suele mejorar la mantenibilidad: código más claro, responsabilidades bien definidas y menos acoplamiento oculto. Un uso inadecuado puede empeorarla: sobreingeniería, acoplamiento fuerte a detalles de implementación o uso “por moda”. Diseña APIs claras, documenta las decisiones de diseño y revisa periódicamente (por ejemplo en retrospectivas técnicas) si el diseño sigue siendo adecuado o si ha aparecido deuda técnica.

En code reviews, cuestionar “¿realmente necesitamos {concept} aquí?” o “¿podemos simplificar?” es sano; no se trata de evitar tecnología sino de usarla donde aporta valor.""",
    """**Respuesta:** {concept} se puede combinar con otros conceptos del ecosistema según el caso de uso: por ejemplo con patrones de persistencia (repositorios, unidades de trabajo), colas de mensajes, APIs REST o GraphQL, o estrategias de testing. La documentación y los ejemplos del área «{seccion}» suelen mostrar integraciones típicas; [preguntas_respuestas_entrevista_senior_python.md](preguntas_respuestas_entrevista_senior_python.md) incluye más contexto para temas afines y patrones de arquitectura.

Al combinar varias tecnologías, define bien los límites entre ellas (quién es responsable de qué) y documenta los contratos (formatos de datos, versionado) para que el sistema sea mantenible a largo plazo.""",
    """**Respuesta:** En una entrevista sobre {concept} se suelen hacer preguntas sobre cuándo usarlo, trade-offs frente a alternativas, implementación práctica (código o diseño) y problemas reales que hayas resuelto con ello. El propio banco de preguntas y el archivo de respuestas desarrolladas son buenas fuentes para preparar y profundizar; repasar las respuestas en voz alta ayuda a afianzar y a ajustar el tiempo de respuesta.

Además de lo técnico, en un perfil senior se valora que puedas explicar el contexto en el que tomaste decisiones (restricciones, plazos, equipo) y qué harías distinto con lo que sabes ahora.""",
    """**Respuesta:** Para dominar {concept} combina varias fuentes: documentación oficial (para el contrato exacto y las opciones), libros y cursos del ecosistema Python (para visión de conjunto y buenas prácticas), y práctica en proyectos reales (para enfrentarte a edge cases y decisiones de diseño). El archivo [preguntas_respuestas_entrevista_senior_python.md](preguntas_respuestas_entrevista_senior_python.md) complementa con respuestas desarrolladas que puedes usar como referencia y para repasar antes de una entrevista.

No hace falta “saberlo todo” de memoria; lo importante es saber dónde buscar, cómo experimentar en local y cómo relacionar el concepto con problemas que hayas resuelto.""",
    """**Respuesta:** Al adoptar {concept}, decide con claridad el alcance (qué partes del sistema lo usan y cuáles no), cómo se integra con el resto (configuración, logging, manejo de errores), y los criterios de éxito (rendimiento, mantenibilidad, tiempo de onboarding). Documenta estas decisiones (por ejemplo en un ADR) y revísalas con el equipo para alinear expectativas y poder revisarlas más adelante.

Si la adopción es gradual, define hitos (por ejemplo “primera integración en producción”, “todos los flujos críticos migrados”) y criterios para considerar la adopción estable o para revertir si algo sale mal.""",
    """**Respuesta:** Para explicar {concept} a un desarrollador junior: empieza por el problema que resuelve y cuándo tiene sentido usarlo en lugar de alternativas más simples; pon un ejemplo concreto y evita jerga innecesaria. Puedes apoyarte en las respuestas desarrolladas del archivo de preguntas para tener un hilo claro y ejemplos que hayan funcionado en entrevistas o en formación interna.

Comprobar que la otra persona ha entendido (por ejemplo pidiendo que lo resuma con sus palabras o que lo aplique a un caso distinto) ayuda a detectar malentendidos y a afianzar el aprendizaje.""",
    """**Respuesta:** Los trade-offs de elegir {concept} suelen ser: complejidad frente a beneficio (más capacidades pero más cosas que aprender y mantener), dependencias frente a control (usar una librería frente a implementar algo a medida), y curva de aprendizaje frente a productividad a medio plazo. Hay que evaluarlos en tu contexto (equipo, plazos, requisitos) y documentar la decisión para que no se pierda el razonamiento.

En una entrevista, explicar que conoces estos trade-offs y que has tomado decisiones conscientes (incluso cuando no eran las “óptimas” en abstracto por restricciones del proyecto) demuestra madurez.""",
    """**Respuesta:** Para garantizar consistencia o idempotencia al usar {concept}: diseña operaciones que se puedan repetir sin efectos secundarios indeseados (por ejemplo “crear o actualizar” con clave única en lugar de “crear” a ciegas); usa claves únicas y transacciones cuando el almacén lo permita; y documenta el comportamiento esperado ante reintentos o reprocesamiento. En el archivo de respuestas hay preguntas específicas sobre idempotencia en pipelines y APIs.

En sistemas distribuidos o con colas, la idempotencia es especialmente importante porque los mensajes pueden entregarse más de una vez; el consumidor debe poder procesarlos sin duplicar efectos (por ejemplo sin insertar dos veces el mismo registro).""",
    """**Respuesta:** La configuración típica de {concept} en producción debe seguir la documentación oficial y adaptarse al entorno (dev, staging, prod). Usa variables de entorno o un gestor de secretos para datos sensibles (claves, tokens); evita valores por defecto inseguros y revisa permisos y redes (qué puede llamar a qué, qué puertos están abiertos). Documenta qué variables son obligatorias y qué valores son válidos para cada entorno.

En despliegues con Kubernetes o similar, ConfigMaps y Secrets permiten separar configuración por entorno; evita hardcodear entornos en el código. Revisar la configuración en las revisiones de seguridad es buena práctica.""",
    """**Respuesta:** Para monitorizar una aplicación que usa {concept}: logs estructurados con contexto (request_id, usuario, acción) para poder filtrar y correlacionar; métricas de latencia y tasa de error (y si aplica throughput, uso de recursos); y trazas distribuidas si hay varios servicios, para seguir una petición de punta a punta. La sección de Observabilidad en [preguntas_respuestas_entrevista_senior_python.md](preguntas_respuestas_entrevista_senior_python.md) detalla opciones, herramientas (Prometheus, Grafana, Jaeger, etc.) y buenas prácticas.

Definir qué se considera “normal” (líneas base de latencia, error rate aceptable) y alertar cuando se desvíe permite actuar antes de que impacte a los usuarios. Revisar periódicamente las alertas para evitar fatiga (demasiadas falsas alarmas) o lag (alertas que nadie atiende).""",
    """**Respuesta:** Posibles problemas de concurrencia con {concept} incluyen condiciones de carrera (varios hilos o tareas modificando el mismo estado), bloqueos (locks) mal usados (deadlocks, contención excesiva) o el GIL en CPython (que limita el paralelismo real de threads para código Python puro). Según el caso, usa las primitivas adecuadas (threading, multiprocessing, asyncio) y diseña para evitar estado compartido mutable cuando sea posible. El archivo de respuestas desarrolladas incluye preguntas sobre GIL, threading y concurrencia con más detalle.

En entrevistas senior se valora que conozcas no solo las herramientas sino cuándo aplicarlas: I/O-bound frente a CPU-bound, ventajas e inconvenientes de cada modelo, y cómo depurar problemas de concurrencia (herramientas, logs, reproducción).""",
    """**Respuesta:** En un contexto de microservicios, integra {concept} en los límites del servicio: por ejemplo en la API (entrada/salida), en colas de mensajes (consumo o publicación) o en eventos (publicar o suscribirse). Documenta los contratos (payloads, versionado, compatibilidad hacia atrás) y ten en cuenta la resiliencia entre servicios: timeouts, reintentos, circuit breaker y degradación controlada cuando un dependiente no esté disponible.

Evita acoplamiento fuerte entre servicios (por ejemplo no asumir que todos usan la misma versión de un mensaje); diseña para evolución y para que un servicio pueda actualizarse sin tirar del resto.""",
    """**Respuesta:** Para evaluar el impacto de {concept} en latencia y throughput: mide con benchmarks representativos y bajo carga real o simulada (por ejemplo con Locust o k6); identifica cuellos de botella (profiling de CPU, memoria, I/O) y optimiza solo donde aporte valor, evitando optimizaciones prematuras. Las preguntas de rendimiento en el archivo de respuestas desarrolladas dan más criterios y herramientas (cProfile, memory_profiler, métricas en producción).

Establecer líneas base antes de cambiar algo y comparar después permite saber si la optimización ha merecido la pena. En producción, métricas continuas (p50, p95, p99 de latencia) ayudan a detectar regresiones.""",
    """**Respuesta:** Para rollback o recuperación ante fallos con {concept}: tener un plan de rollback claro (volver a la versión anterior, desactivar feature flags o rutas nuevas) y probado; backups de datos si aplica, con procedimiento de restauración documentado; y monitoreo que alerte ante errores o degradación para actuar con rapidez. El equipo debe saber quién puede ejecutar el rollback y bajo qué condiciones.

En despliegues con CI/CD, mantener la posibilidad de desplegar la versión anterior en un solo paso (por ejemplo “redeploy last green”) reduce el tiempo de recuperación. Post-mortems después de incidentes ayudan a mejorar el plan para la próxima vez.""",
    """**Respuesta:** Los requisitos de infraestructura de {concept} (CPU, memoria, red, servicios externos como bases de datos o colas) suelen estar en su documentación oficial. Diseña la infraestructura para soportar la carga esperada y para escalar si es necesario (horizontal o vertical); documenta requisitos mínimos y recomendados para tu entorno (desarrollo, staging, producción) para que nuevos entornos se configuren de forma coherente.

Si {concept} depende de servicios externos, considera su disponibilidad, límites de rate y SLA; en entornos cloud, los costes de esos servicios pueden ser significativos y hay que incluirlos en la planificación.""",
    """**Respuesta:** Al modelar datos o dominios con {concept}, adapta el modelo a las capacidades que ofrece y al dominio de negocio; evita modelos anémicos (solo getters/setters sin comportamiento) o excesivamente complejos (demasiadas entidades o relaciones que no aportan). Para patrones de modelado (por ejemplo DDD, agregados, value objects) en Python, consulta la sección de Arquitectura en el archivo de respuestas desarrolladas.

Un modelo bien pensado facilita el cambio futuro y la comunicación con el negocio; involucrar a dominio en el diseño (event storming, ejemplos concretos) suele dar mejor resultado que modelar solo desde la perspectiva técnica.""",
    """**Respuesta:** Los estándares o RFCs relacionados con {concept} (por ejemplo HTTP, protocolos de red, formatos como JSON o Protocol Buffers) suelen citarse en la documentación oficial. Consultarlos ayuda a entender límites, compatibilidad entre versiones y comportamiento en edge cases (por ejemplo qué hace un proxy con ciertos headers, o cómo se serializa un valor nulo).

En integraciones entre sistemas, seguir el estándar reduce bugs y facilita que otras partes (clientes, otros equipos) interoperen sin sorpresas. Cuando te desvías del estándar, documéntalo y justifícalo.""",
    """**Respuesta:** Para evitar sobrecarga o abuso al usar {concept}: aplicar rate limiting (por IP, por usuario o por API key) para limitar el número de peticiones por unidad de tiempo; validar y limitar tamaños de entrada (cuerpos de petición, parámetros) para evitar ataques de agotamiento de recursos; definir cuotas de uso si aplica; y monitorizar uso anómalo (picos, patrones inusuales). En el archivo de respuestas hay preguntas sobre rate limiting y protección de APIs con más detalle.

Comunicar los límites a los consumidores (documentación, códigos de respuesta 429, headers de rate limit) permite que adapten su uso y evita frustración. Revisar periódicamente los límites según el crecimiento del uso real.""",
    """**Respuesta:** Aplica el principio de menor privilegio al usar {concept}: cada componente (servicio, usuario, proceso) debe tener solo los permisos y el acceso a datos estrictamente necesarios para su función. Define roles y permisos claros, documenta quién puede hacer qué y no expongas más superficie (APIs, endpoints, datos) de la necesaria. Revisa periódicamente accesos y configuración (por ejemplo con auditorías o revisiones de seguridad) para detectar permisos obsoletos o excesivos.

En sistemas multi-tenant o con datos sensibles, este principio es crítico; un fallo en un componente no debería permitir escalar privilegios o acceder a datos de otros clientes.""",
    """**Respuesta:** Para versionar APIs o contratos que usan {concept}: usa versionado explícito (por ejemplo /v1/ en rutas, o un campo de versión en el contrato) para que cliente y servidor se entiendan. Mantén compatibilidad hacia atrás cuando sea posible (campos opcionales, no eliminar campos sin aviso); si tienes que romper compatibilidad, define una estrategia de deprecación y comunícarla con tiempo a los consumidores (changelog, avisos en respuestas, periodo de gracia).

Documentar qué versiones están soportadas y hasta cuándo ayuda a que los consumidores planifiquen su migración. En eventos o mensajes, incluir la versión del esquema en el payload facilita evolución futura.""",
    """**Respuesta:** La estrategia de caché con {concept} depende del patrón de acceso: cache-aside (la aplicación consulta caché y, si no está, carga y guarda), TTL (tiempo de vida), invalidación por eventos o por escritura. Define una política de invalidación clara para no servir datos obsoletos que lleven a inconsistencias o bugs difíciles de reproducir. En el archivo de respuestas hay preguntas sobre Redis y estrategias de caché con más detalle.

Considera también el tamaño de la caché, la política de evicción (LRU, etc.) y qué ocurre cuando la caché falla (degradación a fuente de verdad, o error). En sistemas distribuidos, la coherencia entre caché y fuente de verdad puede ser eventual; documenta las garantías.""",
    """**Respuesta:** Diseña tests de integración que involucren {concept} usando instancias reales o contenedores cuando sea viable (por ejemplo PostgreSQL en Docker, Redis en memoria); aísla los fallos con buenos mensajes de error y nombres descriptivos; y cubre flujos críticos y casos de error (timeouts, datos inválidos, servicio no disponible). La sección de Testing en el archivo de respuestas desarrolladas amplía estrategias (mocks, fixtures, cobertura, property-based testing).

Los tests de integración suelen ser más lentos y frágiles que los unitarios; úsalos donde aporten valor (contratos entre componentes, flujos de negocio críticos) y mantén el resto rápido con mocks o stubs. Documentar cómo levantar el entorno de test (docker-compose, variables) facilita que cualquiera pueda ejecutarlos.""",
    """**Respuesta:** Para logging y trazabilidad con {concept}: usa logs estructurados (por ejemplo JSON) con contexto (request_id, usuario, acción, duración) para poder filtrar y agregar; si hay varios servicios, usa trazas distribuidas (trace_id, span_id) para seguir una petición de punta a punta. Consulta la sección de Observabilidad en [preguntas_respuestas_entrevista_senior_python.md](preguntas_respuestas_entrevista_senior_python.md) para herramientas (OpenTelemetry, Jaeger, etc.) y buenas prácticas.

No loguees datos sensibles (contraseñas, tokens, PII) ni en texto plano; en entornos regulados puede ser obligatorio. Definir niveles por entorno (DEBUG en dev, INFO en prod) y no abusar del nivel DEBUG en producción evita ruido y coste de almacenamiento.""",
    """**Respuesta:** Para desplegar en Kubernetes una aplicación que usa {concept}: define un Deployment (imagen, réplicas, recursos, health checks liveness/readiness), un Service para exponer los pods internamente o externamente, e Ingress si necesitas HTTP/HTTPS externo con routing. Configuración y secretos vía ConfigMap y Secret; no hardcodear en la imagen. En el archivo de respuestas hay preguntas específicas sobre Kubernetes y Helm con más detalle.

Considera estrategias de despliegue (rolling update, blue-green) y cómo manejar migraciones de datos o cambios incompatibles. Documentar el proceso de despliegue y rollback permite que cualquier miembro del equipo pueda operar en producción.""",
    """**Respuesta:** Para reducir la deuda técnica al usar {concept}: haz refactors incrementales respaldados por tests (para no romper comportamiento); documenta la deuda conocida (qué está mal, por qué existe, qué habría que hacer) y priorízala en el backlog; evita grandes reescrituras sin valorar alternativas más acotadas (a veces un par de cambios localizados resuelven el problema sin tocar todo el módulo).

Comunicar al equipo y a stakeholders que existe deuda y que tiene coste (más tiempo en cambios futuros, más bugs) ayuda a conseguir tiempo para abordarla. Incluir partidas de “deuda técnica” o “mejora interna” en las iteraciones evita que solo se priorice funcionalidad nueva.""",
    """**Respuesta:** Prioriza tareas en un proyecto que adopta {concept} según valor de negocio (qué impacto tiene en usuarios o ingresos), riesgo técnico (qué se rompe si no se hace) y dependencias (qué bloquea a otros). Equilibra deuda técnica y nuevas funcionalidades para no acumular demasiada deuda; comunica las prioridades al equipo y a stakeholders para alinear expectativas y para que se entienda por qué algo va antes que otra cosa.

Herramientas como matrices impacto/esfuerzo o RICE pueden ayudar, pero en la práctica la priorización suele ser una conversación continua. Revisar las prioridades en cada iteración o sprint permite ajustar según feedback y cambios de contexto.""",
    """**Respuesta:** Riesgos típicos al adoptar {concept} incluyen: adopción prematura (antes de entender bien el problema o de validar que encaja), falta de formación del equipo (que lleva a mal uso o rechazo), o dependencia excesiva de una tecnología que luego cambia o desaparece. Mitiga con POCs o spikes que validen la decisión, formación (documentación, talleres, pair programming), documentación de decisiones y diseño que permita sustituir o aislar {concept} si fuera necesario (por ejemplo detrás de una abstracción).

Incluir en el plan de proyecto tiempo para aprendizaje y para resolver problemas inesperados reduce la presión y la tentación de cortar corners. Revisar la decisión tras un tiempo (por ejemplo a los 6 meses) permite corregir si la realidad no coincide con lo esperado.""",
    """**Respuesta:** Evalúa si {concept} es la solución correcta comprobando que el problema encaja con sus capacidades (no usar un martillo para un tornillo), que el coste de adopción (tiempo, formación, complejidad operativa) es asumible para el equipo y el proyecto, y que has considerado alternativas (incluida la de no hacer nada o hacer algo más simple). Un spike o POC puede validar la decisión antes de comprometerte en grande y exponer limitaciones o problemas que no se ven en la documentación.

En una entrevista, explicar que has hecho esta evaluación (aunque la decisión final no fuera tuya) demuestra pensamiento crítico y capacidad de tomar decisiones técnicas con información incompleta.""",
    """**Respuesta:** En una entrevista sobre diseño con {concept}, pregunta por límites de responsabilidad (qué hace este servicio y qué no), escalabilidad (cómo crece con la carga, cuellos de botella), manejo de fallos (reintentos, circuit breaker, degradación) y operación (despliegue, monitorización, rollback). El banco de preguntas y el archivo de respuestas desarrolladas ofrecen muchas preguntas de diseño que puedes reutilizar o adaptar para profundizar.

Como entrevistador, valora respuestas que muestren experiencia real (casos concretos, trade-offs que se tomaron) más que respuestas genéricas de libro. Como candidato, prepara 2-3 ejemplos de proyectos donde hayas aplicado conceptos similares.""",
    """**Respuesta:** Explica el flujo de datos describiendo de forma clara: de dónde entran los datos (API, cola, archivo), qué transformaciones o reglas aplica {concept} (validación, enriquecimiento, agregación), y hacia dónde salen (base de datos, otra API, evento). Diagramas de secuencia o de flujo y documentación actualizada ayudan a que todo el equipo tenga la misma visión y a onboarding de nuevos miembros.

Si hay varios sistemas involucrados, indica responsabilidades (quién es dueño de qué dato) y cómo se mantiene la consistencia (síncrona, asíncrona, eventual). Esto es especialmente importante en arquitecturas distribuidas o con eventos.""",
    """**Respuesta:** Para encontrar alternativas open source a {concept}: busca en PyPI, GitHub (por estrellas, actividad reciente, issues) y en comparativas o artículos del ecosistema. Evalúa mantenimiento activo (commits recientes, respuestas a issues), licencia (compatibilidad con tu proyecto o empresa), comunidad (tamaño, calidad de documentación) y si la funcionalidad se ajusta a tus requisitos antes de decidir.

No elijas solo por “el que tiene más estrellas”; a veces una librería más pequeña o específica encaja mejor. Probar en un spike o branch con una o dos alternativas antes de comprometerte reduce el riesgo.""",
    """**Respuesta:** Los costes operativos de {concept} pueden incluir: infraestructura (servidores, servicios gestionados, red), licencias si las hubiera, tiempo de operación (monitorización, incidentes, actualizaciones) y formación del equipo. Inclúyelos en la decisión de adopción y en el presupuesto del proyecto para no llevarte sorpresas; a veces el coste de licencia o de operación supera el beneficio funcional.

En proyectos con presupuesto ajustado, las alternativas open source o las opciones “managed” (donde el proveedor se encarga de la operación) pueden cambiar la ecuación. Revisar los costes periódicamente (por ejemplo cuando crece el uso) evita desviaciones.""",
    """**Respuesta:** Para alta disponibilidad con {concept}: usa réplicas o múltiples instancias detrás de un balanceador o servicio de descubrimiento; configura health checks (liveness, readiness) y reinicio automático cuando fallen; si aplica, diseña failover (cambio de líder, promoción de réplica) y procedimientos de recuperación ante fallos documentados y probados. Las preguntas sobre alta disponibilidad en el archivo de respuestas desarrolladas entran en más detalle (patrones, trade-offs).

Define qué nivel de disponibilidad necesitas (por ejemplo 99.9%) y diseña para ello; no toda aplicación requiere el mismo nivel y el coste de “siempre disponible” puede ser alto. Comunicar las expectativas a negocio y usuarios evita malentendidos.""",
    """**Respuesta:** Para formar a un equipo que va a usar {concept}: prepara documentación interna (qué es, cuándo se usa, cómo se configura, ejemplos), organiza talleres o sesiones prácticas (hands-on), fomenta pair programming en tareas reales que usen {concept} y comparte referencias externas (documentación oficial, archivo de respuestas desarrolladas). Ajusta el ritmo al nivel del equipo y deja espacio para preguntas y experimentación.

Incluir {concept} en el onboarding de nuevos miembros (con un “tour” guiado o un pequeño ejercicio) acelera que puedan contribuir. Revisar la documentación cuando cambie la versión o las prácticas evita que quede obsoleta.""",
    """**Respuesta:** Para comparar {concept} con soluciones en otros lenguajes: compara el modelo de uso (¿es similar la API o el flujo?), el rendimiento en benchmarks comparables (con las mismas condiciones), el ecosistema (librerías, comunidad, soporte comercial) y el esfuerzo de mantenimiento a largo plazo. La documentación y las comparativas oficiales o de la comunidad son la base; adapta las conclusiones a tu contexto (equipo, stack existente, requisitos).

En entrevistas o en decisiones técnicas, ser capaz de explicar “en Java sería X, en Python usamos Y porque…” demuestra visión amplia y capacidad de elegir la herramienta adecuada al contexto en lugar de aplicar siempre la misma receta.""",
]

# Preguntas genéricas de entrevista senior (no ligadas a un concepto)
PREGUNTAS_GENERICAS = [
    "¿Cómo estructurarías un proyecto Python de tamaño medio?",
    "¿Qué criterios usas para elegir entre herencia y composición?",
    "¿Cómo manejarías dependencias circulares entre módulos?",
    "¿Qué estrategia de versionado semántico seguirías en una librería?",
    "¿Cómo diseñarías una API interna para otro equipo?",
    "¿Qué harías ante un bug que solo aparece en producción?",
    "¿Cómo equilibrarías deuda técnica y nuevas funcionalidades?",
    "¿Qué métricas de código considerarías útiles en un equipo?",
    "¿Cómo conducirías una revisión de código efectiva?",
    "¿Qué preguntas harías al recibir un requisito ambiguo?",
    "¿Cómo descompondrías un requisito grande en tareas estimables?",
    "¿Qué harías si un compañero entrega código de baja calidad de forma reiterada?",
    "¿Cómo priorizarías bugs vs features en un sprint?",
    "¿Qué experiencia tienes con refactoring de código legacy?",
    "¿Cómo explicarías un concepto técnico complejo a un no técnico?",
    "¿Qué libros o recursos recomendarías para un desarrollador que quiere ser senior?",
    "¿Cómo te mantienes al día con el ecosistema Python?",
    "¿Qué te gusta y qué no te gusta de Python?",
    "¿Cómo manejarías un desacuerdo técnico con un compañero?",
    "¿Qué harías si una decisión arquitectónica anterior resulta ser incorrecta?",
    "¿Cómo definirías 'hecho' para una tarea en tu equipo?",
    "¿Qué prácticas evitas en Python y por qué?",
    "¿Cómo abordarías la documentación de un sistema complejo?",
    "¿Qué experiencia tienes con sistemas distribuidos?",
    "¿Cómo garantizarías que un despliegue no rompa producción?",
    "¿Qué harías para reducir el tiempo de onboarding de un nuevo desarrollador?",
    "¿Cómo manejarías plazos muy ajustados sin sacrificar calidad?",
    "¿Qué rol darías a la automatización en un equipo?",
    "¿Cómo definirías éxito en un proyecto de software?",
]


def extraer_conceptos(ruta: Path) -> list[tuple[str, str]]:
    """Extrae (sección, concepto) de habilidades_python.md."""
    texto = ruta.read_text(encoding="utf-8")
    lineas = texto.splitlines()
    conceptos = []
    seccion_actual = ""
    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue
        if linea.startswith("##"):
            seccion_actual = re.sub(r"^#+\s*", "", linea).strip()
            continue
        if linea.startswith("- "):
            concepto = linea[2:].strip()
            if concepto and not concepto.startswith("("):
                conceptos.append((seccion_actual, concepto))
    return conceptos


def normalizar_para_plantilla(concepto: str) -> str:
    """Normaliza el concepto para insertar en plantillas (evitar duplicados raros)."""
    return concepto.strip()


def generar_preguntas_para_concepto(concepto: str, plantillas: list[str]) -> list[tuple[str, int]]:
    """Genera lista de (pregunta, índice_plantilla) para un concepto."""
    c = normalizar_para_plantilla(concepto)
    resultado = []
    vistas = set()
    for idx, p in enumerate(plantillas):
        try:
            q = p.format(concept=c)
        except KeyError:
            q = p.replace("{concept}", c)
        if q not in vistas:
            vistas.add(q)
            resultado.append((q, idx))
    return resultado


def main():
    conceptos = extraer_conceptos(HABILIDADES_PATH)
    print(f"Conceptos extraídos: {len(conceptos)}")
    print(f"Plantillas: {len(PLANTILLAS)}")

    todas_las_preguntas = []
    por_seccion = {}

    for seccion, concepto in conceptos:
        preguntas_con_idx = generar_preguntas_para_concepto(concepto, PLANTILLAS)
        for q, idx in preguntas_con_idx:
            todas_las_preguntas.append((seccion, concepto, q, idx))
        if seccion not in por_seccion:
            por_seccion[seccion] = []
        por_seccion[seccion].extend([q for q, _ in preguntas_con_idx])

    # Añadir preguntas genéricas (índice -1 para respuesta genérica)
    for g in PREGUNTAS_GENERICAS:
        todas_las_preguntas.append(("General (Senior)", "", g, -1))

    total = len(todas_las_preguntas)
    print(f"Total preguntas generadas: {total}")

    RESPUESTA_GENERICA = (
        "**Respuesta:** Son preguntas de diseño, proceso o experiencia como desarrollador senior. "
        "Conviene responder con ejemplos concretos de tu experiencia: cómo lo has hecho, qué trade-offs consideraste y qué resultado obtuviste. "
        "Para más ideas y respuestas desarrolladas sobre temas técnicos, consulta [preguntas_respuestas_entrevista_senior_python.md](preguntas_respuestas_entrevista_senior_python.md)."
    )

    def formatear_respuesta(idx: int, concepto: str, seccion: str) -> str:
        if idx < 0:
            return RESPUESTA_GENERICA
        try:
            return RESPUESTAS[idx].format(concept=concepto, seccion=seccion)
        except KeyError:
            return RESPUESTAS[idx].replace("{concept}", concepto).replace("{seccion}", seccion)

    # Crear directorio de partes
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    num_archivos = (total + PREGUNTAS_POR_ARCHIVO - 1) // PREGUNTAS_POR_ARCHIVO
    indice_lineas = []

    for num_archivo in range(num_archivos):
        inicio = num_archivo * PREGUNTAS_POR_ARCHIVO
        fin = min(inicio + PREGUNTAS_POR_ARCHIVO, total)
        nombre = f"banco_preguntas_{num_archivo + 1:03d}.md"
        ruta = OUTPUT_DIR / nombre

        with open(ruta, "w", encoding="utf-8") as f:
            f.write(f"# Parte {num_archivo + 1} — Preguntas {inicio + 1} a {fin}\n\n")
            f.write(f"**{fin - inicio} preguntas con respuesta.**\n\n")
            f.write("[← Índice del banco](../banco_10000_indice.md)")
            if num_archivo > 0:
                f.write(f" · [← Parte anterior](banco_preguntas_{num_archivo:03d}.md)")
            if num_archivo < num_archivos - 1:
                f.write(f" · [Siguiente parte →](banco_preguntas_{num_archivo + 2:03d}.md)")
            f.write("\n\n---\n\n")

            seccion_actual = None
            for i in range(inicio, fin):
                seccion, concepto, pregunta, idx = todas_las_preguntas[i]
                if seccion != seccion_actual:
                    seccion_actual = seccion
                    f.write(f"\n## {seccion}\n\n")
                num_preg = i + 1
                f.write(f"### {num_preg}. {pregunta}\n\n")
                r = formatear_respuesta(idx, concepto, seccion)
                # Enlaces al archivo de respuestas desde banco_partes/ requieren ../
                r = r.replace("](preguntas_respuestas_entrevista_senior_python.md)", "](../preguntas_respuestas_entrevista_senior_python.md)")
                f.write(r)
                f.write("\n\n")

        indice_lineas.append(f"| Parte {num_archivo + 1} | Preguntas {inicio + 1}–{fin} | [{nombre}](banco_partes/{nombre}) |")
        print(f"  Escrito: {nombre} (preguntas {inicio + 1}-{fin})")

    # Índice en el directorio preguntas/ (no dentro de banco_partes)
    indice_path = Path(__file__).resolve().parent / "banco_10000_indice.md"
    with open(indice_path, "w", encoding="utf-8") as f:
        f.write("# Índice del Banco de Preguntas — Entrevista Senior Python\n\n")
        f.write(f"**Total: {total} preguntas**, repartidas en **{num_archivos} archivos** de hasta {PREGUNTAS_POR_ARCHIVO} preguntas cada uno.\n\n")
        f.write("Cada pregunta incluye una respuesta con contexto. Para respuestas más desarrolladas, ver [preguntas_respuestas_entrevista_senior_python.md](preguntas_respuestas_entrevista_senior_python.md).\n\n")
        f.write("| Parte | Rango de preguntas | Archivo |\n")
        f.write("|-------|--------------------|--------|\n")
        f.write("\n".join(indice_lineas))
        f.write("\n")

    print(f"Índice escrito en: {indice_path}")
    return total


if __name__ == "__main__":
    main()
