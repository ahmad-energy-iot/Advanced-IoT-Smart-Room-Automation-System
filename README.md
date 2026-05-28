# Advanced IoT Smart Room Automation System

ESP32 • MQTT • Node-RED • Firebase Realtime Database • Smart Dashboard • IoT Automation

---

# Deutsche Version

## Projektbeschreibung

Dieses Projekt präsentiert ein professionelles IoT Smart Room Automation System basierend auf einem ESP32 Mikrocontroller, Node-RED Dashboard, MQTT Kommunikation und Firebase Realtime Database.

Das System wurde entwickelt, um Raumdaten in Echtzeit zu überwachen und intelligente Automatisierungsfunktionen bereitzustellen. Verschiedene Sensoren analysieren kontinuierlich die Umgebungsbedingungen wie Temperatur, Luftfeuchtigkeit, Lichtintensität und Bewegungserkennung.

Das System reagiert automatisch auf Umweltänderungen und steuert RGB-LEDs sowie einen Lüfter intelligent und energieeffizient.

Zusätzlich ermöglicht die MQTT-Kommunikation eine vollständige Fernüberwachung und Steuerung über Computer, Smartphone oder Cloud-Dashboard.

Dieses Projekt kombiniert moderne IoT-Technologien, Embedded Systems, Smart Energy Management, Cloud Synchronization und Echtzeit-Datenvisualisierung in einem professionellen Automatisierungssystem.

---

# Hauptfunktionen

* Echtzeit Smart Room Monitoring
* MQTT-basierte Kommunikation
* Node-RED Live Dashboard
* Firebase Cloud Synchronisation
* Temperaturüberwachung
* Luftfeuchtigkeitsüberwachung
* PIR Bewegungsdetektion
* LDR Lichtintensitätsmessung
* RGB LED Statusanzeige
* Automatische Lüftersteuerung
* AUTO MODE
* MANUAL ON MODE
* MANUAL OFF MODE
* Smartphone Fernsteuerung
* Cloud-basierte Datenspeicherung
* Live Charts und Datenvisualisierung
* Energieeffiziente Automatisierung
* Intelligente Raumüberwachung
* IoT Smart Home Integration
* Realtime System Analytics

---

# Verwendete Komponenten

| Komponente                 | Beschreibung                            |
| -------------------------- | --------------------------------------- |
| ESP32 DevKit V1            | Hauptcontroller und WiFi-Kommunikation  |
| DHT11 / DHT22              | Temperatur- und Luftfeuchtigkeitssensor |
| PIR Sensor                 | Bewegungsdetektion                      |
| LDR Sensor                 | Lichtintensitätsmessung                 |
| RGB LED                    | Status- und Lichtanzeige                |
| Relay Modul                | Lüftersteuerung                         |
| Cooling Fan                | Automatische Raumkühlung                |
| OLED Display SSD1306       | Lokale Echtzeit-Systemanzeige           |
| Breadboard                 | Hardware-Aufbau                         |
| Jumper Kabel               | Elektrische Verbindungen                |
| Node-RED Dashboard         | Echtzeit Benutzeroberfläche             |
| Firebase Realtime Database | Cloud Datenspeicherung                  |
| MQTT Broker                | IoT Kommunikationssystem                |

---

# Systemarchitektur

Das System basiert auf einer mehrschichtigen IoT-Architektur:

1. Sensoren erfassen Umgebungsdaten.
2. Der ESP32 verarbeitet die Sensordaten lokal.
3. Daten werden über MQTT übertragen.
4. Node-RED visualisiert die Daten in Echtzeit.
5. Firebase speichert die Daten in der Cloud.
6. Benutzer können das System remote überwachen und steuern.
7. RGB LEDs und Lüfter reagieren automatisch auf Umgebungsbedingungen.

---

# Betriebsmodi

## AUTO MODE

Das System arbeitet vollständig automatisch:

* LDR analysiert die Umgebungshelligkeit
* PIR erkennt Bewegungen
* RGB LED reagiert abhängig von Licht und Bewegung
* Lüftersteuerung erfolgt automatisch
* Firebase aktualisiert Echtzeitdaten
* Dashboard synchronisiert Live-Daten

### Automatische RGB Logik

| Zustand              | RGB Farbe |
| -------------------- | --------- |
| Helle Umgebung       | AUS       |
| Dunkel ohne Bewegung | Blau      |
| Dunkel mit Bewegung  | Weiß      |

---

## MANUAL ON MODE

