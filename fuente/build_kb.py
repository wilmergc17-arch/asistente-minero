import json, os, sys

OUT = sys.argv[1]

fuentes = {
    "ANM": {"titulo": "Glosario Técnico Minero, Agencia Nacional de Minería (Colombia)",
            "url": "https://www.anm.gov.co/sites/default/files/DocumentosAnm/glosariominero.pdf"},
    "D2191": {"titulo": "Decreto 2191 de 2003, Glosario Técnico Minero (Colombia)",
              "url": "https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=9198"},
    "JORC": {"titulo": "Código JORC 2012 (reporte de recursos y reservas)",
             "url": "https://www.jorc.org/docs/JORC_code_2012.pdf"},
    "MF": {"titulo": "Estudio sobre factor de acoplamiento pala-camión, Journal of Mining and Environment",
           "url": "https://jme.shahroodut.ac.ir/article_3606.html"},
    "WITS": {"titulo": "Métodos de simulación del ciclo pala-camión en minería superficial, Univ. Witwatersrand",
             "url": "https://wiredspace.wits.ac.za/items/2a04ef59-6d36-4163-92b1-591204285d0b"},
    "ENERGIMINAS": {"titulo": "Proceso de minado en Cerro Corona (Gold Fields), Energiminas 2023",
                    "url": "https://energiminas.com/2023/08/11/gold-fields-ejecuta-proceso-de-minado-eficiente-en-cerro-corona-con-7-equipos-de-carguio-y-45-volquetes/"},
    "TSE": {"titulo": "Costos de chancado y molienda, Thunder Said Energy",
            "url": "https://thundersaidenergy.com/downloads/mining-crushing-grinding-and-communition-costs/"},
    "MTTODD": {"titulo": "Mt Todd Benchmarking Study (Vista Gold, 2019), ejemplo de estudio de costos",
               "url": "https://vistagold.com/images/pdf/technical_reports/2019/Mt_Todd_Benchmarking_Study_-_Rev_3.2_Public.pdf"},
    "SME": {"titulo": "SME Mining Engineering Handbook, 3ª ed. (libro de referencia, conocimiento técnico general)",
            "url": None},
}

# ---------------- GLOSARIO ----------------
G = []
def t(termino, definicion, categoria, fuente="ANM", sinonimos=None):
    G.append({"termino": termino, "definicion": definicion, "categoria": categoria,
              "sinonimos": sinonimos or [], "fuente": fuente})

# Geología y recursos
t("Mena", "Mineral o roca que contiene un elemento de valor en concentración suficiente para ser extraído con beneficio económico.", "geologia", sinonimos=["mineral económico"])
t("Ganga", "Minerales sin valor económico que acompañan a la mena y se separan en el procesamiento.", "geologia")
t("Desmonte", "Material estéril sin valor económico que se extrae para acceder al mineral y se envía a botaderos.", "geologia", sinonimos=["estéril", "lastre", "waste"])
t("Ley", "Concentración del elemento de valor en el mineral, expresada en % (cobre), g/t (oro, plata) u otras unidades.", "geologia", sinonimos=["grade"])
t("Ley de corte", "Ley mínima a la que un bloque de mineral paga su extracción y procesamiento. Por debajo se trata como desmonte o mineral marginal.", "geologia", "SME", ["cut-off grade"])
t("Recurso mineral", "Concentración de material de interés económico con perspectivas razonables de extracción. Se clasifica en inferido, indicado y medido según el nivel de confianza geológica.", "geologia", "JORC")
t("Reserva mineral", "Parte económicamente extraíble de un recurso medido o indicado, tras aplicar factores modificantes (mineros, metalúrgicos, económicos, legales, ambientales). Se clasifica en probable y probada.", "geologia", "JORC")
t("Factores modificantes", "Consideraciones mineras, metalúrgicas, económicas, de mercado, legales, ambientales, sociales y gubernamentales usadas para convertir recursos en reservas.", "geologia", "JORC")
t("Modelo de bloques", "Representación 3D del yacimiento dividida en bloques, cada uno con ley, densidad, tipo de roca y otros atributos estimados.", "planeamiento", "SME")
t("Dilución", "Material estéril o de baja ley que se mezcla con el mineral durante la extracción y baja la ley enviada a planta.", "planeamiento", "SME")
t("Recuperación minera", "Porcentaje del mineral planificado que realmente se extrae y llega a planta.", "planeamiento", "SME")
t("Densidad aparente", "Masa por unidad de volumen de la roca in situ (t/m³). Sirve para convertir volúmenes en toneladas.", "geologia", "SME")
t("Esponjamiento", "Aumento de volumen de la roca al ser fragmentada. El factor de esponjamiento suele estar entre 1,2 y 1,6.", "operaciones", "SME", ["swell factor"])
t("Veta", "Cuerpo mineralizado tabular, relleno de una fractura en la roca.", "geologia", sinonimos=["filón"])
t("Yacimiento", "Concentración natural de minerales que puede ser explotada económicamente.", "geologia", sinonimos=["depósito"])

