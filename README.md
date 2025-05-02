🎯 Buckshot Roulette – Wahrscheinlichkeitsrechner & Lernsystem

    🧠 Probability Tool & Self-Learning System for Buckshot Roulette

🇩🇪 DEUTSCH
🕹️ Funktionen

    Zeigt die Wahrscheinlichkeit der nächsten Patrone (Rot oder Blau)

    Auswahl an Start-Patronen (Rot = geladen, Blau = leer)

    Integriertes Lernsystem, das sich an Fehlvorhersagen anpasst

    Einbindung von Items wie Inverter, Hand Saw usw.

    Inverter-Funktion, die Vorhersagen dynamisch dreht

    Speichert Fortschritt automatisch als .json im Unterordner

💡 Wie funktioniert das Programm?
1. Patronen eingeben

Beim Start wirst du gefragt:

Anzahl roter Patronen (z. B. 3)
Anzahl blauer Patronen (z. B. 5)

2. Vorhersage erhalten

Das Programm nutzt:

self.counts[color] * self.weights[color]

→ Die Wahrscheinlichkeit wird dynamisch berechnet.
3. Ziehung bestätigen

Du gibst ein, ob die Vorhersage korrekt war bzw. welche Patrone tatsächlich kam.
4. So lernt der Code

Wenn die Vorhersage falsch war, merkt sich das Programm:

if prediction != gezogen:
    self.weights[gezogen] += 1.0

→ Das bedeutet: beim nächsten Mal wird diese Farbe wahrscheinlicher vorausgesagt.
5. Inverter verwenden

Wenn der Inverter im Spiel ist, kannst du mit einem Klick die Vorhersage umdrehen:

    z. B. aus Nächste Patrone: Blau wird → ROT

Das wird in der Lernlogik korrekt behandelt, damit kein Fehler entsteht.
🧠 Speicherort

Das Programm speichert seine Lernwerte automatisch:

Lernverhalten/Lernverhalten Buckshot Roulette.json

Beispielinhalt:

{
  "rot": 3.0,
  "blau": 1.0
}

⚠️ Hinweis

    🔔 Dies ist kein Cheat, sondern ein intelligenter Wahrscheinlichkeitsrechner.

    Das Tool greift nicht ins Spiel ein

    Es basiert nur auf ehrlicher Eingabe

    Wenn du falsche Werte angibst, lernt das Programm falsch

📌 Teste das System ehrlich – je genauer du bist, desto besser wird es!
In eigenen Tests lag die Treffergenauigkeit bei ca. 80 % nach 5 vollständigen Runden.
📦 Voraussetzungen

    Python 3.10 oder neuer

    tkinter (in Python enthalten)

▶️ Start

python buckshot_gui.py

🇺🇸 ENGLISH
🕹️ Features

    Predicts the next shell (red or blue) with percentage chance

    Enter number of live and empty shells

    Integrated learning algorithm that adapts over time

    Supports special items like Inverter, Hand Saw, etc.

    One-click Inverter logic to flip predictions on the fly

    Progress saved in a .json file in a subfolder

💡 How It Works
1. Set Shell Counts

You start by entering:

Red shells (e.g. 3)
Blue shells (e.g. 5)

2. Get a Prediction

The app uses:

self.counts[color] * self.weights[color]

→ Calculates the weighted chance for each color.
3. Input the Actual Shell

You confirm whether the prediction was correct.
4. The Learning Mechanism

If the guess was wrong, the app does this:

if prediction != drawn:
    self.weights[drawn] += 1.0

→ This increases the chance for the correct result next time.
5. Using the Inverter

If the Inverter item is used, click:

    INVERTER USED?
    → The prediction flips, and the logic adjusts correctly.

🧠 Data Storage

The learning data is saved to:

Lernverhalten/Lernverhalten Buckshot Roulette.json

Example:

{
  "rot": 3.0,
  "blau": 1.0
}

⚠️ Please Note

    ⚠️ This is not a cheat, just a smart assistant.

    It does not access or manipulate the game

    It depends fully on honest user input

    If you give incorrect results on purpose, the AI learns incorrectly

📌 In tests, it was ~80% accurate after 5 rounds — but only if you give honest inputs.
Use this as a support tool, not a cheat.
📦 Requirements

    Python 3.10+

    tkinter (usually built-in)

▶️ Run

python buckshot_gui.py
