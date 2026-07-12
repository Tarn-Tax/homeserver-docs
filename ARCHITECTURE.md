# Homeserver Documentation Framework – Architectuur

## Doel

Het framework inventariseert een Proxmox-omgeving zonder wijzigingen aan te brengen en genereert actuele technische documentatie.

## Principes

- Read-only inventarisatie.
- Modulair ontwerp.
- Eén verantwoordelijkheid per module.
- Scheiding tussen verzamelen, verwerken en presenteren.
- Uitbreidbaar zonder bestaande modules te wijzigen.

## Architectuur

```text
CLI
 │
 ▼
Application
 │
 ├── Collectors
 │     ├── Proxmox
 │     ├── Storage
 │     ├── Network
 │     ├── VM
 │     ├── LXC
 │     ├── Docker
 │     ├── Home Assistant
 │     └── Services
 │
 ▼
Intern datamodel
 │
 ├── Markdown Renderer
 ├── JSON Renderer
 ├── Mermaid Renderer
 └── HTML Renderer
```

## Ontwikkelregels

- Geen shell-commando's direct vanuit renderers.
- Collectors verzamelen alleen gegevens.
- Renderers maken alleen output.
- Businesslogica hoort niet in de CLI.
- Elke module is afzonderlijk testbaar.