# Planeamiento y diseño
t("Tajo abierto", "Método de explotación superficial en el que se extrae el mineral desde la superficie formando un hoyo escalonado.", "planeamiento", sinonimos=["open pit", "rajo abierto"])
t("Banco", "Escalón horizontal del tajo, definido por su altura (típicamente 10 a 15 m en minería grande) y su ancho.", "planeamiento", "SME")
t("Berma", "Plataforma horizontal que se deja entre bancos para contener caída de rocas y dar estabilidad.", "planeamiento", "SME")
t("Talud", "Pared inclinada del tajo. Se habla de ángulo de cara de banco, ángulo interrampa y ángulo global.", "planeamiento", "SME")
t("Relación de desbroce", "Toneladas de desmonte que deben moverse por cada tonelada de mineral. Indicador clave de costo en tajo abierto.", "planeamiento", "SME", ["stripping ratio", "relación estéril/mineral"])
t("Pit final", "Límite económico último del tajo, calculado con algoritmos como Lerchs-Grossmann o pseudoflow.", "planeamiento", "SME")
t("Fase", "Subdivisión del tajo que se explota secuencialmente para adelantar el mineral y diferir el desbroce.", "planeamiento", "SME", ["pushback"])
t("Rampa", "Vía inclinada que conecta bancos y permite el tránsito de equipos. Pendientes típicas de 8% a 10%.", "planeamiento", "SME")
t("Plan de minado", "Programa de extracción que define qué, cuánto y cuándo se mina, por periodo (vida de mina, anual, mensual, semanal).", "planeamiento", "SME")
t("Subterránea", "Explotación mediante labores bajo la superficie (galerías, rampas, piques, tajeos).", "planeamiento", sinonimos=["socavón"])
t("Sublevel stoping", "Método subterráneo de tajeo por subniveles con perforación larga y voladura en tajeos abiertos.", "planeamiento", "SME", ["tajeo por subniveles"])
t("Corte y relleno", "Método subterráneo donde se extrae el mineral en franjas horizontales y se rellena el vacío para dar soporte.", "planeamiento", "SME", ["cut and fill"])
t("Block caving", "Método subterráneo masivo en el que se socava la base del cuerpo y el mineral se hunde por gravedad.", "planeamiento", "SME", ["hundimiento por bloques"])
t("Pique", "Excavación vertical que conecta superficie con los niveles subterráneos para transporte de personal, mineral o ventilación.", "planeamiento", sinonimos=["shaft"])
t("Galería", "Excavación horizontal subterránea de acceso o transporte.", "planeamiento")
t("Chimenea", "Excavación vertical o inclinada entre niveles, usada para ventilación, traspaso de mineral o acceso.", "planeamiento", sinonimos=["raise"])

