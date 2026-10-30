"""Genera servicios/index.html y el resumen de servicios del portafolio (index.html).

PRECIOS: se cambian SOLO en servicios/precios.json. Al subir ese archivo a GitHub,
la acción .github/workflows/precios.yml ejecuta este script y publica las dos páginas.
Uso manual:  python3 tools/build_servicios.py
Textos, ejemplos y preguntas frecuentes se editan aquí.
"""
import os, re, html, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IG = "https://www.instagram.com/melina_rivera_developer/"
LI = "https://www.linkedin.com/in/deliamelinarivera"
FORM = "https://formspree.io/f/xbdplnyg"

PR = json.load(open(os.path.join(ROOT, "servicios", "precios.json"), encoding="utf-8"))

def _eur(n): return f"{n:,}".replace(",", ".") + " €"
def _mxn(n): return "$" + f"{n:,}" + " MXN"
def fill(text):
    """Sustituye [[clave.eur]], [[clave.mxn]], [[clave.ahorro_eur]]… y [[clave.eur_n]] (número) por su valor."""
    def sub(m):
        key, field = m.group(1), m.group(2)
        v = PR[key]
        if field == "n": return str(v)
        if field == "n_fmt": return f"{v:,}".replace(",", ".")
        raw = field.endswith("_n"); f = field[:-2] if raw else field
        val = v[f] if isinstance(v, dict) else v
        if raw: return str(val)
        return _mxn(val) if f.endswith("mxn") else _eur(val) if f.endswith("eur") else f"{val:,}".replace(",", ".")
    return re.sub(r"\[\[([a-z_]+)\.([a-z_]+)\]\]", sub, text)

# ───────────────────────── PRECIOS (España € / México MXN) ─────────────────────────
# Revisados en oct 2026 con tarifas publicadas por freelancers y agencias pequeñas de España.
S = [
  dict(id="landing", icon="rocket", name="Landing page sencilla", ideal="Para autónomos y negocios que empiezan",
       eur="desde [[d_landing.eur]]", mxn="desde [[d_landing.mxn]]", per="/ proyecto",
       items=["Una página clara y rápida, pensada para móvil", "Botón de WhatsApp, formulario y mapa", "Textos orientados a conseguir contactos", "SEO local básico para Google", "Lista en 1–2 semanas"],
       aparte="Dominio y alojamiento a tu nombre · textos legales con iubenda",
       ex=[("Piñatas Madrid", "https://melinarivera.github.io/pinata/"), ("Efsun tienda", "https://melinarivera.github.io/tienda-esoterica/")]),
  dict(id="web", icon="store", name="Web corporativa", ideal="Para pymes que quieren generar confianza",
       eur="desde [[d_web.eur]]", mxn="desde [[d_web.mxn]]", per="/ proyecto", popular=True,
       items=["5–7 páginas con estructura pensada para vender", "Blog o catálogo de servicios", "SEO básico en cada página", "WhatsApp, formulario y analítica", "Aviso legal con tus datos + privacidad y cookies con iubenda"],
       aparte="Dominio y alojamiento a tu nombre · suscripción a iubenda",
       ex=[("ETERN-ME", "https://etern-me.com"), ("Cotidiana", "https://cotidiana.app")]),
  dict(id="tienda", icon="shopping-bag", name="Tienda online o reservas", ideal="Para vender o reservar online 24/7",
       eur="desde [[d_tienda.eur]]", mxn="desde [[d_tienda.mxn]]", per="/ proyecto",
       items=["Catálogo, carrito y pago con tarjeta (Stripe, TPV o Mercado Pago)", "O agenda de citas con recordatorios", "Panel para gestionar pedidos o reservas", "Diseño a medida, sin plantillas", "30 días de soporte tras el lanzamiento"],
       aparte="Comisión de la pasarela de pago en cada venta · alojamiento",
       ex=[("Efsun plataforma", "https://melinarivera.github.io/pyme-efsun/")]),
  dict(id="ia", icon="sparkles", name="Asistente de WhatsApp con IA", ideal="Para dejar de responder siempre lo mismo",
       eur="desde [[d_ia.eur]]", mxn="desde [[d_ia.mxn]]", per="+ [[d_ia_cuota.eur]]/mes", per_mx="+ [[d_ia_cuota.mxn]]/mes", new=True,
       items=["Responde dudas 24/7 en WhatsApp o en tu web", "Entrenado con tu información: precios, horarios, servicios", "Pasa la conversación a una persona cuando hace falta", "<b>Con citas</b> (agenda, recordatorios y ficha en el CRM): <span class='js-price' data-eur='desde [[d_ia_citas.eur]] + [[d_ia_citas_cuota.eur]]/mes' data-mxn='desde [[d_ia_citas.mxn]] + [[d_ia_citas_cuota.mxn]]/mes'>desde [[d_ia_citas.eur]] + [[d_ia_citas_cuota.eur]]/mes</span>", "<b>Tope claro:</b> la cuota incluye [[ia_incluidas.n_fmt]] conversaciones al mes ([[ia_citas_incluidas.n_fmt]] con citas), con la IA, el servidor y el mantenimiento. No es ilimitado: si te acercas, te aviso, y si necesitas más, +1.000 conversaciones por <span class='js-price' data-eur='[[ia_bloque_extra.eur]]' data-mxn='[[ia_bloque_extra.mxn]]'>[[ia_bloque_extra.eur]]</span>. Nunca se corta sin avisar"],
       aparte="Mensajes de WhatsApp: los cobra Meta a tu negocio. <a href='#ia-claro'>Calcula tu gasto</a>",
       extra=("Automatizaciones de procesos (facturas, recordatorios, informes)", "desde [[d_automatizacion.eur]]", "desde [[d_automatizacion.mxn]]", "por flujo"),
       ex=[("Demo estética", "../demos/asistente-whatsapp/#estetica"), ("Demo extranjería", "../demos/asistente-whatsapp/#extranjeria"), ("Nexo: facturas con IA", "https://melinarivera.github.io/Nexo_Facturas/")]),
  dict(id="voz", icon="phone-call", name="Recepcionista de voz con IA", ideal="Para no perder ni una llamada",
       eur="desde [[d_voz.eur]]", mxn="desde [[d_voz.mxn]]", per="+ [[d_voz_cuota.eur]]/mes", per_mx="+ [[d_voz_cuota.mxn]]/mes", new=True,
       items=["Contesta el teléfono 24/7 con voz natural, en español", "Da información (horarios, precios, servicios) y toma citas o reservas", "Te envía un resumen de cada llamada por WhatsApp o email", "Pasa la llamada a una persona cuando hace falta", "<b>Tope claro:</b> la cuota incluye la IA, la voz, el número y [[voz_minutos.n_fmt]] minutos de llamada al mes (unas 100 llamadas de 2 minutos). Si necesitas más, +100 minutos por <span class='js-price' data-eur='[[voz_bloque_extra.eur]]' data-mxn='[[voz_bloque_extra.mxn]]'>[[voz_bloque_extra.eur]]</span>. Te aviso antes de llegar al límite"],
       aparte="Desviar tu línea al asistente: según tu operador (normalmente gratis)",
       extra=("Minutos extra", "+[[voz_bloque_extra.eur]]", "+[[voz_bloque_extra.mxn]]", "cada 100 minutos"),
       ex=[("Demo: restaurante", "../demos/recepcionista-voz/#restaurante"), ("Demo: clínica", "../demos/recepcionista-voz/#clinica")]),
  dict(id="avatar", icon="clapperboard", name="Vídeos con avatar IA", ideal="Para tener vídeos sin ponerte delante de la cámara",
       eur="desde [[d_avatar_video.eur]]", mxn="desde [[d_avatar_video.mxn]]", per="/ vídeo", new=True,
       items=["Un presentador virtual que habla por tu negocio, con voz natural", "Guion, subtítulos y formato para Reels, TikTok o web. <b>Cada vídeo dura hasta 1 minuto</b>", "<b>Pack mensual</b> (4 vídeos al mes, uno por semana): <span class='js-price' data-eur='desde [[d_avatar_pack.eur]]/mes' data-mxn='desde [[d_avatar_pack.mxn]]/mes'>desde [[d_avatar_pack.eur]]/mes</span>", "Ideal para explicar servicios, preguntas frecuentes, cursos y novedades", "Las licencias de la herramienta de vídeo van incluidas"],
       aparte="Nada: el vídeo es tuyo y lo publicas donde quieras",
       extra=("Tu propio avatar (con tu cara y tu voz, con tu permiso)", "desde +[[d_avatar_propio.eur]]", "desde +[[d_avatar_propio.mxn]]", "pago único"),
       ex=[]),
  dict(id="crm", icon="layout-dashboard", name="CRM y planners a medida", ideal="Para tener clientes y tareas en orden",
       eur="desde [[d_crm.eur]]", mxn="desde [[d_crm.mxn]]", per="/ proyecto",
       items=["Fichas de cliente con historial y segmentos", "Reservas, agenda o embudo de ventas", "Campañas por WhatsApp o email respetando el RGPD", "Exportación a Excel", "Formación para usarlo desde el primer día"],
       aparte="Base de datos con copias de seguridad: unos 25 $/mes, a tu nombre",
       extra=("¿Prefieres HubSpot, Notion u otro? Te lo configuro", "desde [[d_crm_configurar.eur]]", "desde [[d_crm_configurar.mxn]]", ""),
       ex=[("Demo CRM restaurante", "../demos/crm-restaurante/"), ("Nexo para gestorías", "https://melinarivera.github.io/Nexo_Facturas/"), ("ZenWi", "https://zenwi.app")]),
  dict(id="formacion", icon="graduation-cap", name="Formación en IA para equipos", ideal="Para que tu equipo use la IA en su trabajo diario",
       eur="desde [[d_formacion_ia.eur]]", mxn="desde [[d_formacion_ia.mxn]]", per="/ taller", new=True,
       items=["Taller práctico de 2 horas, hasta 10 personas, presencial u online", "Cada persona sale usando la IA en 3 tareas reales de su puesto", "Guía con 15–20 instrucciones listas para copiar, hecha para tu negocio", "Semáforo de datos y normas de uso de IA para tu equipo", "Constancia de asistencia y 2 semanas de dudas por WhatsApp", "En España se puede bonificar con FUNDAE"],
       aparte="Licencias de las herramientas de IA, si el equipo quiere planes de pago",
       ex=[("Demo: semáforo de datos", "../demos/semaforo-ia/"), ("Tesovia", "https://www.tesovia.com")]),
  dict(id="redes", icon="megaphone", name="Redes sociales y reputación", ideal="Para que te encuentren y te elijan",
       eur="desde [[d_redes.eur]]", mxn="desde [[d_redes.mxn]]", per="/ mes", per_mx="/ mes", new=True,
       items=["<b>Esencial</b> · <span class='js-price' data-eur='desde [[d_redes.eur]]/mes' data-mxn='desde [[d_redes.mxn]]/mes'>desde [[d_redes.eur]]/mes</span>: 2 redes, 8 publicaciones al mes", "<b>Crecimiento</b> · <span class='js-price' data-eur='desde [[d_redes_crecimiento.eur]]/mes' data-mxn='desde [[d_redes_crecimiento.mxn]]/mes'>desde [[d_redes_crecimiento.eur]]/mes</span>: 12 posts + 4 reels y gestión de anuncios", "Diseños propios con IA y calendario mensual", "Respuesta a reseñas y perfil de Google optimizado"],
       aparte="La inversión en anuncios la pagas tú directamente a Meta o Google",
       extra=("Auditoría de tus perfiles con plan de acción", "desde [[d_auditoria_redes.eur]]", "desde [[d_auditoria_redes.mxn]]", "pago único"),
       ex=[("Mi Instagram", IG)]),
  dict(id="seo", icon="map-pin", name="Ficha de Google y SEO local", ideal="Para aparecer en Google Maps cuando te buscan cerca",
       eur="desde [[d_seo_local.eur]]", mxn="desde [[d_seo_local.mxn]]", per="pago único", per_mx="pago único", new=True,
       items=["Ficha de Google completa: categorías, horarios, servicios y fotos", "Textos con las palabras que usan tus clientes", "Respuesta a las reseñas pendientes", "Plantillas para pedir reseñas a tus clientes", "Comprobación de que tus datos coinciden en internet"],
       aparte="Nada: la ficha de Google es gratuita y va a tu nombre",
       ex=[("Demo: ficha de Google completa", "../demos/ficha-google/")]),
  dict(id="uxui", icon="pen-tool", name="Diseño UX/UI", ideal="Para ver y probar tu web o app antes de construirla",
       eur="desde [[d_uxui.eur]]", mxn="desde [[d_uxui.mxn]]", per="/ proyecto", new=True,
       items=["Entrevista y mapa de lo que necesita tu cliente", "Diseño de pantallas en Figma (web: hasta 5 pantallas)", "Prototipo navegable para probarlo antes de programar", "Guía de estilo: colores, tipografías y botones", "<b>App completa</b> (hasta 15 pantallas y flujo de usuario): <span class='js-price' data-eur='desde [[d_uxui_app.eur]]' data-mxn='desde [[d_uxui_app.mxn]]'>desde [[d_uxui_app.eur]]</span>"],
       aparte="Figma: el archivo se entrega en tu cuenta (plan gratuito suficiente para verlo)",
       extra=("Auditoría UX de tu web o app actual, con informe de mejoras", "desde [[d_auditoria_ux.eur]]", "desde [[d_auditoria_ux.mxn]]", "pago único"),
       ex=[("Demo: prototipo de app", "../demos/prototipo-ux/"), ("Tesovia", "https://www.tesovia.com")]),
  dict(id="identidad", icon="palette", name="Identidad visual básica", ideal="Para que tu negocio se reconozca a primera vista",
       eur="desde [[d_identidad.eur]]", mxn="desde [[d_identidad.mxn]]", per="/ proyecto", new=True,
       items=["Logo sencillo con 2 propuestas y versión para redes", "Paleta de colores y tipografías", "Mini guía de marca en PDF", "5 plantillas de Canva para redes", "2 rondas de cambios"],
       aparte="Registro de la marca, si lo quieres (se hace en la oficina de patentes)",
       ex=[("Demo: tu marca en un minuto", "../demos/identidad-visual/"), ("Piñatas Madrid", "https://melinarivera.github.io/pinata/")]),
  dict(id="app", icon="smartphone", name="App o SaaS a medida", ideal="Para tu idea o tu herramienta interna",
       eur="MVP desde [[d_app.eur]]", mxn="MVP desde [[d_app.mxn]]", per="/ proyecto",
       items=["Definimos juntos la primera versión (MVP)", "Usuarios, roles y panel de administración", "Base de datos y backend incluidos", "Publicación en producción", "30 días de soporte tras el lanzamiento"],
       aparte="Alojamiento, base de datos y, si lleva IA, su consumo",
       ex=[("Tesovia", "https://www.tesovia.com"), ("ETERN-ME", "https://etern-me.com"), ("TravelMates", "https://melinarivera.github.io/TravelMates-App")]),
  dict(id="mant", icon="wrench", name="Mantenimiento", ideal="Para que tu web siempre funcione",
       eur="desde [[d_mantenimiento.eur]]", mxn="desde [[d_mantenimiento.mxn]]", per="/ mes", per_mx="/ mes",
       items=["Vigilancia de dominio, alojamiento y certificado SSL", "Copias de seguridad", "Pequeños cambios de contenido incluidos", "Soporte directo por WhatsApp"],
       aparte="Las renovaciones de dominio y alojamiento siguen a tu nombre", ex=[("Demo: informe mensual", "../demos/informe-mantenimiento/")]),
]

