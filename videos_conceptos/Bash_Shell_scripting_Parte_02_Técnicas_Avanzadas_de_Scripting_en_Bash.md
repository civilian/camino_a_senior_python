Cualquiera puede escribir un script que funcione una vez. Pero, ¿cómo creas uno que sea seguro, robusto y que no falle en producción a las 3 AM? La diferencia está en los detalles y en las técnicas que separan a un aficionado de un profesional.

# Bash / Shell scripting

### Caso de Estudio: Script de Backup Automatizado

Imaginemos que necesitamos un script para hacer backups diarios de un directorio a otro, comprimiéndolo y manteniendo solo los últimos 7.

**Versión Junior (Funciona, pero es frágil):**

```bash
#!/bin/bash
# backup_junior.sh
SOURCE="/var/www/html"
DEST="/mnt/backups"
DATE=$(date +%Y-%m-%d)
FILENAME="backup-$DATE.tar.gz"

tar -czf $DEST/$FILENAME $SOURCE
echo "Backup completado en $DEST/$FILENAME"
```
*Problemas: Sin manejo de errores, sin limpieza de backups antiguos, rutas hardcodeadas, se romperá si los directorios no existen.*

**Versión Senior (Robusto, configurable y seguro):**

```bash
#!/bin/bash
# backup_senior.sh

# --- Modo Estricto ---
set -euo pipefail
IFS=$'\n\t'

# --- Configuración ---
readonly SOURCE_DIR="${1:-/var/www/html}" # Usa el primer argumento o un valor por defecto
readonly BACKUP_DIR="${2:-/mnt/backups}"
readonly RETENTION_DAYS=7
readonly LOCK_FILE="/var/run/$(basename "$0").lock"

# --- Funciones ---
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

cleanup() {
    log "Ejecutando limpieza..."
    rm -f "${LOCK_FILE}"
    log "Limpieza finalizada."
}

# --- Lógica Principal ---
trap cleanup EXIT # Asegura que cleanup() se ejecute al salir, incluso en error.

# Evitar ejecuciones concurrentes (patrón de archivo de bloqueo atómico)
if ! mkdir "${LOCK_FILE}" 2>/dev/null; then
    log "Error: El script ya se está ejecutando. Saliendo."
    exit 1
fi

log "Iniciando backup..."

# Validar directorios
if [[ ! -d "${SOURCE_DIR}" ]]; then
    log "Error: El directorio fuente '${SOURCE_DIR}' no existe."
    exit 1
fi
mkdir -p "${BACKUP_DIR}" # Crear directorio de destino si no existe

# Crear el backup
readonly DATE_STAMP=$(date '+%Y-%m-%d_%H-%M-%S')
readonly FILENAME="backup-${DATE_STAMP}.tar.gz"
readonly ARCHIVE_PATH="${BACKUP_DIR}/${FILENAME}"

log "Creando archivo: ${ARCHIVE_PATH}"
if tar -czf "${ARCHIVE_PATH}" -C "$(dirname "${SOURCE_DIR}")" "$(basename "${SOURCE_DIR}")"; then
    log "Backup creado exitosamente."
else
    log "Error: Falló la creación del backup."
    # El 'set -e' ya se encargaría de esto, pero la lógica explícita es más clara.
    exit 1
fi

# Limpiar backups antiguos
log "Limpiando backups antiguos (retención de ${RETention_DAYS} días)..."
find "${BACKUP_DIR}" -name "backup-*.tar.gz" -mtime "+${RETENTION_DAYS}" -print -delete
log "Limpieza de backups antiguos completada."

log "Script finalizado con éxito."

exit 0
```
**Justificación de Diseño Senior:**
*   **Configurabilidad**: Acepta argumentos de línea de comandos.
*   **Robustez**: Usa `set -euo pipefail`. Valida la existencia de directorios.
*   **Concurrencia**: Implementa un archivo de bloqueo (`lockfile`) para prevenir ejecuciones simultáneas, un problema común en tareas de `cron`.
*   **Mantenibilidad**: Usa funciones (`log`, `cleanup`) y variables `readonly` para constantes.
*   **Seguridad**: Usa `trap` para garantizar la limpieza incluso si el script falla. Cita todas las variables para manejar espacios y caracteres especiales.
*   **Idempotencia**: `mkdir -p` asegura que el script no falle si el directorio ya existe.

