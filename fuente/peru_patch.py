"""Adapta la base al Perú, agrega SSOMA y la ficha de referencia de CMH. Uso: peru_patch.py <dir>"""
import json, os, sys

D = sys.argv[1]
JP = os.path.join(D, "base_conocimiento.json")
base = json.load(open(JP, encoding="utf-8"))

base["version"] = "0.2.0"
base["pais"] = "Perú"
base["aviso"] = ("Contenido de referencia general reunido de fuentes públicas, con terminología peruana. "
                 "Los rangos de costo y los valores normativos son referenciales; verifica siempre el texto vigente "
                 "del D.S. 024-2016-EM y sus modificatorias, y los estándares de tu unidad, antes de decidir.")

F = base["fuentes"]
F.update({
 "DS024": {"titulo": "D.S. 024-2016-EM, Reglamento de Seguridad y Salud Ocupacional en Minería (modificado por D.S. 023-2017-EM)",
           "url": "https://faolex.fao.org/docs/pdf/per160277.pdf"},
 "DS023": {"titulo": "D.S. 023-2017-EM, modifica artículos y anexos del D.S. 024-2016-EM (SNI)",
           "url": "https://sni.org.pe/modifican-diversos-articulos-y-anexos-del-reglamento-de-seguridad-y-salud-ocupacional-en-mineria-aprobado-por-decreto-supremo-no-024-2016-em/"},
 "LEY29783": {"titulo": "Ley 29783, Ley de Seguridad y Salud en el Trabajo (El Peruano)",
              "url": "https://diariooficial.elperuano.pe/Normas/obtenerDocumento?idNorma=38"},
 "DS005": {"titulo": "D.S. 005-2012-TR, Reglamento de la Ley 29783 (LP Derecho, texto actualizado)",
           "url": "https://lpderecho.pe/reglamento-ley-seguridad-salud-trabajo-ley-decreto-supremo-005-2012-tr-actualizado/"},
 "CMH": {"titulo": "Consorcio Minero Horizonte, página institucional",
         "url": "https://cmh.com.pe/consorcio-minero-horizonte/"},
 "CMH_PLANTA": {"titulo": "Evaluación técnica de ampliación de planta Parcoy de 1500 a 2000 TMD, CMH (ALICIA-CONCYTEC)",
                "url": "https://alicia.concytec.gob.pe/vufind/Record/RUMP_7deacedbd18ba08041d97df6a651d653"},
 "CMH_COSTOS": {"titulo": "Estructura de costos unitarios en la actividad minera, CMH Unidad Parcoy (tesis UNI, ALICIA-CONCYTEC)",
                "url": "https://alicia.concytec.gob.pe/vufind/Record/UUNI_33f52bd4670c4846b43200cb94a6dafe"},
 "CMH_PROD": {"titulo": "Ampliación de la producción en la Unidad Minera Parcoy de CMH (tesis UNSAAC)",
              "url": "https://repositorio.unsaac.edu.pe/handle/20.500.12918/5475"},
 "GF_SSO": {"titulo": "Programa de capacitación en SSO, Gold Fields La Cima (ejemplo de documento SSOMA en Perú)",
            "url": "https://www.goldfields.com.pe/wp-content/uploads/2022/06/SSYMA-D03.19-Programa-de-Capacitacion-en-SSO_V3.doc.pdf"},
 "PE_USO": {"titulo": "Uso común en minería peruana (terminología de campo)", "url": None},
})

G = base["glosario"]
byname = {g["termino"]: g for g in G}

# Términos genéricos que cambian a su forma peruana
renames = {
 "Botadero": ("Cancha de desmonte", "Depósito del material estéril. En tajo abierto también se le llama botadero.", ["botadero", "depósito de desmonte", "escombrera"]),
 "Stockpile": ("Cancha de mineral", "Pila de mineral roto almacenado en superficie o cerca de la bocamina, para regular la alimentación a planta.", ["stockpile", "acopio"]),
 "Desatado": ("Desatado de rocas", "Retiro de rocas sueltas del techo (corona) y hastiales con barretilla, después de la voladura y antes de cualquier otra tarea. Es la primera línea de defensa contra la caída de rocas.", ["desate", "acuñadura (Chile)", "scaling"]),
 "Voladura": ("Voladura", "Fragmentación de la roca con explosivos. En Perú se llama voladura; en Chile, tronadura.", ["disparo", "tronadura (Chile)"]),
 "Sostenimiento": ("Sostenimiento", "Elementos que estabilizan labores subterráneas: puntales, cuadros de madera, cribbing, pernos split set y helicoidales, malla electrosoldada, shotcrete y cimbras. Se define según la tabla geomecánica (GSI/RMR) de cada labor.", ["fortificación (Chile)"]),
 "Acarreo": ("Acarreo", "Transporte del mineral o desmonte. En subterránea suele hacerse con scoop hasta el echadero y luego con locomotora, volquete o dumper hasta superficie.", ["transporte", "limpieza y acarreo", "haulage"]),
}
for old, (new, d, syn) in renames.items():
    g = byname[old]; g["termino"] = new; g["definicion"] = d; g["sinonimos"] = syn; g["fuente"] = "PE_USO"
