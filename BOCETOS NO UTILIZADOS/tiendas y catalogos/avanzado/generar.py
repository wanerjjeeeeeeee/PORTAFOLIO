# -*- coding: utf-8 -*-
"""
Generador de bocetos de catálogo (misma estructura que la tienda Ciriaco Makeup Bag).
Cada rubro es un diccionario en RUBROS: cambia los datos, ejecuta `python generar.py`
y se crea un archivo .html por rubro (más un index.html que los enlaza).
"""
import html, os

ICONOS = {
    "search": '<circle cx="11" cy="11" r="6"/><path d="M16 16l5 5"/>',
    "heart": '<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/>',
    "cart": '<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M3 4h2l2.5 11h11L21 7H6"/>',
    "chat": '<path d="M4 20l1.3-4.2A8 8 0 1 1 8.4 18.8L4 20z"/><path d="M9 10h6M9 13h4"/>',
    "shield": '<path d="M12 3l7 3v5c0 5-3 8-7 10-4-2-7-5-7-10V6z"/><path d="M9 12l2 2 4-4"/>',
    "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/>',
}

def ico(nombre):
    return '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-%s"/></svg>' % nombre

CSS = """
:root{--p:__P__;--a:__A__;--s:__S__;--bg:__BG__;--t:__T__;--r:16px;--fh:__FH__}
*{box-sizing:border-box}
html,body{margin:0;max-width:100%;overflow-x:clip}
body{font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;color:var(--t);background:var(--bg)}
h1,h2,h3,p,ul,ol{margin:0}ul,ol{padding:0;list-style:none}
h1,h2,h3{font-family:var(--fh);line-height:1.1;color:var(--p)}
a{color:inherit}
.i{width:1.3em;height:1.3em;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;flex:none}
.w{width:100%;max-width:1100px;margin-inline:auto;padding-inline:1rem}
.aviso{background:#111;color:#ffd;text-align:center;font-size:.75rem;padding:.3rem}
.top{background:var(--p);color:#fff;text-align:center;padding:.55rem 1rem;font-weight:800;letter-spacing:.12em;font-size:.85rem}
header{position:sticky;top:0;z-index:5;background:#fff;box-shadow:0 1px 0 rgba(0,0,0,.1)}
.bar{display:flex;flex-wrap:wrap;align-items:center;gap:.6rem;padding:.6rem 0}
.logo{display:flex;align-items:center;gap:.55rem;margin-right:auto;font:700 1.3rem var(--fh);color:var(--p);text-decoration:none}
.logo b{display:grid;place-items:center;width:46px;height:46px;border-radius:50%;background:var(--p);color:#fff;font-size:1.3rem}
.buscar{order:3;flex:1 1 100%;min-width:0;display:flex;height:44px;border:2px solid var(--p);border-radius:999px;overflow:hidden;background:#fff}
.buscar span{display:flex;align-items:center;padding:0 .8rem;background:var(--s);color:var(--p);font-weight:700;font-size:.8rem;white-space:nowrap}
.buscar input{flex:1;width:0;min-width:0;border:0;padding:0 .7rem;font:inherit;font-size:.9rem}
.buscar i{display:grid;place-items:center;width:48px;background:var(--p);color:#fff}
.acc{display:flex;gap:.3rem}
.acc a{position:relative;display:grid;place-items:center;width:44px;height:44px;color:var(--p)}
.acc em{position:absolute;top:2px;right:0;min-width:18px;height:18px;border-radius:9px;background:var(--a);color:#fff;font:700 .7rem/18px system-ui;text-align:center}
nav{display:flex;flex-wrap:wrap;gap:.3rem 1.2rem;padding:0 0 .6rem;font-weight:600;font-size:.9rem}
.hero{padding:2.2rem 0 3.6rem;background:var(--patron),linear-gradient(180deg,var(--s),var(--bg));border-radius:0 0 40px 40px}
.hero .w{display:grid;gap:1.6rem;align-items:center}
.hero h1{font-size:clamp(2.3rem,9vw,4.2rem)}
.hero p{margin:.8rem 0 1.2rem;font-size:1.15rem;max-width:34ch}
.btns{display:flex;flex-wrap:wrap;gap:.7rem}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:.5rem;min-height:48px;padding:0 1.4rem;border:2px solid var(--p);border-radius:999px;background:var(--p);color:#fff;font-weight:800;text-decoration:none;box-shadow:4px 4px 0 var(--a)}
.btn.o{background:#fff;color:var(--p)}
.foto{display:grid;place-items:center;aspect-ratio:4/3;padding:.5rem;border:2px dashed var(--a);border-radius:var(--r);background:rgba(255,255,255,.75);color:var(--p);font-weight:700;font-size:.85rem;text-align:center}
.conf{display:grid;gap:.8rem;margin-top:-2.4rem;position:relative}
.conf li{display:flex;align-items:center;gap:.9rem;padding:1rem;background:#fff;border:2px solid var(--s);border-radius:20px;box-shadow:0 8px 24px rgba(0,0,0,.1)}
.conf .i{width:2.6rem;height:2.6rem;padding:.6rem;border-radius:50%;background:var(--p);color:#fff}
.conf strong{display:block;color:var(--p)}.conf span{font-size:.92rem}
.sec{padding-block:2.2rem}.sec>h2,.sec .cab h2{font-size:clamp(1.6rem,5vw,2.3rem);margin-bottom:1.1rem}
.sec>h2::after,.sec .cab h2::after{content:"✦ ✦ ✦";display:block;margin-top:.3rem;font:.7rem system-ui;letter-spacing:.5em;color:var(--a)}
.cats{display:grid;grid-template-columns:repeat(2,1fr);gap:1rem}
.cats li{text-align:center;font-weight:800;color:var(--p)}
.cats .foto{aspect-ratio:1;border-radius:50%;margin-bottom:.5rem}
.g{display:grid;gap:1rem}.g3{grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}.g4{grid-template-columns:repeat(2,1fr)}
.card{position:relative;display:flex;flex-direction:column;gap:.5rem;padding:.8rem;background:#fff;border:1px solid rgba(0,0,0,.1);border-radius:var(--r)}
.card h3{font-size:1.15rem}.card ul{font-size:.92rem;display:grid;gap:.2rem}
.card li::before{content:"✓ ";color:var(--a);font-weight:800}
.precio{font-weight:800;color:var(--p);font-size:1.1rem}
.tag{position:absolute;top:1.2rem;left:1.2rem;z-index:1;padding:.15rem .7rem;border-radius:999px;background:var(--a);color:#fff;font-size:.75rem;font-weight:800}
.card .btn{width:100%;min-height:42px;box-shadow:none;margin-top:auto}
.band{background:var(--s);padding:2.2rem 0;margin-block:1rem}
.cab{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:.5rem}
.chips{display:flex;flex-wrap:wrap;gap:.5rem;margin-bottom:1rem}
.chips span{padding:.4rem 1rem;border:1.5px solid var(--p);border-radius:999px;font-weight:800;font-size:.9rem;color:var(--p);background:#fff}
.chips span:first-child{background:var(--p);color:#fff}
.pasos{display:grid;gap:1rem;counter-reset:n}
.pasos li{padding:1.2rem;text-align:center;background:#fff;border:2px solid var(--s);border-radius:20px}
.pasos li::before{counter-increment:n;content:counter(n);display:grid;place-items:center;width:2.6rem;height:2.6rem;margin:0 auto .6rem;border-radius:50%;background:var(--p);color:#fff;font:700 1.3rem var(--fh)}
.pasos h3{font-size:1.1rem;margin-bottom:.2rem}
.contacto{display:grid;gap:1.2rem;padding:1.2rem;background:#fff;border:2px solid var(--p);border-radius:22px}
.burbuja{padding:.8rem 1rem;background:#d9fdd3;color:#1f2c34;border-radius:14px 14px 4px 14px;font-size:.92rem}
.prev{padding:1rem;background:var(--s);border-radius:18px}.prev>p{font-weight:800;color:var(--p);margin:.2rem 0 .6rem}
form{display:grid;gap:.8rem}
label{display:block;font-weight:800;color:var(--p);margin-bottom:.25rem}
.campo{width:100%;min-height:46px;padding:.6rem 1rem;border:2px solid var(--p);border-radius:14px;background:#fff;font:inherit}
footer{margin-top:2rem;padding:2rem 0 5rem;background:var(--p);color:#fff}
footer .w{display:grid;gap:1rem;grid-template-columns:repeat(2,1fr)}footer h3{color:var(--a);font-size:1rem;margin-bottom:.4rem}
footer p{font-size:.92rem;opacity:.9}
.wa{position:fixed;right:14px;bottom:14px;z-index:6;display:flex;align-items:center;gap:.4rem;height:52px;padding:0 16px;border-radius:999px;background:#167a42;color:#fff;font-weight:800;text-decoration:none;box-shadow:0 4px 14px rgba(0,0,0,.3)}
@media(min-width:640px){.cats{grid-template-columns:repeat(4,1fr)}.conf{grid-template-columns:repeat(3,1fr)}.pasos{grid-template-columns:repeat(3,1fr)}}
@media(min-width:760px){.g4{grid-template-columns:repeat(4,1fr)}}
@media(min-width:900px){.hero .w{grid-template-columns:1.1fr 1fr}.buscar{order:0;flex:1;margin-inline:1rem}.contacto{grid-template-columns:5fr 7fr;padding:2rem;gap:2rem}footer .w{grid-template-columns:2fr 1fr 1fr 1fr}}
"""