## 5. Nivel Senior - Conceptos Avanzados

### Trade-offs: ¿Cuándo NO usar Bash?

Un ingeniero senior sabe cuándo su herramienta favorita NO es la adecuada.

| Característica | Usar Bash | Usar un lenguaje de "alto nivel" (Python, Go, Ruby) |
| :--- | :--- | :--- |
| **Propósito** | Orquestación de comandos, manipulación de archivos, automatización de sistemas. "Pegamento". | Lógica de negocio compleja, estructuras de datos, algoritmos, APIs, servicios web. |
| **Manejo de Datos** | Flujos de texto, archivos línea por línea. | JSON, XML, bases de datos, objetos complejos. |
| **Dependencias** | Mínimas. Usa herramientas del sistema. Altamente portable en entornos *nix. | Requiere un intérprete y gestión de librerías (pip, npm). |
| **Rendimiento** | Lento para computación intensiva (crea muchos procesos). Rápido para E/S de archivos. | Mucho más rápido para algoritmos y procesamiento en memoria. |
| **Legibilidad** | Puede volverse críptico rápidamente. "Write-only code". | Generalmente más legible y mantenible para scripts largos. |

> "Aunque el shell es un lenguaje de programación, no está diseñado para grandes programas. Los scripts de más de unas pocas docenas de líneas deberían escribirse en un lenguaje más convencional." — **Brian W. Kernighan & Rob Pike**, *The Unix Programming Environment* (1984)

La regla de oro: si tu script necesita estructuras de datos más allá de arrays simples o está haciendo más procesamiento de texto que llamadas a comandos externos, probablemente deberías estar escribiéndolo en Python.

### Anti-Patrones y Cómo Evitarlos

1.  **Useless Use of `cat`**:
    *   **Anti-Patrón**: `cat archivo.txt | grep "patron"`
    *   **Por qué es malo**: Crea un proceso `cat` innecesario. `grep` puede leer archivos directamente.
    *   **Solución**: `grep "patron" archivo.txt`

2.  **No citar variables**:
    *   **Anti-Patrón**: `rm $FILENAME`
    *   **Por qué es malo**: Si `$FILENAME` es "Mi Documento.txt", el comando se convierte en `rm Mi Documento.txt`. ¡Desastre!
    *   **Solución**: `rm "$FILENAME"`

3.  **Usar `[ ... ]` en lugar de `[[ ... ]]`**:
    *   **Anti-Patrón**: `if [ $VAR = "foo" ]`
    *   **Por qué es malo**: `[` es un comando (también conocido como `test`). Está sujeto a división de palabras y expansión de nombres de archivo.
    *   **Solución**: `if [[ "$VAR" == "foo" ]]`. `[[` es una palabra clave del shell. Es más seguro, no realiza división de palabras en las variables citadas y permite patrones de globbing (`[[ "$FILENAME" == *.txt ]]`) y expresiones regulares (`[[ "$VAR" =~ [0-9]+ ]]`).

### Técnicas Avanzadas que te Distinguirán

*   **Sustitución de Procesos (`<(...)` y `>(...)`)**: Trata la salida de un comando como si fuera un archivo. Es magia.
    ```bash
    # Compara la salida de dos comandos sin crear archivos temporales
    diff <(ls -1 dir1) <(ls -1 dir2)
    ```

*   **Arrays Asociativos (Bash 4+)**: Hashes o diccionarios directamente en Bash.
    ```bash
    declare -A user_roles
    user_roles["admin"]="Alice"
    user_roles["guest"]="Bob"

    echo "El admin es ${user_roles['admin']}"
    ```

*   **Traps**: Ejecuta código cuando el script recibe una señal del sistema (`EXIT`, `INT`, `TERM`). Ya lo vimos en el script de backup, es la clave para la robustez.
    ```bash
    trap 'echo "¡No me interrumpas!"; exit 1' INT
    echo "PID: $$; Intenta presionar Ctrl+C"
    sleep 10
    ```

