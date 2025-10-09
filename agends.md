# Projektagenda

Dieses Dokument fasst offene Aufgaben und mögliche nächste Schritte für die Weiterentwicklung des Opening Range Breakout Dashboards zusammen.

## Kurzfristige Aufgaben

- [ ] `requirements.txt` erstellen oder aktualisieren, um alle notwendigen Python-Abhängigkeiten eindeutig zu dokumentieren.
- [ ] Beispiel-Datensätze im Verzeichnis `data/` bereitstellen, damit neue Nutzerinnen und Nutzer die App ohne zusätzliche Vorbereitung testen können.
- [ ] Dokumentation zum Machine-Learning-Workflow in `ml_models.py` ergänzen (Trainingsablauf, Evaluationsmetriken, Export der Pickle-Dateien).

## Mittelfristige Ideen

- [ ] Erweiterung des Strategie-Backtesters um Risiko-/Money-Management-Kennzahlen (z. B. maximaler Drawdown, Sharpe Ratio).
- [ ] Integration eines automatisierten Datenimports (z. B. über eine Datenbank oder eine API), um die CSV-Dateien aktuell zu halten.
- [ ] Mehrsprachige Unterstützung innerhalb der Streamlit-App (Deutsch/Englisch).

## Langfristige Vision

- [ ] Aufbau eines kontinuierlichen Trainingsprozesses für die Machine-Learning-Modelle inklusive Modellbewertung und Versionierung.
- [ ] Bereitstellung eines Deployment-Setups (Docker oder Cloud), um das Dashboard produktiv hosten zu können.
- [ ] Entwicklung zusätzlicher Module für verwandte Handelsstrategien (z. B. VWAP-Reversion, Opening-Drive).