# Operaciones
t("Perforación", "Operación que abre taladros en la roca para alojar explosivos.", "operaciones")
t("Voladura", "Fragmentación de la roca con explosivos.", "operaciones", sinonimos=["tronadura"])
t("Malla de perforación", "Disposición geométrica de los taladros, definida por burden y espaciamiento.", "operaciones", "SME")
t("Burden", "Distancia entre una fila de taladros y la cara libre o la fila siguiente.", "operaciones", "SME", ["piedra"])
t("Espaciamiento", "Distancia entre taladros de una misma fila.", "operaciones", "SME")
t("Sobreperforación", "Longitud que se perfora por debajo del nivel del piso del banco para evitar repiés.", "operaciones", "SME", ["subdrill"])
t("Factor de carga", "Cantidad de explosivo por volumen o peso de roca volada (kg/m³ o kg/t).", "operaciones", "SME", ["powder factor"])
t("ANFO", "Explosivo compuesto de nitrato de amonio (aprox. 94%) y petróleo diésel (aprox. 6%). No resiste agua.", "operaciones", "SME")
t("Emulsión", "Explosivo resistente al agua formado por una solución oxidante en una fase de combustible.", "operaciones", "SME")
t("Fragmentación", "Distribución de tamaños de la roca después de la voladura. Influye en el carguío, acarreo y chancado.", "operaciones", "SME")
t("Carguío", "Operación de cargar el material volado a los camiones con palas, excavadoras o cargadores frontales.", "operaciones")
t("Acarreo", "Transporte del material desde el frente hasta chancadora, pila o botadero.", "operaciones", sinonimos=["transporte", "haulage"])
t("Botadero", "Área de depósito del desmonte.", "operaciones", sinonimos=["escombrera", "depósito de desmonte"])
t("Stockpile", "Pila de mineral almacenado para regular la alimentación a planta o guardar mineral de baja ley.", "operaciones", sinonimos=["cancha de mineral", "acopio"])
t("Sostenimiento", "Elementos que estabilizan excavaciones subterráneas: pernos, mallas, shotcrete, cimbras.", "operaciones", "SME", ["fortificación"])
t("Desatado", "Retiro manual o mecanizado de rocas sueltas del techo y paredes tras la voladura.", "operaciones", sinonimos=["acuñadura", "scaling"])
t("Disponibilidad mecánica", "Porcentaje del tiempo total en que el equipo está apto para operar (no en mantenimiento ni reparación).", "operaciones", "SME")
t("Utilización", "Porcentaje del tiempo disponible en que el equipo efectivamente opera.", "operaciones", "SME")
t("OEE", "Eficiencia global del equipo: disponibilidad × utilización (o rendimiento) × calidad.", "operaciones", "SME")
t("Despacho", "Sistema que asigna camiones a palas y destinos en tiempo real para maximizar producción.", "operaciones", "WITS", ["dispatch"])

# Procesamiento
t("Chancado", "Reducción de tamaño de la roca en chancadoras primaria, secundaria y terciaria.", "procesamiento", sinonimos=["trituración"])
t("Molienda", "Reducción fina de tamaño en molinos (SAG, bolas, barras) para liberar el mineral.", "procesamiento")
t("Flotación", "Proceso que separa minerales aprovechando diferencias de afinidad con burbujas de aire, con reactivos.", "procesamiento")
t("Lixiviación", "Disolución del metal de interés con una solución química (por ejemplo cianuro para oro, ácido sulfúrico para cobre).", "procesamiento")
t("Concentrado", "Producto de la planta con alta ley del metal, listo para fundición o venta.", "procesamiento")
t("Relave", "Residuo sólido-líquido que queda tras el procesamiento, depositado en presas o depósitos de relaves.", "procesamiento", sinonimos=["cola", "tailings"])
t("Recuperación metalúrgica", "Porcentaje del metal contenido en el mineral alimentado que pasa al producto final.", "procesamiento", "SME")
t("Work index", "Índice de Bond que mide la energía requerida para moler un mineral (kWh/t).", "procesamiento", "SME", ["índice de trabajo"])

# Economía
t("CAPEX", "Gastos de capital: inversión en activos de larga vida (equipos, planta, infraestructura, desarrollo de mina).", "economia", "SME", ["capital expenditure", "inversión"])
t("OPEX", "Gastos operativos recurrentes: mano de obra, combustible, explosivos, energía, repuestos, contratistas.", "economia", "SME", ["operating expenditure", "costo operativo"])
t("Capital de sostenimiento", "CAPEX que se invierte durante la operación para mantener la capacidad (reemplazo de flota, recrecimiento de relaves).", "economia", "SME", ["sustaining capex"])
t("VAN", "Valor actual neto: suma de flujos de caja futuros descontados a una tasa, menos la inversión.", "economia", "SME", ["NPV", "valor presente neto"])
t("TIR", "Tasa interna de retorno: tasa de descuento con la que el VAN es cero.", "economia", "SME", ["IRR"])
t("Payback", "Tiempo necesario para recuperar la inversión con los flujos de caja.", "economia", "SME", ["periodo de recuperación"])
t("Costo C1", "Costo de caja directo por unidad de metal: mina, planta, G&A del sitio, transporte y refinación, menos créditos de subproductos.", "economia", "SME", ["cash cost"])
t("AISC", "All-in sustaining cost: costo C1 más capital de sostenimiento, regalías, G&A corporativo y otros costos para mantener la producción.", "economia", "SME")
t("Valor de mineral (NSR)", "Ingreso neto por tonelada de mineral después de descontar recuperación, fundición, refinación y transporte.", "economia", "SME", ["net smelter return"])
t("Regalía", "Pago al Estado o a un tercero, normalmente un porcentaje de ingresos o utilidades.", "economia")
t("Cierre de mina", "Conjunto de actividades para rehabilitar el área al final de la vida de la mina; tiene provisión de costos propia.", "economia")