*   **Coprocesos (`coproc`)**: Ejecuta un comando de forma asíncrona y comunícate con él a través de descriptores de archivo. Para tareas de fondo complejas.

### Consideraciones de Seguridad y Rendimiento

*   **Seguridad**: La principal amenaza es la **Inyección de Comandos**. Si alguna vez construyes un comando a partir de una entrada no confiable (ej. un formulario web), estás en peligro.
    *   **NUNCA**: `eval "comando $USER_INPUT"`
    *   **SIEMPRE**: Cita todas las variables. Usa herramientas como `shellcheck` (un linter estático para scripts de shell) de forma religiosa. Es el `eslint` o `flake8` del mundo Bash.
*   **Rendimiento**:
    *   **Evita los subshells en bucles**: `cat file | while read line; do ... done` crea un subshell, por lo que las variables modificadas dentro del bucle no persisten. `while read line; do ... done < file` es más eficiente y correcto.
    *   **Minimiza la creación de procesos**: Cada comando externo (`grep`, `awk`, `sed`) tiene un costo de `fork/exec`. A veces, un solo `awk` puede reemplazar una cadena de `grep | sed | cut`.
    *   **Usa built-ins**: Comandos como `test` (`[ ... ]`), `echo`, `read` son internos al shell y mucho más rápidos que sus contrapartes externas.

## 6. Referencias y Citaciones Académicas

1.  > "The primary goal is to provide a shell that is `sh`-compatible, but integrates useful features from other shells like the Korn Shell (`ksh`) and the C Shell (`csh`)." — **Brian Fox**, *Bash-0.99 README* (1989)

2.  > "The power of a system comes more from the relationships among programs than from the programs themselves." — **Brian W. Kernighan & Rob Pike**, *The Unix Programming Environment* (1984) - [Enlace a Amazon](https://www.amazon.com/Unix-Programming-Environment-Prentice-Hall-Software/dp/013937681X)

3.  > "Word splitting and filename expansion are the features that make unquoted variable expansions unsafe and are the cause of many shell scripting bugs." — **Koalaman (Vidal Holmqvist)**, *ShellCheck Wiki, SC2086* - [Enlace a ShellCheck Wiki](https://github.com/koalaman/shellcheck/wiki/SC2086)

4.  > "The Bourne shell was developed as a replacement for the original Thompson shell. Its major advance was to add control-flow and variables to the shell, making it a real programming language." — **Stephen R. Bourne**, *The Unix Shell* (1983)

5.  > "The essence of the Unix philosophy is to build simple tools that do one thing well, and then combine them to do more complex things." — **Eric S. Raymond**, *The Art of Unix Programming* (2003) - [Enlace al libro](http://www.catb.org/~esr/writings/taoup/html/)

6.  > "The GNU Project was conceived in 1983 as a way of bringing back the cooperative spirit that had prevailed in the computing community in earlier days—to make cooperation possible once again by removing the obstacles to cooperation imposed by the owners of proprietary software." — **Richard Stallman**, *The GNU Manifesto* (1985) - [Enlace al manifiesto](https://www.gnu.org/gnu/manifesto.en.html)

7.  > "In the original Bourne shell, `[` was just a link to the `test` command, which made for a nice illusion. The `[[` keyword was introduced in ksh to be a better version of `[`." — **David G. Korn**, *KornShell Q&A* (Varias fuentes)

8.  > "Bash is a 'sh-compatible' command language interpreter that executes commands read from the standard input or from a file. Bash also incorporates useful features from the Korn and C shells (ksh and csh)." — **Chet Ramey**, *Official Bash Manual* - [Enlace a la documentación oficial](https://www.gnu.org/software/bash/manual/bash.html)

***

Dominar Bash no es memorizar comandos. Es interiorizar una filosofía. Es aprender a ver el sistema operativo no como una caja negra, sino como una colección de herramientas esperando a ser dirigidas por un maestro orquestador. Ahora, ve y construye algo robusto, elegante y automatizado. El shell te espera.