Conocer las fórmulas es una cosa, pero ¿qué separa a un buen programador de un verdadero líder técnico? Se trata de entender los matices, los anti-patrones a evitar y cómo pensar en el sistema como un todo. Aquí es donde la ingeniería se convierte en un arte.

# Estimación / Prioridades / Riesgos / Go-live Support

### 5. Nivel Senior - Conceptos Avanzados: Más Allá de las Fórmulas

Aquí es donde se separa un buen programador de un líder técnico.

#### Trade-offs: No Hay Balas de Plata

| **Concepto** | **Cuándo Usarlo** | **Cuándo NO Usarlo (o usar con cuidado)** |
| :--- | :--- | :--- |
| **Story Points** | En equipos ágiles estables para estimación relativa y planificación de sprints. Fomenta la conversación. | Para comparar equipos, predecir fechas exactas (son abstractos), o cuando el equipo es nuevo o cambia constantemente. |
| **Estimación en "Días Ideales"** | Cuando necesitas comunicarte con stakeholders no técnicos que piensan en tiempo de calendario. | Si no se aplica un "factor de foco" realista. Un día ideal rara vez es un día real (reuniones, interrupciones). |
| **#NoEstimates** | En sistemas de flujo continuo (Kanban) con items de trabajo pequeños y de tamaño similar. Se enfoca en el flujo y el tiempo de ciclo. | En proyectos con grandes dependencias externas, fechas límite fijas impuestas, o cuando el trabajo es muy heterogéneo en tamaño. |
| **Priorización RICE** | Para decisiones basadas en datos sobre un gran número de features de producto. | Para deuda técnica, tareas de plataforma o habilitadores, donde "Reach" e "Impact" son difíciles de cuantificar. Aquí, WSJF o un % fijo de capacidad es mejor. |
| **Lanzamiento "Big Bang"** | Prácticamente nunca en software moderno. Quizás para un producto completamente nuevo (v1.0) donde no hay usuarios existentes. | En cualquier sistema en producción con usuarios activos. El riesgo es astronómico. |
| **Canary Release** | Para validar nuevas features con alto riesgo o impacto en el rendimiento en un subconjunto de usuarios reales. | Para cambios muy pequeños y de bajo riesgo, donde un despliegue Blue-Green o un simple feature flag podría ser más simple. |

#### Anti-Patrones: Las Sirenas del Desarrollo de Software

*   **Tratar las estimaciones como compromisos inamovibles**: Una estimación es una predicción probabilística, no un contrato de sangre. Un senior educa a los stakeholders sobre esto.
*   **Weaponizing Velocity / Métricas**: Usar la velocidad de un equipo para presionarlos o compararlos con otros. La velocidad es una herramienta de planificación para el equipo, no un KPI de rendimiento.
    > "La medición utilizada como un medio para controlar a las personas destruirá la motivación intrínseca y la cooperación." — **Peter Scholtes**, *The Leader's Handbook* (1998)
*   **Análisis-Parálisis de Riesgos**: Pasar tanto tiempo analizando y mitigando riesgos de baja probabilidad/impacto que el proyecto nunca avanza. Un senior sabe qué riesgos aceptar.
*   **El "Hero Mode" en Go-Live**: Depender de un individuo o un pequeño grupo para trabajar toda la noche y solucionar problemas durante el lanzamiento. Es un signo de una planificación deficiente, no de heroísmo. El objetivo de un buen Go-Live es que sea *aburrido*.
*   **Ignorar la Deuda Técnica en la Priorización**: Siempre priorizar nuevas features sobre la salud del sistema. Esto es como pedir préstamos con intereses altísimos; eventualmente, la bancarrota (la paralización del desarrollo) es inevitable.

#### Integración y el Ciclo Virtuoso

Un senior no ve estos cuatro conceptos como silos, sino como un sistema interconectado:

```
      +------------------------> ESTIMACIÓN (¿Cuánto costará?)
      |                              |
      |                              v
      |                         PRIORIZACIÓN (¿Qué es lo más valioso ahora?)
      |                              |
      |                              v
      +<-- Feedback del mundo real -- GO-LIVE SUPPORT (¿Funcionó como esperábamos?)
      |                              ^
      |                              |
      +------------------------ RIESGOS (¿Qué podría salir mal?)
```
El análisis de **Riesgos** informa qué tareas necesitan un buffer en la **Estimación**. La **Estimación** (esfuerzo) es un input clave para la **Priorización**. La **Priorización** determina qué se lanza. El **Soporte Go-live** y los post-mortems nos dan datos reales que refinan nuestras futuras estimaciones y nos descubren nuevos riesgos. Es un ciclo de aprendizaje continuo.

