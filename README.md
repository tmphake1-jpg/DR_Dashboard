# Opening Range Breakout Dashboard

Dieses Repository enthält eine interaktive Streamlit-Anwendung zur Analyse von Opening-Range-Breakout-Strategien (ORB) für verschiedene Futures- und FX-Märkte. Das Dashboard unterstützt Trader dabei, historische Sitzungsdaten zu untersuchen, Wahrscheinlichkeiten zu bewerten und eigene Handelsannahmen anhand statistischer Kennzahlen und Machine-Learning-Ausgaben zu prüfen.

## Hauptfunktionen

- **Interaktive Filter**: Auswahl von Symbol, Handelssession (New York, London, Tokio) und Opening-Range-Dauer (30 oder 60 Minuten) sowie zusätzliche Filter nach Wochentag, Monat oder Jahr.
- **Breakout-Statistiken**: Kennzahlen zu Range-Breakouts, Range-Holds, Retracements, Expansions und Schlusskursen außerhalb der Opening Range.
- **Verteilungsanalysen**: Visualisierungen mit Plotly für Breakout-Fenster, Retracement- und Expansionslevel inklusive kumulativer Wahrscheinlichkeitslinien.
- **Modellübersicht**: Darstellung der erkannten Session-Modelle (z. B. Strong Uptrend, Expansion) inklusive Bildmaterial und Szenarioanalyse basierend auf vergangenen Sitzungen.
- **Strategie-Backtesting**: Einfache Parametrisierung von Einstiegs-, Ausstiegs- und Stoppregeln, um die ausgewählten Filtereinstellungen historisch zu testen.
- **Machine-Learning-Bereich**: Laden vorkonfigurierter Modelle und Skalierer zur Einschätzung der aktuellen Session anhand gespeicherter Pickle-Dateien.
- **Datentransformationen**: `orb_calculations.py` erzeugt und aktualisiert die zugrundeliegenden CSV-Datensätze auf Basis von 5-Minuten-Kerzen.

## Projektstruktur

```
DR_Dashboard/
├── data/                 # CSV-Dateien für Symbole, Sessions und Opening-Range-Dauer
├── ml_models/            # Trainierte ML-Modelle und Skalierer (.pickle)
├── pictures/             # Grafiken zur Modellbeschreibung im Dashboard
├── session_models/       # Zusätzliche Session-Modelldaten
├── streamlit_app.py      # Hauptanwendung des Dashboards
├── orb_calculations.py   # Skript zur Erstellung/Aktualisierung der Datensätze
├── ml_models.py          # Hilfsfunktionen für ML-Workflows
└── README.md             # Dieses Dokument
```

## Voraussetzungen

- Python 3.10 oder neuer (empfohlen)
- Virtuelle Umgebung (z. B. `venv` oder `conda`)
- Installierte Abhängigkeiten: `streamlit`, `pandas`, `numpy`, `plotly`, `polars`, `scikit-learn` (für ML), `python-dateutil` sowie Standardbibliotheken.

> **Hinweis:** Ergänzen Sie weitere Pakete entsprechend Ihrer lokalen Umgebung und den verwendeten ML-Modellen.

## Installation & Start

1. Repository klonen:
   ```bash
   git clone <repo-url>
   cd DR_Dashboard
   ```
2. Virtuelle Umgebung anlegen und aktivieren:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
3. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```
   Falls keine `requirements.txt` vorhanden ist, installieren Sie die benötigten Pakete manuell.
4. Streamlit-App starten:
   ```bash
   streamlit run streamlit_app.py
   ```
5. Öffnen Sie den angezeigten lokalen URL im Browser, um das Dashboard zu verwenden.

## Datenquellen & -format

- Die CSV-Dateien in `data/` werden mit Semikolon (`;`) getrennt und nutzen einen Datumsindex.
- Zeitstempel (z. B. `breakout_time`, `max_retracement_time`, `max_expansion_time`) sind in Mikrosekunden gespeichert und werden in der App in die entsprechende Zeitzone (`America/New_York`) konvertiert.
- `orb_calculations.py` kann genutzt werden, um aus Rohdaten (5-Minuten-Candles) neue ORB-Datensätze zu generieren oder bestehende zu aktualisieren.

## Machine-Learning-Modelle

- Modelle und Skalierer werden als Pickle-Dateien in `ml_models/` erwartet. Die Benennung folgt dem Muster `<symbol>_<session>_simple_confirmation_bias_model.pickle`.
- Beim Laden prüft die App automatisch, ob für das gewählte Symbol und die Session ein passendes Modell vorhanden ist.
- Nutzen Sie `ml_models.py`, um Training, Evaluierung und Export eigener Modelle zu organisieren.

## Weiterentwicklung

- Ergänzen Sie zusätzliche Symbole oder Sessions, indem Sie entsprechende CSV-Datensätze hinzufügen.
- Integrieren Sie neue Visualisierungen (Plotly) oder Metriken direkt in `streamlit_app.py`.
- Passen Sie die Strategie-Backtesting-Regeln an, um spezifische Handelslogiken abzubilden.

## Support

Bei Fragen oder Verbesserungsvorschlägen eröffnen Sie bitte ein Issue oder erstellen Sie einen Pull Request.

