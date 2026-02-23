#!/usr/bin/env python3
"""
Genera un banco de preguntas de entrevista Senior Python a partir de
habilidades_python.md y plantillas, con el objetivo de llegar a ~10.000 preguntas.
"""

import re
from pathlib import Path

HABILIDADES_PATH = Path(__file__).resolve().parent.parent / "habilidades_python.md"
OUTPUT_PATH = Path(__file__).resolve().parent / "banco_10000_preguntas.md"

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

# Plantillas de respuesta (mismo orden que PLANTILLAS). Se reemplaza {concept} y {seccion}.
RESPUESTAS = [
    "**Respuesta:** {concept} es un concepto o herramienta del ecosistema Python (área: {seccion}). Para una explicación detallada consulta la documentación oficial y [preguntas_respuestas_entrevista_senior_python.md](preguntas_respuestas_entrevista_senior_python.md).",
    "**Respuesta:** En Python, {concept} se implementa típicamente mediante la stdlib o librerías de la comunidad. Consulta la documentación de {concept} y ejemplos en el archivo de respuestas desarrolladas.",
    "**Respuesta:** Usa {concept} cuando el problema encaje con sus ventajas (consultar docs y mejores prácticas). Evítalo cuando existan alternativas más adecuadas al contexto.",
    "**Respuesta:** No conviene usar {concept} cuando el requisito no lo justifica, cuando hay alternativas más simples o cuando el equipo no tiene experiencia; valora el coste de adopción.",
    "**Respuesta:** Un ejemplo típico de {concept} en Python se puede encontrar en la documentación oficial o en [preguntas_respuestas_entrevista_senior_python.md](preguntas_respuestas_entrevista_senior_python.md) para temas afines.",
    "**Respuesta:** Las ventajas de {concept} suelen ser: mejor estructura, rendimiento o mantenibilidad según el caso. Detalles en documentación y en el archivo de respuestas desarrolladas.",
    "**Respuesta:** Limitaciones típicas: complejidad, dependencias, curva de aprendizaje o requisitos de infraestructura. Evaluar trade-offs antes de adoptar.",
    "**Respuesta:** En un proyecto real: definir responsabilidades, integrar con el resto del stack, documentar y testear. Ver patrones en [preguntas_respuestas_entrevista_senior_python.md](preguntas_respuestas_entrevista_senior_python.md).",
    "**Respuesta:** {concept} se diferencia de alternativas en alcance, modelo de uso o ecosistema. Consulta comparativas en la documentación y en el archivo de respuestas desarrolladas.",
    "**Respuesta:** Errores comunes: mal uso de la API, no manejar edge cases, ignorar rendimiento o seguridad. Revisar docs y buenas prácticas.",
    "**Respuesta:** Usar logging, breakpoints (pdb), y reproducir el caso; aislar el componente que usa {concept} y verificar configuración y dependencias.",
    "**Respuesta:** Tests unitarios que mockean dependencias, tests de integración con instancias reales o contenedores, y cubrir casos de error. Ver sección Testing en el archivo de respuestas.",
    "**Respuesta:** Considerar uso de CPU/memoria, I/O, latencia y escalabilidad. Medir con profiling y métricas antes y después de cambios.",
    "**Respuesta:** Validar entradas, no exponer datos sensibles, usar principios de menor privilegio y revisar dependencias (p. ej. con bandit o pip-audit).",
    "**Respuesta:** Escalar horizontalmente (más instancias) o verticalmente según el cuello de botella; usar colas, caché y particionamiento cuando aplique.",
    "**Respuesta:** Patrones relacionados dependen del dominio (repositorio, factory, estrategia, etc.). Ver sección Arquitectura en el archivo de respuestas desarrolladas.",
    "**Respuesta:** Alternativas: otras librerías o enfoques del ecosistema. Elegir según requisitos, rendimiento y experiencia del equipo. Documentación y comparativas ayudan.",
    "**Respuesta:** Documentar en README o docs del proyecto: cuándo se usa, cómo configurarlo y ejemplos. Mantener actualizado con los cambios.",
    "**Respuesta:** Dependencias típicas: otras librerías Python, servicios externos o infraestructura. Revisar requirements o pyproject.toml del proyecto.",
    "**Respuesta:** Revisar changelog y documentación oficial de {concept}; muchas librerías soportan Python 3.8+. Verificar en PyPI o en el repo.",
    "**Respuesta:** Anti-patrones: usarlo para todo, no testear, acoplamiento excesivo o ignorar alternativas más simples. Ver archivo de respuestas desarrolladas.",
    "**Respuesta:** Ejecutar tests y lint en CI; desplegar con pipelines que validen antes de producción. Ver sección CI/CD en el archivo de respuestas.",
    "**Respuesta:** Métricas: latencia, throughput, tasa de error y uso de recursos. Exportar a Prometheus/Grafana o similar; ver sección Observabilidad en el archivo de respuestas.",
    "**Respuesta:** Reintentos con backoff, circuit breaker y fallbacks; definir política de reintentos y timeouts. Ver preguntas sobre resiliencia en el archivo de respuestas.",
    "**Respuesta:** Seguir guías de estilo (PEP 8), convenciones del equipo y documentación oficial de {concept}. Revisar código en equipo.",
    "**Respuesta:** Plan de migración por fases: pruebas, feature flags, migración gradual y rollback. Documentar y comunicar al equipo.",
    "**Respuesta:** Un buen uso de {concept} suele mejorar mantenibilidad; un mal uso la reduce. Diseñar APIs claras y documentar decisiones.",
    "**Respuesta:** Combinar con otros conceptos del ecosistema según el caso de uso; ver ejemplos en documentación y en [preguntas_respuestas_entrevista_senior_python.md](preguntas_respuestas_entrevista_senior_python.md).",
    "**Respuesta:** Preguntas que profundicen en cuándo usarlo, trade-offs, implementación y problemas reales. Ver el propio banco y el archivo de respuestas desarrolladas.",
    "**Respuesta:** Documentación oficial, libros del ecosistema Python, cursos y práctica en proyectos. El archivo de respuestas desarrolladas es un buen complemento.",
    "**Respuesta:** Decidir alcance, integración con el resto del sistema, configuración y criterios de éxito. Documentar y revisar con el equipo.",
    "**Respuesta:** Explicar el problema que resuelve, cuándo usarlo y un ejemplo simple. Evitar jerga innecesaria; ver respuestas desarrolladas para inspiración.",
    "**Respuesta:** Trade-offs: complejidad vs beneficio, dependencias vs control, curva de aprendizaje vs productividad. Evaluar en contexto.",
    "**Respuesta:** Diseñar operaciones idempotentes cuando sea posible; usar claves únicas y transacciones según el almacén. Ver preguntas sobre idempotencia en el archivo de respuestas.",
    "**Respuesta:** Configuración según documentación oficial y entorno (dev/staging/prod); usar variables de entorno o secrets para datos sensibles.",
    "**Respuesta:** Logs estructurados, métricas (latencia, errores) y trazas si aplica. Ver sección Observabilidad en [preguntas_respuestas_entrevista_senior_python.md](preguntas_respuestas_entrevista_senior_python.md).",
    "**Respuesta:** Posibles problemas: GIL, locks, condiciones de carrera. Usar primitivas adecuadas (threading, multiprocessing, asyncio). Ver preguntas sobre concurrencia en el archivo de respuestas.",
    "**Respuesta:** Integrar {concept} en los límites del servicio (API, colas, eventos); documentar contratos y considerar resiliencia entre servicios.",
    "**Respuesta:** Medir con benchmarks y bajo carga; optimizar cuellos de botella. Ver preguntas de rendimiento en el archivo de respuestas desarrolladas.",
    "**Respuesta:** Plan de rollback (versión anterior, feature flags), backups si aplica, y monitoreo para detectar fallos pronto.",
    "**Respuesta:** Revisar documentación de {concept}: requisitos de CPU, memoria, red y servicios externos. Diseñar para escalar si hace falta.",
    "**Respuesta:** Modelar según el dominio y las capacidades de {concept}; evitar anémico o sobrecomplicado. Ver DDD y arquitectura en el archivo de respuestas.",
    "**Respuesta:** Consultar estándares o RFCs citados en la documentación de {concept} (p. ej. HTTP, protocolos).",
    "**Respuesta:** Rate limiting, validación de entrada, cuotas y monitoreo de uso. Ver preguntas sobre rate limiting y seguridad en el archivo de respuestas.",
    "**Respuesta:** Aplicar principio de menor privilegio; roles y permisos según necesidad. No exponer más de lo necesario.",
    "**Respuesta:** Versionado de API (ej. /v1/) y de contratos; compatibilidad hacia atrás o estrategia de deprecación.",
    "**Respuesta:** Caché según patrón de acceso (cache-aside, TTL); invalidación clara. Ver preguntas sobre Redis y caché en el archivo de respuestas.",
    "**Respuesta:** Tests que usen instancias reales o contenedores; aislar fallos y cubrir flujos críticos. Ver sección Testing en el archivo de respuestas.",
    "**Respuesta:** Logs con contexto (request_id, usuario); trazas si hay varios servicios. Ver Observabilidad en [preguntas_respuestas_entrevista_senior_python.md](preguntas_respuestas_entrevista_senior_python.md).",
    "**Respuesta:** Definir Deployment, Service e Ingress; configurar recursos y health checks. Ver preguntas sobre Kubernetes en el archivo de respuestas.",
    "**Respuesta:** Refactors incrementales, tests que den confianza, documentar deuda conocida y priorizar en el backlog.",
    "**Respuesta:** Priorizar por valor y riesgo; equilibrar deuda técnica y features. Comunicar con el equipo y stakeholders.",
    "**Respuesta:** Riesgos: adopción prematura, falta de formación, dependencia. Mitigar con POCs, formación y documentación.",
    "**Respuesta:** Evaluar si el problema encaja con las capacidades de {concept}, el coste de adopción y las alternativas. Validar con un spike si hace falta.",
    "**Respuesta:** Preguntas de diseño sobre límites, escalabilidad, fallos y operación. Ver el banco y el archivo de respuestas desarrolladas.",
    "**Respuesta:** Describir el flujo de datos (entrada, transformación, salida) y dónde interviene {concept}. Diagramas y documentación ayudan.",
    "**Respuesta:** Buscar en PyPI, GitHub y comparativas; evaluar mantenimiento, licencia y comunidad.",
    "**Respuesta:** Costes: infraestructura, licencias si aplica, tiempo de operación y formación. Incluir en la decisión de adopción.",
    "**Respuesta:** Réplicas, health checks, failover y recuperación ante fallos. Ver preguntas sobre alta disponibilidad en el archivo de respuestas.",
    "**Respuesta:** Documentación, talleres internos, pair programming y referencias (docs, archivo de respuestas desarrolladas).",
    "**Respuesta:** Comparar modelo de uso, rendimiento, ecosistema y mantenimiento. La documentación y las comparativas oficiales son la referencia.",
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

    RESPUESTA_GENERICA = "**Respuesta:** Cuestiones de diseño, proceso o experiencia senior. Desarrolla según tu experiencia y contexto; más ideas en [preguntas_respuestas_entrevista_senior_python.md](preguntas_respuestas_entrevista_senior_python.md)."

    # Escribir markdown
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("# Banco de Preguntas para Entrevista Senior Python\n\n")
        f.write(f"**Total: {total} preguntas con respuesta.**\n\n")
        f.write("Generado a partir de [habilidades_python.md](../habilidades_python.md) y plantillas. Cada pregunta incluye una respuesta breve; para respuestas más desarrolladas ver [preguntas_respuestas_entrevista_senior_python.md](preguntas_respuestas_entrevista_senior_python.md).\n\n")
        f.write("---\n\n")

        # Por sección
        seccion_actual = None
        num = 0
        for seccion, concepto, pregunta, idx in todas_las_preguntas:
            if seccion != seccion_actual:
                seccion_actual = seccion
                f.write(f"\n## {seccion}\n\n")
            num += 1
            f.write(f"### {num}. {pregunta}\n\n")
            if idx >= 0:
                try:
                    r = RESPUESTAS[idx].format(concept=concepto, seccion=seccion)
                except KeyError:
                    r = RESPUESTAS[idx].replace("{concept}", concepto).replace("{seccion}", seccion)
                f.write(f"{r}\n\n")
            else:
                f.write(f"{RESPUESTA_GENERICA}\n\n")

    print(f"Escrito en: {OUTPUT_PATH}")
    return total


if __name__ == "__main__":
    main()