PLANTILLA = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__NOMBRE__ | Boceto de catálogo</title>
<style>__CSS__</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true">__SPRITE__</svg>
<div class="aviso">BOCETO · textos, precios y fotos de ejemplo</div>
<div class="top">__SLOGAN__</div>

<header><div class="w">
  <div class="bar">
    <a class="logo" href="#"><b>__INICIAL__</b>__NOMBRE__</a>
    <div class="buscar"><span>Todas ▾</span><input placeholder="__BUSCAR__" aria-label="Buscar"><i>__I_SEARCH__</i></div>
    <div class="acc"><a href="#" aria-label="Favoritos">__I_HEART__<em>0</em></a><a href="#" aria-label="__CARRITO__">__I_CART__<em>0</em></a></div>
  </div>
  <nav>__NAV__</nav>
</div></header>

<section class="hero"><div class="w">
  <div><h1>__HERO_T__</h1><p>__HERO_P__</p>
    <div class="btns"><a class="btn" href="#catalogo">__CTA1__</a><a class="btn o" href="#contacto">__CTA2__</a></div></div>
  <div class="foto">Foto o video de portada</div>
</div></section>

<ul class="w conf">__CONF__</ul>

<section class="w sec"><h2>Explora por categoría</h2><ul class="cats">__CATS__</ul></section>

