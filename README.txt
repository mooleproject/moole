MONITOR SYSTEM PACKAGE
=======================

CONTENUTO:
- Monitor_Documentation.pdf → documentazione professionale
- /uml/architecture.puml → diagramma architetturale
- /code/monitor_client.py → codice client
- /code/monitor_server.py → codice server
- /config/*.ini → file di configurazione

UTILIZZO:
1. Modificare client.ini e server.ini secondo necessità.
2. Avviare monitor.server.
3. Avviare monitor.client.
4. Verificare file .wsl aggiornato automaticamente.

REQUISITI:
- Python 3.10+
- librerie: pycryptodome, requests

NOTE:
Il sistema usa AES-256-GCM.