* RGB LED leuchtet dauerhaft Grün
* Lüfter wird manuell aktiviert
* Automatische Sensorlogik wird deaktiviert

---

## MANUAL OFF MODE

* RGB LED leuchtet Rot
* Lüfter wird deaktiviert
* Automatische Funktionen werden gestoppt

---

# Node-RED Dashboard Funktionen

Das Dashboard bietet:

* Live Sensorwerte
* Echtzeit Diagramme
* Temperaturanzeige
* Luftfeuchtigkeitsanzeige
* Lichtintensitätsanzeige
* Bewegungsstatus
* RGB Statusanzeige
* Betriebsmodusanzeige
* Lüfterstatus
* Remote Steuerung
* Smartphone Zugriff
* Cloud Synchronisation

---

# Firebase Funktionen

Firebase Realtime Database speichert:

* Temperaturwerte
* Luftfeuchtigkeitswerte
* Lichtintensität
* Bewegungsstatus
* RGB Status
* Lüfterstatus
* Betriebsmodus
* Uptime Informationen

Dadurch wird Cloud-basierte Echtzeitüberwachung ermöglicht.

---

# MQTT Kommunikation

## Publish Topics

```text
ahmadazroun/esp32v4/light
ahmadazroun/esp32v4/motion
ahmadazroun/esp32v4/temperature
ahmadazroun/esp32v4/humidity
ahmadazroun/esp32v4/state
ahmadazroun/esp32v4/rgb
ahmadazroun/esp32v4/mode
```

## Subscribe Topic

```text
ahmadazroun/esp32v4/control
```

## Unterstützte Befehle

```text
AUTO
ON
OFF
```

---

# Systemlogik

1. ESP32 verbindet sich mit WLAN
2. Verbindung zum MQTT Broker wird hergestellt
3. Sensorwerte werden kontinuierlich gelesen
4. OLED Display zeigt Echtzeitdaten
5. MQTT überträgt Sensordaten
6. Node-RED aktualisiert Dashboard
7. Firebase speichert Cloud-Daten
8. RGB LED und Lüfter reagieren automatisch
9. Benutzer können das System remote steuern

---

# Praktische Anwendungen

Dieses Projekt kann verwendet werden für:

* Smart Home Systeme
* Intelligente Raumautomatisierung
* Energieeffiziente Gebäude
* Sicherheitsüberwachung
* Bewegungsbasierte Beleuchtung
* Smart City Anwendungen
* Industrieüberwachung
* IoT Lernplattformen
* Smart Energy Systeme
* Automatische Nachtbeleuchtung
* Cloud-basierte Gebäudeüberwachung
* Embedded Systems Ausbildung

---

# Verwendete Technologien

* ESP32 Microcontroller
* MQTT Communication
* Node-RED
* Firebase Realtime Database
* Embedded Systems
* WiFi Networking
* IoT Automation
* Cloud Synchronization
* Smart Dashboard
* OLED Display Communication
* Sensor Integration
* Realtime Data Monitoring

---

# Benötigte Bibliotheken

```python
from machine import Pin, ADC, PWM, I2C
import network
import time
import ssd1306
from umqtt.simple import MQTTClient
```

Zusätzlich benötigte Dateien:

```text
ssd1306.py
umqtt/simple.py
```

---

# Entwickler

## Ahmad Azroun

Renewable Energy Manager | IoT & Smart Energy Systems Developer

---

# English Version

## Project Description

This project demonstrates a professional IoT Smart Room Automation System based on an ESP32 microcontroller, Node-RED dashboard, MQTT communication, and Firebase Realtime Database.

The system was developed to monitor room conditions in real time and provide intelligent automation features. Multiple sensors continuously analyze environmental conditions such as temperature, humidity, light intensity, and motion detection.

The system automatically reacts to environmental changes while intelligently controlling RGB LEDs and a cooling fan in an energy-efficient way.

Additionally, MQTT communication enables complete remote monitoring and control through computer, smartphone, or cloud dashboard interfaces.

This project combines modern IoT technologies, embedded systems, smart energy management, cloud synchronization, and real-time data visualization into one professional automation platform.

---

# Main Features

* Real-Time Smart Room Monitoring
* MQTT-Based Communication
* Node-RED Live Dashboard
* Firebase Cloud Synchronization
* Temperature Monitoring
* Humidity Monitoring
* PIR Motion Detection
* LDR Light Intensity Monitoring
* RGB LED Status Indication
* Automatic Fan Control
* AUTO MODE
* MANUAL ON MODE
* MANUAL OFF MODE
* Smartphone Remote Control
* Cloud-Based Data Storage
* Live Charts and Data Visualization
* Energy-Efficient Automation
* Intelligent Room Monitoring
* IoT Smart Home Integration
* Real-Time System Analytics