#### Consideraciones de SRE (Site Reliability Engineering)

El Go-Live Support a nivel senior es SRE. Los conceptos clave son:
*   **SLIs (Service Level Indicators)**: Métricas cuantificables. Ej: latencia de la API, tasa de errores.
*   **SLOs (Service Level Objectives)**: El objetivo para un SLI. Ej: "El 99.9% de las peticiones a la API `/login` deben completarse en menos de 200ms".
*   **Error Budgets (Presupuesto de Errores)**: `100% - SLO`. Si tu SLO es 99.9%, tienes un 0.1% de presupuesto para fallos. Este presupuesto le da al equipo la libertad de innovar y tomar riesgos. Si lo agotas, se congelan los nuevos lanzamientos y todo el foco se pone en la fiabilidad. Es un mecanismo de auto-regulación basado en datos.

### 6. Referencias y Citaciones Académicas: Los Hombros de Gigantes

1.  > "The bearing of a child takes nine months, no matter how many women are assigned. Many software tasks have this characteristic because of the sequential nature of debugging." — **Frederick P. Brooks, Jr.**, *The Mythical Man-Month: Essays on Software Engineering* (1975)

2.  > "The purpose of software engineering is to control complexity, not to create it." — **Pamela Zave**, *An Insider's Evaluation of CMM* (1995)

3.  > "Responding to change over following a plan." — **Kent Beck, et al.**, *Manifesto for Agile Software Development* (2001) - [https://agilemanifesto.org/](https://agilemanifesto.org/)

4.  > "The key to effective estimation is to acknowledge that all software estimates are uncertain and to manage them as probability distributions." — **Steve McConnell**, *Software Estimation: Demystifying the Black Art* (2006)

5.  > "If you cannot measure it, you cannot improve it." — **Lord Kelvin (William Thomson)**, (citado a menudo en contextos de ingeniería, aunque la cita original es más matizada). Relevante para la mentalidad SRE.

6.  > "The first 90 percent of the code accounts for the first 90 percent of the development time. The remaining 10 percent of the code accounts for the other 90 percent of the development time." — **Tom Cargill**, Bell Labs (conocida como la Regla del 90-90, un chiste interno sobre la dificultad de estimar la fase final de un proyecto).

7.  > "Hope is not a strategy. A solid Go-Live plan is." — **Ben Treynor Sloss**, VP of Engineering at Google, fundador de SRE. (Parafraseado de sus muchas charlas sobre SRE).

8.  > "The economic value of a feature is not its development cost, but the cost of not having it. This is the Cost of Delay." — **Don Reinertsen**, *The Principles of Product Development Flow* (2009)

9.  > "The essence of the waterfall model is a sequential, non-iterative process. I was describing how not to build software." — **Winston W. Royce**, en retrospectiva sobre su propio paper de 1970 que fue malinterpretado para popularizar el modelo de cascada.

10. > "SRE is what happens when you ask a software engineer to design an operations team." — **Ben Treynor Sloss**, *Keys to SRE* - [https://sre.google/sre-book/keys-to-sre/](https://sre.google/sre-book/keys-to-sre/)

11. > "The most dangerous phrase in the language is, 'We've always done it this way.'" — **Grace Hopper**, Almirante y pionera de la computación.

12. > "Black Swan events are unpredictable, have a massive impact, and are rationalized in hindsight as if they could have been predicted." — **Nassim Nicholas Taleb**, *The Black Swan: The Impact of the Highly Improbable* (2007). Un recordatorio para los gestores de riesgos de que no se puede prever todo.

---

**Conclusión: De Programador a Ingeniero**

Dominar estos cuatro pilares es el rito de paso que transforma a un programador, que resuelve problemas técnicos aislados, en un ingeniero de software senior, que entrega valor de manera consistente en un entorno complejo y dinámico. No se trata de tener siempre la respuesta correcta, sino de tener el marco correcto para hacer las preguntas correctas, comunicar la incertidumbre de manera honesta y guiar a tu equipo y a tu organización a través de la niebla del desarrollo de software, no con un mapa perfecto, sino con una brújula fiable y la habilidad de navegar por las estrellas.