# Logística
t("Cadena de suministro minera", "Flujo de insumos (combustible, explosivos, repuestos, reactivos) hacia la mina y de productos (concentrado, cátodos) hacia puerto o cliente.", "logistica", "SME")
t("Factor de acoplamiento", "Relación entre la capacidad de la flota de camiones y la de los equipos de carguío. Un valor cercano a 1 indica flota equilibrada.", "logistica", "MF", ["match factor"])
t("Tiempo de ciclo", "Tiempo que tarda un camión en completar un viaje: cola + carga + acarreo cargado + descarga + retorno vacío + esperas.", "logistica", "WITS")
t("Stock de seguridad", "Inventario adicional para cubrir variaciones de demanda o retrasos de entrega.", "logistica")
t("Punto de reorden", "Nivel de inventario en el que debe emitirse un nuevo pedido: demanda diaria × tiempo de entrega + stock de seguridad.", "logistica")
t("Clasificación ABC", "Clasificación de inventario por valor de consumo: A (alto valor, pocos ítems), B (intermedio), C (bajo valor, muchos ítems).", "logistica")
t("Repuesto crítico", "Componente cuya falta detiene un equipo clave y cuyo tiempo de entrega es largo. Se mantiene en stock aunque rote poco.", "logistica")
t("Polvorín", "Almacén autorizado para explosivos, con controles de seguridad y registro.", "logistica")
t("Incoterms", "Reglas internacionales que definen responsabilidades de comprador y vendedor en el transporte (FOB, CIF, DAP, etc.). Se usan en la venta de concentrados.", "logistica")

# Seguridad
t("IPERC", "Identificación de Peligros, Evaluación de Riesgos y medidas de Control. Herramienta de gestión de seguridad usada en la minería peruana.", "seguridad")
t("PETS", "Procedimiento Escrito de Trabajo Seguro: describe paso a paso cómo realizar una tarea de forma segura.", "seguridad")
t("Bloqueo y etiquetado", "Procedimiento que aísla fuentes de energía de un equipo antes de intervenirlo.", "seguridad", sinonimos=["LOTO"])
t("Gases de voladura", "Gases tóxicos (CO, NOx) generados por la voladura. Requieren ventilación y tiempo de espera antes de ingresar.", "seguridad", "SME")