PACKS = [
  dict(name="Pack Arranque", for_="Para empezar a recibir clientes por internet", items=["Landing page sencilla", "Asistente de WhatsApp con IA", "Auditoría de redes con plan de acción"],
       eur="desde [[pack_arranque.eur]]", mxn="desde [[pack_arranque.mxn]]", s_eur="Ahorras [[pack_arranque.ahorro_eur]] · después, [[ia_cuota.eur]]/mes del asistente", s_mxn="Ahorras [[pack_arranque.ahorro_mxn]] · después, [[ia_cuota.mxn]]/mes del asistente"),
  dict(name="Pack Pyme Digital", for_="Para profesionalizar tu presencia online", items=["Web corporativa", "Asistente de WhatsApp con IA", "3 meses de redes plan Esencial"], popular=True,
       eur="desde [[pack_pyme_digital.eur]]", mxn="desde [[pack_pyme_digital.mxn]]", s_eur="Ahorras [[pack_pyme_digital.ahorro_eur]] · después, [[ia_cuota.eur]]/mes del asistente", s_mxn="Ahorras [[pack_pyme_digital.ahorro_mxn]] · después, [[ia_cuota.mxn]]/mes del asistente"),
  dict(name="Pack Organiza tu negocio", for_="Para dejar las hojas de cálculo y el papel", items=["CRM a medida", "2 automatizaciones de procesos", "Formación para tu equipo"],
       eur="desde [[pack_organiza.eur]]", mxn="desde [[pack_organiza.mxn]]", s_eur="Ahorras [[pack_organiza.ahorro_eur]]", s_mxn="Ahorras [[pack_organiza.ahorro_mxn]]"),
]