byname["IPERC"]["fuente"] = "DS024"
byname["IPERC"]["definicion"] = ("Identificación de Peligros, Evaluación de Riesgos y Medidas de Control. Tiene dos formas: IPERC de línea base "
                                 "(lo elabora la empresa por proceso y se actualiza al menos una vez al año o cuando cambian las condiciones) "
                                 "e IPERC continuo (lo llena el trabajador en campo al inicio de cada tarea o guardia).")
byname["PETS"]["fuente"] = "DS024"
byname["Bloqueo y etiquetado"]["definicion"] = "Procedimiento que aísla y bloquea con candado y tarjeta las fuentes de energía de un equipo antes de intervenirlo. Es trabajo de alto riesgo."

def t(termino, definicion, categoria, fuente="PE_USO", sinonimos=None):
    G.append({"termino": termino, "definicion": definicion, "categoria": categoria, "sinonimos": sinonimos or [], "fuente": fuente})

# Operación subterránea peruana
t("Labor", "Cualquier excavación minera: galería, crucero, subnivel, chimenea, tajo o rampa.", "planeamiento")
t("Frente", "Extremo de avance de una labor donde se perfora y dispara.", "operaciones")
t("Tajo", "Labor de explotación donde se extrae el mineral en subterránea.", "planeamiento", sinonimos=["tajeo", "stope"])
t("Crucero", "Labor horizontal que corta transversalmente a la veta para llegar a ella.", "planeamiento")
t("Subnivel", "Galería auxiliar entre dos niveles principales, usada para preparar tajos.", "planeamiento")
t("Echadero", "Chimenea por donde se deja caer el mineral o desmonte por gravedad hacia un nivel inferior.", "operaciones", sinonimos=["ore pass", "chute"])
t("Tolva", "Estructura al pie del echadero que almacena el mineral y permite cargar carros o volquetes.", "operaciones", sinonimos=["buzón"])
t("Bocamina", "Entrada de la mina subterránea desde superficie.", "planeamiento")
t("Estocada", "Pequeña labor lateral para alojar equipos, refugios o materiales, o para dar paso a vehículos.", "planeamiento", sinonimos=["cámara"])
t("Ventana", "Labor de acceso desde una rampa o galería hacia el cuerpo mineral o un tajo.", "planeamiento")
t("Corte y relleno ascendente", "Método en el que el tajo se explota en rebanadas horizontales de abajo hacia arriba, y cada rebanada se rellena para servir de piso a la siguiente. Muy usado en vetas angostas del Perú, como en Pataz.", "planeamiento", "CMH_PLANTA", ["cut and fill", "OCF"])
t("Relleno detrítico", "Relleno con desmonte de la mina, colocado con scoop o por gravedad.", "operaciones")
t("Relleno hidráulico", "Relave clasificado transportado con agua por tuberías hasta el tajo. Puede llevar cemento (relleno cementado).", "operaciones")
t("Relleno en pasta", "Relave espesado con cemento que se bombea al tajo con poca agua.", "operaciones")
t("Scoop", "Cargador de bajo perfil para limpiar el mineral de los tajos y frentes.", "operaciones", sinonimos=["scooptram", "LHD"])
t("Jumbo", "Equipo de perforación mecanizada con uno o más brazos para frentes y sostenimiento.", "operaciones")
t("Jackleg", "Perforadora neumática manual con barra de avance, usada en minería convencional.", "operaciones", sinonimos=["perforadora neumática"])
t("Winche", "Equipo de arrastre con cable y rastrillo para limpiar mineral en tajos angostos.", "operaciones", sinonimos=["winche de rastrillo"])
t("Volquete", "Camión de acarreo. En subterránea se usan volquetes convencionales o dumpers de bajo perfil.", "operaciones")
t("Locomotora", "Equipo sobre rieles que arrastra carros mineros por las galerías.", "operaciones")
t("Guardia", "Turno de trabajo. Se habla de guardia día y guardia noche.", "operaciones")
t("Jefe de guardia", "Supervisor responsable de la operación y la seguridad durante la guardia.", "seguridad")
t("Cachorreo", "Voladura secundaria para reducir bancos (rocas grandes) que no pasan la parrilla o el echadero.", "operaciones", sinonimos=["voladura secundaria", "plasteo"])
t("Desquinche", "Ampliación de la sección de una labor ya abierta.", "operaciones")
t("Tiro cortado", "Taladro cargado que no detonó. Es una condición de alto riesgo que se trata según procedimiento y nunca se reperfora.", "seguridad", sinonimos=["tiro fallado", "tiro soplado"])
t("Gaseado", "Persona afectada por exposición a gases por encima de los límites permisibles (CO, NO2, falta de oxígeno).", "seguridad", "DS024")
t("Puntal de seguridad", "Madera redonda colocada entre piso y techo como sostenimiento temporal o de avance.", "seguridad")
t("Cuadro de madera", "Sostenimiento con postes y sombrero de madera en labores de roca mala.", "operaciones")
t("Split set", "Perno de fricción ranurado que se instala a presión en el taladro.", "operaciones")
t("Perno helicoidal", "Barra corrugada anclada con resina o cemento para sostenimiento permanente.", "operaciones")
t("Shotcrete", "Concreto lanzado sobre la roca para sostenerla.", "operaciones", sinonimos=["concreto lanzado"])
t("GSI", "Índice geológico de resistencia. En Perú se usa la tabla GSI modificada para definir el sostenimiento en cada labor.", "seguridad", "DS024")
t("TMS", "Tonelada métrica seca: tonelada de mineral descontando la humedad.", "economia")
t("TMH", "Tonelada métrica húmeda: tonelada de mineral con su humedad.", "economia")
t("TMD", "Toneladas métricas por día. Unidad común de capacidad de planta en Perú.", "economia")
t("Merrill-Crowe", "Proceso que precipita el oro de la solución cianurada con polvo de zinc.", "procesamiento", "CMH_PLANTA")
t("Contrata", "Empresa contratista minera que ejecuta labores de avance, explotación o servicios para el titular.", "economia", sinonimos=["empresa contratista minera", "ECM"])
t("Precio unitario", "Costo por metro de avance o por tonelada que se paga a la contrata. Incluye mano de obra, materiales, explosivos, EPP, herramientas, equipos, gastos generales y utilidad.", "economia", "CMH_COSTOS")

