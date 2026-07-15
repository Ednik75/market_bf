# -*- coding: utf-8 -*-
"""Génère le dossier de soutenance PDF de Market BF."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, PageBreak, NextPageTemplate)

OUT = os.path.join(os.path.dirname(__file__), "Dossier_Soutenance_MarketBF.pdf")

# Palette (drapeau burkinabè adouci)
GREEN = HexColor("#166534")
GREEN_DARK = HexColor("#0e3d20")
RED = HexColor("#c0392b")
YELLOW = HexColor("#f0b429")
GREY = HexColor("#4b5563")
LIGHT = HexColor("#f0fdf4")
BORDER = HexColor("#d1d5db")

AUTHORS = "NITIEMA Martial  •  [Nom du binôme]"
TITLE = "Market BF — Marketplace locale du Burkina Faso"

styles = getSampleStyleSheet()
def S(name, **kw):
    kw.setdefault("fontName", "Helvetica")
    kw.setdefault("parent", styles["Normal"])
    st = ParagraphStyle(name, **kw)
    styles.add(st); return st

h1 = S("H1", fontName="Helvetica-Bold", fontSize=17, textColor=GREEN_DARK,
       spaceBefore=18, spaceAfter=10)
h2 = S("H2", fontName="Helvetica-Bold", fontSize=12.5, textColor=GREEN,
       spaceBefore=12, spaceAfter=6)
body = S("Body", fontSize=10.2, leading=14.5, alignment=TA_JUSTIFY, spaceAfter=6,
         textColor=HexColor("#1f2937"))
bullet = S("BulletX", parent=body, leftIndent=14, bulletIndent=4, spaceAfter=3)
small = S("Small", fontSize=8.5, textColor=GREY)
cell = S("Cell", fontSize=9, leading=12, textColor=HexColor("#1f2937"))
cellb = S("CellB", parent=cell, fontName="Helvetica-Bold", textColor=white)

def P(txt): return Paragraph(txt, body)
def B(txt): return Paragraph(txt, bullet, bulletText="•")
def H(txt): return Paragraph(txt, h1)
def H2(txt): return Paragraph(txt, h2)

def table(headers, rows, widths):
    data = [[Paragraph(h, cellb) for h in headers]] + \
           [[Paragraph(c, cell) for c in r] for r in rows]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GREEN),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT]),
        ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    t.spaceAfter = 10
    return t

# ---------------------------------------------------------------- mise en page
def on_cover(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(GREEN_DARK); canvas.rect(0, 0, w, h, fill=1, stroke=0)
    canvas.setFillColor(RED);    canvas.rect(0, h - 1.1*cm, w, 1.1*cm, fill=1, stroke=0)
    canvas.setFillColor(YELLOW); canvas.rect(0, h - 1.35*cm, w, 0.25*cm, fill=1, stroke=0)
    canvas.setFillColor(GREEN);  canvas.rect(0, 0, w, 1.1*cm, fill=1, stroke=0)

    canvas.setFillColor(white)
    canvas.setFont("Helvetica-Bold", 34)
    canvas.drawCentredString(w/2, h - 8.2*cm, "Market BF")
    canvas.setFont("Helvetica", 15)
    canvas.setFillColor(HexColor("#bbf7d0"))
    canvas.drawCentredString(w/2, h - 9.5*cm, "Marketplace locale et gestion commerciale")
    canvas.drawCentredString(w/2, h - 10.3*cm, "pour les commerces du Burkina Faso")

    canvas.setFillColor(YELLOW)
    canvas.setFont("Helvetica-Bold", 13)
    canvas.drawCentredString(w/2, h - 13*cm, "DOSSIER DE SOUTENANCE")

    canvas.setFillColor(white); canvas.setFont("Helvetica", 11.5)
    canvas.drawCentredString(w/2, h - 15.6*cm, "Application web full-stack — Node.js / Express • React • SQLite (Turso)")
    canvas.drawCentredString(w/2, h - 16.4*cm, "Déployée en production : https://marketbf.onrender.com")

    canvas.setFont("Helvetica", 12)
    canvas.drawCentredString(w/2, 5.6*cm, "Présenté par : %s" % AUTHORS)
    canvas.drawCentredString(w/2, 4.8*cm, "Juillet 2026")
    canvas.restoreState()

def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(GREEN); canvas.rect(0, h - 0.5*cm, w, 0.5*cm, fill=1, stroke=0)
    canvas.setFont("Helvetica", 8); canvas.setFillColor(GREY)
    canvas.drawString(2*cm, 1.05*cm, "Market BF — Dossier de soutenance")
    canvas.drawRightString(w - 2*cm, 1.05*cm, "Page %d" % (doc.page - 1))
    canvas.setStrokeColor(BORDER)
    canvas.line(2*cm, 1.35*cm, w - 2*cm, 1.35*cm)
    canvas.restoreState()

doc = BaseDocTemplate(OUT, pagesize=A4, title=TITLE, author=AUTHORS,
                      leftMargin=2*cm, rightMargin=2*cm,
                      topMargin=1.8*cm, bottomMargin=1.8*cm)
frame = Frame(2*cm, 1.8*cm, A4[0]-4*cm, A4[1]-3.6*cm, id="main")
doc.addPageTemplates([
    PageTemplate(id="cover", frames=[frame], onPage=on_cover),
    PageTemplate(id="normal", frames=[frame], onPage=on_page),
])

E = []  # elements
E.append(NextPageTemplate("normal"))
E.append(PageBreak())

# ------------------------------------------------------------------- sommaire
E.append(H("Sommaire"))
for i, s in enumerate([
    "Introduction et contexte",
    "Objectifs du projet",
    "Acteurs et fonctionnalités réalisées",
    "Stack technique",
    "Architecture de l'application",
    "Modèle de données",
    "Commandes et paiements",
    "Sécurité",
    "Déploiement et mise en production",
    "Démonstration et déroulé de la soutenance",
    "Difficultés rencontrées et solutions",
    "Perspectives d'évolution",
    "Conclusion",
], 1):
    E.append(Paragraph("<b>%d.</b>  %s" % (i, s),
             ParagraphStyle("toc", parent=body, fontSize=11, spaceAfter=7, leftIndent=6)))
E.append(PageBreak())

# ------------------------------------------------------------ 1. introduction
E.append(H("1. Introduction et contexte"))
E.append(P("Au Burkina Faso, le commerce de proximité constitue le cœur de l'activité "
           "économique. Pourtant, la grande majorité des commerçants gèrent encore leurs "
           "stocks, leurs ventes et leurs commandes de façon manuelle, sans aucun outil "
           "numérique. Côté clients, trouver un produit précis suppose de se déplacer de "
           "boutique en boutique, sans garantie de disponibilité ni visibilité sur les prix."))
E.append(P("<b>Market BF</b> répond à ce double problème : offrir aux commerçants "
           "burkinabè un outil complet de gestion commerciale (produits, stocks, commandes, "
           "statistiques) et offrir aux clients une marketplace géolocalisée permettant de "
           "rechercher des produits, vérifier leur disponibilité en temps réel, commander "
           "et payer selon les moyens de paiement locaux (Orange Money, Moov Money, Wave, "
           "paiement à la livraison)."))
E.append(P("Le résultat est une application web full-stack opérationnelle, déployée en "
           "production à l'adresse <b>https://marketbf.onrender.com</b>, comptant environ "
           "<b>7 000 lignes de code</b>, <b>9 modules d'API REST</b> et <b>16 pages</b> "
           "d'interface réparties sur trois espaces (client, commerçant, administrateur)."))

# -------------------------------------------------------------- 2. objectifs
E.append(H("2. Objectifs du projet"))
E.append(P("Le projet poursuit cinq objectifs, tous atteints dans la version livrée :"))
for t in ["Digitaliser la gestion des commerces locaux (produits, stocks, ventes, commandes)",
          "Faciliter la recherche de produits pour les clients, avec disponibilité en temps réel",
          "Permettre la gestion des stocks en temps réel, avec alertes et historique des mouvements",
          "Intégrer un système de commande et de paiement adapté au contexte burkinabè",
          "Améliorer la visibilité des commerces grâce à la géolocalisation sur carte interactive"]:
    E.append(B(t))

# ------------------------------------------------------------- 3. fonctionnel
E.append(H("3. Acteurs et fonctionnalités réalisées"))
E.append(P("La plateforme distingue trois rôles, chacun disposant de son propre espace et "
           "de droits contrôlés côté serveur."))
E.append(H2("3.1. Espace client"))
for t in ["Inscription / connexion (e-mail + mot de passe, ou connexion Google en un clic)",
          "Mot de passe oublié : lien de réinitialisation envoyé par e-mail (valable 1 heure)",
          "Catalogue de produits avec recherche par nom et filtrage par catégorie",
          "Carte interactive des boutiques (Leaflet) avec géolocalisation",
          "Fiche boutique : produits, disponibilité en temps réel, avis clients",
          "Panier et passage de commande avec choix du mode de paiement",
          "Reçu envoyé par e-mail à la commande, confirmation par e-mail à la livraison",
          "Historique et suivi de l'état des commandes",
          "Dépôt d'avis (note 1-5 + commentaire) sur les boutiques"]:
    E.append(B(t))
E.append(H2("3.2. Espace commerçant"))
for t in ["Création de la boutique avec localisation sur carte ; visible après validation par l'admin",
          "Ajout, modification et suppression des produits, avec upload de photos",
          "Gestion du stock : quantités, seuils d'alerte, mouvements d'entrée/sortie tracés",
          "Alertes automatiques de stock faible",
          "Réception des commandes et mise à jour de leur statut (en attente → confirmée → livrée / annulée)",
          "Statistiques de vente : chiffre d'affaires, volume, produits les plus vendus (graphiques Recharts)"]:
    E.append(B(t))
E.append(H2("3.3. Espace administrateur"))
for t in ["Validation ou rejet des boutiques en attente",
          "Gestion des utilisateurs (liste, suppression)",
          "Statistiques globales de la plateforme"]:
    E.append(B(t))

# ------------------------------------------------------------------- 4. stack
E.append(PageBreak())
E.append(H("4. Stack technique"))
E.append(P("Les technologies ont été choisies avec un fil conducteur : une plateforme "
           "réellement utilisable au Burkina Faso — accessible depuis n'importe quel "
           "navigateur (téléphone ou PC, sans installation) et avec un coût "
           "d'infrastructure nul."))
E.append(table(["Couche", "Technologies"], [
    ["Backend", "Node.js, Express, better-sqlite3 / libSQL (Turso), jsonwebtoken, bcryptjs, "
                "express-validator, multer, nodemailer"],
    ["Frontend", "React 18, Vite, React Router, Tailwind CSS, Axios, Leaflet / React-Leaflet, "
                 "Recharts, Lucide React, React Hot Toast"],
    ["Infrastructure", "Docker &amp; Docker Compose, Nginx, Render (hébergement), Turso "
                       "(base de données), Cloudinary (images), GitHub (déploiement continu)"],
], [3.5*cm, 13.5*cm]))
E.append(table(["Choix", "Motivation"], [
    ["Application web responsive (React)",
     "Accessible immédiatement sur tout téléphone ou ordinateur via un simple navigateur, "
     "sans installation ni store d'applications."],
    ["Node.js + Express",
     "Écosystème JavaScript unifié entre le frontend et le backend, léger et rapide à déployer."],
    ["SQLite en local, Turso (libSQL) en production",
     "Zéro administration, transactions ACID, hébergement gratuit et répliqué ; les données "
     "survivent aux redémarrages du serveur."],
    ["JWT (HS256) + Google Identity Services",
     "Authentification stateless standard, complétée par une connexion Google en un clic."],
    ["Leaflet + OpenStreetMap",
     "Cartographie gratuite et open source, sans clé d'API ni carte bancaire, bonne "
     "couverture du Burkina Faso."],
], [5.5*cm, 11.5*cm]))

# ------------------------------------------------------------ 5. architecture
E.append(H("5. Architecture de l'application"))
E.append(P("L'application suit une architecture <b>client-serveur découplée</b> : une "
           "API REST stateless côté serveur, consommée par une single-page application "
           "React. En production, un conteneur Docker unique sert à la fois l'API et le "
           "build statique du frontend (même origine, pas de problème CORS)."))
E.append(table(["Composant", "Rôle"], [
    ["Frontend React (SPA)", "16 pages réparties en trois espaces : client (7), commerçant (6), "
     "administrateur (3). Routage protégé par rôle via un contexte d'authentification global."],
    ["API REST Express", "9 modules de routes : auth, shops, products, stock, orders, reviews, "
     "stats, admin, upload. Toutes les routes préfixées par /api, protégées par JWT."],
    ["Middleware d'authentification", "Vérification du token JWT et contrôle des rôles "
     "(client / merchant / admin) avant chaque route protégée."],
    ["Base de données", "SQLite locale en développement ; Turso (libSQL) en production. "
     "Schéma créé et peuplé automatiquement au premier démarrage."],
    ["Stockage d'images", "Upload via multer ; fichiers sur disque en local, sur Cloudinary "
     "en production (persistance garantie)."],
    ["E-mails transactionnels", "Nodemailer + SMTP : reçu de commande, confirmation de "
     "livraison, lien de réinitialisation de mot de passe."],
], [4.6*cm, 12.4*cm]))
E.append(H2("Vue d'ensemble des endpoints"))
E.append(table(["Ressource", "Endpoints principaux"], [
    ["auth", "POST /register, /login, /google, /forgot-password, /reset-password — GET /me, /config"],
    ["shops", "GET /, /:id, /merchant/mine — POST / — PUT /:id"],
    ["products", "GET /, /:id, /merchant/mine — POST / — PUT /:id — DELETE /:id"],
    ["stock", "GET /product/:id, /movements/:id, /alerts — PUT /product/:id — POST /movement"],
    ["orders", "POST / — GET /, /:id — PUT /:id/status"],
    ["reviews", "GET /shop/:shopId — POST / — DELETE /:id"],
    ["stats", "GET /overview, /sales, /products"],
    ["admin", "GET /shops, /users, /stats — PUT /shops/:id/validate — DELETE /users/:id"],
], [3*cm, 14*cm]))

# ------------------------------------------------------------------ 6. modèle
E.append(PageBreak())
E.append(H("6. Modèle de données"))
E.append(P("Le schéma relationnel compte neuf tables. Il est créé et peuplé "
           "automatiquement au premier démarrage avec des boutiques et produits de "
           "démonstration burkinabè."))
E.append(table(["Table", "Contenu"], [
    ["users", "Clients, commerçants et admins ; rôle, e-mail unique, mot de passe haché (bcrypt)"],
    ["shops", "Boutiques géolocalisées (latitude/longitude), statut pending / active / rejected"],
    ["products", "Produits rattachés à une boutique : nom, catégorie, prix, image"],
    ["stock", "Quantité disponible et seuil d'alerte par produit"],
    ["stock_movements", "Historique horodaté des entrées / sorties de stock"],
    ["orders", "Commandes : client, boutique, statut, montant, adresse de livraison"],
    ["order_items", "Lignes de commande : produit, quantité, prix unitaire"],
    ["payments", "Paiement lié à une commande : méthode, montant, statut"],
    ["reviews", "Avis client sur une boutique : note 1 à 5 + commentaire"],
], [4*cm, 13*cm]))

# ---------------------------------------------------------------- 7. paiement
E.append(H("7. Commandes et paiements"))
E.append(P("La commande est traitée de façon <b>transactionnelle</b> : le stock de chaque "
           "produit est décrémenté atomiquement (protection contre les commandes "
           "simultanées — pas de survente possible) et restitué automatiquement si la "
           "commande est annulée."))
E.append(P("Quatre méthodes de paiement sont proposées : <b>Orange Money, Moov Money, "
           "Wave et paiement à la livraison</b>. Chaque commande génère un enregistrement "
           "de paiement avec méthode, montant et statut (pending → completed à la "
           "livraison, failed en cas d'annulation) : la plateforme conserve donc un "
           "historique complet des transactions. Les paiements mobiles sont "
           "<b>simulés</b> : l'intégration réelle des API Orange Money / Moov / Wave "
           "nécessite un contrat marchand et un agrégateur agréé. Le flux complet étant "
           "déjà implémenté, brancher un agrégateur réel ne demandera aucune refonte. Un "
           "reçu détaillé est envoyé par e-mail au client à chaque commande."))

# ----------------------------------------------------------------- 8. sécurité
E.append(H("8. Sécurité"))
E.append(table(["Domaine", "Mise en œuvre dans Market BF"], [
    ["Authentification",
     "JWT signé HS256 avec secret fort obligatoire en production (le serveur refuse de "
     "démarrer sinon) ; mots de passe bcrypt 12 rounds ; politique de complexité ; "
     "anti-énumération de comptes (réponses en temps constant)."],
    ["Données sensibles",
     "Mots de passe hachés bcrypt ; tokens de réinitialisation aléatoires 256 bits stockés "
     "hachés SHA-256, usage unique, expiration 1 h ; HTTPS de bout en bout en production."],
    ["Paiements",
     "Enregistrement transactionnel du paiement ; transitions de statut contrôlées côté "
     "serveur selon le rôle."],
    ["Protection de l'API",
     "Contrôle des rôles sur chaque route ; Helmet (en-têtes HTTP) ; rate limiting global "
     "(300 req/15 min) et renforcé sur l'authentification (20 tentatives/15 min) ; CORS "
     "restreint ; validation systématique des entrées (express-validator) ; uploads durcis "
     "(extension + type MIME, 5 Mo max, nom aléatoire) ; payload JSON limité à 100 ko."],
    ["Persistance des données",
     "Base hébergée sur Turso (répliquée, persistante, indépendante du serveur applicatif) ; "
     "images sur Cloudinary. Un redéploiement ou un crash ne perd aucune donnée."],
], [4.5*cm, 12.5*cm]))

# --------------------------------------------------------------- 9. déploiement
E.append(PageBreak())
E.append(H("9. Déploiement et mise en production"))
E.append(P("L'application est <b>conteneurisée avec Docker</b> (build multi-étapes : build "
           "Vite du frontend, puis image Node servant l'API et les fichiers statiques) et "
           "déployée sur <b>Render</b> via un blueprint <i>render.yaml</i>. Chaque "
           "<i>git push</i> sur GitHub déclenche automatiquement un redéploiement."))
for t in ["Hébergement : Render (plan gratuit), un seul service tout-en-un — https://marketbf.onrender.com",
          "Base de données : Turso (SQLite hébergé, libSQL) — les données survivent aux redémarrages",
          "Images : Cloudinary — stockage persistant des photos produits et logos",
          "Secrets (JWT, SMTP, OAuth Google) : variables d'environnement Render, jamais dans le code",
          "Développement local : ./start.sh ou docker-compose up, base SQLite locale automatique",
          "Coût total de l'infrastructure : 0 F CFA"]:
    E.append(B(t))

# ------------------------------------------------------------------- 10. démo
E.append(H("10. Démonstration et déroulé de la soutenance"))
E.append(P("La soutenance dure <b>10 minutes</b> et est présentée en binôme :"))
E.append(table(["Partie", "Intervenant", "Contenu", "Durée"], [
    ["Partie 1", "Intervenant 1",
     "Contexte et problématique, présentation de Market BF, fonctionnalités des trois "
     "espaces, parcours d'une commande", "≈ 5 min"],
    ["Partie 2", "Intervenant 2",
     "Architecture et choix techniques, sécurité, déploiement, démonstration en direct, "
     "conclusion", "≈ 5 min"],
], [2.2*cm, 3*cm, 9.3*cm, 2.5*cm]))
E.append(P("L'application est accessible en ligne : <b>https://marketbf.onrender.com</b> "
           "(ouvrir le site 2 minutes avant la soutenance pour réveiller le service "
           "gratuit). Comptes de démonstration :"))
E.append(table(["Rôle", "E-mail", "Mot de passe"], [
    ["Administrateur", "admin@marketbf.com", "Admin123!"],
    ["Commerçant", "merchant1@marketbf.com", "Merchant1!"],
    ["Client", "client@marketbf.com", "Client123!"],
], [4*cm, 7*cm, 6*cm]))
E.append(P("Scénario de démonstration : (1) le client recherche un produit, consulte la "
           "carte, commande avec Orange Money et reçoit son reçu par e-mail ; (2) le "
           "commerçant voit la commande, la confirme puis la marque livrée — le stock a "
           "été décrémenté et une alerte apparaît s'il passe sous le seuil ; (3) "
           "l'administrateur valide une nouvelle boutique en attente."))

# ------------------------------------------------------------ 11. difficultés
E.append(H("11. Difficultés rencontrées et solutions"))
E.append(table(["Difficulté", "Solution apportée"], [
    ["Persistance des données sur un hébergement gratuit (disque effacé à chaque "
     "redéploiement Render)",
     "Externalisation de la base vers Turso (SQLite hébergé) et des images vers Cloudinary."],
    ["Cohérence du stock lors de commandes simultanées",
     "Commandes transactionnelles avec décrément atomique et restitution du stock en cas "
     "d'annulation."],
    ["Intégration des paiements mobiles sans contrat marchand",
     "Flux de paiement complet mais simulé, architecture prête pour un agrégateur réel."],
    ["Coût des services de cartographie",
     "Leaflet + OpenStreetMap : gratuit, sans clé API, bonne couverture du Burkina Faso."],
    ["Sécurité d'une application exposée publiquement",
     "Durcissement systématique : Helmet, rate limiting, validation des entrées, uploads "
     "contrôlés, secrets en variables d'environnement."],
], [7.5*cm, 9.5*cm]))

# ------------------------------------------------------------ 12. perspectives
E.append(H("12. Perspectives d'évolution"))
for t in ["Intégration réelle des paiements mobiles via un agrégateur (Orange Money, Moov, Wave) puis carte bancaire",
          "Génération de factures PDF téléchargeables",
          "Module de livraison intégré (suivi livreur, frais calculés par distance)",
          "Recommandations de produits par intelligence artificielle",
          "Application mobile (React Native ou PWA installable) pour capitaliser sur l'existant",
          "Wallet numérique et programme de fidélité",
          "Montée en charge : migration PostgreSQL, multi-boutiques par commerçant"]:
    E.append(B(t))

# ------------------------------------------------------------- 13. conclusion
E.append(H("13. Conclusion"))
E.append(P("Market BF démontre qu'une plateforme complète de digitalisation du commerce "
           "local est réalisable avec des technologies open source et un coût "
           "d'infrastructure nul. Les trois rôles disposent chacun d'un espace "
           "fonctionnel, et la chaîne complète — de la recherche géolocalisée d'un produit "
           "jusqu'à sa livraison confirmée par e-mail — fonctionne en production, avec des "
           "données persistantes et un socle de sécurité sérieux."))
E.append(P("Le projet constitue une base saine pour les évolutions prévues : paiements "
           "réels, livraison intégrée et application mobile. Il illustre la maîtrise du "
           "cycle complet d'un projet web : analyse du besoin, choix d'architecture "
           "argumentés, développement full-stack, sécurisation et mise en production."))

doc.build(E)
print("PDF généré :", OUT)