# Qué incluye el precio y qué pagas aparte
COSTES = [
  ("Mi trabajo: diseño, desarrollo, configuración y formación", "Incluido en el precio", "—", "Presupuesto cerrado antes de empezar."),
  ("Dominio (.es, .com, .mx)", "Tú, a tu nombre", "unos 10–15 € al año", "Es tuyo. Si algún día cambias de proveedor, te lo llevas."),
  ("Alojamiento (hosting)", "Tú, a tu nombre", "0 € en webs sencillas · 3–10 €/mes en tiendas o WordPress", "Uso planes con uso comercial permitido. Te ayudo a contratarlo."),
  ("Textos legales: privacidad y cookies", "Tú, a tu nombre (iubenda)", "plan gratuito limitado o desde unos 6 €/mes", "Se actualizan cuando cambia la normativa. Yo los configuro e instalo el banner de cookies."),
  ("Aviso legal", "Incluido", "—", "Lo redacto con los datos de tu negocio. En despachos, extranjería o salud, recomiendo que lo revise tu abogado/a."),
  ("Pagos online", "Comisión de la pasarela", "según Stripe, TPV de tu banco o Mercado Pago", "Se descuenta de cada venta. Yo no cobro comisión."),
  ("IA (tokens) del asistente", "Incluida en la cuota mensual", "hasta [[ia_incluidas.n_fmt]] conversaciones/mes ([[ia_citas_incluidas.n_fmt]] con citas)", "La pago yo desde mi cuenta de Claude, con límite de gasto por cliente. Si te acercas al límite, te aviso; nunca se corta sin avisar."),
  ("Conversaciones extra de IA", "Tú, solo si las usas", "+1.000 conversaciones: [[ia_bloque_extra.eur]]", "Te aviso al llegar al 80 %. Tú decides si añades un bloque o subimos de plan."),
  ("IA, voz y número del recepcionista de voz", "Incluido en la cuota mensual", "hasta [[voz_minutos.n_fmt]] minutos de llamadas al mes", "Si te acercas al límite, te aviso. Minutos extra: [[voz_bloque_extra.eur]] cada 100."),
  ("Herramienta de vídeo con avatar", "Incluida", "—", "Uso mi licencia profesional; los vídeos son tuyos."),
  ("Mensajes de WhatsApp (Meta)", "Tu negocio, directamente a Meta", "responder a clientes: gratis hasta 1.000/mes · recordatorio ≈ 0,017 € · campaña ≈ 0,059 €", "Tarifas de Meta para España en 2026. Meta te factura a ti; yo no añado margen."),
  ("Anuncios en Meta o Google", "Tú, directamente a la plataforma", "lo decides tú", "Mi gestión va en la cuota de redes."),
  ("Canva Pro, plantillas y herramientas de diseño", "Incluido", "—", "Las uso yo; no tienes que contratar nada."),
  ("Base de datos de un CRM o app", "Tú, a tu nombre", "unos 25 $/mes", "Plan de pago desde el primer día: el gratuito se pausa si no se usa y no guarda copias diarias."),
]

EJEMPLOS = [  # solo proyectos con página real funcionando
  dict(name="Tesovia", tag="SaaS con IA", desc="Asistente académico con IA en español e inglés: citas APA, feedback, detección de IA y plagio.", img="../img/thumbs/tesovia.jpg", url="https://www.tesovia.com", fit="cover", bg="#F5F6FF", featured=True),
  dict(name="Nexo · Facturas con IA", tag="Automatización para gestorías", desc="Demo multiempresa: la factura entra, la IA la lee y valida, el equipo aprueba y sale lista para el programa contable (SAP).", img="../img/thumbs/nexo-facturas.jpg", url="https://melinarivera.github.io/Nexo_Facturas/", fit="cover", bg="#F3F5EF"),
  dict(name="Piñatas Madrid", tag="Web de negocio local", desc="Catálogo de piñatas artesanales con pedido directo por WhatsApp, reserva con señal y entrega en metro.", img="../img/thumbs/pinata.jpg", url="https://melinarivera.github.io/pinata/", fit="cover", bg="#1E1433"),
  dict(name="ETERN-ME", tag="SaaS", desc="Organiza cuentas, documentos e información esencial para que nada importante se pierda.", img="../img/etern-me-hero.png", url="https://etern-me.com", fit="contain", bg="#140F20"),
  dict(name="Cotidiana", tag="App", desc="Organizador del día a día para personas mayores o con poca experiencia tecnológica.", img="../img/cotidiana-hero.png", url="https://cotidiana.app", fit="contain", bg="#0D1A30"),
  dict(name="ZenWi", tag="App RRHH", desc="Detección temprana del burnout en equipos, anónima por diseño.", img="../img/zenwi-logo.png", url="https://zenwi.app", fit="logo", bg="#0B1428"),
  dict(name="Efsun · Plataforma", tag="Web con IA y reservas", desc="Horóscopo generado con IA, reservas de sesiones, blog y WhatsApp.", img="../img/thumbs/efsun_plataforma.jpg", url="https://melinarivera.github.io/pyme-efsun/", fit="cover", bg="#0A0A1F"),
  dict(name="Efsun · Tienda", tag="Tienda online", desc="Catálogo, carrito y diseño a medida para una consultora esotérica.", img="../img/thumbs/efsun_tienda.jpg", url="https://melinarivera.github.io/tienda-esoterica/", fit="cover", bg="#0D0A1F"),
  dict(name="TravelMates", tag="App colaborativa", desc="Viajes en grupo: itinerarios, gastos y votaciones en un solo lugar.", img="../img/travelmates-hero.png", url="https://melinarivera.github.io/TravelMates-App", fit="contain", bg="#0F1E30"),
]

SECTORES = [
  ("Consultoras de extranjería", "scale", ["Asistente que filtra consultas y pide cita", "Contenido que resuelve dudas frecuentes", "Reseñas de Google bien respondidas"]),
  ("Despachos profesionales", "briefcase", ["Web clara con áreas de práctica", "Agenda de primeras consultas", "LinkedIn y Google Business al día"]),
  ("Centros de estética", "flower-2", ["Reservas y recordatorios por WhatsApp", "Reels de tratamientos y antes/después (con permiso)", "Campañas a clientas que no vuelven"]),
  ("Gestorías y asesorías", "calculator", ["Facturas leídas con IA y listas para contabilidad", "Portal para que los clientes suban documentos", "Recordatorios de plazos por WhatsApp"]),
  ("Tiendas de barrio", "shopping-basket", ["Perfil de Google y mapa optimizados", "Catálogo en WhatsApp o tienda sencilla", "Publicaciones de novedades y ofertas"]),
]

FAQ = [
  ("¿De dónde sale la IA y quién la paga?", "El asistente usa Claude, de Anthropic. La contrato yo con mi cuenta de empresa (pago por uso, con límite de gasto para cada cliente) y va incluida en tu cuota: hasta [[ia_incluidas.n_fmt]] conversaciones al mes en el plan básico y [[ia_citas_incluidas.n_fmt]] en el de citas. No necesitas crear ninguna cuenta de IA."),
  ("¿Cuánto cuesta la IA de verdad?", "Muy poco: un negocio con 1.000 conversaciones al mes consume entre 1 y 5 € de IA. La cuota cubre eso, el servidor donde funciona el asistente y mi mantenimiento (ajustes, nuevas respuestas, revisar que todo va bien)."),
  ("¿Qué pasa si paso de las conversaciones incluidas?", "Te aviso al llegar al 80 %. Puedes añadir bloques de 1.000 conversaciones por [[ia_bloque_extra.eur]] o pasar al plan superior. El asistente nunca se apaga sin avisarte."),
  ("¿Prefiero pagar la IA yo directamente, se puede?", "Sí. Creas tu cuenta en Anthropic, pones tu tarjeta y la cuota baja [[ia_descuento_propia.eur]] al mes. Pagas exactamente lo que consumes; yo lo configuro y te enseño a ver el gasto."),
  ("¿Puedo seguir usando WhatsApp en mi móvil?", "Sí. Con la coexistencia de Meta (disponible en España) sigues contestando desde la app de WhatsApp Business con el mismo número, y el asistente responde cuando tú no puedes."),
  ("¿Qué pasa si la IA se equivoca?", "Solo responde con la información que tú apruebas (precios, horarios, servicios). Si no sabe algo, no se lo inventa: pasa la conversación a una persona. Cada mes reviso las preguntas sin respuesta y las añado."),
  ("¿Y los datos de mis clientes?", "Firmamos un contrato de encargado de tratamiento (RGPD). El asistente pide consentimiento antes de guardar datos y solo guarda lo necesario para la cita o la consulta."),
  ("¿La web y el dominio son míos?", "Sí. El dominio, el alojamiento y las cuentas van a tu nombre desde el primer día. Si dejamos de trabajar juntas, te lo llevas todo."),
  ("¿Los textos legales me protegen?", "Uso iubenda, que genera la política de privacidad y de cookies y la actualiza cuando cambia la ley. En sectores regulados recomiendo que tu abogado/a revise el aviso legal."),
  ("¿Puedo dejar las cuotas mensuales?", "Sí, sin permanencia. Avisas con 30 días y te dejo todo documentado para que otra persona pueda seguir."),
  ("¿Trabajas con negocios de otros países?", "Sí. Trabajo en remoto con negocios de cualquier lugar: nos vemos por videollamada y todo se gestiona online. Si tu negocio está en México, elige México arriba para ver los precios en pesos."),
]

# ───────────────────────── helpers ─────────────────────────
def P(eur, mxn, cls=""):
    return f'<span class="js-price{(" " + cls) if cls else ""}" data-eur="{html.escape(eur)}" data-mxn="{html.escape(mxn)}">{html.escape(eur)}</span>'

def link(label, href, cls="ex"):
    ext = href.startswith("http")
    icon = "external-link" if ext else "play"
    return f'<a class="{cls}" href="{href}"{" target=\"_blank\" rel=\"noopener\"" if ext else ""}><i data-lucide="{icon}"></i>{html.escape(label)}</a>'