# SSOMA
t("SSOMA", "Seguridad, Salud Ocupacional y Medio Ambiente. Área y sistema de gestión que integra la prevención de accidentes, la salud de los trabajadores y el cuidado ambiental.", "seguridad", "DS024", ["SSO", "HSE", "SSYMA"])
t("PETAR", "Permiso Escrito para Trabajo de Alto Riesgo. Lo firman en cada guardia el supervisor y el jefe de área antes de iniciar el trabajo (Anexo 18 del D.S. 024-2016-EM).", "seguridad", "DS024")
t("ATS", "Análisis de Trabajo Seguro. Herramienta para identificar los riesgos de una tarea y sus controles antes de ejecutarla (Anexo 11).", "seguridad", "DS024")
t("Trabajo de alto riesgo", "Tarea con alto potencial de daño grave o muerte, como trabajos en altura, en caliente, en espacios confinados, con energía eléctrica, excavaciones o izaje. Requiere PETAR.", "seguridad", "DS024")
t("Comité de SSO", "Órgano paritario (empresa y trabajadores) que vigila la gestión de seguridad. Obligatorio con 20 o más trabajadores; con menos, se designa un supervisor de SSO.", "seguridad", "DS024")
t("Inducción", "Capacitación inicial al trabajador antes de asignarle su puesto, sobre políticas, reglas y riesgos (Anexo 4).", "seguridad", "DS024")
t("Acto subestándar", "Acción del trabajador que no cumple el procedimiento o estándar y puede causar un incidente.", "seguridad", "DS024")
t("Condición subestándar", "Situación del entorno de trabajo que no cumple el estándar y puede causar un incidente.", "seguridad", "DS024")
t("Incidente peligroso", "Suceso que pudo causar lesiones graves o muerte. Se notifica a la autoridad (Anexo 21).", "seguridad", "DS024")
t("Accidente incapacitante", "Accidente que, tras la evaluación médica, impide al trabajador volver a su labor al día siguiente.", "seguridad", "DS024")
t("Estándar", "Documento que fija los parámetros y requisitos mínimos aceptables para una tarea o equipo (Anexo 9).", "seguridad", "DS024")
t("Refugio minero", "Cámara subterránea equipada con aire, agua y comunicación para que el personal se proteja durante una emergencia (Anexo 19).", "seguridad", "DS024", ["estación de refugio"])
t("Autorrescatador", "Equipo personal que entrega aire respirable o filtra CO por un tiempo limitado durante una emergencia.", "seguridad", "DS024")
t("EMO", "Examen médico ocupacional: de ingreso, periódico y de retiro.", "seguridad", "DS024")
t("EPP", "Equipo de protección personal: casco, lámpara, respirador, lentes, protector auditivo, guantes, botas, ropa con cinta reflectiva, arnés, autorrescatador.", "seguridad", "DS024")
t("Check list pre-uso", "Inspección del equipo que el operador hace al inicio de cada guardia antes de operarlo.", "seguridad")
t("OSINERGMIN", "Organismo que fiscaliza la seguridad de la infraestructura en la mediana y gran minería.", "seguridad")
t("SUNAFIL", "Superintendencia Nacional de Fiscalización Laboral. Fiscaliza el cumplimiento de la normativa de seguridad y salud en el trabajo.", "seguridad")
t("OEFA", "Organismo de Evaluación y Fiscalización Ambiental. Supervisa el cumplimiento de compromisos ambientales.", "medio_ambiente")
t("IGA", "Instrumento de Gestión Ambiental (por ejemplo EIA, EIA-sd, DIA). Aprueba y fija los compromisos ambientales de la operación.", "medio_ambiente")
t("Plan de cierre de minas", "Plan que define las actividades y la garantía financiera para rehabilitar el área al final de la operación (Ley 28090).", "medio_ambiente")
t("Drenaje ácido de roca", "Agua ácida con metales que se genera cuando los sulfuros se oxidan al contacto con aire y agua.", "medio_ambiente", "SME")
t("Degradación de cianuro", "Tratamiento de soluciones y relaves para destruir el cianuro antes de reutilizar el agua o disponer los relaves.", "medio_ambiente", "CMH_PLANTA")

