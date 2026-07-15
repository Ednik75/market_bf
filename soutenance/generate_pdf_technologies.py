# -*- coding: utf-8 -*-
"""Génère le document « Justification des choix technologiques » de Market BF."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Table, TableStyle, PageBreak, NextPageTemplate)

OUT = os.path.join(os.path.dirname(__file__), "Justification_Technologies_MarketBF.pdf")

GREEN = HexColor("#166534")
GREEN_DARK = HexColor("#0e3d20")
RED = HexColor("#c0392b")
YELLOW = HexColor("#f0b429")
GREY = HexColor("#4b5563")
LIGHT = HexColor("#f0fdf4")
BORDER = HexColor("#d1d5db")

AUTHORS = "NITIEMA Martial  •  [Nom du binôme]"
TITLE = "Market BF — Justification des choix technologiques"

styles = getSampleStyleSheet()
def S(name, **kw):
    kw.setdefault("fontName", "Helvetica")
    kw.setdefault("parent", styles["Normal"])
    st = ParagraphStyle(name, **kw)
    styles.add(st); return st

h1 = S("H1", fontName="Helvetica-Bold", fontSize=16, textColor=GREEN_DARK,
       spaceBefore=18, spaceAfter=8)
h2 = S("H2", fontName="Helvetica-Bold", fontSize=12, textColor=GREEN,
       spaceBefore=10, spaceAfter=5)
body = S("Body", fontSize=10.2, leading=14.5, alignment=TA_JUSTIFY, spaceAfter=6,
         textColor=HexColor("#1f2937"))
bullet = S("BulletX", parent=body, leftIndent=14, bulletIndent=4, spaceAfter=3)
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

def on_cover(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(GREEN_DARK); canvas.rect(0, 0, w, h, fill=1, stroke=0)
    canvas.setFillColor(RED);    canvas.rect(0, h - 1.1*cm, w, 1.1*cm, fill=1, stroke=0)
    canvas.setFillColor(YELLOW); canvas.rect(0, h - 1.35*cm, w, 0.25*cm, fill=1, stroke=0)
    canvas.setFillColor(GREEN);  canvas.rect(0, 0, w, 1.1*cm, fill=1, stroke=0)

    canvas.setFillColor(white)
    canvas.setFont("Helvetica-Bold", 32)
    canvas.drawCentredString(w/2, h - 8.2*cm, "Market BF")
    canvas.setFont("Helvetica", 15)
    canvas.setFillColor(HexColor("#bbf7d0"))
    canvas.drawCentredString(w/2, h - 9.5*cm, "Marketplace locale et gestion commerciale")
    canvas.drawCentredString(w/2, h - 10.3*cm, "pour les commerces du Burkina Faso")

    canvas.setFillColor(YELLOW)
    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawCentredString(w/2, h - 13*cm, "JUSTIFICATION DES CHOIX TECHNOLOGIQUES")

    canvas.setFillColor(white); canvas.setFont("Helvetica", 11.5)
    canvas.drawCentredString(w/2, h - 15.6*cm, "Node.js / Express  •  React + Vite  •  SQLite (Turso)  •  Docker / Render")

    canvas.setFont("Helvetica", 12)
    canvas.drawCentredString(w/2, 5.6*cm, "Présenté par : %s" % AUTHORS)
    canvas.drawCentredString(w/2, 4.8*cm, "Juillet 2026")
    canvas.restoreState()

def on_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(GREEN); canvas.rect(0, h - 0.5*cm, w, 0.5*cm, fill=1, stroke=0)
    canvas.setFont("Helvetica", 8); canvas.setFillColor(GREY)
    canvas.drawString(2*cm, 1.05*cm, "Market BF — Justification des choix technologiques")
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

E = []
E.append(NextPageTemplate("normal"))
E.append(PageBreak())

# ------------------------------------------------------------ 1. critères
E.append(H("1. Les critères qui ont guidé tous nos choix"))
E.append(P("Avant de choisir la moindre technologie, nous avons fixé quatre critères, "
           "directement liés au contexte du projet : une marketplace destinée aux "
           "commerçants et aux clients du Burkina Faso, développée en binôme, sans budget."))
E.append(table(["Critère", "Ce que cela impose concrètement"], [
    ["<b>Accessibilité maximale</b>",
     "L'application doit fonctionner sur n'importe quel téléphone ou ordinateur, sans "
     "installation, y compris avec une connexion modeste. Cela oriente vers le web "
     "plutôt qu'une application mobile native."],
    ["<b>Coût d'infrastructure nul</b>",
     "Aucun service payant, aucune carte bancaire requise : hébergement, base de données, "
     "cartographie et stockage d'images doivent être gratuits."],
    ["<b>Simplicité et productivité</b>",
     "Une équipe de deux personnes et un délai court : un seul langage sur toute la "
     "chaîne, des outils bien documentés, peu d'administration système."],
    ["<b>Évolutivité</b>",
     "Les choix ne doivent pas bloquer l'avenir : pouvoir migrer vers PostgreSQL, brancher "
     "un agrégateur de paiement réel ou ajouter une application mobile sans tout refaire."],
], [4.5*cm, 12.5*cm]))
E.append(P("Chaque section qui suit applique cette grille : ce que fait la technologie "
           "dans Market BF, pourquoi elle a été retenue, et quelles alternatives ont été "
           "écartées."))

# ------------------------------------------------------------ 2. backend
E.append(H("2. Backend : Node.js + Express"))
E.append(H2("Rôle dans le projet"))
E.append(P("Node.js exécute toute la logique serveur ; Express structure l'API REST en "
           "9 modules de routes (authentification, boutiques, produits, stocks, commandes, "
           "avis, statistiques, administration, upload)."))
E.append(H2("Pourquoi ce choix"))
for t in ["<b>Un seul langage partout</b> : JavaScript côté serveur comme côté client. En binôme, "
          "chacun peut intervenir sur tout le code sans changer de langage, de conventions ni d'outillage.",
          "<b>Léger et rapide à mettre en route</b> : un serveur Express tient en quelques lignes ; "
          "pas de structure imposée lourde, ce qui convient à un MVP.",
          "<b>Modèle non bloquant</b> : Node.js gère naturellement de nombreuses requêtes simultanées "
          "(consultations du catalogue, commandes) avec très peu de ressources — important sur un "
          "hébergement gratuit aux capacités limitées.",
          "<b>Écosystème npm</b> : tous les besoins du projet (JWT, bcrypt, validation, upload, "
          "e-mails) sont couverts par des bibliothèques éprouvées, installées en une commande."]:
    E.append(B(t))
E.append(H2("Alternatives écartées"))
E.append(P("<b>Django (Python)</b> apportait un back-office intégré mais imposait un second "
           "langage et un cadre plus rigide pour une API simple. <b>PHP/Laravel</b> restait "
           "possible mais aurait également cassé l'unité JavaScript du projet. Express est le "
           "standard de facto pour une API REST Node.js, minimaliste et documenté partout."))

# ------------------------------------------------------------ 3. base de données
E.append(H("3. Base de données : SQLite (better-sqlite3) puis Turso en production"))
E.append(H2("Rôle dans le projet"))
E.append(P("La base contient les 9 tables du modèle (utilisateurs, boutiques, produits, "
           "stocks et mouvements, commandes et lignes, paiements, avis). En développement, "
           "c'est un simple fichier SQLite local ; en production, la même base est hébergée "
           "chez Turso (libSQL, un SQLite accessible par le réseau)."))
E.append(H2("Pourquoi ce choix"))
for t in ["<b>Zéro administration</b> : pas de serveur de base de données à installer, configurer, "
          "sauvegarder ; la base est créée et peuplée automatiquement au premier démarrage.",
          "<b>Transactions ACID</b> : SQLite garantit l'atomicité dont dépend la partie la plus "
          "sensible du projet — le décrément de stock à la commande, protégé contre les commandes "
          "simultanées (pas de survente), et la restitution du stock en cas d'annulation.",
          "<b>Turso résout la persistance</b> : le plan gratuit de Render efface le disque à chaque "
          "redéploiement. En déplaçant la base chez Turso (gratuit, répliqué), comptes, produits et "
          "commandes survivent aux redémarrages — sans changer de moteur SQL.",
          "<b>Adapté à l'échelle réelle</b> : pour un MVP avec quelques dizaines de boutiques, "
          "SQLite est largement suffisant et plus rapide qu'un aller-retour vers un serveur SQL."]:
    E.append(B(t))
E.append(H2("Alternatives écartées"))
E.append(P("<b>PostgreSQL</b> est plus puissant (concurrence en écriture élevée, types avancés) "
           "mais exige un serveur dédié — payant ou limité dans les offres gratuites — et une "
           "administration continue. Le SQL utilisé restant standard, une migration PostgreSQL "
           "est prévue si la charge l'exige. <b>MongoDB</b> a été écarté : nos données sont "
           "fortement relationnelles (une commande référence un client, une boutique, des "
           "produits, un paiement), ce qui plaide pour le relationnel et ses contraintes "
           "d'intégrité."))

# ------------------------------------------------------------ 4. frontend
E.append(PageBreak())
E.append(H("4. Frontend : React 18 + Vite, application web responsive"))
E.append(H2("Rôle dans le projet"))
E.append(P("Le frontend est une single-page application de 16 pages réparties en trois "
           "espaces (client, commerçant, administrateur), construite avec React et servie "
           "en production sous forme de fichiers statiques."))
E.append(H2("Pourquoi le web plutôt qu'une application mobile"))
E.append(P("C'est le choix le plus structurant du projet. Une application web responsive "
           "est <b>immédiatement accessible</b> à tout possesseur de smartphone ou "
           "d'ordinateur au Burkina Faso : pas de téléchargement, pas de Play Store, pas "
           "d'espace de stockage requis, mises à jour instantanées pour tous. Un seul code "
           "à développer et maintenir à deux, au lieu d'un code mobile + un code web. "
           "L'API REST étant indépendante du client, une application mobile (PWA ou React "
           "Native) pourra s'y brancher plus tard sans rien réécrire côté serveur."))
E.append(H2("Pourquoi React et Vite"))
for t in ["<b>React 18</b> : découpage en composants réutilisables (cartes produit, notation par "
          "étoiles, barres de navigation), état géré proprement (panier, session), et le plus grand "
          "écosystème de bibliothèques du marché.",
          "<b>Vite</b> : serveur de développement quasi instantané et build de production optimisé "
          "(code minifié, découpé), sans configuration — un gain de productivité net face à des "
          "outillages plus anciens.",
          "<b>React Router</b> : routage côté client avec protection par rôle — un client ne peut "
          "pas atteindre les pages commerçant ou admin, en complément du contrôle serveur."]:
    E.append(B(t))
E.append(H2("Alternatives écartées"))
E.append(P("<b>Flutter</b> produit de belles applications mobiles mais impose le langage Dart, "
           "un passage par les stores et un second code à maintenir. <b>Vue/Angular</b> sont "
           "des équivalents crédibles de React ; React a été préféré pour son écosystème "
           "(React-Leaflet, Recharts) et sa documentation."))

# ------------------------------------------------------------ 5. UI
E.append(H("5. Interface : Tailwind CSS, Leaflet, Recharts"))
E.append(table(["Bibliothèque", "Rôle", "Pourquoi elle a été retenue"], [
    ["<b>Tailwind CSS</b>", "Tout le style de l'application",
     "Classes utilitaires directement dans les composants : design responsive (mobile "
     "d'abord) rapide à produire et cohérent, sans feuilles de style à synchroniser. "
     "Le build ne conserve que les classes utilisées (CSS final très léger)."],
    ["<b>Leaflet + OpenStreetMap</b> (React-Leaflet)", "Carte interactive des boutiques géolocalisées",
     "Cartographie 100 % gratuite et open source, sans clé d'API ni carte bancaire — là où "
     "Google Maps exige un compte de facturation. Couverture correcte du Burkina Faso, "
     "bibliothèque légère, intégration React officielle."],
    ["<b>Recharts</b>", "Graphiques des statistiques commerçant (CA, ventes, top produits)",
     "Bibliothèque de graphiques pensée pour React (composants déclaratifs), gratuite, "
     "suffisante pour des courbes et histogrammes lisibles sans configuration complexe."],
    ["<b>Axios</b>", "Appels HTTP vers l'API",
     "Instance unique préconfigurée : URL de base et jeton JWT ajoutés automatiquement à "
     "chaque requête, gestion centralisée des erreurs (session expirée, etc.)."],
    ["<b>Lucide React / React Hot Toast</b>", "Icônes et notifications",
     "Deux bibliothèques minimalistes qui améliorent l'expérience (retours visuels "
     "immédiats : produit ajouté, commande passée) sans alourdir l'application."],
], [3.6*cm, 4.4*cm, 9*cm]))

# ------------------------------------------------------------ 6. auth
E.append(PageBreak())
E.append(H("6. Authentification : JWT, bcrypt et Google Identity Services"))
E.append(H2("Pourquoi JWT"))
E.append(P("L'API est <b>stateless</b> : à la connexion, le serveur délivre un jeton signé "
           "(HS256) contenant l'identité et le rôle de l'utilisateur ; chaque requête le "
           "présente dans l'en-tête Authorization. Aucune session à stocker côté serveur — "
           "ce qui simplifie le déploiement (le serveur peut redémarrer sans déconnecter "
           "personne) et permettra demain à une application mobile d'utiliser exactement la "
           "même API. Le middleware vérifie le jeton et le rôle (client / merchant / admin) "
           "avant chaque route protégée."))
E.append(H2("Pourquoi bcrypt"))
E.append(P("Les mots de passe ne sont jamais stockés en clair : bcrypt les hache avec un "
           "facteur de coût de 12, ce qui rend une attaque par force brute prohibitive "
           "même en cas de fuite de la base. C'est le standard recommandé, préféré à des "
           "hachages rapides (SHA-256 seul) précisément parce qu'il est lent."))
E.append(H2("Pourquoi Google Identity Services en complément"))
E.append(P("La connexion Google en un clic réduit la friction à l'inscription — beaucoup "
           "d'utilisateurs ont un compte Google sur leur téléphone Android, très répandu "
           "au Burkina Faso. Contrairement à une dépendance complète à Firebase Auth, "
           "notre authentification maison reste maîtrisée : Google n'est qu'un moyen "
           "d'identification supplémentaire, gratuit et optionnel (l'application "
           "fonctionne sans)."))

# ------------------------------------------------------------ 7. services
E.append(H("7. Services d'appui : Multer, Cloudinary, Nodemailer"))
E.append(table(["Outil", "Rôle", "Pourquoi"], [
    ["<b>Multer</b>", "Réception des images uploadées (produits, boutiques)",
     "Middleware standard d'Express pour les fichiers ; il permet nos contrôles de "
     "sécurité : extension et type MIME vérifiés, 5 Mo maximum, nom de fichier aléatoire."],
    ["<b>Cloudinary</b>", "Stockage des images en production",
     "Le disque de Render étant effacé à chaque redéploiement, les photos doivent vivre "
     "ailleurs. Cloudinary offre un stockage gratuit, un CDN rapide et le "
     "redimensionnement à la volée. En local, simple dossier uploads/ sans compte requis."],
    ["<b>Nodemailer + SMTP</b>", "Reçus de commande, confirmations de livraison, réinitialisation de mot de passe",
     "Bibliothèque de référence pour l'e-mail en Node.js, compatible avec n'importe quel "
     "fournisseur SMTP (Gmail gratuit ici). Sans configuration SMTP, les e-mails sont "
     "simulés dans la console — pratique en développement."],
], [3*cm, 5*cm, 9*cm]))

# ------------------------------------------------------------ 8. infra
E.append(H("8. Infrastructure : Docker, Nginx, Render, GitHub"))
E.append(H2("Docker et Docker Compose"))
E.append(P("L'application est conteneurisée avec un build multi-étapes : une première "
           "étape construit le frontend avec Vite, la seconde produit une image Node "
           "unique qui sert à la fois l'API et les fichiers statiques. Résultat : "
           "<b>le même environnement partout</b> (machine de développement, Render, ou un "
           "futur VPS), plus de « ça marche chez moi », et un seul service à déployer — "
           "donc pas de configuration CORS entre un frontend et un backend séparés. "
           "Docker Compose permet aussi de lancer toute l'application en local en une "
           "commande."))
E.append(H2("Render + GitHub : le déploiement continu"))
E.append(P("Render construit et déploie automatiquement l'image Docker à chaque "
           "<i>git push</i> (blueprint render.yaml). Plan gratuit, HTTPS automatique, "
           "variables d'environnement pour les secrets (JWT, SMTP, OAuth) — jamais dans le "
           "code. Les limites du gratuit (mise en veille après 15 minutes, disque non "
           "persistant) sont compensées par Turso et Cloudinary. Alternatives écartées : "
           "Heroku n'a plus d'offre gratuite ; un VPS (~5 €/mois) contredisait le critère "
           "de coût nul — le docker-compose du projet y fonctionnerait toutefois tel quel."))

# ------------------------------------------------------------ 9. récap
E.append(H("9. Vue d'ensemble"))
E.append(table(["Besoin", "Technologie retenue", "Critère décisif"], [
    ["Serveur / API REST", "Node.js + Express", "Un seul langage, léger, écosystème npm"],
    ["Base de données", "SQLite → Turso (libSQL)", "Zéro administration, ACID, gratuit et persistant"],
    ["Interface utilisateur", "React 18 + Vite", "Accessible sans installation, composants, productivité"],
    ["Style", "Tailwind CSS", "Responsive rapide et cohérent, CSS final minimal"],
    ["Cartographie", "Leaflet + OpenStreetMap", "Gratuit, open source, sans clé d'API"],
    ["Graphiques", "Recharts", "Composants React déclaratifs, gratuit"],
    ["Authentification", "JWT + bcrypt + Google", "Stateless, sécurisé, connexion en un clic"],
    ["Images", "Multer + Cloudinary", "Uploads contrôlés, stockage persistant gratuit"],
    ["E-mails", "Nodemailer + SMTP", "Standard Node.js, fournisseur libre"],
    ["Conteneurisation", "Docker + Compose", "Même environnement partout, un seul service"],
    ["Hébergement", "Render + GitHub", "Déploiement continu gratuit, HTTPS automatique"],
], [4.2*cm, 5.3*cm, 7.5*cm]))

# ------------------------------------------------------------ 10. conclusion
E.append(H("10. Conclusion"))
E.append(P("Aucune de ces technologies n'a été choisie par habitude ou par effet de mode : "
           "chacune répond à au moins un des quatre critères de départ — accessibilité, "
           "coût nul, productivité en binôme, évolutivité. L'ensemble forme une chaîne "
           "cohérente : un seul langage (JavaScript) du navigateur à la base de données, "
           "un seul conteneur à déployer, et un coût d'infrastructure de 0 F CFA pour une "
           "application réellement en production."))
E.append(P("Ces choix ne ferment aucune porte : le SQL standard autorise une migration "
           "PostgreSQL, l'API stateless accueillera une application mobile, et la brique "
           "de paiement simulée est prête à recevoir un agrégateur réel (Orange Money, "
           "Moov Money, Wave). La stack retenue est donc à la fois la plus adaptée au "
           "MVP d'aujourd'hui et un socle crédible pour la suite."))

doc.build(E)
print("PDF généré :", OUT)
