# PyQt6 OpenGL Weather App Nevelykyy desktopnyy dodatok na Python z vykorystannyam PyQt6 i OpenGL dlya vidobrazhennya obertovoyi 3D-piramidy ta vidzhetu z potochnoyu pohodoyu. ## Funktsional - **3D-piramida**: obertannya mysheyu, masshtab kolishchatkom, vybir kolʹoru, skydannya polozhennya. - **Pohoda**: otrymannya ta vidobrazhennya danykh z wttr.in (Kyyiv), avtomatychne onovlennya kozhni 10 khv. ## Struktura proyektu
Показати більше
394 / 5 000
# PyQt6 OpenGL Weather App

A small desktop application in Python using PyQt6 and OpenGL to display a rotating 3D pyramid and a widget with the current weather.

## Functionality
- **3D pyramid**: rotate with the mouse, zoom with the wheel, choose a color, reset position.
- **Weather**: receive and display data from wttr.in (Kyiv), automatic update every 10 minutes.

## Project structure
weather_app/
├── README.md           # Project description
├── main.py             # Application entry point
├── ui/                 # UI components package
│   ├── init.py
│   ├── main_window.py  # Main window
│   └── weather_widget.py # Weather widget
├── gl/                 # OpenGL components package
│   ├── init.py
│   └── pyramida_widget.py # 3D pyramid widget
├── services/           # Services package
│   ├── init.py
│   └── weather_service.py # Weather fetching logic and error handling
├── requirements.txt    # Dependencies
└── .gitignore          # Ignored files

## Installation
```bash
pip install -r requirements.txt
```

## Start project
```bash
python main.py
```