# ---------------- SSOMA ----------------
S = [
 {"id": "marco-legal", "titulo": "Marco legal de SSOMA en minería peruana",
  "contenido": "La seguridad minera en el Perú se rige por la Ley 29783 de Seguridad y Salud en el Trabajo y su reglamento (D.S. 005-2012-TR), y de forma específica por el Reglamento de Seguridad y Salud Ocupacional en Minería (D.S. 024-2016-EM) y su modificatoria (D.S. 023-2017-EM). En lo ambiental aplican la Ley General del Ambiente (Ley 28611), los instrumentos de gestión ambiental aprobados y la Ley de Cierre de Minas (Ley 28090).",
  "puntos": ["El D.S. 024-2016-EM trae 37 anexos con formatos obligatorios: IPERC continuo (7), IPERC línea base (8), estándares (9), PETS (10), ATS (11), señales y colores (17), PETAR (18), refugios (19), notificación de accidentes e incidentes (21 a 23), entre otros.",
             "Fiscalizan SUNAFIL (seguridad y salud laboral), OSINERGMIN (infraestructura en mediana y gran minería) y OEFA (ambiental). Verifica el reparto de competencias vigente para tu estrato."],
  "fuentes": ["DS024", "DS023", "LEY29783", "DS005"]},
 {"id": "herramientas-gestion", "titulo": "Herramientas de gestión de riesgos",
  "contenido": "Cada tarea se planifica y controla con un conjunto de documentos que se complementan.",
  "puntos": ["IPERC línea base: matriz por proceso que elabora la empresa; se actualiza al menos una vez al año o cuando cambian las condiciones.",
             "IPERC continuo: lo llena el trabajador en el lugar de trabajo al inicio de cada tarea, identificando peligros y controles del momento.",
             "PETS: procedimiento paso a paso de cómo hacer la tarea de forma segura. Debe existir para cada proceso.",
             "PETAR: permiso firmado en cada guardia para trabajos de alto riesgo.",
             "ATS: análisis rápido de la tarea cuando no hay PETS o la tarea es nueva.",
             "Check list pre-uso de equipos y herramientas, inspecciones planeadas y reportes de actos y condiciones subestándar."],
  "fuentes": ["DS024"]},
 {"id": "jerarquia-controles", "titulo": "Jerarquía de controles",
  "contenido": "Los controles se aplican en este orden de preferencia, de mayor a menor eficacia.",
  "pasos": ["Eliminación del peligro.", "Sustitución por algo menos peligroso.", "Controles de ingeniería (guardas, ventilación, sostenimiento).",
            "Señalización, advertencias y controles administrativos (PETS, capacitación, rotación).", "Equipo de protección personal, como última barrera."],
  "fuentes": ["DS024"], "confianza": "verificar artículo vigente"},
 {"id": "riesgos-criticos-subterranea", "titulo": "Riesgos críticos en minería subterránea",
  "contenido": "Los peligros que más accidentes graves causan en minería subterránea peruana, con sus controles clave.",
  "riesgos": [
    {"riesgo": "Caída o desprendimiento de rocas", "controles": ["Desatado antes de iniciar cualquier tarea y durante la guardia.", "Sostenimiento según tabla GSI de la labor.", "Nunca trabajar bajo techo sin sostener.", "Inspección geomecánica diaria."]},
    {"riesgo": "Gaseamiento y falta de oxígeno", "controles": ["Medir oxígeno y gases antes de ingresar.", "Ventilar después de cada disparo y respetar el tiempo de espera.", "Clausurar labores sin ventilación.", "Portar autorrescatador."]},
    {"riesgo": "Equipos móviles y tránsito", "controles": ["Check list pre-uso.", "Respetar velocidades y prioridad de paso.", "Usar estocadas como refugio peatonal.", "Luces y alarmas de retroceso operativas."]},
    {"riesgo": "Voladura", "controles": ["Horarios fijos de disparo y vigías en todos los accesos.", "Conteo de tiros y control de tiros cortados.", "Manipulación de explosivos solo por personal autorizado.", "Polvorines con control de entradas y salidas."]},
    {"riesgo": "Caída a echaderos, chimeneas y piques", "controles": ["Parrillas y barandas en echaderos.", "Arnés y línea de vida en chimeneas.", "Señalización y bloqueo de accesos."]},
    {"riesgo": "Energía eléctrica y mecánica", "controles": ["Bloqueo y etiquetado.", "Personal calificado.", "Inspección de cables y tableros."]},
    {"riesgo": "Incendio subterráneo", "controles": ["Extintores en equipos y estaciones.", "Plan de respuesta a emergencias y simulacros.", "Refugios mineros equipados."]}],
  "fuentes": ["DS024", "PE_USO"]},
 {"id": "desatado-rocas", "titulo": "Desatado de rocas paso a paso",
  "contenido": "Procedimiento general. Siempre sigue el PETS de tu unidad.",
  "pasos": ["Ventilar la labor y verificar condiciones de gases.", "Iluminar bien el techo y los hastiales.",
            "Usar barretilla del largo adecuado a la altura de la labor.", "Desatar desde zona segura (ya desatada o sostenida), avanzando hacia el frente.",
            "Ubicarse a un costado, nunca debajo de la roca a desatar.", "Golpear y escuchar: sonido hueco indica roca suelta.",
            "Repetir el desatado durante la guardia, sobre todo después de cada disparo.", "Reportar si la roca no se puede desatar y colocar sostenimiento."],
  "fuentes": ["PE_USO", "DS024"]},
 {"id": "ventilacion", "titulo": "Ventilación (valores de referencia)",
  "contenido": "Valores de referencia usados en la minería peruana. Confírmalos con el texto vigente del reglamento.",
  "puntos": ["Oxígeno mínimo en el aire: 19,5%.",
             "Caudal de aire por persona según altitud: 3 m³/min hasta 1500 msnm, 4 de 1500 a 3000, 5 de 3000 a 4000, y 6 por encima de 4000 msnm.",
             "Equipos diésel: alrededor de 3 m³/min por cada HP de potencia efectiva.",
             "Velocidad mínima del aire en labores: 20 m/min.",
             "Monitorear CO, NO2, CO2 y O2 en los frentes de trabajo, sobre todo después de la voladura."],
  "fuentes": ["DS024"], "confianza": "verificar artículo vigente"},
 {"id": "indicadores-seguridad", "titulo": "Indicadores de seguridad",
  "contenido": "Indicadores estadísticos de seguridad usados en la minería peruana.",
  "formulas": [
    {"nombre": "Índice de frecuencia (IF)", "expresion": "IF = N° accidentes incapacitantes y mortales × 1 000 000 / horas-hombre trabajadas"},
    {"nombre": "Índice de severidad (IS)", "expresion": "IS = días perdidos o cargados × 1 000 000 / horas-hombre trabajadas"},
    {"nombre": "Índice de accidentabilidad (IA)", "expresion": "IA = IF × IS / 1000"}],
  "fuentes": ["DS024"]},
 {"id": "emergencias", "titulo": "Respuesta a emergencias",
  "contenido": "Cada unidad debe tener un plan de preparación y respuesta a emergencias.",
  "puntos": ["Brigada de rescate minero entrenada y equipada (Anexo 20 lista el equipo mínimo).",
             "Refugios mineros con aire comprimido, agua, comunicación y botiquín (Anexo 19).",
             "Simulacros periódicos de incendio, sismo, gaseamiento y derrumbe.",
             "Notificar a la autoridad los accidentes mortales e incidentes peligrosos con los formatos del reglamento (Anexos 21 a 23)."],
  "fuentes": ["DS024"]},
 {"id": "salud-ocupacional", "titulo": "Salud ocupacional",
  "contenido": "Agentes que afectan la salud del trabajador minero y cómo controlarlos.",
  "puntos": ["Polvo y sílice: riesgo de silicosis. Perforación con agua, ventilación y respirador con filtro adecuado.",
             "Ruido: límites en Anexo 12; protector auditivo y medición periódica.",
             "Altura: riesgo de hipoxia y mal de montaña; evaluación médica y aclimatación.",
             "Estrés térmico: valores límite en Anexo 13.",
             "Agentes químicos como el cianuro: límites en Anexo 15, hojas de seguridad, detectores de HCN.",
             "Exámenes médicos ocupacionales de ingreso, periódicos y de retiro (ficha en Anexo 16)."],
  "fuentes": ["DS024"]},
 {"id": "medio-ambiente", "titulo": "Gestión ambiental",
  "contenido": "Compromisos ambientales típicos de una mina aurífera subterránea con planta de cianuración.",
  "puntos": ["Cumplir los compromisos del instrumento de gestión ambiental aprobado.",
             "Manejo de relaves: estabilidad física y química del depósito, monitoreo de filtraciones.",
             "Cianuro: transporte, almacenamiento y uso controlado; degradación antes de reutilizar agua o disponer relaves.",
             "Control de drenaje ácido de roca en canchas de desmonte.",
             "Monitoreo de calidad de agua, aire y suelo según el plan aprobado.",
             "Plan de cierre de minas con garantía financiera (Ley 28090)."],
  "fuentes": ["CMH_PLANTA", "SME"]},
]

