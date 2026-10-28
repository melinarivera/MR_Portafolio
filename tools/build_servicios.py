"""Genera servicios/index.html y el resumen de servicios del portafolio desde un único sitio.

Uso:  python3 tools/build_servicios.py
Edita aquí precios, textos y ejemplos; las dos páginas se actualizan a la vez.
"""
import os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IG = "https://www.instagram.com/melina_rivera_developer/"
LI = "https://www.linkedin.com/in/deliamelinarivera"
FORM = "https://formspree.io/f/xbdplnyg"

# ───────────────────────── PRECIOS (España € / México MXN) ─────────────────────────
# Revisados en oct 2026 con tarifas publicadas por freelancers y agencias pequeñas de España.
S = [
  dict(id="landing", icon="rocket", name="Landing page sencilla", ideal="Para autónomos y negocios que empiezan",
       eur="desde 350 €", mxn="desde $3,500 MXN", per="/ proyecto",
       items=["Una página clara y rápida, pensada para móvil", "Botón de WhatsApp, formulario y mapa", "Textos orientados a conseguir contactos", "SEO local básico para Google", "Lista en 1–2 semanas"],
       aparte="Dominio y alojamiento a tu nombre · textos legales con iubenda",
       ex=[("Efsun tienda", "https://melinarivera.github.io/tienda-esoterica/")]),
  dict(id="web", icon="store", name="Web corporativa", ideal="Para pymes que quieren generar confianza",
       eur="desde 1.100 €", mxn="desde $12,000 MXN", per="/ proyecto", popular=True,
       items=["5–7 páginas con estructura pensada para vender", "Blog o catálogo de servicios", "SEO básico en cada página", "WhatsApp, formulario y analítica", "Aviso legal con tus datos + privacidad y cookies con iubenda"],
       aparte="Dominio y alojamiento a tu nombre · suscripción a iubenda",
       ex=[("ETERN-ME", "https://etern-me.com"), ("Cotidiana", "https://cotidiana.app")]),
  dict(id="tienda", icon="shopping-bag", name="Tienda online o reservas", ideal="Para vender o reservar online 24/7",
       eur="desde 1.600 €", mxn="desde $16,000 MXN", per="/ proyecto",
       items=["Catálogo, carrito y pago con tarjeta (Stripe, TPV o Mercado Pago)", "O agenda de citas con recordatorios", "Panel para gestionar pedidos o reservas", "Diseño a medida, sin plantillas", "30 días de soporte tras el lanzamiento"],
       aparte="Comisión de la pasarela de pago en cada venta · alojamiento",
       ex=[("Efsun plataforma", "https://melinarivera.github.io/pyme-efsun/")]),
  dict(id="ia", icon="sparkles", name="Asistente de WhatsApp con IA", ideal="Para dejar de responder siempre lo mismo",
       eur="desde 490 €", mxn="desde $5,500 MXN", per="+ 39 €/mes", per_mx="+ $650 MXN/mes", new=True,
       items=["Responde dudas 24/7 en WhatsApp o en tu web", "Entrenado con tu información: precios, horarios, servicios", "Pasa la conversación a una persona cuando hace falta", "<b>Con citas</b> (agenda, recordatorios y ficha en el CRM): <span class='js-price' data-eur='desde 890 € + 69 €/mes' data-mxn='desde $9,900 MXN + $1,100 MXN/mes'>desde 890 € + 69 €/mes</span>", "La cuota incluye mantenimiento y el coste de la IA"],
       aparte="Mensajes de WhatsApp: los cobra Meta a tu negocio (responder a clientes es gratis hasta 1.000/mes)",
       extra=("Automatizaciones de procesos (facturas, recordatorios, informes)", "desde 290 €", "desde $3,500 MXN", "por flujo"),
       ex=[("Demo estética", "../demos/asistente-whatsapp/#estetica"), ("Demo extranjería", "../demos/asistente-whatsapp/#extranjeria"), ("Tesovia", "https://www.tesovia.com")]),
  dict(id="crm", icon="layout-dashboard", name="CRM y planners a medida", ideal="Para tener clientes y tareas en orden",
       eur="desde 1.200 €", mxn="desde $14,000 MXN", per="/ proyecto",
       items=["Fichas de cliente con historial y segmentos", "Reservas, agenda o embudo de ventas", "Campañas por WhatsApp o email respetando el RGPD", "Exportación a Excel", "Formación para usarlo desde el primer día"],
       aparte="Base de datos: plan gratuito al empezar; si crece, desde unos 25 $/mes",
       extra=("¿Prefieres HubSpot, Notion u otro? Te lo configuro", "desde 400 €", "desde $4,500 MXN", ""),
       ex=[("Demo CRM restaurante", "../demos/crm-restaurante/"), ("ZenWi", "https://zenwi.app")]),
  dict(id="redes", icon="megaphone", name="Redes sociales y reputación", ideal="Para que te encuentren y te elijan",
       eur="desde 220 €", mxn="desde $3,500 MXN", per="/ mes", per_mx="/ mes", new=True,
       items=["<b>Esencial</b> · <span class='js-price' data-eur='220 €/mes' data-mxn='$3,500 MXN/mes'>220 €/mes</span>: 2 redes, 8 publicaciones al mes", "<b>Crecimiento</b> · <span class='js-price' data-eur='420 €/mes' data-mxn='$6,500 MXN/mes'>420 €/mes</span>: 12 posts + 4 reels y gestión de anuncios", "Diseños propios con IA y calendario mensual", "Respuesta a reseñas y perfil de Google optimizado"],
       aparte="La inversión en anuncios la pagas tú directamente a Meta o Google",
       extra=("Auditoría de tus perfiles con plan de acción", "120 €", "$1,500 MXN", "pago único"),
       ex=[("Mi Instagram", IG)]),
  dict(id="app", icon="smartphone", name="App o SaaS a medida", ideal="Para tu idea o tu herramienta interna",
       eur="MVP desde 3.000 €", mxn="MVP desde $35,000 MXN", per="/ proyecto",
       items=["Definimos juntos la primera versión (MVP)", "Usuarios, roles y panel de administración", "Base de datos y backend incluidos", "Publicación en producción", "30 días de soporte tras el lanzamiento"],
       aparte="Alojamiento, base de datos y, si lleva IA, su consumo",
       ex=[("Tesovia", "https://www.tesovia.com"), ("ETERN-ME", "https://etern-me.com"), ("TravelMates", "https://melinarivera.github.io/TravelMates-App")]),
  dict(id="mant", icon="wrench", name="Mantenimiento", ideal="Para que tu web siempre funcione",
       eur="desde 49 €", mxn="desde $700 MXN", per="/ mes", per_mx="/ mes",
       items=["Vigilancia de dominio, alojamiento y certificado SSL", "Copias de seguridad", "Pequeños cambios de contenido incluidos", "Soporte directo por WhatsApp"],
       aparte="Las renovaciones de dominio y alojamiento siguen a tu nombre", ex=[]),
]