def service_card(s):
    badges = ""
    if s.get("popular"): badges += '<span class="flag">Más pedido</span>'
    if s.get("new"): badges += '<span class="flag new">Nuevo</span>'
    per_mx = s.get("per_mx", s["per"].replace("€", "MXN") if "€" in s["per"] else s["per"])
    extra = ""
    if s.get("extra"):
        t, e, m, u = s["extra"]
        extra = f'<p class="svc-extra">{t}: <b>{P(e, m)}</b>{(" " + u) if u else ""}</p>'
    ex = ""
    if s["ex"]:
        ex = '<div class="svc-ex"><span>Ejemplos reales</span>' + "".join(link(l, h) for l, h in s["ex"]) + "</div>"
    return f"""
      <article class="svc" id="srv-{s['id']}">
        <div class="svc-top"><span class="svc-icon"><i data-lucide="{s['icon']}"></i></span>{badges}</div>
        <h3>{s['name']}</h3>
        <p class="svc-ideal">{s['ideal']}</p>
        <p class="svc-price">{P(s['eur'], s['mxn'])} <small>{P(s['per'], per_mx)}</small></p>
        {extra}
        <ul>{''.join(f'<li>{i}</li>' for i in s['items'])}</ul>
        <p class="svc-aparte"><i data-lucide="info"></i><span><b>Aparte:</b> {s['aparte']}. <a href="#incluye">Ver detalle</a></span></p>
        {ex}
        <a class="btn {'primary' if s.get('popular') else 'ghost'} js-service" data-service="{s['name']}" href="#contacto">Pedir presupuesto</a>
      </article>"""

def pack_card(p):
    return f"""
      <article class="pack{' popular' if p.get('popular') else ''}">
        {'<span class="flag">Recomendado</span>' if p.get('popular') else ''}
        <h3>{p['name']}</h3>
        <p class="pack-for">{p['for_']}</p>
        <ul>{''.join(f'<li>{i}</li>' for i in p['items'])}</ul>
        <p class="pack-price">{P(p['eur'], p['mxn'])}</p>
        <p class="pack-save">{P(p['s_eur'], p['s_mxn'])}</p>
        <a class="btn {'primary' if p.get('popular') else 'ghost'} js-service" data-service="{p['name']}" href="#contacto">Lo quiero</a>
      </article>"""

def ejemplo_card(e):
    if e["fit"] == "logo":
        media = f'<div class="ej-media" style="background:{e["bg"]}"><img src="{e["img"]}" alt="{e["name"]}" class="ej-logo" loading="lazy"/></div>'
    else:
        media = f'<div class="ej-media" style="background:{e["bg"]}"><img src="{e["img"]}" alt="{e["name"]}" loading="lazy" style="object-fit:{e["fit"]};{"padding:6% 4%;" if e["fit"]=="contain" else ""}"/></div>'
    return f"""
      <a class="ej{' featured' if e.get('featured') else ''}" href="{e['url']}" target="_blank" rel="noopener">
        {media}
        <div class="ej-body"><span class="ej-tag">{e['tag']}</span><h3>{e['name']}</h3><p>{e['desc']}</p><span class="ej-go">Abrir la web <i data-lucide="arrow-up-right"></i></span></div>
      </a>"""