# ---------------- REFERENCIA CMH ----------------
R = [
 {"id": "cmh", "titulo": "Consorcio Minero Horizonte (referencia)",
  "contenido": "Empresa minera aurífera peruana fundada en 1978, que explota oro en minería subterránea en el Batolito de Pataz, región La Libertad.",
  "puntos": ["Unidades de producción: Parcoy (principal, explotación desde 1986) y Los Zambos (adquirida en 2008).",
             "Método de explotación en Parcoy: corte y relleno ascendente en vetas.",
             "Planta Parcoy: flotación y cianuración con recuperación por Merrill-Crowe. Un estudio evaluó ampliarla de 1500 a 2000 TMD con una inversión estimada de US$ 8,38 millones.",
             "Certificaciones declaradas: ISO 45001 (seguridad y salud), ISO 14001 (ambiental) e ISO 9001 (calidad).",
             "Por qué sirve de referencia: es un caso típico de mina mediana subterránea aurífera peruana, con vetas angostas, relleno, planta de cianuración y fuerte exigencia en SSOMA."],
  "fuentes": ["CMH", "CMH_PLANTA", "CMH_PROD", "CMH_COSTOS"],
  "confianza": "datos públicos; pueden no estar actualizados"},
]

# Ficha de costos peruana
base["economia"].append(
 {"id": "costos-unitarios-subterranea", "titulo": "Estructura de costos unitarios en mina subterránea peruana",
  "contenido": "En las minas subterráneas peruanas el costo se calcula por labor: US$/m para avances (galerías, cruceros, chimeneas, rampas) y US$/TMS para explotación de tajos. Así se paga también a las contratas.",
  "formulas": [
    {"nombre": "Precio unitario de una labor", "expresion": "PU = mano_de_obra (con leyes sociales) + materiales + explosivos + EPP + herramientas + costo_horario_equipos + gastos_generales + utilidad"},
    {"nombre": "Costo de avance por metro", "expresion": "US$/m = costo_por_disparo / avance_efectivo_por_disparo_m"},
    {"nombre": "Costo de explotación por tonelada", "expresion": "US$/TMS = costo_por_disparo / (volumen_roto_m³ × densidad × (1 − humedad))"},
    {"nombre": "Ley diluida", "expresion": "Ley_diluida = Ley_veta × ancho_veta / ancho_minado"}],
  "notas": ["En vetas angostas, la dilución pesa mucho en el costo por onza: controlar el ancho de minado es clave.",
            "El costo de sostenimiento y relleno puede ser una parte importante del costo de explotación en corte y relleno."],
  "fuentes": ["CMH_COSTOS", "SME"]})