<div class="band"><section class="w"><div class="cab"><h2>__DEST_T__</h2></div><div class="g g3">__DEST__</div></section></div>

<section class="w sec" id="catalogo"><div class="cab"><h2>Todo el catálogo</h2></div>
  <div class="chips"><span>Todos</span>__CHIPS__</div>
  <div class="g g4">__ITEMS__</div></section>

<section class="w sec"><h2>Pide en tres pasos</h2><ol class="pasos">__PASOS__</ol></section>

<section class="w sec" id="contacto"><div class="contacto">
  <div class="prev"><h2>Escríbenos</h2><p>Llena el formulario y mira cómo va tu mensaje.</p>
    <div class="burbuja">__BURBUJA__</div></div>
  <form onsubmit="return false">
    <div><label>Tu nombre</label><input class="campo" placeholder="Nombre"></div>
    <div><label>Motivo</label><select class="campo">__MOTIVOS__</select></div>
    <div><label>Tu selección</label><div class="campo" style="color:#777">Aquí aparece lo que elegiste</div></div>
    <div><label>Mensaje (opcional)</label><textarea class="campo" rows="3"></textarea></div>
    <a class="btn" href="#">__I_CHAT__ Enviar por WhatsApp</a>
  </form>
</div></section>

<footer><div class="w">
  <div><h3>__NOMBRE__</h3><p>__SLOGAN_PIE__</p></div>
  <div><h3>Tienda</h3><p>Catálogo<br>Destacados</p></div>
  <div><h3>Ayuda</h3><p>Cómo pedir<br>Preguntas</p></div>
  <div><h3>Contacto</h3><p>Formulario<br>Redes</p></div>