# ---------------- PROCESOS ----------------
P = [
 {"id": "ciclo-minado", "titulo": "Ciclo de minado en tajo abierto",
  "resumen": "Secuencia básica de operaciones unitarias que se repite en cada banco.",
  "pasos": ["Perforación de taladros según malla diseñada.", "Carga de explosivos y voladura.",
            "Carguío del material fragmentado con palas, excavadoras o cargadores.",
            "Acarreo con camiones a chancadora, stockpile o botadero.",
            "Servicios auxiliares: mantenimiento de vías, drenaje, limpieza con tractores y motoniveladoras."],
  "indicadores": ["Toneladas por día movidas", "Costo por tonelada en cada operación", "Fragmentación P80", "Productividad de pala (t/h)"],
  "consejos": ["Una mejor fragmentación baja el costo de carguío, acarreo y chancado aunque suba el costo de voladura (concepto mine-to-mill).",
               "Mantener las vías en buen estado reduce el tiempo de ciclo y el desgaste de neumáticos."],
  "fuentes": ["ENERGIMINAS", "SME"]},
 {"id": "perforacion-voladura", "titulo": "Perforación y voladura",
  "resumen": "Diseño y ejecución de la fragmentación de roca.",
  "pasos": ["Definir altura de banco, diámetro de taladro, burden y espaciamiento.",
            "Marcar la malla en el terreno con topografía.", "Perforar y verificar profundidad de cada taladro.",
            "Cargar explosivo (ANFO en seco, emulsión con agua) y colocar retacado.",
            "Conectar la secuencia de iniciación y evacuar el área.", "Disparar, ventilar y revisar tiros fallados."],
  "indicadores": ["Factor de carga (kg/t)", "Metros perforados por turno", "Costo por tonelada volada", "Fragmentación"],
  "consejos": ["El burden suele estar entre 25 y 40 veces el diámetro del taladro como primera aproximación.",
               "Registrar cada voladura para correlacionar diseño con resultados."],
  "fuentes": ["SME"]},
 {"id": "carguio-acarreo", "titulo": "Carguío y acarreo",
  "resumen": "Mover el material volado al destino correcto con la flota más eficiente.",
  "pasos": ["Asignar palas a frentes según plan de minado.", "Dimensionar flota de camiones con el factor de acoplamiento.",
            "Usar un sistema de despacho para asignar camiones en tiempo real.",
            "Controlar destinos: mineral a chancadora o stockpile, desmonte a botadero."],
  "indicadores": ["Tiempo de ciclo", "Factor de acoplamiento", "Colas en pala", "Rendimiento t/h por camión", "Costo $/t-km"],
  "consejos": ["El acarreo suele ser la partida más grande del costo mina en tajo abierto.",
               "Colas largas en pala indican exceso de camiones; palas esperando indican déficit."],
  "fuentes": ["MF", "WITS", "SME"]},
 {"id": "procesamiento", "titulo": "Procesamiento de minerales",
  "resumen": "Transformar el mineral en un producto vendible.",
  "pasos": ["Chancado primario, secundario y terciario.", "Molienda (SAG y bolas) hasta el tamaño de liberación.",
            "Concentración: flotación para sulfuros, lixiviación para óxidos y oro.",
            "Espesamiento y filtrado del concentrado.", "Disposición de relaves."],
  "indicadores": ["Toneladas tratadas por hora", "Recuperación metalúrgica", "Ley de concentrado", "kWh/t", "Consumo de reactivos"],
  "consejos": ["La molienda suele ser el mayor consumidor de energía de la planta."],
  "fuentes": ["TSE", "SME"]},
 {"id": "mantenimiento", "titulo": "Mantenimiento de equipos mineros",
  "resumen": "Mantener la disponibilidad de la flota al menor costo.",
  "pasos": ["Plan de mantenimiento preventivo por horas de operación.", "Monitoreo de condición (análisis de aceite, vibraciones, termografía).",
            "Gestión de componentes mayores (motores, transmisiones) con programa de cambio.",
            "Registro de fallas y análisis de causa raíz."],
  "indicadores": ["Disponibilidad mecánica", "MTBF (tiempo medio entre fallas)", "MTTR (tiempo medio de reparación)", "Costo de mantenimiento por hora"],
  "consejos": ["Una disponibilidad objetivo habitual para camiones grandes está en torno a 85% a 90%."],
  "fuentes": ["SME"]},
 {"id": "seguridad-operacional", "titulo": "Gestión de seguridad en operación",
  "resumen": "Controles mínimos antes y durante cualquier tarea.",
  "pasos": ["Identificar peligros y evaluar riesgos (IPERC).", "Seguir el procedimiento escrito de la tarea (PETS).",
            "Aplicar bloqueo y etiquetado antes de intervenir equipos.", "Reportar incidentes y casi incidentes."],
  "indicadores": ["Índice de frecuencia", "Índice de severidad", "Reportes de casi incidentes"],
  "consejos": ["La normativa varía por país; verificar el reglamento local de seguridad minera."],
  "fuentes": ["SME"]},
]