FQ = [
 ("¿Cuál es la diferencia entre IPERC línea base e IPERC continuo?", "El de línea base lo hace la empresa por proceso y se actualiza al menos una vez al año. El continuo lo llena el trabajador en campo al inicio de cada tarea, con los peligros del momento.", ["DS024"]),
 ("¿Cuándo necesito un PETAR?", "Para todo trabajo de alto riesgo: en altura, en caliente, en espacios confinados, con energía eléctrica, excavaciones, izaje y otros que defina la empresa. Lo firman en cada guardia el supervisor y el jefe de área.", ["DS024"]),
 ("¿Qué diferencia hay entre PETS y ATS?", "El PETS es el procedimiento formal y aprobado de una tarea. El ATS es un análisis rápido que se hace cuando la tarea es nueva o no tiene PETS.", ["DS024"]),
 ("¿Puedo retirarme de una labor si veo un peligro?", "Sí. El reglamento reconoce el derecho del trabajador a retirarse de un área cuando detecta un peligro de alto riesgo, avisando de inmediato a su supervisor.", ["DS024"]),
 ("¿Cómo se calcula el índice de frecuencia?", "IF = número de accidentes incapacitantes y mortales × 1 000 000 / horas-hombre trabajadas.", ["DS024"]),
 ("¿Qué hago ante un tiro cortado?", "No te acerques ni lo reperfores. Señaliza y bloquea el acceso, avisa al supervisor y sigue el procedimiento de la unidad para eliminarlo.", ["DS024", "PE_USO"]),
 ("¿Cuándo es obligatorio el Comité de SSO?", "Con 20 trabajadores o más. Con menos de 20 se designa un supervisor de SSO.", ["DS024"]),
 ("¿Qué método de explotación usa Consorcio Minero Horizonte?", "En Parcoy, corte y relleno ascendente en vetas, con planta de flotación y cianuración.", ["CMH_PLANTA"]),
 ("¿Qué es una contrata?", "Una empresa contratista minera que ejecuta labores para el titular de la mina y cobra por precio unitario (US$/m o US$/TMS).", ["PE_USO"]),
 ("¿Por qué el desatado es tan importante?", "Porque la caída de rocas ha sido históricamente una de las principales causas de accidentes mortales en la minería subterránea peruana. El desatado y el sostenimiento son los controles clave.", ["DS024", "PE_USO"]),
]
base["faq"] = [{"pregunta": q, "respuesta": a, "fuentes": s} for q, a, s in FQ] + base["faq"]
base["ssoma"] = S
base["referencias_empresa"] = R