---

# Components Used

| Component                  | Description                            |
| -------------------------- | -------------------------------------- |
| ESP32 DevKit V1            | Main controller and WiFi communication |
| DHT11 / DHT22              | Temperature and humidity sensor        |
| PIR Sensor                 | Motion detection                       |
| LDR Sensor                 | Ambient light measurement              |
| RGB LED                    | Lighting and status indication         |
| Relay Module               | Fan switching control                  |
| Cooling Fan                | Automatic room cooling                 |
| OLED Display SSD1306       | Local real-time system display         |
| Breadboard                 | Hardware assembly                      |
| Jumper Wires               | Electrical connections                 |
| Node-RED Dashboard         | Real-time user interface               |
| Firebase Realtime Database | Cloud data storage                     |
| MQTT Broker                | IoT communication system               |

---

# System Architecture

The system is based on a multi-layer IoT architecture:

1. Sensors collect environmental data
2. ESP32 processes sensor values locally
3. Data is transmitted through MQTT
4. Node-RED visualizes data in real time
5. Firebase stores cloud data
6. Users can remotely monitor and control the system
7. RGB LEDs and fan automatically react to environmental conditions

---

# Operating Modes

## AUTO MODE

The system operates fully automatically:

* LDR measures room brightness
* PIR detects motion
* RGB LED reacts based on light and motion
* Fan control operates automatically
* Firebase updates real-time data
* Dashboard synchronizes live information

### Automatic RGB Logic

| Condition           | RGB Color |
| ------------------- | --------- |
| Bright Environment  | OFF       |
| Dark without Motion | Blue      |
| Dark with Motion    | White     |

---

## MANUAL ON MODE

* RGB LED glows Green
* Fan is manually activated
* Automatic sensor logic is disabled

---

## MANUAL OFF MODE

* RGB LED glows Red
* Fan is disabled
* Automatic functions are stopped

---

# Node-RED Dashboard Features

The dashboard provides:

* Live sensor values
* Real-time charts
* Temperature display
* Humidity display
* Light intensity monitoring
* Motion status
* RGB status indication
* Operating mode display
* Fan status
* Remote control interface
* Smartphone accessibility
* Cloud synchronization

---

# Firebase Features

Firebase Realtime Database stores:

* Temperature values
* Humidity values
* Light intensity
* Motion status
* RGB status
* Fan status
* Operating mode
* Uptime information

This enables cloud-based real-time monitoring.

---

# MQTT Communication

## Publish Topics

```text
ahmadazroun/esp32v4/light
ahmadazroun/esp32v4/motion
ahmadazroun/esp32v4/temperature
ahmadazroun/esp32v4/humidity
ahmadazroun/esp32v4/state
ahmadazroun/esp32v4/rgb
ahmadazroun/esp32v4/mode
```

## Subscribe Topic

```text
ahmadazroun/esp32v4/control
```

## Supported Commands

```text
AUTO
ON
OFF
```

---

# System Logic

1. ESP32 connects to WiFi
2. ESP32 connects to MQTT broker
3. Sensor values are continuously monitored
4. OLED display updates real-time data
5. MQTT transfers sensor information
6. Node-RED updates dashboard values
7. Firebase stores cloud data
8. RGB LED and fan react automatically
9. Users can remotely control the system

---

# Practical Applications

This project can be used for:

* Smart Home systems
* Intelligent room automation
* Energy-efficient buildings
* Security monitoring
* Motion-based lighting
* Smart City applications
* Industrial monitoring systems
* IoT educational platforms
* Smart energy systems
* Automatic night lighting
* Cloud-based building monitoring
* Embedded systems education

---

# Technologies Used

* ESP32 Microcontroller
* MQTT Communication
* Node-RED
* Firebase Realtime Database
* Embedded Systems
* WiFi Networking
* IoT Automation
* Cloud Synchronization
* Smart Dashboard
* OLED Display Communication
* Sensor Integration
* Real-Time Data Monitoring

---

# Required Libraries

```python
from machine import Pin, ADC, PWM, I2C
import network
import time
import ssd1306
from umqtt.simple import MQTTClient
```

Additional required files:

```text
ssd1306.py
umqtt/simple.py
```

---

# Developer

## Ahmad Azroun

Renewable Energy Manager | IoT & Smart Energy Systems Developer