# ───────────────────────── página de servicios ─────────────────────────
CSS = r"""
:root{
  /* Layout: una columna de lectura con bandas; tarjetas en rejilla que se apilan en móvil */
  --bg:#F7F6F2; --bg2:#FFFFFF; --bg3:#F1EFE8; --line:#E2DFD6; --line2:#D5D0C4;
  --fg:#13203A; --muted:#5B6578; --muted2:#7A8396;
  --accent:#0A1526; --accent-2:#96681A; --accent-dim:rgba(200,145,46,.14); --ok:#1E7F51;
  --gold:#C8912E;
  --display:Fraunces,Georgia,'Times New Roman',serif; --body:'DM Sans',system-ui,-apple-system,'Segoe UI',sans-serif;
  --r:16px; color-scheme:light;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;scroll-padding-top:84px}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important}}
body{background:var(--bg);color:var(--fg);font-family:var(--body);font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:#2F5FA8}
img{max-width:100%;display:block}
i[data-lucide],svg.lucide{width:1em;height:1em;stroke-width:2;flex:none}
.wrap{max-width:1160px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
section{padding-block:76px}
.band{background:var(--bg2);border-block:1px solid var(--line)}
h1,h2,h3{text-wrap:balance}
h2{font-family:var(--display);font-weight:600;font-variation-settings:"SOFT" 14,"WONK" 1;font-size:clamp(28px,4vw,40px);line-height:1.15;letter-spacing:-.01em}
h2 em{font-style:normal;color:var(--gold);font-weight:600}
.lead{color:var(--muted);max-width:62ch;margin-top:12px}
.eyebrow{display:inline-flex;align-items:center;gap:10px;font-family:var(--display);font-size:15px;font-weight:600;color:var(--gold);margin-bottom:10px}
.eyebrow::before{content:"";width:26px;height:2px;background:var(--gold);border-radius:2px}
.head{margin-bottom:36px}
/* nav */
.nav{position:sticky;top:env(safe-area-inset-top,0px);z-index:20;background:rgba(247,246,242,.9);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:21;background:var(--bg)}
.nav-in{display:flex;align-items:center;gap:20px;min-height:64px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--fg);font-weight:600;white-space:nowrap}
.brand img{height:40px;width:auto;border-radius:8px}
@media(max-width:600px){.brand .bn{display:none}.brand img{height:36px}}
.nav-links{display:flex;gap:18px;margin-left:auto}
.nav-links a{color:var(--muted);text-decoration:none;font-size:14px;font-weight:500}
.nav-links a:hover{color:var(--fg)}
.toggle{display:inline-flex;background:var(--bg3);border:1px solid var(--line);border-radius:99px;padding:3px;gap:2px}
.toggle button{border:0;background:transparent;color:var(--muted);font:inherit;font-size:13px;font-weight:600;padding:6px 12px;border-radius:99px;cursor:pointer;white-space:nowrap}
.toggle button.on{background:var(--accent);color:#fff}
.nav-links a:hover{border-bottom:1.5px solid var(--gold)}
.toggle button:focus-visible,.btn:focus-visible,a:focus-visible,summary:focus-visible{outline:2px solid var(--accent-2);outline-offset:2px}
@media (max-width:860px){.nav-links{display:none}.nav-in{justify-content:space-between}}
/* hero */
.hero{padding-block:64px 56px}
.hero h1{font-family:var(--display);font-weight:600;font-variation-settings:"SOFT" 14,"WONK" 1;font-size:clamp(34px,6vw,60px);line-height:1.06;letter-spacing:-.02em;max-width:17ch}
.hero h1 em{font-style:normal;font-weight:600;color:var(--gold)}
.hero .lead{font-size:18px}
.actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:26px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:46px;padding:12px 22px;border-radius:99px;font-weight:600;font-size:15px;text-decoration:none;border:1.5px solid var(--line2);color:var(--fg);background:var(--bg2);transition:.2s}
.btn.primary{background:var(--accent);border-color:var(--accent);color:#fff}
.btn.primary:hover{background:#17294a}
.btn.ghost:hover{border-color:var(--gold)}
.sectors{display:flex;flex-wrap:wrap;gap:8px;margin-top:28px}
.sectors span{font-size:13px;color:var(--muted);border:1px solid var(--line);border-radius:99px;padding:5px 12px}
.tax{font-size:13px;color:var(--muted2);margin-top:14px}
/* servicios */
.svc-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px}
.svc{background:var(--bg2);border:1px solid var(--line);border-radius:var(--r);padding:24px;display:flex;flex-direction:column;gap:10px;min-width:0}
.svc-top{display:flex;align-items:center;gap:8px}
.svc-icon{width:42px;height:42px;border-radius:12px;display:grid;place-items:center;background:var(--accent-dim);color:var(--accent-2);font-size:20px;margin-right:auto}
.flag{font-size:11.5px;font-weight:700;letter-spacing:.04em;padding:4px 11px;border-radius:99px;background:var(--accent);color:#fff}
.flag.new{background:transparent;border:1px solid var(--gold);color:var(--accent-2)}
.svc h3,.pack h3{font-family:var(--display);font-size:22px;font-weight:600;line-height:1.2}
.svc-ideal{font-size:14px;font-weight:500;color:var(--muted)}
.svc-price{font-family:var(--display);font-size:27px;font-weight:600;color:var(--fg);line-height:1.2;margin-top:4px}
.svc-price small{font-family:var(--body);font-size:13px;color:var(--muted)}
.svc-extra{font-size:13.5px;color:var(--muted)}
.svc-extra b{color:var(--fg);font-weight:600}
.svc ul,.pack ul{list-style:none;display:flex;flex-direction:column;gap:7px;margin:6px 0 4px}
.svc li,.pack li{font-size:14.5px;color:var(--muted);padding-left:22px;position:relative}
.svc li::before{content:"";position:absolute;left:2px;top:.62em;width:10px;height:6px;border-left:2px solid var(--gold);border-bottom:2px solid var(--gold);transform:rotate(-45deg) translateY(-3px)}
.svc li b{color:var(--fg);font-weight:600}
.svc-aparte{display:flex;gap:8px;font-size:13px;color:var(--muted);background:var(--bg3);border-radius:12px;padding:10px 12px;margin-top:auto}
.svc-aparte i,.svc-aparte svg{margin-top:3px;color:var(--gold)}
.svc-aparte b{color:var(--fg);font-weight:600}
.svc-ex{display:flex;flex-wrap:wrap;gap:6px}
.svc-ex>span{width:100%;font-size:13px;font-weight:600;color:var(--muted2)}
.ex{display:inline-flex;align-items:center;gap:6px;font-size:13.5px;font-weight:600;text-decoration:none;color:var(--accent-2);border:1px solid rgba(200,145,46,.34);background:var(--accent-dim);border-radius:99px;padding:6px 12px}
.ex:hover{background:var(--accent);color:#fff;border-color:var(--accent)}
.svc .btn{margin-top:6px}
/* tabla de costes */
.table{overflow-x:auto;border:1px solid var(--line);border-radius:var(--r);background:var(--bg2)}
table{width:100%;border-collapse:collapse;min-width:760px}
th,td{text-align:left;padding:14px 16px;border-bottom:1px solid var(--line);vertical-align:top;font-size:14.5px}
th{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted2);font-weight:700;background:var(--bg3)}
td:first-child{color:var(--fg);font-weight:600;width:26%}
td:nth-child(2){width:20%}
td:nth-child(3){color:var(--fg);width:22%}
td:last-child{color:var(--muted)}
tr:last-child td{border-bottom:0}
.who{display:inline-block;font-size:12.5px;font-weight:600;padding:3px 10px;border-radius:99px;background:var(--bg3);color:var(--muted)}
.who.inc{background:rgba(76,175,130,.14);color:var(--ok)}
.note{font-size:13.5px;color:var(--muted2);margin-top:14px;max-width:80ch}
/* calculadora */
.calc{display:grid;grid-template-columns:1fr 1fr;gap:24px;background:var(--bg2);border:1px solid var(--line);border-radius:var(--r);padding:24px}
@media (max-width:820px){.calc{grid-template-columns:1fr}}
.calc-in{display:flex;flex-direction:column;gap:6px;min-width:0}
.calc-in label{display:flex;justify-content:space-between;font-size:14px;color:var(--muted);font-weight:600;margin-top:8px}
.calc-in output{color:var(--fg);font-variant-numeric:tabular-nums}
.calc-in input[type=range]{width:100%;accent-color:var(--accent)}
.calc-plan{display:flex;flex-wrap:wrap;gap:6px;margin-top:14px}
.calc-plan button{border:1px solid var(--line2);background:transparent;color:var(--muted);font:inherit;font-size:13.5px;font-weight:600;padding:8px 14px;border-radius:99px;cursor:pointer}
.calc-plan button.on{background:var(--accent);border-color:var(--accent);color:#fff}
.calc-out{display:flex;flex-direction:column;gap:2px;min-width:0}
.calc-row,.calc-total{display:flex;justify-content:space-between;gap:12px;padding:10px 0;border-bottom:1px solid var(--line);align-items:baseline}
.calc-row span,.calc-total span{font-size:14.5px}
.calc-row small,.calc-total small{display:block;font-size:12.5px;color:var(--muted2)}
.calc-row b{font-variant-numeric:tabular-nums;font-weight:600}
.calc-total{border-bottom:0;padding-top:14px}
.calc-total b{font-family:var(--display);font-size:32px;font-weight:600;color:var(--fg);font-variant-numeric:tabular-nums}
.calc-ia{font-size:13.5px;color:var(--muted);background:var(--bg3);border-radius:12px;padding:10px 12px;margin-top:6px}
.calc-ia b{color:var(--ok)}
/* packs */
.pack-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}
.pack{background:var(--bg2);border:1px solid var(--line);border-radius:var(--r);padding:26px;display:flex;flex-direction:column;gap:8px;position:relative}
.pack.popular{border-color:var(--accent);box-shadow:0 18px 40px -26px rgba(10,21,38,.55)}
.pack .flag{position:absolute;top:-12px;left:24px}
.pack-for{color:var(--muted);font-size:14px}
.pack li::before{content:"+";position:absolute;left:4px;color:var(--gold);font-weight:700}
.pack-price{font-family:var(--display);font-size:31px;font-weight:600;color:var(--fg);margin-top:auto}
.pack-save{font-size:13.5px;color:var(--ok);margin-bottom:8px}
/* demos */
.demo-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:18px}
.demo{background:var(--bg2);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;display:flex;flex-direction:column}
.demo img{aspect-ratio:16/10;object-fit:cover;object-position:top center;width:100%;border-bottom:1px solid var(--line)}
.demo .ph{aspect-ratio:16/9;display:grid;place-items:center;background:#0A1526;color:var(--gold);border-bottom:1px solid var(--line)}
.demo .ph svg{width:44px;height:44px}
.demo-body{padding:22px;display:flex;flex-direction:column;gap:10px;flex:1}
.demo h3{font-family:var(--display);font-size:21px;font-weight:600}
.demo p{color:var(--muted);font-size:14.5px}
.demo .actions{margin-top:auto;padding-top:6px}
/* ejemplos */
.ej-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.ej{background:var(--bg2);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;text-decoration:none;color:var(--fg);display:flex;flex-direction:column;transition:.2s}
.ej:hover{border-color:var(--gold);transform:translateY(-3px);box-shadow:0 18px 38px -24px rgba(10,21,38,.5)}
.ej.featured{grid-column:1/-1;flex-direction:row}
.ej-media{aspect-ratio:16/9;position:relative;overflow:hidden;flex:none}
.ej-media img{position:absolute;inset:0;width:100%;height:100%;object-position:top}
.ej-media .ej-logo{position:static;width:96px;height:96px;margin:auto;border-radius:20px;object-fit:cover}
.ej-media:has(.ej-logo){display:grid;place-items:center}
.ej.featured .ej-media{width:52%;aspect-ratio:auto;min-height:280px}
.ej-body{padding:20px;display:flex;flex-direction:column;gap:6px;min-width:0}
.ej.featured .ej-body{padding:32px;justify-content:center}
.ej-tag{font-size:13px;font-weight:600;color:var(--muted2)}
.ej h3{font-family:var(--display);font-size:20px;font-weight:600}
.ej.featured h3{font-size:30px}
.ej p{color:var(--muted);font-size:14.5px}
.ej-go{display:inline-flex;align-items:center;gap:6px;font-size:14.5px;font-weight:600;color:#2F5FA8;margin-top:6px}
@media (max-width:980px){.ej-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:640px){.ej-grid{grid-template-columns:1fr}.ej.featured{flex-direction:column}.ej.featured .ej-media{width:100%;aspect-ratio:16/9;min-height:0}.ej.featured .ej-body{padding:20px}.ej.featured h3{font-size:22px}}
/* sectores */
.sec-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px}
.sec{border:1px solid var(--line);border-radius:var(--r);padding:22px;background:var(--bg2)}
.sec .svc-icon{margin-bottom:12px}
.sec h3{font-size:17px;margin-bottom:8px}
.sec li{font-size:14px;color:var(--muted);list-style:none;padding-left:16px;position:relative;margin-top:4px}
.sec li::before{content:"·";position:absolute;left:4px;color:var(--gold);font-weight:800}
/* proceso */
.steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px;counter-reset:s}
.step{border-top:2px solid var(--fg);padding-top:16px;position:relative}
.step::before{content:"";position:absolute;top:-7px;left:0;width:12px;height:12px;border-radius:50%;background:var(--gold)}
.step b{display:block;font-family:var(--display);font-size:19px;font-weight:600;margin-bottom:6px}
.step b::before{counter-increment:s;content:counter(s) ". ";color:var(--gold)}
.step p{color:var(--muted);font-size:14.5px}
@media (max-width:860px){.steps{grid-template-columns:1fr 1fr}}
@media (max-width:520px){.steps{grid-template-columns:1fr}}
/* faq */
.faq{max-width:780px;display:flex;flex-direction:column;gap:10px}
details{border:1px solid var(--line);border-radius:14px;background:var(--bg2);padding:0 18px}
summary{cursor:pointer;list-style:none;padding:16px 0;font-weight:600;display:flex;justify-content:space-between;gap:12px}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";color:var(--gold);font-size:22px;line-height:1}
details[open] summary::after{content:"–"}
details p{color:var(--muted);padding-bottom:16px;font-size:15px}
/* contacto */
.contact{display:grid;grid-template-columns:1fr 1.2fr;gap:40px;align-items:start}
@media (max-width:860px){.contact{grid-template-columns:1fr}}
.form{display:grid;grid-template-columns:1fr 1fr;gap:14px;background:var(--bg2);border:1px solid var(--line);border-radius:var(--r);padding:24px}
.form .full{grid-column:1/-1}
@media (max-width:520px){.form{grid-template-columns:1fr}}
.form label{display:flex;flex-direction:column;gap:6px;font-size:13px;font-weight:600;color:var(--muted)}
.form input,.form select,.form textarea{background:var(--bg);border:1px solid var(--line2);border-radius:10px;padding:12px 13px;color:var(--fg);font:inherit;font-size:16px;width:100%;min-height:48px}
.form textarea{min-height:120px;resize:vertical}
.form input:focus,.form select:focus,.form textarea:focus{outline:none;border-color:var(--accent)}
.form-msg{font-size:14px;color:var(--muted)}
.socials{display:flex;gap:10px;flex-wrap:wrap;margin-top:20px}
footer{border-top:1px solid var(--line);padding-block:28px;color:var(--muted2);font-size:13px}
footer .wrap{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
footer a{color:var(--muted)}
"""

def build_page():
    secs = "".join(f'<span>{n}</span>' for n, _, _ in SECTORES) + "<span>Restaurantes</span>"
    rows = "".join(
        f"<tr><td>{c}</td><td><span class=\"who{' inc' if w.startswith('Incluid') else ''}\">{w}</span></td><td>{a}</td><td>{n}</td></tr>"
        for c, w, a, n in COSTES)
    page = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"/>
