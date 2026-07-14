# Homeserver-handboek

## 1. Systeemoverzicht

- Doel van de homeserver
- Architectuuroverzicht
- Belangrijkste systemen
- IP-adressen
- Statusoverzicht
- Diagram van de volledige omgeving

## 2. Proxmox-host

- Hostnaam
- Proxmox-versie
- Kernel
- Processor
- Geheugen
- Uptime
- Hardware
- BIOS en firmware
- Temperatuursensoren
- Ventilatoren

## 3. Storage

- Proxmox-storageoverzicht
- Fysieke schijven
- Partities
- ZFS-pools
- ZFS-datasets
- Mountpoints
- Capaciteit en gebruik
- SMART-status
- Relaties tussen storage, VM’s en containers
- Waarschuwingen bij volle opslag

## 4. Netwerk

- Fysieke netwerkinterfaces
- Linux-bridges
- IP-adressen
- Gateway
- DNS
- VLAN’s
- Interne netwerken
- DMZ
- Firewall
- Netwerkdiagram

## 5. Virtuele machines

Per VM:

- VMID
- Naam
- Status
- Functie
- CPU
- Geheugen
- Disks
- Storage
- Netwerkinterfaces
- IP-adres
- Gastbesturingssysteem
- Tags
- Opstartinstellingen
- Snapshots
- Back-ups
- Afhankelijkheden

## 6. LXC-containers

Per container:

- CT-ID
- Naam
- Status
- Functie
- CPU
- Geheugen
- Rootdisk
- Mountpoints
- Netwerk
- IP-adres
- Tags
- Opstartinstellingen
- Back-ups
- Afhankelijkheden

## 7. Docker-server

- Docker-host
- Docker-versie
- Compose-projecten
- Containers
- Images
- Volumes
- Netwerken
- Bind mounts
- Poorten
- Restart policies
- Afhankelijkheden

## 8. Applicaties en diensten

Per applicatie:

- Naam
- Functie
- Host of container
- IP-adres
- Poorten
- Externe URL
- Reverse proxy
- Opslaglocaties
- Database
- Cache
- Back-upmethode
- Updateprocedure
- Herstelprocedure

Op te nemen applicaties:

- Nextcloud
- Immich
- Jellyfin
- Syncthing
- Duplicati
- Collabora
- Nginx Proxy Manager
- Home Assistant
- AdGuard
- Overige diensten

## 9. Reverse proxy en certificaten

- Nginx Proxy Manager
- Proxy-hosts
- Domeinnamen
- Doelhosts en poorten
- SSL-certificaten
- Certificaatvervaldata
- Externe bereikbaarheid

## 10. DNS

- DNS-servers
- Interne DNS-records
- AdGuard-configuratie
- Upstream DNS
- Lokale domeinen
- Blokkeerlijsten

## 11. Back-ups

- Back-upstrategie
- Proxmox-back-ups
- Duplicati-back-ups
- DATA-back-ups
- BACKUP_A
- BACKUP_B
- NFS-shares
- Schema’s
- Retentie
- Controle op geslaagde back-ups
- Hersteltests

## 12. Beveiliging

- SSH
- Gebruikers en rechten
- Firewall
- Updates
- Extern bereikbare diensten
- Certificaten
- Secrets en wachtwoorden
- Risico’s en aanbevelingen

## 13. Monitoring en gezondheid

- Status van VM’s en containers
- Storagegebruik
- ZFS-status
- SMART-status
- Temperatuur
- Geheugengebruik
- CPU-gebruik
- Back-upstatus
- Certificaten
- Waarschuwingen

## 14. Onderhoud

- Proxmox bijwerken
- VM’s en containers bijwerken
- Docker-images bijwerken
- Oude kernels verwijderen
- Ongebruikte images en volumes verwijderen
- Storage controleren
- Back-ups controleren

## 15. Herstel en calamiteiten

- Herstel van Proxmox
- Herstel van VM’s
- Herstel van LXC-containers
- Herstel van Docker
- Herstel van databases
- Herstel van Nextcloud
- Herstel van Immich
- Herstel van configuratiebestanden
- Benodigde wachtwoorden en sleutels
- Volgorde bij volledig herstel

## 16. Wijzigingshistorie

- Datum
- Wijziging
- Reden
- Uitgevoerd door