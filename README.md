# Concept Drift Detektor für das vPW
## Übersicht
Dieses Programm ist darauf ausgelegt, Daten aus einem Elasticsearch-Index zu verarbeiten und Concept Drifts in verschiedenen Variablen zu erkennen. Es enthält Funktionen zum Überwachen von Aktivitäten, Durchlaufzeiten und mehreren Porzessvariablen im Laufe der Zeit. Das System verwendet die River-Bibliothek für die Drifterkennung und Slack für Benachrichtigungen.

## Voraussetzungen
Vor dem Ausführen des Skripts stellen Sie sicher, dass Folgendes installiert ist:

- Python 3.10.11
- Abhängigkeiten aus requirements.txt
- Docker
- vPW ist installiert: https://github.com/viadee/vPW
   
## Konfiguration
- Elasticsearch-Verbindung: Stellen Sie sicher, dass Ihre Elasticsearch-Instanz unter http://host.docker.internal:9200 erreichbar ist.
- Webhook in derSlack-API erstellen: https://api.slack.com/
- Slack-Webhook: Richten Sie einen Slack-Webhook ein und geben Sie die URL als Umgebungsvariable mit dem Namen SLACK_CONNECT an.
- Indexkonfiguration: Legen Sie den Elasticsearch-Index fest, der verarbeitet werden soll, indem Sie dessen Namen als Umgebungsvariable mit dem Namen INDEX angeben.
- Geben Sie an, mit wie vielen Datensätzen das Programm den Durchschnitt bilden soll. 
- Das bereitgestellte Dockerfile richtet die erforderliche Umgebung ein und installiert Abhängigkeiten. Passen Sie bei Bedarf Umgebungsvariablen und Abhängigkeiten an.
## Abhängigkeiten
 ### Module
    Python            3.10.11
    elasticsearch     8.10.0
    numpy             1.26.0
    pandas            2.1.1
    river             0.19.0

## Dokumentation
   - main/run.py: Einstiegspunkt des Skripts. Initialisiert Elasticsearch-Verbindungen und startet Threads zur Verarbeitung von Aktivitäts-IDs, Bearbeitungszeiten und mehreren Variablen.
   - loadDataFromElastic/elasticsearchDataFetcherActivityId.py: Überwacht Konzeptdrift in den Aktivitäten. 
   - loadDataFromElastic/elasticsearchDataFetcherLeadTime.py: Überwacht Konzeptdrift in Durchlaufzeiten.
   - multiVariablesFetcher.py: Ruft Daten für mehrere Variablen ab und verarbeitet jede Variable in einem separaten Thread.
   - configMessage.py: Enthält die Funktion send_message_to_slack zum Senden von Nachrichten an Slack.

Das Skript verwendet die River-Bibliothek für die binäre Drifterkennung.
Die Elasticsearch-Abfragen sind darauf ausgelegt, spezifische Daten basierend auf Zeitstempel, Ereignistyp und Variablennamen abzurufen.
## Hinweise zur Fehlersuche
Wenn Probleme auftreten, stellen Sie sicher, dass Ihre Elasticsearch-Instanz läuft und die erforderlichen Python-Abhängigkeiten installiert sind. Überprüfen Sie die Konfiguration des Slack-Webhooks und stellen Sie sicher, dass der angegebene Index existiert.
Bei Bedarf können Sie sich für Unterstützung oder weitere Anpassungen gerne melden.
## Installation und Ausführung
### Docker
Das bereitgestellte Dockerfile richtet die erforderliche Umgebung ein und installiert Abhängigkeiten. 

1. **Bau des Docker-Images:**
    ```bash
    docker build -t dein_image_name .
    ```

2. **Ausführung des Docker-Containers:**
    ```bash
    docker run -e SLACK_CONNECT="dein_slack_webhook_url" -e INDEX="dein_elasticsearch_index" dein_image_name
    ```

**Hinweis:** Passe bei Bedarf Umgebungsvariablen und Abhängigkeiten an.

Das bereitgestellte Dockerfile richtet die erforderliche Umgebung ein und installiert Abhängigkeiten. Passen Sie bei Bedarf Umgebungsvariablen und Abhängigkeiten an.
docker build -t dein_image_name .
docker run -e SLACK_CONNECT="dein_slack_webhook_url" -e INDEX="dein_elasticsearch_index" dein_image_name

### Clone dieses Repository:

   ```bash
   git clone https://github.com/viadee-internal/fue-bpm-vpw-drift-detection
   ```
## Kontakt
- Fridolin Lüschen
- fridolin.lueschen@viadee.de

## Lizenz

### elasticsearch (Version 8.10.0)
**Elasticsearch Python Client**

- Lizenz: Apache License 2.0
- [Link zur Lizenz](https://www.apache.org/licenses/LICENSE-2.0)

### numpy (Version 1.26.0)
**Numerische Bibliothek für Python**

- Lizenz: NumPy Open Source License
- [Link zur Lizenz](https://numpy.org/doc/stable/license.html)

### pandas (Version 2.1.1)
**Datenanalyse-Bibliothek für Python**

- Lizenz: BSD 3-Clause License
- [Link zur Lizenz](https://opensource.org/licenses/BSD-3-Clause)

### river (Version 0.19.0)
**Maschinelles Lernen in Echtzeit für Python**

- Lizenz: BSD 3-Clause License
- [Link zur Lizenz](https://opensource.org/licenses/BSD-3-Clause)