# ---------------- LOGISTICA ----------------
L = [
 {"id": "dimensionamiento-flota", "titulo": "Dimensionamiento de flota de camiones",
  "contenido": "Para saber cuántos camiones necesita una pala, se compara el tiempo de ciclo del camión con el tiempo que tarda la pala en cargarlo.",
  "formulas": [
    {"nombre": "Tiempo de ciclo del camión", "expresion": "Tc = t_cola + t_carga + t_viaje_cargado + t_descarga + t_viaje_vacio + t_maniobras"},
    {"nombre": "Camiones por pala", "expresion": "N = Tc / t_carga"},
    {"nombre": "Factor de acoplamiento", "expresion": "MF = (camiones × t_carga) / (palas × Tc)",
     "interpretacion": "MF < 1: palas esperando camiones. MF > 1: camiones haciendo cola. Óptimo económico cerca de 1."}],
  "fuentes": ["MF", "WITS"]},
 {"id": "inventario", "titulo": "Gestión de inventario de insumos y repuestos",
  "contenido": "El objetivo es no detener la operación por falta de insumos sin inmovilizar demasiado capital en almacén.",
  "formulas": [
    {"nombre": "Punto de reorden", "expresion": "PR = consumo_diario × tiempo_entrega_dias + stock_seguridad"},
    {"nombre": "Stock de seguridad", "expresion": "SS = Z × σ_consumo_diario × √tiempo_entrega_dias",
     "interpretacion": "Z = 1,65 para 95% de nivel de servicio; 2,33 para 99%."},
    {"nombre": "Lote económico (EOQ)", "expresion": "EOQ = √(2 × demanda_anual × costo_pedido / costo_mantener_unidad_año)"}],
  "fuentes": ["SME"]},
 {"id": "combustible", "titulo": "Logística de combustible",
  "contenido": "El diésel es uno de los insumos más grandes en minería superficial. Se controla por consumo en litros por hora de cada equipo y autonomía de tanques en sitio.",
  "formulas": [
    {"nombre": "Días de autonomía", "expresion": "Autonomía = capacidad_tanques_litros / consumo_diario_litros"},
    {"nombre": "Consumo de la flota", "expresion": "Consumo diario = Σ (litros_por_hora_equipo × horas_operadas)"}],
  "fuentes": ["SME"]},
 {"id": "explosivos", "titulo": "Logística de explosivos",
  "contenido": "Los explosivos requieren polvorines autorizados, control de entradas y salidas y transporte con permisos. El consumo se planifica con el factor de carga y el tonelaje a volar.",
  "formulas": [{"nombre": "Explosivo requerido", "expresion": "kg_explosivo = toneladas_a_volar × factor_de_carga_kg_por_t"}],
  "fuentes": ["SME"]},
 {"id": "concentrado", "titulo": "Transporte de concentrado a puerto",
  "contenido": "El concentrado se transporta en camiones encapsulados, tren o mineroducto hasta el puerto. Se controla humedad (límite de humedad transportable, TML), peso y muestreo para la liquidación con el comprador.",
  "formulas": [{"nombre": "Costo de transporte por tonelada", "expresion": "Costo_t = (tarifa_t_km × distancia_km) + costos_portuarios_t"}],
  "fuentes": ["SME"]},
]

# ---------------- CAPEX / OPEX ----------------
E = [
 {"id": "estructura-capex", "titulo": "Estructura típica del CAPEX inicial",
  "contenido": "El capital inicial de un proyecto minero suele dividirse en: desarrollo de mina (pre-desbroce, accesos), flota minera, planta de procesamiento, infraestructura (energía, agua, campamento, caminos), depósito de relaves, costos indirectos (ingeniería, gestión de construcción, EPCM) y contingencia.",
  "notas": ["La contingencia suele estar entre 10% y 25% según el nivel del estudio.",
            "Precisión típica: estudio de perfil ±35% a ±50%, prefactibilidad ±25%, factibilidad ±10% a ±15%."],
  "fuentes": ["SME", "MTTODD"]},
 {"id": "estructura-opex", "titulo": "Estructura típica del OPEX",
  "contenido": "El costo operativo se agrupa en mina (perforación, voladura, carguío, acarreo, servicios), planta (energía, reactivos, medios de molienda, revestimientos), G&A (administración, campamento, seguridad) y costos de venta (transporte, fundición, refinación).",
  "notas": ["En tajo abierto grande, el acarreo suele ser la mayor partida del costo mina.",
            "En planta, la energía y los medios de molienda suelen ser las mayores partidas."],
  "fuentes": ["SME", "TSE"]},
 {"id": "rangos-referenciales", "titulo": "Rangos referenciales de costo (orientativos)",
  "contenido": "Valores aproximados para conversación inicial. Varían mucho con escala, país, precio de energía y tipo de roca. No usar para decisiones sin datos propios.",
  "tabla": [
    {"concepto": "Costo mina tajo abierto grande", "rango": "1,5 a 3,5 US$/t movida"},
    {"concepto": "Costo mina subterránea", "rango": "15 a 60 US$/t de mineral"},
    {"concepto": "Procesamiento por flotación", "rango": "5 a 15 US$/t tratada"},
    {"concepto": "Lixiviación en pilas", "rango": "2 a 6 US$/t tratada"},
    {"concepto": "G&A", "rango": "1 a 5 US$/t tratada"}],
  "fuentes": ["SME"], "confianza": "orientativa"},
 {"id": "evaluacion-economica", "titulo": "Evaluación económica de un proyecto o decisión",
  "contenido": "Para comparar alternativas (comprar vs. alquilar equipos, ampliar planta, cambiar método) se construye el flujo de caja de cada opción y se comparan VAN, TIR y payback.",
  "formulas": [
    {"nombre": "Valor actual neto", "expresion": "VAN = Σ [FC_t / (1 + r)^t] − Inversión_0"},
    {"nombre": "Flujo de caja anual", "expresion": "FC = Ingresos − OPEX − Impuestos − CAPEX_sostenimiento"},
    {"nombre": "Ingreso por tonelada (simplificado)", "expresion": "Ingreso_t = ley × recuperación × precio − costos_venta"},
    {"nombre": "Ley de corte de equilibrio", "expresion": "Ley_corte = (costo_planta + G&A) / (precio − costo_venta) / recuperación"}],
  "fuentes": ["SME"]},
 {"id": "costo-propiedad-equipo", "titulo": "Costo horario de propiedad y operación de un equipo",
  "contenido": "Útil para comparar equipos o decidir entre flota propia y contratista.",
  "formulas": [
    {"nombre": "Costo de propiedad por hora", "expresion": "(Precio − Valor_residual) / Horas_vida_util + intereses_seguros_por_hora"},
    {"nombre": "Costo de operación por hora", "expresion": "combustible + lubricantes + neumáticos + mantenimiento + operador"},
    {"nombre": "Costo por tonelada", "expresion": "(Costo_propiedad_h + Costo_operacion_h) / Productividad_t_por_h"}],
  "fuentes": ["SME"]},
]

