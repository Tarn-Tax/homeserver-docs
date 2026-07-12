# Homeserver Documentation Framework

## Doel

Dit project inventariseert automatisch een Proxmox-gebaseerde homeserver en genereert actuele technische documentatie.

Het framework is ontworpen om:

- de volledige infrastructuur automatisch te documenteren;
- afhankelijkheden tussen systemen inzichtelijk te maken;
- configuraties centraal vast te leggen;
- een basis te bieden voor beheer, migratie en disaster recovery.

---

# Ontwerpprincipes

Dit project volgt de volgende uitgangspunten:

- Lees alleen configuratie; wijzig niets aan de infrastructuur.
- Bouw modulair.
- Eén verantwoordelijkheid per module.
- Broncode en gegenereerde documentatie zijn gescheiden.
- Documentatie moet opnieuw te genereren zijn.
- Uitbreidingen mogen bestaande modules niet breken.

---

# Architectuur

```
Collector
        │
        ▼
Inventarisatie
        │
        ▼
Intern datamodel
        │
        ▼
Renderers
        │
        ├── Markdown
        ├── JSON
        └── Mermaid
```

---

# Projectstructuur

```
homeserver-docs/

src/
tests/
docs/
output/

README.md
requirements.txt
inventory.py
```

---

# Roadmap

## Fase 1
- Projectbasis
- Logging
- Configuratie
- CLI

## Fase 2
- Proxmox Collector
- Storage Collector
- VM Collector
- LXC Collector
- Network Collector

## Fase 3
- Docker Collector
- Docker Compose
- Volumes
- Networks

## Fase 4
- Home Assistant
- Nginx Proxy Manager
- AdGuard
- Back-upcontrole

## Fase 5
- Markdown generator
- Mermaid diagrammen
- HTML rapportage
- Health Report

---

# Licentie

Wordt later toegevoegd.