<title>Servicios Melina Rivera</title>
<meta name="claude:viewport-fit-sides" content="cover"/>
<meta name="description" content="Webs, asistentes de WhatsApp con IA, CRM y redes sociales para pymes. Trabajo en remoto, desde cualquier lugar. Precios claros, qué incluye cada uno y qué pagas aparte, con demos que puedes probar."/>
<meta property="og:title" content="Servicios y precios · Melina Rivera"/>
<meta property="og:description" content="Tecnología que trabaja por tu negocio: webs, IA, CRM y redes. Precios claros y demos que puedes probar."/>
<meta property="og:image" content="https://melinarivera.github.io/MR_Portafolio/img/og-melina.jpg?v=2"/>
<meta property="og:url" content="https://melinarivera.github.io/MR_Portafolio/servicios/?v=2"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta property="og:type" content="website"/>
<meta property="og:locale" content="es_ES"/>
<meta name="twitter:card" content="summary_large_image"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet"/>
<script src="https://cdn.jsdelivr.net/npm/lucide@0.469.0/dist/umd/lucide.min.js"></script>
<style>{CSS}</style>
</head>
<body>
<header class="nav"><div class="wrap nav-in">
  <a class="brand" href="#inicio"><img src="../marca/mr-logo-3d.png" alt="MR"/><span class="bn">Melina Rivera</span></a>
  <nav class="nav-links" aria-label="Secciones">
    <a href="#servicios">Servicios</a><a href="#incluye">Qué incluye</a><a href="#ia-claro">Gasto mensual</a><a href="#demos">Demos</a><a href="#ejemplos">Ejemplos</a><a href="#contacto">Contacto</a>
  </nav>
  <div class="toggle" role="group" aria-label="País y moneda">
    <button type="button" data-country="es" class="on" id="c-es">España · €</button>
    <button type="button" data-country="mx" id="c-mx">México · MXN</button>
  </div>
</div></header>

<main id="inicio">
  <section class="hero"><div class="wrap">
    <p class="eyebrow">Webs · IA · CRM · Redes</p>
    <h1>Lo digital de tu negocio, <em>sin letra pequeña</em></h1>
    <p class="lead">Webs, asistentes de WhatsApp con IA, CRM y redes sociales para pymes, en remoto y desde cualquier lugar. Cada servicio tiene precio de partida, qué incluye, qué pagas aparte y ejemplos que puedes abrir.</p>
    <div class="actions">
      <a class="btn primary" href="#servicios"><i data-lucide="tag"></i>Ver precios</a>
      <a class="btn ghost" href="#demos"><i data-lucide="play"></i>Probar las demos</a>
    </div>
    <div class="sectors" aria-label="Sectores">{secs}</div>
    <p class="tax js-tax">Todos los precios son + IVA (o + impuestos en otros países). Los «desde» son el punto de partida; el precio final depende del alcance y te lo doy cerrado, por escrito, antes de empezar.</p>
  </div></section>

  <section class="band" id="servicios"><div class="wrap">
    <div class="head"><p class="eyebrow">Servicios y precios</p><h2>Elige lo que necesitas <em>ahora</em></h2>
      <p class="lead">Precios de partida revisados con lo que cobran hoy otras freelancers y agencias pequeñas. El precio final depende del alcance y te lo doy cerrado antes de empezar.</p></div>
    <div class="svc-grid">{''.join(service_card(s) for s in S)}
    </div>
  </div></section>

  <section id="incluye"><div class="wrap">
    <div class="head"><p class="eyebrow">Transparencia</p><h2>Qué incluye el precio y <em>qué pagas aparte</em></h2>
      <p class="lead">Las herramientas van siempre a nombre de tu negocio, así nada depende de mí. Esto es lo que paga cada parte.</p></div>
    <div class="table" role="region" aria-label="Costes" tabindex="0"><table>
      <thead><tr><th>Concepto</th><th>Quién lo paga</th><th>Coste aproximado</th><th>Cómo funciona</th></tr></thead>
      <tbody>{rows}</tbody>
    </table></div>
    <p class="note js-note">Importes orientativos de octubre de 2026 (España, + IVA). En México las tarifas de Meta y de los proveedores son distintas: te las detallo en el presupuesto.</p>
  </div></section>

  <section class="band" id="ia-claro"><div class="wrap">
    <div class="head"><p class="eyebrow">Asistentes con IA</p><h2>Lo que vas a pagar <em>cada mes</em></h2>
      <p class="lead">Tres partes: mi cuota (incluye la IA), lo que cobra Meta por los mensajes de WhatsApp y, si quieres, los anuncios. Mueve los valores para ver tu caso.</p></div>
    <div class="calc">
      <div class="calc-in">
        <label for="k-conv">Conversaciones al mes<output id="o-conv">300</output></label>
        <input type="range" id="k-conv" min="50" max="3000" step="50" value="300"/>
        <label for="k-resp">Respuestas por conversación<output id="o-resp">5</output></label>
        <input type="range" id="k-resp" min="2" max="12" step="1" value="5"/>
        <label for="k-rec">Recordatorios de cita al mes<output id="o-rec">150</output></label>
        <input type="range" id="k-rec" min="0" max="1500" step="10" value="150"/>
        <label for="k-camp">Mensajes de campaña al mes<output id="o-camp">0</output></label>
        <input type="range" id="k-camp" min="0" max="2000" step="50" value="0"/>
        <div class="calc-plan" role="group" aria-label="Plan">
          <button type="button" class="on" data-plan="basic">Asistente · [[ia_cuota.eur]]/mes</button>
          <button type="button" data-plan="citas">Con citas · [[ia_citas_cuota.eur]]/mes</button>
        </div>
      </div>
      <div class="calc-out" aria-live="polite">
        <div class="calc-row"><span>Mi cuota <small>incluye IA, servidor y mantenimiento</small></span><b id="r-fee">39,00 €</b></div>
        <div class="calc-row"><span>Conversaciones extra de IA <small id="r-extra-n">dentro del plan</small></span><b id="r-extra">0,00 €</b></div>
        <div class="calc-row"><span>Meta: respuestas a clientes <small id="r-serv-n">gratis hasta 1.000 al mes</small></span><b id="r-serv">0,00 €</b></div>
        <div class="calc-row"><span>Meta: recordatorios <small>≈ 0,0166 € cada uno</small></span><b id="r-rec">0,00 €</b></div>
        <div class="calc-row"><span>Meta: campañas <small>≈ 0,0585 € cada mensaje</small></span><b id="r-camp">0,00 €</b></div>
        <div class="calc-total"><span>Total aproximado al mes <small>+ IVA</small></span><b id="r-total">0,00 €</b></div>
        <p class="calc-ia">De esa cuota, la IA real que consumes son unos <b id="r-ia">0,00 €</b>. El resto es servidor y mi trabajo de mantenimiento.</p>
      </div>
    </div>
    <p class="note">Tarifas de Meta para España vigentes desde el 1 de octubre de 2026. Meta factura directamente a tu negocio y puede cambiar sus precios. Coste de IA calculado con Claude Haiku (unos 3.000 tokens de entrada y 250 de salida por respuesta).</p>
  </div></section>

  <section id="packs"><div class="wrap">
    <div class="head"><p class="eyebrow">Packs</p><h2>Combina y <em>ahorra</em></h2><p class="lead">Lo que más piden las pymes, en un solo precio.</p></div>
    <div class="pack-grid">{''.join(pack_card(p) for p in PACKS)}
    </div>
  </div></section>

  <section class="band" id="demos"><div class="wrap">
    <div class="head"><p class="eyebrow">Demos interactivas</p><h2>Pruébalo como si fuera <em>tu negocio</em></h2>
      <p class="lead">Con datos ficticios. Funcionan también en el móvil.</p></div>
    <div class="demo-grid">
      <article class="demo"><img src="../img/demos-thumbs/asistente-whatsapp.jpg" alt="Demo del asistente de WhatsApp" loading="lazy"/>
        <div class="demo-body"><h3>Asistente de WhatsApp con IA</h3>
          <p>Escríbele como un cliente: pide cita en un centro de estética o una primera consulta en una consultoría de extranjería. Verás cómo rellena la ficha del CRM, programa recordatorios y lo que cuesta cada conversación.</p>
          <div class="actions"><a class="btn primary" href="../demos/asistente-whatsapp/#estetica"><i data-lucide="play"></i>Estética</a><a class="btn ghost" href="../demos/asistente-whatsapp/#extranjeria"><i data-lucide="play"></i>Extranjería</a></div></div></article>
      <article class="demo"><img src="../img/demos-thumbs/crm-restaurante.jpg" alt="Demo del CRM para restaurantes" loading="lazy"/>
        <div class="demo-body"><h3>CRM para restaurantes</h3>
          <p>Reservas por turnos, fichas con los 14 alérgenos, consentimiento RGPD, clientes VIP y dormidos, campañas por WhatsApp y exportación a Excel.</p>
          <div class="actions"><a class="btn primary" href="../demos/crm-restaurante/"><i data-lucide="play"></i>Abrir la demo</a></div></div></article>
      <article class="demo"><img src="../img/thumbs/nexo-facturas.jpg" alt="Demo de Nexo, facturas con IA" loading="lazy"/>
        <div class="demo-body"><h3>Nexo: facturas con IA para gestorías</h3>
          <p>Para despachos que llevan varias empresas: recepción de facturas, lectura con IA, aprobaciones, conciliación, incidencias y exportación al programa contable.</p>
          <div class="actions"><a class="btn primary" href="https://melinarivera.github.io/Nexo_Facturas/" target="_blank" rel="noopener"><i data-lucide="external-link"></i>Abrir la demo</a></div></div></article>
      <article class="demo"><img src="../img/demos-thumbs/informe-mantenimiento.jpg" alt="Demo: Informe mensual de mantenimiento" loading="lazy"/>
        <div class="demo-body"><h3>Informe mensual de mantenimiento</h3>
          <p>Lo que recibe cada mes quien tiene mantenimiento: web disponible, copias de seguridad, certificado, dominio y los cambios hechos. Pide un cambio y mira cómo queda anotado.</p>
          <div class="actions"><a class="btn primary" href="../demos/informe-mantenimiento/"><i data-lucide="play"></i>Abrir la demo</a></div></div></article>
      <article class="demo"><img src="../img/demos-thumbs/prototipo-ux.jpg" alt="Demo: Prototipo de app" loading="lazy"/>
        <div class="demo-body"><h3>Diseño UX/UI: prototipo de app</h3>
          <p>Un prototipo de reservas en el que puedes tocar y avanzar, con la razón de cada pantalla y su guía de estilo.</p>
          <div class="actions"><a class="btn primary" href="../demos/prototipo-ux/"><i data-lucide="play"></i>Abrir la demo</a></div></div></article>
      <article class="demo"><img src="../img/demos-thumbs/identidad-visual.jpg" alt="Demo: Generador de identidad visual" loading="lazy"/>
        <div class="demo-body"><h3>Identidad visual: tu marca en un minuto</h3>
          <p>Escribe el nombre de tu negocio, elige estilo y color, y mira el logo, la paleta, una publicación y una tarjeta de visita.</p>
          <div class="actions"><a class="btn primary" href="../demos/identidad-visual/"><i data-lucide="play"></i>Abrir la demo</a></div></div></article>
      <article class="demo"><img src="../img/demos-thumbs/ficha-google.jpg" alt="Demo: Ficha de Google completa" loading="lazy"/>
        <div class="demo-body"><h3>Ficha de Google completa</h3>
          <p>Marca lo que tiene la ficha de un negocio y mira cómo cambia lo que ve quien lo busca en Google Maps.</p>
          <div class="actions"><a class="btn primary" href="../demos/ficha-google/"><i data-lucide="play"></i>Abrir la demo</a></div></div></article>
      <article class="demo"><img src="../img/demos-thumbs/semaforo-ia.jpg" alt="Demo: Semáforo de datos del taller de IA" loading="lazy"/>
        <div class="demo-body"><h3>Taller de IA: el semáforo de datos</h3>
          <p>Una muestra del taller: toca una situación y mira si se puede meter en la IA, y copia tres instrucciones listas para usar en el trabajo diario.</p>
          <div class="actions"><a class="btn primary" href="../demos/semaforo-ia/"><i data-lucide="play"></i>Abrir la demo</a></div></div></article>
      <article class="demo"><img src="../img/demos-thumbs/recepcionista-voz.jpg" alt="Demo: Recepcionista de voz con IA" loading="lazy"/>
        <div class="demo-body"><h3>Recepcionista de voz con IA</h3>
          <p>Escucha cómo atiende una llamada: toma una reserva en un restaurante o una cita en una clínica, y te envía el resumen por WhatsApp. Simulada, con datos ficticios.</p>
          <div class="actions"><a class="btn primary" href="../demos/recepcionista-voz/#restaurante"><i data-lucide="play"></i>Restaurante</a><a class="btn ghost" href="../demos/recepcionista-voz/#clinica">Clínica</a></div></div></article>
    </div>
  </div></section>

  <section id="ejemplos"><div class="wrap">
    <div class="head"><p class="eyebrow">Ejemplos reales</p><h2>Proyectos que puedes <em>abrir ahora</em></h2>
      <p class="lead">Solo enlazo lo que está publicado y funcionando.</p></div>
    <div class="ej-grid">{''.join(ejemplo_card(e) for e in EJEMPLOS)}
    </div>
  </div></section>

  <section class="band" id="sectores"><div class="wrap">
    <div class="head"><p class="eyebrow">Redes y reputación</p><h2>Pensado para <em>negocios locales y despachos</em></h2>
      <p class="lead">Así adapto las redes, Google y WhatsApp a cada tipo de negocio.</p></div>
    <div class="sec-grid">{''.join(f'<article class="sec"><span class="svc-icon"><i data-lucide="{ic}"></i></span><h3>{n}</h3><ul>{"".join(f"<li>{b}</li>" for b in bs)}</ul></article>' for n, ic, bs in SECTORES)}
    </div>
  </div></section>

  <section><div class="wrap">
    <div class="head"><p class="eyebrow">Cómo trabajo</p><h2>De la llamada al <em>lanzamiento</em></h2></div>
    <div class="steps">
      <div class="step"><b>Llamada gratuita</b><p>20 minutos para entender tu negocio y qué te quita tiempo.</p></div>
      <div class="step"><b>Presupuesto cerrado</b><p>Qué incluye, qué pagas aparte y plazos, por escrito.</p></div>
      <div class="step"><b>Construcción</b><p>Te enseño avances cada semana para que decidas sobre la marcha.</p></div>
      <div class="step"><b>Lanzamiento y formación</b><p>Lo publicamos, te enseño a usarlo y quedo de soporte.</p></div>
    </div>
  </div></section>

  <section class="band" id="faq"><div class="wrap">
    <div class="head"><p class="eyebrow">Preguntas frecuentes</p><h2>Lo que suelen <em>preguntarme</em></h2></div>
    <div class="faq">{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)}</div>
  </div></section>

  <section id="contacto"><div class="wrap contact">
    <div><p class="eyebrow">Contacto</p><h2>Cuéntame qué <em>necesitas</em></h2>
      <p class="lead">Te respondo en menos de 24 horas con una propuesta o con las preguntas que necesite para dártela.</p>
      <div class="socials">
        <a class="btn ghost" href="{IG}" target="_blank" rel="noopener"><i data-lucide="instagram"></i>Instagram</a>
        <a class="btn ghost" href="{LI}" target="_blank" rel="noopener"><i data-lucide="linkedin"></i>LinkedIn</a>
        <a class="btn ghost" href="../"><i data-lucide="user"></i>Mi portafolio</a>
      </div>
    </div>
    <form class="form" id="contact-form" action="{FORM}" method="POST">
      <label>Tu nombre<input id="f-name" name="nombre" required placeholder="Ana García"/></label>
      <label>Email<input id="f-email" name="email" type="email" required placeholder="ana@negocio.com"/></label>
      <label>¿Qué necesitas?<select id="f-service" name="servicio">
        {''.join(f'<option>{s["name"]}</option>' for s in S)}{''.join(f'<option>{p["name"]}</option>' for p in PACKS)}<option selected>No lo sé, quiero que me orientes</option></select></label>
      <label>País<select id="f-country" name="pais"><option>España</option><option>México</option><option>Otro país</option></select></label>
      <label class="full">Tu negocio y lo que quieres conseguir<textarea id="f-msg" name="mensaje" required placeholder="Tengo un centro de estética en Carabanchel y quiero que me reserven por WhatsApp…"></textarea></label>
      <div class="full"><button class="btn primary" type="submit" id="f-submit">Enviar</button> <span class="form-msg" id="f-msg-status" role="status"></span></div>
    </form>
  </div></section>