PACKS = [
  dict(name="Pack Arranque", for_="Para empezar a recibir clientes por internet", items=["Landing page sencilla", "Asistente de WhatsApp con IA", "Auditoría de redes con plan de acción"],
       eur="desde 790 €", mxn="desde $8,900 MXN", s_eur="Ahorras 170 € · después, 39 €/mes del asistente", s_mxn="Ahorras $1,600 MXN · después, $650 MXN/mes del asistente"),
  dict(name="Pack Pyme Digital", for_="Para profesionalizar tu presencia online", items=["Web corporativa", "Asistente de WhatsApp con IA", "3 meses de redes plan Esencial"], popular=True,
       eur="desde 1.890 €", mxn="desde $23,900 MXN", s_eur="Ahorras 360 € · después, 39 €/mes del asistente", s_mxn="Ahorras $4,100 MXN · después, $650 MXN/mes del asistente"),
  dict(name="Pack Organiza tu negocio", for_="Para dejar las hojas de cálculo y el papel", items=["CRM a medida", "2 automatizaciones de procesos", "Formación para tu equipo"],
       eur="desde 1.590 €", mxn="desde $18,500 MXN", s_eur="Ahorras 190 €", s_mxn="Ahorras $2,500 MXN"),
]

# Qué incluye el precio y qué pagas aparte
COSTES = [
  ("Mi trabajo: diseño, desarrollo, configuración y formación", "Incluido en el precio", "—", "Presupuesto cerrado antes de empezar."),
  ("Dominio (.es, .com, .mx)", "Tú, a tu nombre", "unos 10–15 € al año", "Es tuyo. Si algún día cambias de proveedor, te lo llevas."),
  ("Alojamiento (hosting)", "Tú, a tu nombre", "0 € en webs sencillas · 3–10 €/mes en tiendas o WordPress", "Uso planes con uso comercial permitido. Te ayudo a contratarlo."),
  ("Textos legales: privacidad y cookies", "Tú, a tu nombre (iubenda)", "plan gratuito limitado o desde unos 6 €/mes", "Se actualizan cuando cambia la normativa. Yo los configuro e instalo el banner de cookies."),
  ("Aviso legal", "Incluido", "—", "Lo redacto con los datos de tu negocio. En despachos, extranjería o salud, recomiendo que lo revise tu abogado/a."),
  ("Pagos online", "Comisión de la pasarela", "según Stripe, TPV de tu banco o Mercado Pago", "Se descuenta de cada venta. Yo no cobro comisión."),
  ("IA (tokens) del asistente", "Incluida en la cuota mensual", "uso normal de una pyme: pocos euros al mes", "Si superas unas 1.000 conversaciones al mes, te aviso antes de ajustar la cuota."),
  ("Mensajes de WhatsApp (Meta)", "Tu negocio, directamente a Meta", "responder a clientes: gratis hasta 1.000/mes · recordatorio ≈ 0,017 € · campaña ≈ 0,059 €", "Tarifas de Meta para España en 2026. Meta te factura a ti; yo no añado margen."),
  ("Anuncios en Meta o Google", "Tú, directamente a la plataforma", "lo decides tú", "Mi gestión va en la cuota de redes."),
  ("Canva Pro, plantillas y herramientas de diseño", "Incluido", "—", "Las uso yo; no tienes que contratar nada."),
  ("Base de datos de un CRM o app", "Gratis al empezar · tú si crece", "desde unos 25 $/mes cuando hay mucho uso", "Te aviso antes de que haga falta subir de plan."),
]