</div></footer>
<a class="wa" href="#contacto">__I_CHAT__ WhatsApp</a>
</body>
</html>
"""

def tarjeta_dest(n, precio, puntos, etiqueta, cta):
    lis = "".join("<li>%s</li>" % html.escape(p) for p in puntos)
    return ('<article class="card"><span class="tag">%s</span><div class="foto">Foto</div><h3>%s</h3><ul>%s</ul>'
            '<p class="precio">%s</p><a class="btn" href="#">%s</a></article>') % tuple(html.escape(x) if x is not lis else x for x in (etiqueta, n)) + "" if False else \
           ('<article class="card"><span class="tag">%s</span><div class="foto">Foto</div><h3>%s</h3><ul>%s</ul><p class="precio">%s</p><a class="btn" href="#">%s</a></article>'
            % (html.escape(etiqueta), html.escape(n), lis, html.escape(precio), html.escape(cta)))

def tarjeta_item(n, precio, cta):
    return ('<article class="card"><div class="foto">Foto</div><h3>%s</h3><p class="precio">%s</p><a class="btn" href="#">%s</a></article>'
            % (html.escape(n), html.escape(precio), html.escape(cta)))

def generar(slug, d):
    e = html.escape
    sprite = "".join('<symbol id="i-%s" viewBox="0 0 24 24">%s</symbol>' % (k, v) for k, v in ICONOS.items())
    css = CSS.replace("__P__", d["p"]).replace("__A__", d["a"]).replace("__S__", d["s"]).replace("__BG__", d["bg"]).replace("__T__", d["t"]).replace("__FH__", d["fh"])
    css = ":root{--patron:%s}" % d["patron"] + css
    cta = d["cta_item"]
    datos = {
        "__NOMBRE__": e(d["nombre"]), "__CSS__": css, "__SPRITE__": sprite, "__SLOGAN__": e(d["slogan"]),
        "__INICIAL__": e(d["nombre"][0]), "__BUSCAR__": e(d["buscar"]), "__CARRITO__": e(d["carrito"]),
        "__I_SEARCH__": ico("search"), "__I_HEART__": ico("heart"), "__I_CART__": ico("cart"), "__I_CHAT__": ico("chat"),
        "__NAV__": "".join('<a href="#">%s</a>' % e(x) for x in d["nav"]),
        "__HERO_T__": e(d["hero_t"]), "__HERO_P__": e(d["hero_p"]), "__CTA1__": e(d["cta1"]), "__CTA2__": e(d["cta2"]),
        "__CONF__": "".join('<li>%s<div><strong>%s</strong><span>%s</span></div></li>' % (ico(i), e(t), e(x)) for i, t, x in d["conf"]),
        "__CATS__": "".join('<li><div class="foto">Foto</div>%s</li>' % e(c) for c in d["cats"]),
        "__DEST_T__": e(d["dest_t"]),
        "__DEST__": "".join(tarjeta_dest(*x, cta) for x in d["dest"]),
        "__CHIPS__": "".join("<span>%s</span>" % e(c) for c in d["cats"]),
        "__ITEMS__": "".join(tarjeta_item(n, p, cta) for n, p in d["items"]),
        "__PASOS__": "".join("<li><h3>%s</h3><p>%s</p></li>" % (e(t), e(x)) for t, x in d["pasos"]),
        "__BURBUJA__": "<br>".join(e(l) for l in d["burbuja"]),
        "__MOTIVOS__": "".join("<option>%s</option>" % e(m) for m in ["Selecciona un motivo"] + d["motivos"]),
        "__SLOGAN_PIE__": e(d["slogan"].capitalize()),
    }
    salida = PLANTILLA
    for k in sorted(datos, key=len, reverse=True):
        salida = salida.replace(k, datos[k])
    return salida

RUBROS = {
 "reposteria": dict(nombre="Dulce Encanto", rubro="Repostería y pasteles por encargo", slogan="PASTELES Y DULCES HECHOS CON AMOR",
   p="#6b3a2e", a="#e58fa6", s="#fde8ec", bg="#fffaf8", t="#3b2a26", fh="Georgia,'Times New Roman',serif",
   patron="radial-gradient(circle at 1px 1px,rgba(229,143,166,.4) 2px,transparent 2.5px) 0 0/22px 22px",
   buscar="Buscar pasteles…", carrito="Mi pedido", nav=["Inicio","Pasteles","Cupcakes","Encargos","Contacto"],
   hero_t="Pasteles para cada celebración", hero_p="Elige sabor, tamaño y decoración. Pide con anticipación por WhatsApp.",
   cta1="Ver pasteles", cta2="Hacer un encargo", cta_item="Pedir",
   conf=[("shield","Hecho por encargo","Confirmamos fecha y detalles contigo"),("chat","Atención por WhatsApp","Te ayudamos a elegir sabor y tamaño"),("check","Preparado para tu fecha","Coordinamos la entrega contigo")],
   cats=["Pasteles","Cupcakes","Postres","Bocaditos"], dest_t="Lo más pedido",
   dest=[("Pastel de cumpleaños","RD$ 1,800",["Bizcocho a elegir","Relleno y cobertura","Decoración temática"],"Más pedido"),
         ("Caja de 12 cupcakes","RD$ 900",["Sabores surtidos","Decoración sencilla","Caja de regalo"],"Nuevo"),
         ("Mesa de dulces","RD$ 3,500",["Variedad de postres","Para 20 personas","Montaje incluido"],"Para fiestas")],
   items=[("Pastel de chocolate","RD$ 1,600"),("Pastel de vainilla","RD$ 1,500"),("Pastel de zanahoria","RD$ 1,700"),("Tres leches","RD$ 1,400"),
          ("Cheesecake","RD$ 1,800"),("Cupcakes x6","RD$ 500"),("Galletas decoradas","RD$ 650"),("Brownies x9","RD$ 600")],
   pasos=[("Elige tu pastel","Mira sabores y tamaños"),("Cuéntanos la fecha","Para reservar tu encargo"),("Confirma por WhatsApp","Se abre el mensaje ya escrito")],
   burbuja=["Hola, soy María.","Motivo: Hacer un encargo","- 1 x Pastel de chocolate (RD$ 1,600)","Total: RD$ 1,600"],
   motivos=["Hacer un encargo","Consultar sabores","Cotizar una fiesta","Otro motivo"]),
 "boutique": dict(nombre="Moda Aurora", rubro="Tienda de ropa y accesorios", slogan="TU ESTILO, TU HISTORIA",
   p="#1d1d1f", a="#c9a24d", s="#f4eee3", bg="#fbf9f5", t="#2a2a2a", fh="Georgia,'Times New Roman',serif",
   patron="repeating-linear-gradient(135deg,rgba(201,162,77,.2) 0 2px,transparent 2px 18px)",
   buscar="Buscar prendas…", carrito="Mi bolsa", nav=["Inicio","Mujer","Hombre","Accesorios","Contacto"],
   hero_t="Ropa que cuenta tu estilo", hero_p="Nuevas llegadas cada semana. Elige tu talla y pide por WhatsApp.",
   cta1="Ver colección", cta2="Escribir por WhatsApp", cta_item="Agregar",
   conf=[("shield","Compra confirmada","Verificamos talla y disponibilidad contigo"),("chat","Asesoría personal","Te ayudamos a combinar tu outfit"),("check","Nuevas llegadas","Piezas seleccionadas cada semana")],
   cats=["Vestidos","Blusas","Pantalones","Accesorios"], dest_t="Nuevas llegadas",
   dest=[("Conjunto casual","RD$ 2,200",["Blusa y pantalón","Tallas S a XL","Varios colores"],"Nuevo"),
         ("Vestido de fiesta","RD$ 3,400",["Tela ligera","Tallas S a L","Con forro"],"Más vendido"),
         ("Set de accesorios","RD$ 1,100",["Collar y aretes","Cartera mini","Caja de regalo"],"Oferta")],
   items=[("Blusa de lino","RD$ 1,200"),("Pantalón palazzo","RD$ 1,500"),("Vestido midi","RD$ 2,400"),("Jeans clásico","RD$ 1,800"),
          ("Falda plisada","RD$ 1,300"),("Cartera mini","RD$ 1,600"),("Cinturón de cuero","RD$ 700"),("Lentes de sol","RD$ 900")],
   pasos=[("Elige tu pieza","Mira la colección"),("Indica tu talla","Y el color que prefieres"),("Confirma por WhatsApp","Se abre el mensaje ya escrito")],
   burbuja=["Hola, soy Ana.","Motivo: Hacer un pedido","- 1 x Vestido midi, talla M (RD$ 2,400)","Total: RD$ 2,400"],
   motivos=["Hacer un pedido","Consultar disponibilidad","Cotizar por mayor","Otro motivo"]),
 "barberia": dict(nombre="Corte Fino", rubro="Barbería y servicios de belleza", slogan="ESTILO Y PRECISIÓN EN CADA CORTE",
   p="#14243b", a="#c77d3a", s="#e9eef5", bg="#f7f9fc", t="#1c2533", fh="'Trebuchet MS',Arial,sans-serif",
   patron="linear-gradient(rgba(20,36,59,.07) 1px,transparent 1px) 0 0/24px 24px,linear-gradient(90deg,rgba(20,36,59,.07) 1px,transparent 1px) 0 0/24px 24px",
   buscar="Buscar servicios…", carrito="Mi reserva", nav=["Inicio","Servicios","Paquetes","Galería","Contacto"],
   hero_t="Tu mejor versión, en nuestra silla", hero_p="Reserva tu cita, elige tu servicio y evita esperas.",
   cta1="Ver servicios", cta2="Reservar cita", cta_item="Reservar",
   conf=[("check","Citas con horario","Reserva tu turno y evita esperas"),("shield","Higiene y cuidado","Herramientas limpias en cada servicio"),("chat","Reserva por WhatsApp","Respuesta directa del barbero")],
   cats=["Cortes","Barba","Cejas","Paquetes"], dest_t="Servicios más pedidos",
   dest=[("Corte + barba","RD$ 700",["Corte a elección","Perfilado de barba","Toalla caliente"],"Más pedido"),
         ("Corte clásico","RD$ 400",["Tijera o máquina","Lavado incluido","Peinado final"],"Clásico"),
         ("Padre e hijo","RD$ 1,000",["Dos cortes","Mismo horario","Peinado final"],"Paquete")],
   items=[("Corte clásico","RD$ 400"),("Corte degradado","RD$ 450"),("Arreglo de barba","RD$ 300"),("Perfilado de cejas","RD$ 150"),
          ("Tinte de barba","RD$ 500"),("Mascarilla facial","RD$ 350"),("Corte infantil","RD$ 300"),("Lavado y peinado","RD$ 250")],
   pasos=[("Elige tu servicio","Uno o varios"),("Escoge día y hora","Según disponibilidad"),("Confirma por WhatsApp","Se abre el mensaje ya escrito")],
   burbuja=["Hola, soy Luis.","Motivo: Reservar una cita","- 1 x Corte + barba (RD$ 700)","Día y hora: sábado, 3:00 p. m."],
   motivos=["Reservar una cita","Consultar precios","Cotizar un evento","Otro motivo"]),
 "tecnologia": dict(nombre="TecnoPlus", rubro="Accesorios de celular y tecnología", slogan="ACCESORIOS QUE TU CELULAR NECESITA",
   p="#0b3d91", a="#00a6d6", s="#e6f1fb", bg="#f5f9fe", t="#14233b", fh="system-ui,-apple-system,'Segoe UI',Arial,sans-serif",
   patron="radial-gradient(rgba(0,166,214,.3) 1.5px,transparent 2px) 0 0/26px 26px",
   buscar="Buscar accesorios…", carrito="Mi carrito", nav=["Inicio","Fundas","Cargadores","Audio","Contacto"],
   hero_t="Todo para tu celular en un solo lugar", hero_p="Fundas, cargadores y audífonos. Dinos tu modelo y pide por WhatsApp.",
   cta1="Ver accesorios", cta2="Consultar mi modelo", cta_item="Comprar",
   conf=[("shield","Compra confirmada","Verificamos compatibilidad con tu modelo"),("chat","Soporte por WhatsApp","Te ayudamos a elegir el accesorio"),("check","Productos revisados","Los revisamos antes de entregarlos")],
   cats=["Fundas","Cargadores","Audio","Protectores"], dest_t="Los más buscados",
   dest=[("Kit de carga rápida","RD$ 1,200",["Cargador de 20 W","Cable USB-C","Compatible con varios modelos"],"Más vendido"),
         ("Audífonos inalámbricos","RD$ 1,800",["Estuche de carga","Conexión Bluetooth","Varios colores"],"Nuevo"),
         ("Funda + protector","RD$ 650",["Funda antigolpes","Protector de pantalla","Para tu modelo"],"Combo")],
   items=[("Funda transparente","RD$ 350"),("Funda antigolpes","RD$ 450"),("Cargador de 20 W","RD$ 700"),("Cable USB-C","RD$ 300"),
          ("Audífonos con cable","RD$ 400"),("Audífonos Bluetooth","RD$ 1,500"),("Protector de pantalla","RD$ 250"),("Soporte para auto","RD$ 600")],
   pasos=[("Elige tu accesorio","Dinos el modelo de tu celular"),("Agrégalo al carrito","Revisa cantidades y total"),("Confirma por WhatsApp","Se abre el mensaje ya escrito")],
   burbuja=["Hola, soy Pedro.","Motivo: Hacer un pedido","- 1 x Kit de carga rápida (RD$ 1,200)","Modelo: Samsung A54"],
   motivos=["Hacer un pedido","Consultar compatibilidad","Cotizar por mayor","Otro motivo"]),
 "restaurante": dict(nombre="Sabor Criollo", rubro="Comida casera y pedidos a domicilio", slogan="COMIDA CASERA, HECHA CON SAZÓN",
   p="#9f2a1b", a="#f2a900", s="#fff1d6", bg="#fffaf0", t="#35231b", fh="Georgia,'Times New Roman',serif",
   patron="repeating-linear-gradient(45deg,rgba(242,169,0,.2) 0 10px,transparent 10px 20px)",
   buscar="Buscar platos…", carrito="Mi pedido", nav=["Inicio","Menú","Combos","Postres","Contacto"],
   hero_t="El sabor de casa, a un mensaje", hero_p="Mira el menú del día y haz tu pedido por WhatsApp.",
   cta1="Ver menú", cta2="Pedir ahora", cta_item="Pedir",
   conf=[("chat","Pedidos por WhatsApp","Confirmamos tu pedido y el tiempo"),("check","Menú del día","Cambia según la jornada"),("shield","Pago coordinado","Acordamos la forma de pago contigo")],
   cats=["Almuerzos","Frituras","Bebidas","Postres"], dest_t="Combos del día",
   dest=[("Combo del día","RD$ 450",["Plato principal","Acompañante","Bebida"],"Más pedido"),
         ("Combo familiar","RD$ 1,600",["4 platos","Ensalada","Jugo de 1 litro"],"Para compartir"),
         ("Picaderas","RD$ 1,200",["Variedad de frituras","Salsas","Para 6 personas"],"Para eventos")],
   items=[("Pollo guisado","RD$ 350"),("Arroz con habichuelas","RD$ 250"),("Pescado frito","RD$ 500"),("Mofongo","RD$ 450"),
          ("Chicharrón","RD$ 400"),("Tostones","RD$ 200"),("Jugo natural","RD$ 120"),("Flan","RD$ 150")],
   pasos=[("Elige tus platos","Mira el menú del día"),("Indica tu dirección","Y la hora que prefieres"),("Confirma por WhatsApp","Se abre el mensaje ya escrito")],
   burbuja=["Hola, soy Carla.","Motivo: Hacer un pedido","- 2 x Combo del día (RD$ 900)","Total: RD$ 900"],
   motivos=["Hacer un pedido","Pedir para un evento","Consultar el menú","Otro motivo"]),
}

if __name__ == "__main__":
    carpeta = os.path.dirname(os.path.abspath(__file__))
    for slug, datos in RUBROS.items():
        with open(os.path.join(carpeta, slug + ".html"), "w", encoding="utf-8") as f:
            f.write(generar(slug, datos))
    tarjetas = "".join('<a class="c" href="%s.html"><b>%s</b><span>%s</span></a>' % (s, html.escape(d["nombre"]), html.escape(d["rubro"])) for s, d in RUBROS.items())
    with open(os.path.join(carpeta, "index.html"), "w", encoding="utf-8") as f:
        f.write('<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Bocetos de catálogo</title>'
                '<style>body{font:16px/1.5 system-ui,Arial,sans-serif;margin:0;padding:2rem 1rem;background:#f6f6f8;color:#222}main{max-width:720px;margin:auto}h1{margin:0 0 .3rem}'
                '.c{display:block;margin:.8rem 0;padding:1rem 1.2rem;background:#fff;border:1px solid #ddd;border-radius:14px;text-decoration:none;color:inherit}'
                '.c:hover{border-color:#333}.c b{display:block;font-size:1.15rem}.c span{color:#555}</style></head><body><main>'
                '<h1>Bocetos de catálogo</h1><p>Misma estructura de la tienda Ciriaco Makeup Bag, en otros rubros. Abre cada uno:</p>' + tarjetas + '</main></body></html>')
    print("Listo:", ", ".join(RUBROS), "+ index.html")
