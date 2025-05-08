# R2 UI Control Panel

A graphical control panel built with **Kivy** for interacting with an R2-D2 styled emotional expression and hardware system.  
It supports dynamic UI updates, joystick interaction, sound feedback, and visual state indicators for network and device status.

---

## 🖥️ Features

- 📡 **WiFi and R2 Connection Indicators**  
  Dynamically updates icons (`Wifi.png`, `NoWifi.png`, `R2.png`, `NoR2.png`) based on connection status.

- 🎭 **Emotion Selector Grid**  
  Displays a 3x3 grid of emotions. Clicking an emotion:
  - Highlights it with an overlay and paw image.
  - Plays a corresponding emotion sound.
  - Sends a virtual signal for expression.

- 🕹️ **Joystick Interaction**  
  - `<` and `>` buttons allow cycling through emotions.
  - Holoprojector (HP) toggle simulated by clicking an on-screen UI.

- 📦 **Modular Layouts**  
  - `Top UI`: Shows status icons (Wifi, Signal, R2).
  - `Fixed Grid`: Emotion selector.
  - `Dynamic Area`: Selection overlays.
  - `Panther Left/Right`: Decorative or functional side UI elements.


---

## ▶️ How to Run

Make sure you have Python 3 and Kivy installed:

```bash
pip install kivy

python main.py