EJEMPLOS = [  # solo proyectos con página real funcionando
  dict(name="Tesovia", tag="SaaS con IA", desc="Asistente académico con IA en español e inglés: citas APA, feedback, detección de IA y plagio.", img="../img/thumbs/tesovia.jpg", url="https://www.tesovia.com", fit="cover", bg="#F5F6FF", featured=True),
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
  ("Tiendas de barrio", "shopping-basket", ["Perfil de Google y mapa optimizados", "Catálogo en WhatsApp o tienda sencilla", "Publicaciones de novedades y ofertas"]),
]

FAQ = [
  ("¿La web y el dominio son míos?", "Sí. El dominio, el alojamiento y las cuentas van a tu nombre desde el primer día. Si dejamos de trabajar juntas, te lo llevas todo."),
  ("¿Quién paga la IA y los mensajes de WhatsApp?", "La IA va incluida en la cuota mensual del asistente. Los mensajes de WhatsApp los cobra Meta directamente a tu negocio, y responder a tus clientes es gratis hasta 1.000 mensajes al mes."),
  ("¿Los textos legales me protegen?", "Uso iubenda, que genera la política de privacidad y de cookies y la actualiza cuando cambia la ley. En sectores regulados recomiendo que tu abogado/a revise el aviso legal."),
  ("¿Puedo dejar las cuotas mensuales?", "Sí, sin permanencia. Avisas con 30 días y te dejo todo documentado para que otra persona pueda seguir."),
  ("¿Trabajas con negocios de México?", "Sí. Elige México arriba para ver precios en pesos. Facturo en remoto y nos vemos por videollamada."),
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
  --bg:#08080F; --bg2:#0F0F1A; --bg3:#16162A; --line:rgba(240,237,232,.09); --line2:rgba(240,237,232,.16);
  --fg:#F0EDE8; --muted:rgba(240,237,232,.68); --muted2:rgba(240,237,232,.48);
  --accent:#5B8DB8; --accent-2:#8BB8D8; --accent-dim:rgba(91,141,184,.14); --ok:#4CAF82;
  --display:'Playfair Display',Georgia,'Times New Roman',serif; --body:'DM Sans',system-ui,-apple-system,'Segoe UI',sans-serif;
  --r:18px; color-scheme:dark;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;scroll-padding-top:84px}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important}}