</main>

<footer><div class="wrap"><span>© 2026 Melina Rivera · Trabajo en remoto</span><span><a href="../">Portafolio</a> · <a href="{IG}" target="_blank" rel="noopener">Instagram</a></span></div></footer>

<script>
(function(){{
  if (window.lucide) lucide.createIcons();
  var TAX = {{ es:'Todos los precios son + IVA (o + impuestos en otros países). Los «desde» son el punto de partida; el precio final depende del alcance y te lo doy cerrado, por escrito, antes de empezar.', mx:'Todos los precios son + IVA (o + impuestos en otros países). Los «desde» son el punto de partida; el precio final depende del alcance y te lo doy cerrado, por escrito, antes de empezar.' }};
  function setCountry(c){{
    document.querySelectorAll('.js-price').forEach(function(el){{ el.textContent = c === 'mx' ? el.dataset.mxn : el.dataset.eur; }});
    document.querySelectorAll('[data-country]').forEach(function(b){{ b.classList.toggle('on', b.dataset.country === c); b.setAttribute('aria-pressed', b.dataset.country === c); }});
    var t = document.querySelector('.js-tax'); if (t) t.textContent = TAX[c];
    var s = document.getElementById('f-country'); if (s) s.value = c === 'mx' ? 'México' : 'España';
    try {{ localStorage.setItem('mr-country', c); }} catch(e) {{}}
  }}
  document.querySelectorAll('[data-country]').forEach(function(b){{ b.addEventListener('click', function(){{ setCountry(b.dataset.country); }}); }});
  var c = null; try {{ c = new URLSearchParams(location.search).get('pais'); }} catch(e) {{}}
  if (c !== 'mx' && c !== 'es') {{ try {{ c = localStorage.getItem('mr-country'); }} catch(e) {{ c = null; }} }}
  if (c !== 'mx' && c !== 'es') {{ var tz = ''; try {{ tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ''; }} catch(e) {{}}
    c = /^America\\/(Mexico_City|Monterrey|Merida|Cancun|Tijuana|Chihuahua|Hermosillo|Mazatlan|Bahia_Banderas|Matamoros|Ojinaga)/.test(tz) ? 'mx' : 'es'; }}
  setCountry(c);
  document.querySelectorAll('.js-service').forEach(function(a){{ a.addEventListener('click', function(){{
    var sel = document.getElementById('f-service'); for (var i = 0; i < sel.options.length; i++) if (sel.options[i].text === a.dataset.service) sel.selectedIndex = i; }}); }});
  // Calculadora de gasto mensual del asistente (España, tarifas de Meta desde oct 2026)
  var plan = 'basic';
  var PLANS = {{ basic:{{ fee:[[ia_cuota.eur_n]], incl:[[ia_incluidas.n]] }}, citas:{{ fee:[[ia_citas_cuota.eur_n]], incl:[[ia_citas_incluidas.n]] }} }};
  var fmt = function(n){{ return n.toLocaleString('es-ES',{{minimumFractionDigits:2,maximumFractionDigits:2}}) + ' €'; }};
  var g = function(id){{ return document.getElementById(id); }};
  function calc(){{
    var conv = +g('k-conv').value, resp = +g('k-resp').value, rec = +g('k-rec').value, camp = +g('k-camp').value;
    g('o-conv').textContent = conv.toLocaleString('es-ES'); g('o-resp').textContent = resp;
    g('o-rec').textContent = rec.toLocaleString('es-ES'); g('o-camp').textContent = camp.toLocaleString('es-ES');
    var p = PLANS[plan], extraConv = Math.max(0, conv - p.incl), bloques = Math.ceil(extraConv / 1000);
    var replies = conv * resp, servPaid = Math.max(0, replies - 1000);
    var fee = p.fee, extra = bloques * [[ia_bloque_extra.eur_n]], serv = servPaid * 0.0166, recC = rec * 0.0166, campC = camp * 0.0585;
    var ia = replies * (3000 * 0.10 + 250 * 0.50) / 1e6 * 0.92;   // USD → EUR aprox.
    g('r-fee').textContent = fmt(fee); g('r-extra').textContent = fmt(extra);
    g('r-extra-n').textContent = bloques ? (bloques + ' bloque' + (bloques > 1 ? 's' : '') + ' de 1.000 · [[ia_bloque_extra.eur]] cada uno') : 'dentro del plan (' + p.incl.toLocaleString('es-ES') + ' incluidas)';
    g('r-serv').textContent = fmt(serv);
    g('r-serv-n').textContent = replies.toLocaleString('es-ES') + ' respuestas · gratis hasta 1.000 al mes';
    g('r-rec').textContent = fmt(recC); g('r-camp').textContent = fmt(campC);
    g('r-total').textContent = fmt(fee + extra + serv + recC + campC); g('r-ia').textContent = fmt(ia);
  }}
  ['k-conv','k-resp','k-rec','k-camp'].forEach(function(id){{ g(id).addEventListener('input', calc); }});
  document.querySelectorAll('[data-plan]').forEach(function(b){{ b.addEventListener('click', function(){{
    plan = b.dataset.plan; document.querySelectorAll('[data-plan]').forEach(function(x){{ x.classList.toggle('on', x === b); }}); calc(); }}); }});
  calc();

  var form = document.getElementById('contact-form'), st = document.getElementById('f-msg-status'), btn = document.getElementById('f-submit');
  form.addEventListener('submit', function(e){{
    e.preventDefault(); btn.disabled = true; st.textContent = 'Enviando…';
    fetch(form.action, {{ method:'POST', body:new FormData(form), headers:{{ Accept:'application/json' }} }})
      .then(function(r){{ if (!r.ok) throw 0; form.reset(); st.textContent = 'Recibido. Te respondo en menos de 24 horas.'; }})
      .catch(function(){{ st.textContent = 'No se ha podido enviar. Escríbeme por Instagram: @melina_rivera_developer'; }})
      .finally(function(){{ btn.disabled = false; }});
  }});
}})();
</script>
</body>
</html>
"""
    os.makedirs(os.path.join(ROOT, "servicios"), exist_ok=True)
    open(os.path.join(ROOT, "servicios", "index.html"), "w", encoding="utf-8").write(fill(page))

# ───────────────────────── resumen en el portafolio ─────────────────────────
HOME_FAMS = [
  ("Tu sitio en internet", "Webs, tiendas y apps", [
    ("Landing de una página", "Para presentar el negocio y recibir mensajes.", "desde [[d_landing.eur]]", "pago único", "Ver ejemplo", "https://melinarivera.github.io/pinata/"),
    ("Web completa", "Varias secciones, blog y formularios conectados.", "desde [[d_web.eur]]", "pago único", "Ver ejemplo", "https://melinarivera.github.io/pyme-efsun/"),
    ("Tienda online", "Catálogo, carrito y pagos.", "desde [[d_tienda.eur]]", "pago único", "Ver ejemplo", "https://melinarivera.github.io/tienda-esoterica/"),
    ("App o SaaS a medida", "Tu idea o tu herramienta interna, desde la primera versión.", "desde [[d_app.eur]]", "por proyecto", "Ver ejemplo", "https://www.tesovia.com"),
  ]),
  ("IA que atiende por ti", "WhatsApp, voz y automatizaciones", [
    ("Asistente de WhatsApp con IA", "Contesta, informa y agenda. Tú ves todo lo que dice.", "desde [[d_ia.eur]]", "+ [[d_ia_cuota.eur]]/mes", "Ver demo", "demos/asistente-whatsapp/#estetica"),
    ("Recepcionista de voz con IA", "Coge el teléfono cuando tú no puedes y te pasa el resumen.", "desde [[d_voz.eur]]", "+ [[d_voz_cuota.eur]]/mes", "Ver demo", "demos/recepcionista-voz/#restaurante"),
    ("Automatizaciones", "Lo que haces a mano cada semana, hecho solo.", "desde [[d_automatizacion.eur]]", "por automatización", "Ver demo", "https://melinarivera.github.io/Nexo_Facturas/"),
    ("Formación en IA para tu equipo", "Taller práctico con lo que sí se puede meter en la IA y lo que no.", "desde [[d_formacion_ia.eur]]", "por sesión", "Ver demo", "demos/semaforo-ia/"),
  ]),
  ("Orden dentro del negocio", "CRM y mantenimiento", [
    ("CRM y planners a medida", "Clientes, reservas y tareas en un sitio, no en cuatro Excels.", "desde [[d_crm.eur]]", "pago único", "Ver demo", "demos/crm-restaurante/"),
    ("Mantenimiento", "Copias, actualizaciones y un informe claro cada mes.", "desde [[d_mantenimiento.eur]]", "al mes", "Ver demo", "demos/informe-mantenimiento/"),
  ]),
  ("Que te vean y te reconozcan", "Marca, diseño y visibilidad", [
    ("Ficha de Google y SEO local", "Para salir cuando te buscan cerca.", "desde [[d_seo_local.eur]]", "pago único", "Ver demo", "demos/ficha-google/"),
    ("Identidad visual básica", "Logo, colores, tipografías y plantillas.", "desde [[d_identidad.eur]]", "por proyecto", "Ver demo", "demos/identidad-visual/"),
    ("Diseño UX/UI", "Ver y tocar tu web o app antes de programarla.", "desde [[d_uxui.eur]]", "por proyecto", "Ver demo", "demos/prototipo-ux/"),
    ("Redes sociales", "Calendario, diseños y respuesta a reseñas.", "desde [[d_redes.eur]]", "al mes", "Ver ejemplo", IG),
    ("Vídeos con avatar IA", "Un presentador virtual que explica tus servicios.", "desde [[d_avatar_video.eur]]", "por vídeo", "Ver demo", "demos/avatar-video/"),
  ]),
]

def build_portfolio_summary():
    """Reescribe la lista de precios del inicio (index.html) entre las marcas PRECIOS."""
    out = []
    for title, sub, items in HOME_FAMS:
        rows = "".join(
            f'    <div class="row"><div class="nm">{html.escape(n)}<small>{html.escape(d)}</small></div>'
            f'<div class="pr">{pr}<em>{per}</em></div>'
            f'<a class="dm" href="{href}"{chr(32)+chr(116)+"arget=" + chr(34) + "_blank" + chr(34) + " rel=" + chr(34) + "noopener" + chr(34) if href.startswith("http") else ""}>'
            f'<i data-lucide="{"external-link" if lbl.startswith("Ver ejemplo") else "play"}"></i>{lbl}</a></div>\n'
            for n, d, pr, per, lbl, href in items)
        out.append(f'  <div class="fam">\n    <h3>{title} <span>{sub}</span></h3>\n{rows}  </div>')
    block = "\n".join(out)
    p = os.path.join(ROOT, "index.html")
    s = open(p, encoding="utf-8").read()
    a, b = "<!-- PRECIOS:inicio -->", "<!-- PRECIOS:fin -->"
    if a not in s or b not in s:
        print("aviso: no encuentro las marcas de precios en index.html; no se toca el inicio")
        return
    i = s.index(a) + len(a); j = s.index(b)
    open(p, "w", encoding="utf-8").write(s[:i] + "\n" + fill(block) + "\n  " + s[j:])

if __name__ == "__main__":
    build_page()
    build_portfolio_summary()
    print("ok")