# Ajustes de procesos al contexto peruano
procs = {p["id"]: p for p in base["procesos"]}
base["procesos"].insert(0,
 {"id": "ciclo-subterraneo", "titulo": "Ciclo de minado subterráneo (corte y relleno)",
  "resumen": "Ciclo típico de un tajo en una mina aurífera de vetas en el Perú, como las de Pataz.",
  "pasos": ["Inicio de guardia: charla de 5 minutos, IPERC continuo y PETAR si aplica.",
            "Ventilación y verificación de gases.", "Desatado de rocas.", "Sostenimiento según tabla GSI.",
            "Perforación con jackleg o jumbo.", "Carguío de explosivos y disparo en horario fijo, con vigías.",
            "Ventilación y espera de gases.", "Limpieza con scoop o winche hacia el echadero.",
            "Acarreo a superficie con locomotora o volquete.", "Relleno del tajo (detrítico, hidráulico o en pasta) para la siguiente rebanada."],
  "indicadores": ["Avance por disparo (m)", "TMS por guardia", "Ley diluida", "Costo US$/TMS", "Índice de frecuencia"],
  "consejos": ["Controlar el ancho de minado reduce la dilución, que en vetas angostas decide la rentabilidad.",
               "Ninguna tarea empieza sin desatado y sin IPERC continuo."],
  "fuentes": ["CMH_PLANTA", "DS024", "PE_USO"]})