# ---------------- FAQ ----------------
F = [
 ("¿Cuál es la diferencia entre recurso y reserva?", "Un recurso tiene perspectivas razonables de extracción; una reserva es la parte del recurso medido o indicado que ya demostró ser económica tras aplicar factores mineros, metalúrgicos, económicos, legales y ambientales.", ["JORC"]),
 ("¿Qué es la relación de desbroce y por qué importa?", "Es cuántas toneladas de desmonte se mueven por cada tonelada de mineral. Una relación alta aumenta el costo por tonelada de mineral y puede volver no rentable una parte del yacimiento.", ["SME"]),
 ("¿Cómo sé si me sobran o me faltan camiones?", "Calcula el factor de acoplamiento. Cerca de 1 está equilibrado. Si las palas esperan camiones faltan camiones; si hay colas en pala sobran.", ["MF"]),
 ("¿Qué entra en CAPEX y qué en OPEX?", "CAPEX es inversión en activos de larga vida (flota, planta, infraestructura, pre-desbroce). OPEX es el gasto recurrente para operar (combustible, explosivos, energía, personal, repuestos).", ["SME"]),
 ("¿Qué es el capital de sostenimiento?", "Es CAPEX que se invierte durante la operación para mantener la capacidad, por ejemplo reemplazar camiones al final de su vida o ampliar la presa de relaves.", ["SME"]),
 ("¿Qué diferencia hay entre costo C1 y AISC?", "C1 es el costo de caja directo por unidad de metal. AISC suma al C1 el capital de sostenimiento, regalías y gastos corporativos para mantener la producción.", ["SME"]),
 ("¿Por qué mejorar la voladura puede bajar el costo total?", "Una fragmentación más fina mejora la productividad de palas, reduce el desgaste y acelera el chancado y la molienda. El ahorro aguas abajo suele superar el mayor costo de explosivo.", ["SME"]),
 ("¿Cómo calculo el punto de reorden de un repuesto?", "Multiplica el consumo diario por el tiempo de entrega en días y suma el stock de seguridad.", ["SME"]),
 ("¿Qué es la ley de corte?", "Es la ley mínima a la que un bloque paga su procesamiento. Los bloques por debajo se tratan como desmonte o se guardan como mineral marginal.", ["SME"]),
 ("¿Qué es disponibilidad mecánica y utilización?", "Disponibilidad es el porcentaje del tiempo en que el equipo puede operar. Utilización es el porcentaje de ese tiempo disponible en que efectivamente opera.", ["SME"]),
 ("¿Conviene comprar o alquilar equipos?", "Compara el costo por tonelada de ambas opciones incluyendo propiedad, operación y mantenimiento, y el VAN del flujo de caja. Alquilar reduce CAPEX pero suele subir el OPEX.", ["SME"]),
 ("¿Qué precisión tiene un estimado de costos?", "Perfil ±35% a ±50%, prefactibilidad alrededor de ±25%, factibilidad ±10% a ±15%.", ["SME"]),
 ("¿Qué es el NSR?", "Net smelter return: el ingreso neto por tonelada de mineral tras descontar recuperación, fundición, refinación y transporte. Se usa para decidir el destino de cada bloque.", ["SME"]),
 ("¿Cuál es la diferencia entre ANFO y emulsión?", "El ANFO es barato pero no resiste agua. La emulsión resiste agua y tiene mayor densidad, pero cuesta más.", ["SME"]),
 ("¿Qué controla el tiempo de ciclo de un camión?", "Las colas en pala y chancadora, la distancia y pendiente de la ruta, el estado de las vías y la velocidad de los equipos.", ["WITS"]),
]
FAQ = [{"pregunta": q, "respuesta": a, "fuentes": s} for q, a, s in F]

