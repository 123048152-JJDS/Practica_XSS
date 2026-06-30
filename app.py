import os
from flask import Flask, request, render_template, make_response
from markupsafe import escape, Markup
from dotenv import load_dotenv

from db import db, init_db, Comentario

load_dotenv()

app = Flask(__name__)
init_db(app)


# ─────────────────────────────────────────────────────────────────────────
# RUTA PRINCIPAL — redirige al laboratorio vulnerable
# ─────────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    from flask import redirect, url_for
    return redirect(url_for("vulnerable"))


# ─────────────────────────────────────────────────────────────────────────
# 1. XSS REFLEJADO — VULNERABLE
# ─────────────────────────────────────────────────────────────────────────
@app.route("/vulnerable")
def vulnerable():
    query = request.args.get("q", "")

    # ❌ VULNERABLE: se marca como Markup (HTML seguro) sin haber
    # sanitizado el input. Esto desactiva el autoescape de Jinja2
    # a propósito, simulando un desarrollador que confía en el input.
    resultado_html = Markup(f"{query}") if query else ""

    return render_template(
        "vulnerable.html",
        title="Vulnerable",
        badge_text="⚠ VULNERABLE",
        badge_color="#dc3545",
        active="vuln",
        query_raw=query,
        resultado_html=resultado_html
    )


# ─────────────────────────────────────────────────────────────────────────
# 2. XSS REFLEJADO — SEGURO (mitigado)
# ─────────────────────────────────────────────────────────────────────────
@app.route("/seguro")
def seguro():
    raw = request.args.get("q", "")

    # ✅ SEGURO: escape() convierte < > " ' & en entidades HTML
    safe = str(escape(raw))

    resp = make_response(render_template(
        "seguro.html",
        title="Seguro",
        badge_text="✓ SEGURO",
        badge_color="#198754",
        active="seg",
        query_safe=safe,
        raw_input=repr(raw)
    ))

    # ✅ SEGURO: Headers de seguridad HTTP
    resp.headers["Content-Security-Policy"] = "default-src 'self'"
    resp.headers["X-XSS-Protection"] = "1; mode=block"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    return resp


# ─────────────────────────────────────────────────────────────────────────
# 3. XSS ALMACENADO — VULNERABLE
# ─────────────────────────────────────────────────────────────────────────
@app.route("/almacenado", methods=["GET", "POST"])
def almacenado():
    if request.method == "POST":
        autor = request.form.get("autor", "Anónimo") or "Anónimo"
        texto = request.form.get("texto", "")

        # ❌ VULNERABLE: el texto se guarda en PostgreSQL TAL CUAL llega,
        # sin sanitizar. SQLAlchemy ya protege contra SQL Injection al
        # usar parámetros internamente, PERO el contenido HTML/JS del
        # campo `texto` queda persistido sin escape, así que al
        # renderizarlo con |safe en la plantilla, el payload se ejecuta
        # para cada visitante — esto es XSS Almacenado real.
        nuevo = Comentario(autor=autor, texto=texto)
        db.session.add(nuevo)
        db.session.commit()

    # Se leen todos los comentarios de la base de datos, más recientes primero
    comentarios = Comentario.query.order_by(Comentario.fecha.desc()).all()

    # Se envuelve el texto en Markup para que Jinja2 NO lo escape
    # (de nuevo, a propósito, para que el ejemplo sea explotable)
    comentarios_view = [
        {"autor": c.autor, "texto_html": Markup(c.texto), "fecha": c.fecha}
        for c in comentarios
    ]

    return render_template(
        "almacenado.html",
        title="XSS Almacenado",
        badge_text="⚠ ALMACENADO (PostgreSQL)",
        badge_color="#fd7e14",
        active="alm",
        comentarios=comentarios_view
    )


# ─────────────────────────────────────────────────────────────────────────
# 4. XSS BASADO EN DOM — VULNERABLE (lado cliente, ver static/js/dom_vuln.js)
# ─────────────────────────────────────────────────────────────────────────
@app.route("/dom")
def dom():
    return render_template(
        "dom.html",
        title="XSS DOM",
        badge_text="⚙ DOM-Based",
        badge_color="#6f42c1",
        active="dom"
    )


# ─────────────────────────────────────────────────────────────────────────
# 5. REFERENCIA — Tabla de payloads y mitigaciones
# ─────────────────────────────────────────────────────────────────────────
@app.route("/info")
def info():
    return render_template(
        "info.html",
        title="Payloads",
        badge_text="📋 Referencia",
        badge_color="#0dcaf0",
        active="info"
    )


# ─────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  BlogApp XSS Lab — Práctica 5 Seguridad Informática")
    print("  UPQ — Grupo S-203")
    print("  Accede en: http://127.0.0.1:5000")
    print("=" * 55)
    app.run(debug=True, host="127.0.0.1", port=5000)