procs["seguridad-operacional"]["pasos"] = ["Charla de inicio de guardia.", "IPERC continuo en la labor.",
  "Seguir el PETS de la tarea; PETAR si es trabajo de alto riesgo.", "Check list pre-uso de equipos.",
  "Bloqueo y etiquetado antes de intervenir equipos.", "Reportar actos y condiciones subestándar, incidentes y casi incidentes."]
procs["seguridad-operacional"]["consejos"] = ["Revisa la sección SSOMA para el detalle de cada herramienta y la normativa."]
procs["seguridad-operacional"]["fuentes"] = ["DS024"]

# validar referencias
ids = set(F)
for g in G: assert g["fuente"] in ids, g
for sec in ("procesos", "logistica", "economia", "faq", "ssoma", "referencias_empresa"):
    for x in base[sec]:
        for f in x["fuentes"]: assert f in ids, (sec, x.get("id"), f)
names = [g["termino"].lower() for g in G]
assert len(names) == len(set(names)), "términos duplicados"

json.dump(base, open(JP, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------- Markdown ----------
def src(l): return ", ".join(l)
md = [f"# Base de conocimiento minero v{base['version']} (Perú)", "", f"_{base['aviso']}_", "",
      f"Contenido: {len(G)} términos, {len(S)} fichas de SSOMA, {len(base['procesos'])} procesos, {len(base['logistica'])} fichas de logística, "
      f"{len(base['economia'])} fichas de CAPEX/OPEX, {len(base['faq'])} preguntas frecuentes y 1 empresa de referencia.", ""]

def ficha(x, lvl="###"):
    out = [f"{lvl} {x['titulo']}", "", x.get("contenido") or x.get("resumen", ""), ""]
    if x.get("confianza"): out += [f"_Confianza: {x['confianza']}._", ""]
    for i, s in enumerate(x.get("pasos", []), 1): out.append(f"{i}. {s}")
    for s in x.get("puntos", []): out.append(f"- {s}")
    for r in x.get("riesgos", []):
        out.append(f"- **{r['riesgo']}:** " + " ".join(r["controles"]))
    for fo in x.get("formulas", []):
        out.append(f"- **{fo['nombre']}:** `{fo['expresion']}`" + (f" {fo['interpretacion']}" if fo.get("interpretacion") else ""))
    for n in x.get("notas", []): out.append(f"- {n}")
    if x.get("indicadores"): out += ["", "**Indicadores:** " + "; ".join(x["indicadores"])]
    if x.get("consejos"): out += [""] + [f"> {c}" for c in x["consejos"]]
    if x.get("tabla"):
        out += ["", "| Concepto | Rango |", "|---|---|"] + [f"| {r['concepto']} | {r['rango']} |" for r in x["tabla"]]
    out += ["", f"Fuentes: {src(x['fuentes'])}", ""]
    return out

md += ["## SSOMA: seguridad, salud ocupacional y medio ambiente", ""]
for x in S: md += ficha(x)
md += ["## Empresa de referencia", ""]
for x in R: md += ficha(x)
md += ["## Procesos", ""]
for x in base["procesos"]: md += ficha(x)
md += ["## Logística", ""]
for x in base["logistica"]: md += ficha(x)
md += ["## CAPEX y OPEX", ""]
for x in base["economia"]: md += ficha(x)
md += ["## Preguntas frecuentes", ""]
for q in base["faq"]: md += [f"**{q['pregunta']}**", "", f"{q['respuesta']} [{src(q['fuentes'])}]", ""]
md += ["## Glosario", ""]
order = ["seguridad", "medio_ambiente", "planeamiento", "operaciones", "geologia", "procesamiento", "economia", "logistica"]
cats = {}
for g in G: cats.setdefault(g["categoria"], []).append(g)
for c in order + [c for c in cats if c not in order]:
    if c not in cats: continue
    md += [f"### {c.replace('_', ' ').capitalize()}", ""]
    for g in sorted(cats[c], key=lambda y: y["termino"].lower()):
        syn = f" _(también: {', '.join(g['sinonimos'])})_" if g["sinonimos"] else ""
        md.append(f"- **{g['termino']}**{syn}: {g['definicion']} [{g['fuente']}]")
    md.append("")
md += ["## Fuentes", ""]
for k, v in F.items():
    md.append(f"- **{k}**: " + (f"[{v['titulo']}]({v['url']})" if v["url"] else v["titulo"]))
open(os.path.join(D, "base_conocimiento.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
print(len(G), len(S), len(base["procesos"]), len(base["logistica"]), len(base["economia"]), len(base["faq"]))