base = {
  "version": "0.1.0", "idioma": "es", "actualizado": "2026-10-12",
  "aviso": "Contenido de referencia general reunido de fuentes públicas. Los rangos de costo son orientativos; verifica con datos de tu operación antes de decidir.",
  "fuentes": fuentes, "glosario": G, "procesos": P, "logistica": L, "economia": E, "faq": FAQ,
}

# validate references
ids = set(fuentes)
for sec in ("glosario",):
    for x in base[sec]:
        assert x["fuente"] in ids, x
for sec in ("procesos", "logistica", "economia", "faq"):
    for x in base[sec]:
        for f in x["fuentes"]:
            assert f in ids, (sec, x)

with open(os.path.join(OUT, "base_conocimiento.json"), "w", encoding="utf-8") as f:
    json.dump(base, f, ensure_ascii=False, indent=1)

# Markdown preview
md = ["# Base de conocimiento minero v0.1", "", f"_{base['aviso']}_", "",
      f"Contenido: {len(G)} términos, {len(P)} procesos, {len(L)} fichas de logística, {len(E)} fichas de CAPEX/OPEX, {len(FAQ)} preguntas frecuentes.", ""]
def src(lst): return ", ".join(lst)
md += ["## Glosario", ""]
cats = {}
for x in G: cats.setdefault(x["categoria"], []).append(x)
for c, items in cats.items():
    md += [f"### {c.capitalize()}", ""]
    for x in sorted(items, key=lambda y: y["termino"].lower()):
        syn = f" _(también: {', '.join(x['sinonimos'])})_" if x["sinonimos"] else ""
        md.append(f"- **{x['termino']}**{syn}: {x['definicion']} [{x['fuente']}]")
    md.append("")
md += ["## Procesos", ""]
for p in P:
    md += [f"### {p['titulo']}", "", p["resumen"], ""]
    md += [f"{i}. {s}" for i, s in enumerate(p["pasos"], 1)]
    md += ["", "**Indicadores:** " + "; ".join(p["indicadores"]), ""]
    md += [f"> {c}" for c in p["consejos"]]
    md += ["", f"Fuentes: {src(p['fuentes'])}", ""]
def fichas(title, lst):
    out = [f"## {title}", ""]
    for x in lst:
        out += [f"### {x['titulo']}", "", x["contenido"], ""]
        for fo in x.get("formulas", []):
            out.append(f"- **{fo['nombre']}:** `{fo['expresion']}`" + (f" {fo['interpretacion']}" if fo.get("interpretacion") else ""))
        for n in x.get("notas", []):
            out.append(f"- {n}")
        if x.get("tabla"):
            out += ["", "| Concepto | Rango |", "|---|---|"] + [f"| {r['concepto']} | {r['rango']} |" for r in x["tabla"]]
        out += ["", f"Fuentes: {src(x['fuentes'])}", ""]
    return out
md += fichas("Logística", L)
md += fichas("CAPEX y OPEX", E)
md += ["## Preguntas frecuentes", ""]
for q in FAQ:
    md += [f"**{q['pregunta']}**", "", f"{q['respuesta']} [{src(q['fuentes'])}]", ""]
md += ["## Fuentes", ""]
for k, v in fuentes.items():
    md.append(f"- **{k}**: " + (f"[{v['titulo']}]({v['url']})" if v["url"] else v["titulo"]))
with open(os.path.join(OUT, "base_conocimiento.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(md) + "\n")

print(len(G), len(P), len(L), len(E), len(FAQ))