body{background:var(--bg);color:var(--fg);font-family:var(--body);font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:var(--accent-2)}
img{max-width:100%;display:block}
i[data-lucide],svg.lucide{width:1em;height:1em;stroke-width:2;flex:none}
.wrap{max-width:1160px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
section{padding-block:76px}
.band{background:var(--bg2);border-block:1px solid var(--line)}
h1,h2,h3{text-wrap:balance}
h2{font-family:var(--display);font-weight:700;font-size:clamp(28px,4vw,40px);line-height:1.15;letter-spacing:-.01em}
h2 em{font-style:italic;color:var(--accent-2);font-weight:500}
.lead{color:var(--muted);max-width:62ch;margin-top:12px}
.eyebrow{display:inline-flex;align-items:center;gap:8px;font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--accent-2);margin-bottom:12px}
.head{margin-bottom:36px}
/* nav */
.nav{position:sticky;top:env(safe-area-inset-top,0px);z-index:20;background:rgba(8,8,15,.86);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:21;background:var(--bg)}
.nav-in{display:flex;align-items:center;gap:20px;min-height:64px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--fg);font-weight:600;white-space:nowrap}
.brand img{width:34px;height:34px;border-radius:50%}
.nav-links{display:flex;gap:18px;margin-left:auto}
.nav-links a{color:var(--muted);text-decoration:none;font-size:14px;font-weight:500}
.nav-links a:hover{color:var(--fg)}
.toggle{display:inline-flex;background:var(--bg3);border:1px solid var(--line);border-radius:99px;padding:3px;gap:2px}
.toggle button{border:0;background:transparent;color:var(--muted);font:inherit;font-size:13px;font-weight:600;padding:6px 12px;border-radius:99px;cursor:pointer;white-space:nowrap}
.toggle button.on{background:var(--accent);color:#fff}
.toggle button:focus-visible,.btn:focus-visible,a:focus-visible,summary:focus-visible{outline:2px solid var(--accent-2);outline-offset:2px}
@media (max-width:860px){.nav-links{display:none}.nav-in{justify-content:space-between}}
/* hero */
.hero{padding-block:64px 56px}
.hero h1{font-family:var(--display);font-weight:700;font-size:clamp(34px,6vw,60px);line-height:1.06;letter-spacing:-.02em;max-width:17ch}
.hero h1 em{font-style:italic;font-weight:500;color:var(--accent-2)}
.hero .lead{font-size:18px}
.actions{display:flex;gap:12px;flex-wrap:wrap;margin-top:26px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:12px 20px;border-radius:99px;font-weight:600;font-size:14.5px;text-decoration:none;border:1px solid var(--line2);color:var(--fg);transition:.2s}
.btn.primary{background:var(--accent);border-color:var(--accent);color:#fff}
.btn.primary:hover{background:#4C7DA8}
.btn.ghost:hover{border-color:var(--accent-2)}
.sectors{display:flex;flex-wrap:wrap;gap:8px;margin-top:28px}
.sectors span{font-size:13px;color:var(--muted);border:1px solid var(--line);border-radius:99px;padding:5px 12px}
.tax{font-size:13px;color:var(--muted2);margin-top:14px}
/* servicios */
.svc-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px}
.svc{background:var(--bg);border:1px solid var(--line);border-radius:var(--r);padding:24px;display:flex;flex-direction:column;gap:10px;min-width:0}
.svc-top{display:flex;align-items:center;gap:8px}
.svc-icon{width:42px;height:42px;border-radius:12px;display:grid;place-items:center;background:var(--accent-dim);color:var(--accent-2);font-size:20px;margin-right:auto}
.flag{font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:4px 10px;border-radius:99px;background:var(--accent);color:#fff}
.flag.new{background:transparent;border:1px solid var(--accent-2);color:var(--accent-2)}
.svc h3,.pack h3{font-family:var(--display);font-size:22px;font-weight:700;line-height:1.2}
.svc-ideal{font-size:12.5px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--muted2)}
.svc-price{font-family:var(--display);font-size:26px;color:var(--accent-2);line-height:1.2;margin-top:4px}
.svc-price small{font-family:var(--body);font-size:13px;color:var(--muted)}
.svc-extra{font-size:13.5px;color:var(--muted)}
.svc-extra b{color:var(--fg);font-weight:600}
.svc ul,.pack ul{list-style:none;display:flex;flex-direction:column;gap:7px;margin:6px 0 4px}
.svc li,.pack li{font-size:14.5px;color:var(--muted);padding-left:22px;position:relative}
.svc li::before{content:"";position:absolute;left:2px;top:.62em;width:10px;height:6px;border-left:2px solid var(--accent-2);border-bottom:2px solid var(--accent-2);transform:rotate(-45deg) translateY(-3px)}
.svc li b{color:var(--fg);font-weight:600}
.svc-aparte{display:flex;gap:8px;font-size:13px;color:var(--muted);background:var(--bg3);border-radius:12px;padding:10px 12px;margin-top:auto}
.svc-aparte i,.svc-aparte svg{margin-top:3px;color:var(--accent-2)}
.svc-aparte b{color:var(--fg);font-weight:600}
.svc-ex{display:flex;flex-wrap:wrap;gap:6px}
.svc-ex>span{width:100%;font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--muted2)}
.ex{display:inline-flex;align-items:center;gap:6px;font-size:13px;text-decoration:none;color:var(--accent-2);border:1px solid rgba(139,184,216,.28);background:var(--accent-dim);border-radius:99px;padding:5px 11px}
.ex:hover{color:#fff;border-color:var(--accent-2)}
.svc .btn{margin-top:6px}
/* tabla de costes */
.table{overflow-x:auto;border:1px solid var(--line);border-radius:var(--r);background:var(--bg)}
table{width:100%;border-collapse:collapse;min-width:760px}
th,td{text-align:left;padding:14px 16px;border-bottom:1px solid var(--line);vertical-align:top;font-size:14.5px}
th{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted2);font-weight:700;background:var(--bg3)}
td:first-child{color:var(--fg);font-weight:600;width:26%}
td:nth-child(2){width:20%}
td:nth-child(3){color:var(--accent-2);width:22%}
td:last-child{color:var(--muted)}
tr:last-child td{border-bottom:0}
.who{display:inline-block;font-size:12.5px;font-weight:600;padding:3px 10px;border-radius:99px;background:var(--bg3);color:var(--muted)}
.who.inc{background:rgba(76,175,130,.14);color:var(--ok)}
.note{font-size:13.5px;color:var(--muted2);margin-top:14px;max-width:80ch}
/* packs */
.pack-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}
.pack{background:var(--bg);border:1px solid var(--line);border-radius:var(--r);padding:26px;display:flex;flex-direction:column;gap:8px;position:relative}
.pack.popular{border-color:var(--accent);background:linear-gradient(170deg,var(--bg3),var(--bg))}
.pack .flag{position:absolute;top:-12px;left:24px}
.pack-for{color:var(--muted);font-size:14px}
.pack li::before{content:"+";position:absolute;left:4px;color:var(--accent-2);font-weight:700}
.pack-price{font-family:var(--display);font-size:30px;color:var(--fg);margin-top:auto}
.pack-save{font-size:13.5px;color:var(--ok);margin-bottom:8px}
/* demos */
.demo-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:18px}
.demo{background:var(--bg);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;display:flex;flex-direction:column}
.demo img{aspect-ratio:16/9;object-fit:cover;width:100%;border-bottom:1px solid var(--line)}
.demo-body{padding:22px;display:flex;flex-direction:column;gap:10px;flex:1}
.demo h3{font-family:var(--display);font-size:22px}
.demo p{color:var(--muted);font-size:14.5px}
.demo .actions{margin-top:auto;padding-top:6px}
/* ejemplos */
.ej-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}
.ej{background:var(--bg2);border:1px solid var(--line);border-radius:var(--r);overflow:hidden;text-decoration:none;color:var(--fg);display:flex;flex-direction:column;transition:.2s}
.ej:hover{border-color:var(--accent);transform:translateY(-3px)}
.ej.featured{grid-column:1/-1;flex-direction:row}
.ej-media{aspect-ratio:16/9;position:relative;overflow:hidden;flex:none}
.ej-media img{position:absolute;inset:0;width:100%;height:100%;object-position:top}
.ej-media .ej-logo{position:static;width:96px;height:96px;margin:auto;border-radius:20px;object-fit:cover}
.ej-media:has(.ej-logo){display:grid;place-items:center}
.ej.featured .ej-media{width:52%;aspect-ratio:auto;min-height:280px}
.ej-body{padding:20px;display:flex;flex-direction:column;gap:6px;min-width:0}
.ej.featured .ej-body{padding:32px;justify-content:center}
.ej-tag{font-size:11.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--accent-2)}
.ej h3{font-family:var(--display);font-size:20px}
.ej.featured h3{font-size:30px}
.ej p{color:var(--muted);font-size:14.5px}
.ej-go{display:inline-flex;align-items:center;gap:6px;font-size:14px;font-weight:600;color:var(--accent-2);margin-top:6px}
@media (max-width:980px){.ej-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:640px){.ej-grid{grid-template-columns:1fr}.ej.featured{flex-direction:column}.ej.featured .ej-media{width:100%;aspect-ratio:16/9;min-height:0}.ej.featured .ej-body{padding:20px}.ej.featured h3{font-size:22px}}
/* sectores */
.sec-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px}
.sec{border:1px solid var(--line);border-radius:var(--r);padding:22px;background:var(--bg)}
.sec .svc-icon{margin-bottom:12px}
.sec h3{font-size:17px;margin-bottom:8px}
.sec li{font-size:14px;color:var(--muted);list-style:none;padding-left:16px;position:relative;margin-top:4px}
.sec li::before{content:"·";position:absolute;left:4px;color:var(--accent-2);font-weight:800}
/* proceso */
.steps{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px;counter-reset:s}
.step{border-top:2px solid var(--accent);padding-top:16px}
.step b{display:block;font-family:var(--display);font-size:19px;margin-bottom:6px}
.step b::before{counter-increment:s;content:counter(s) ". ";color:var(--accent-2)}
.step p{color:var(--muted);font-size:14.5px}
@media (max-width:860px){.steps{grid-template-columns:1fr 1fr}}
@media (max-width:520px){.steps{grid-template-columns:1fr}}
/* faq */
.faq{max-width:780px;display:flex;flex-direction:column;gap:10px}
details{border:1px solid var(--line);border-radius:14px;background:var(--bg);padding:0 18px}
summary{cursor:pointer;list-style:none;padding:16px 0;font-weight:600;display:flex;justify-content:space-between;gap:12px}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";color:var(--accent-2);font-size:20px;line-height:1}
details[open] summary::after{content:"–"}
details p{color:var(--muted);padding-bottom:16px;font-size:15px}
/* contacto */
.contact{display:grid;grid-template-columns:1fr 1.2fr;gap:40px;align-items:start}
@media (max-width:860px){.contact{grid-template-columns:1fr}}
.form{display:grid;grid-template-columns:1fr 1fr;gap:14px;background:var(--bg);border:1px solid var(--line);border-radius:var(--r);padding:24px}
.form .full{grid-column:1/-1}
@media (max-width:520px){.form{grid-template-columns:1fr}}
.form label{display:flex;flex-direction:column;gap:6px;font-size:13px;font-weight:600;color:var(--muted)}
.form input,.form select,.form textarea{background:var(--bg3);border:1px solid var(--line2);border-radius:10px;padding:11px 12px;color:var(--fg);font:inherit;font-size:15px;width:100%}
.form textarea{min-height:120px;resize:vertical}
.form input:focus,.form select:focus,.form textarea:focus{outline:none;border-color:var(--accent)}
.form-msg{font-size:14px;color:var(--muted)}
.socials{display:flex;gap:10px;flex-wrap:wrap;margin-top:20px}
footer{border-top:1px solid var(--line);padding-block:28px;color:var(--muted2);font-size:13px}
footer .wrap{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
footer a{color:var(--muted)}
"""

def build_page():
    secs = "".join(f'<span>{n}</span>' for n, _, _ in SECTORES) + "<span>Restaurantes</span><span>Pymes en general</span>"
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
<meta name="description" content="Webs, asistentes de WhatsApp con IA, CRM y redes sociales para pymes en España y México. Precios claros, qué incluye cada uno y qué pagas aparte, con demos que puedes probar."/>
<meta property="og:title" content="Servicios digitales para pymes · Melina Rivera"/>
<meta property="og:description" content="Precios claros, demos que puedes probar y sin letra pequeña."/>
<meta property="og:image" content="../img/thumbs/asistente-whatsapp.jpg"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,500&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&display=swap" rel="stylesheet"/>
<script src="https://cdn.jsdelivr.net/npm/lucide@0.469.0/dist/umd/lucide.min.js"></script>
<style>{CSS}</style>
</head>
<body>
<header class="nav"><div class="wrap nav-in">
  <a class="brand" href="#inicio"><img src="../img/MR_logo.png" alt=""/>Melina Rivera</a>
  <nav class="nav-links" aria-label="Secciones">
    <a href="#servicios">Servicios</a><a href="#incluye">Qué incluye</a><a href="#demos">Demos</a><a href="#ejemplos">Ejemplos</a><a href="#contacto">Contacto</a>
  </nav>
  <div class="toggle" role="group" aria-label="País y moneda">
    <button type="button" data-country="es" class="on" id="c-es">🇪🇸 España €</button>
    <button type="button" data-country="mx" id="c-mx">🇲🇽 México MXN</button>
  </div>
</div></header>

<main id="inicio">
  <section class="hero"><div class="wrap">
    <p class="eyebrow">Webs · IA · CRM · Redes</p>
    <h1>Lo digital de tu negocio, <em>sin letra pequeña</em></h1>
    <p class="lead">Webs, asistentes de WhatsApp con IA, CRM y redes sociales para pymes de España y México. Cada servicio tiene precio de partida, qué incluye, qué pagas aparte y ejemplos que puedes abrir.</p>
    <div class="actions">
      <a class="btn primary" href="#servicios"><i data-lucide="tag"></i>Ver precios</a>
      <a class="btn ghost" href="#demos"><i data-lucide="play"></i>Probar las demos</a>
    </div>
    <div class="sectors" aria-label="Sectores">{secs}</div>
    <p class="tax js-tax">Precios orientativos sin IVA (21 %). Presupuesto cerrado tras una llamada gratuita de 20 minutos.</p>
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
    <p class="note js-note">Importes orientativos de octubre de 2026 (España, sin IVA). En México las tarifas de Meta y de los proveedores son distintas: te las detallo en el presupuesto.</p>
  </div></section>

  <section class="band" id="packs"><div class="wrap">
    <div class="head"><p class="eyebrow">Packs</p><h2>Combina y <em>ahorra</em></h2><p class="lead">Lo que más piden las pymes, en un solo precio.</p></div>
    <div class="pack-grid">{''.join(pack_card(p) for p in PACKS)}
    </div>
  </div></section>

  <section id="demos"><div class="wrap">
    <div class="head"><p class="eyebrow">Demos interactivas</p><h2>Pruébalo como si fuera <em>tu negocio</em></h2>
      <p class="lead">Funcionan en el móvil, con datos ficticios.</p></div>
    <div class="demo-grid">
      <article class="demo"><img src="../img/thumbs/asistente-whatsapp.jpg" alt="Demo del asistente de WhatsApp" loading="lazy"/>
        <div class="demo-body"><h3>Asistente de WhatsApp con IA</h3>
          <p>Escríbele como un cliente: pide cita en un centro de estética o una primera consulta en una consultoría de extranjería. Verás cómo rellena la ficha del CRM, programa recordatorios y lo que cuesta cada conversación.</p>
          <div class="actions"><a class="btn primary" href="../demos/asistente-whatsapp/#estetica"><i data-lucide="play"></i>Estética</a><a class="btn ghost" href="../demos/asistente-whatsapp/#extranjeria"><i data-lucide="play"></i>Extranjería</a></div></div></article>
      <article class="demo"><img src="../img/thumbs/crm-restaurante.jpg" alt="Demo del CRM para restaurantes" loading="lazy"/>
        <div class="demo-body"><h3>CRM para restaurantes</h3>
          <p>Reservas por turnos, fichas con los 14 alérgenos, consentimiento RGPD, clientes VIP y dormidos, campañas por WhatsApp y exportación a Excel.</p>
          <div class="actions"><a class="btn primary" href="../demos/crm-restaurante/"><i data-lucide="play"></i>Abrir la demo</a></div></div></article>
    </div>
  </div></section>

  <section class="band" id="ejemplos"><div class="wrap">
    <div class="head"><p class="eyebrow">Ejemplos reales</p><h2>Proyectos que puedes <em>abrir ahora</em></h2>
      <p class="lead">Solo enlazo lo que está publicado y funcionando.</p></div>
    <div class="ej-grid">{''.join(ejemplo_card(e) for e in EJEMPLOS)}
    </div>
  </div></section>

  <section id="sectores"><div class="wrap">
    <div class="head"><p class="eyebrow">Redes y reputación</p><h2>Pensado para <em>negocios de barrio y despachos</em></h2>
      <p class="lead">Así adapto las redes, Google y WhatsApp a cada tipo de negocio.</p></div>
    <div class="sec-grid">{''.join(f'<article class="sec"><span class="svc-icon"><i data-lucide="{ic}"></i></span><h3>{n}</h3><ul>{"".join(f"<li>{b}</li>" for b in bs)}</ul></article>' for n, ic, bs in SECTORES)}
    </div>
  </div></section>

  <section class="band"><div class="wrap">
    <div class="head"><p class="eyebrow">Cómo trabajo</p><h2>De la llamada al <em>lanzamiento</em></h2></div>
    <div class="steps">
      <div class="step"><b>Llamada gratuita</b><p>20 minutos para entender tu negocio y qué te quita tiempo.</p></div>
      <div class="step"><b>Presupuesto cerrado</b><p>Qué incluye, qué pagas aparte y plazos, por escrito.</p></div>
      <div class="step"><b>Construcción</b><p>Te enseño avances cada semana para que decidas sobre la marcha.</p></div>
      <div class="step"><b>Lanzamiento y formación</b><p>Lo publicamos, te enseño a usarlo y quedo de soporte.</p></div>
    </div>
  </div></section>

  <section><div class="wrap">
    <div class="head"><p class="eyebrow">Preguntas frecuentes</p><h2>Lo que suelen <em>preguntarme</em></h2></div>
    <div class="faq">{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)}</div>
  </div></section>

  <section class="band" id="contacto"><div class="wrap contact">
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

<footer><div class="wrap"><span>© 2026 Melina Rivera · Madrid</span><span><a href="../">Portafolio</a> · <a href="{IG}" target="_blank" rel="noopener">Instagram</a></span></div></footer>

<script>
(function(){{
  if (window.lucide) lucide.createIcons();
  var TAX = {{ es:'Precios orientativos sin IVA (21 %). Presupuesto cerrado tras una llamada gratuita de 20 minutos.', mx:'Precios orientativos + IVA (16 %). Presupuesto cerrado tras una llamada gratuita de 20 minutos.' }};
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
    open(os.path.join(ROOT, "servicios", "index.html"), "w", encoding="utf-8").write(page)

# ───────────────────────── resumen en el portafolio ─────────────────────────
def build_portfolio_summary():
    cards = "".join(f"""
        <a class="svc-mini fade-in" href="servicios/#srv-{s['id']}">
          <span class="service-icon" style="margin:0 0 .8rem"><i data-lucide="{s['icon']}" class="lucide" style="width:1.2rem;height:1.2rem"></i></span>
          <span class="svc-mini-name">{s['name']}</span>
          <span class="svc-mini-price">{P(s['eur'], s['mxn'])}</span>
        </a>""" for s in S)
    block = f"""  <section id="servicios">
    <div class="container">
      <div class="text-center mb-5 fade-in">
        <div class="section-chip mx-auto"><i data-lucide="tag" class="lucide"></i> Servicios y precios</div>
        <h2 class="section-title">Todo lo digital de tu negocio,<br><em>en un mismo sitio</em></h2>
        <p style="color:var(--muted);font-size:.95rem;max-width:560px;margin:.8rem auto 0;line-height:1.8">Precios de partida, qué incluye cada servicio y qué pagas aparte, con demos para probar.</p>
        <div class="country-toggle" role="group" aria-label="País">
          <button type="button" data-country="es" class="active">🇪🇸 España · €</button>
          <button type="button" data-country="mx">🇲🇽 México · MXN</button>
        </div>
        <div class="tax-note js-tax">Precios orientativos sin IVA (21 %).</div>
      </div>
      <div class="svc-mini-grid">{cards}
      </div>
      <p class="text-center fade-in" style="margin-top:2.5rem">
        <a href="servicios/" class="btn-main" style="display:inline-flex">Ver servicios, qué incluyen y packs <i data-lucide="arrow-right" class="lucide"></i></a>
      </p>
    </div>
  </section>

"""
    p = os.path.join(ROOT, "index.html")
    s = open(p, encoding="utf-8").read()
    i = s.index('  <section id="servicios">'); j = s.index("  <!-- ===== CONTACTO ===== -->", i)
    s = s[:i] + block + s[j:]
    open(p, "w", encoding="utf-8").write(s)

if __name__ == "__main__":
    build_page()
    build_portfolio_summary()
    print("ok")
