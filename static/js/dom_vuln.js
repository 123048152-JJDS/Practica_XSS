/* ============================================================
   dom_vuln.js — Demostración de XSS basado en DOM
   Práctica 5 — Seguridad Informática — UPQ S-203

   Este script lee location.hash (lo que va después del #) y lo
   inserta en el DOM usando innerHTML, sin sanitizar.
   Como location.hash NUNCA se envía al servidor, este ataque
   ocurre completamente del lado del cliente.
   ============================================================ */

// ❌ VULNERABLE: innerHTML interpreta el string como HTML/JS
const name = location.hash ? location.hash.slice(1) : "Visitante";
document.getElementById('welcome').innerHTML = 'Hola, ' + decodeURIComponent(name);

/* ────────────────────────────────────────────────────────────
   VERSIÓN SEGURA (comentada con fines comparativos):

   const name = location.hash ? location.hash.slice(1) : "Visitante";
   document.getElementById('welcome').textContent = 'Hola, ' + decodeURIComponent(name);

   textContent trata el valor como texto plano, nunca como HTML,
   por lo que neutraliza cualquier intento de inyección.
   ──────────────────────────────────────────────────────────── */
