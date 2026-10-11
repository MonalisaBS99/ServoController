from flask import Flask, request, jsonify
import serial
import time

app = Flask(__name__)

# Connect to Arduino
arduino = serial.Serial("COM3", 9600, timeout=1)
time.sleep(2)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ServoCore | Motion Control</title>

<style>
:root {
    --bg: #090d12;
    --panel: #111821;
    --border: #273442;
    --muted: #8292a5;
    --text: #f0f5fa;
    --accent: #53e4c2;
}

* { box-sizing: border-box; }

body {
    margin: 0;
    min-height: 100vh;
    background:
        radial-gradient(ellipse at 80% 0%, #14312f 0%, transparent 35%),
        var(--bg);
    color: var(--text);
    font-family: "Segoe UI", Arial, sans-serif;
}

header {
    height: 76px;
    padding: 0 7%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--border);
}

.brand {
    font-size: 20px;
    font-weight: 800;
    letter-spacing: 2px;
}

.brand span { color: var(--accent); }

.connection {
    font-size: 11px;
    color: var(--accent);
    letter-spacing: 1.5px;
}

main {
    width: min(960px, 90%);
    margin: 48px auto;
}

.eyebrow {
    color: var(--accent);
    font-size: 11px;
    letter-spacing: 3px;
    font-weight: 700;
}

h1 {
    font-size: clamp(32px, 5vw, 48px);
    letter-spacing: -1.5px;
    margin: 12px 0;
}

.intro {
    color: var(--muted);
    line-height: 1.7;
    max-width: 600px;
    margin-bottom: 32px;
}

.panel {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 32px;
    background: linear-gradient(145deg, #141d27, #0f151d);
    border: 1px solid var(--border);
    border-radius: 22px;
    padding: 30px;
    box-shadow: 0 24px 70px #0004;
}

.label {
    font-size: 11px;
    letter-spacing: 1.8px;
    color: var(--muted);
    text-transform: uppercase;
}

.gauge {
    width: min(100%, 290px);
    aspect-ratio: 1;
    margin: 24px auto;
    border-radius: 50%;
    display: grid;
    place-items: center;
    background: conic-gradient(
        from 180deg,
        var(--accent) 0deg,
        var(--accent) 0deg,
        #293542 0deg,
        #293542 360deg
    );
    position: relative;
    box-shadow: 0 0 40px #53e4c210;
}

.gauge::before {
    content: "";
    position: absolute;
    inset: 11px;
    border-radius: 50%;
    background: #111821;
    border: 1px solid #344250;
}

.gauge::after {
    content: "";
    position: absolute;
    inset: 24px;
    border: 1px dashed #293744;
    border-radius: 50%;
}

.reading {
    text-align: center;
    z-index: 1;
}

.angle {
    font-size: 68px;
    font-weight: 750;
    letter-spacing: -4px;
}

.degrees {
    font-size: 22px;
    color: var(--accent);
}

.reading p {
    color: var(--muted);
    font-size: 10px;
    letter-spacing: 2px;
}

.control {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 24px;
}

.value-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.current {
    font-size: 26px;
    font-weight: 700;
}

.current small {
    color: var(--accent);
    font-size: 13px;
}

input[type="range"] {
    width: 100%;
    accent-color: var(--accent);
    cursor: pointer;
    margin: 22px 0 12px;
}

.range-labels {
    display: flex;
    justify-content: space-between;
    color: var(--muted);
    font-size: 12px;
}

.presets {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 9px;
}

button {
    padding: 13px 8px;
    border: 1px solid #354453;
    border-radius: 10px;
    background: #18232e;
    color: var(--text);
    cursor: pointer;
    font-size: 13px;
    transition: 0.2s;
}

button:hover {
    border-color: var(--accent);
    color: var(--accent);
    transform: translateY(-1px);
}

button.active {
    background: var(--accent);
    color: #07130f;
    border-color: var(--accent);
    font-weight: 700;
}

#apply {
    width: 100%;
    padding: 16px;
    background: var(--accent);
    color: #07130f;
    border: none;
    font-weight: 800;
    letter-spacing: 1px;
}

#apply:hover {
    background: #8af4dd;
    color: #07130f;
}

#message {
    min-height: 18px;
    color: var(--muted);
    font-size: 12px;
    line-height: 1.5;
}

.cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-top: 18px;
}

.info {
    padding: 18px;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 13px;
}

.info span {
    font-size: 10px;
    color: var(--muted);
    letter-spacing: 1px;
}

.info strong {
    display: block;
    margin-top: 9px;
    font-size: 15px;
}

footer {
    margin: 26px 0;
    text-align: center;
    color: #607083;
    font-size: 11px;
    letter-spacing: 1px;
}

@media (max-width: 680px) {
    header { padding: 0 5%; }
    main { margin: 30px auto; }
    .panel {
        grid-template-columns: 1fr;
        padding: 21px;
        gap: 10px;
    }
    .gauge { max-width: 235px; }
    .angle { font-size: 56px; }
    .cards { grid-template-columns: 1fr; }
}
</style>
</head>

<body>
<header>
    <div class="brand">SERVO<span>CORE</span></div>
    <div class="connection">● &nbsp; CONTROL INTERFACE</div>
</header>

<main>
    <div class="eyebrow">HARDWARE SYSTEM / 001</div>
    <h1>Motion Control.</h1>
    <p class="intro">
        A browser-based interface for precision servo positioning.
        Adjust the angle, apply the command, and control your Arduino
        hardware through serial communication.
    </p>

    <section class="panel">
        <div>
            <div class="label">Position monitor</div>
            <div class="gauge" id="gauge">
                <div class="reading">
                    <span class="angle" id="display">90</span>
                    <span class="degrees">°</span>
                    <p>SERVO POSITION</p>
                </div>
            </div>
            <div class="value-row">
                <span class="label">Operating range</span>
                <span class="label">0° — 180°</span>
            </div>
        </div>

        <div class="control">
            <div>
                <div class="value-row">
                    <span class="label">Target angle</span>
                    <span class="current"><span id="value">90</span><small>°</small></span>
                </div>

                <input id="slider" type="range" min="0" max="180"
                       value="90" step="1">

                <div class="range-labels">
                    <span>0°</span><span>90°</span><span>180°</span>
                </div>
            </div>

            <div>
                <div class="label" style="margin-bottom:13px">
                    Quick positioning
                </div>
                <div class="presets">
                    <button data-angle="0">0°</button>
                    <button data-angle="45">45°</button>
                    <button data-angle="90" class="active">90°</button>
                    <button data-angle="135">135°</button>
                    <button data-angle="180">180°</button>
                </div>
            </div>

            <button id="apply">APPLY POSITION ↗</button>
            <div id="message" role="status">Ready to send a command.</div>
        </div>
    </section>

    <section class="cards">
        <div class="info">
            <span>MICROCONTROLLER</span>
            <strong>Arduino Uno</strong>
        </div>
        <div class="info">
            <span>COMMUNICATION</span>
            <strong>USB Serial · 9600</strong>
        </div>
        <div class="info">
            <span>ACTUATOR</span>
            <strong>SG90 Servo · Pin 9</strong>
        </div>
    </section>

    <footer>EMBEDDED SYSTEMS · HARDWARE / SOFTWARE INTEGRATION</footer>
</main>

<script>
const slider = document.getElementById("slider");
const display = document.getElementById("display");
const value = document.getElementById("value");
const gauge = document.getElementById("gauge");
const message = document.getElementById("message");
const applyButton = document.getElementById("apply");
const presetButtons = document.querySelectorAll("[data-angle]");

let appliedAngle = 90;
let busy = false;

function updateDisplay(angle) {
    display.textContent = angle;
    value.textContent = angle;

    const degrees = Number(angle) / 180 * 180;
    gauge.style.background = `conic-gradient(
        from 180deg,
        #53e4c2 0deg,
        #53e4c2 ${degrees}deg,
        #293542 ${degrees}deg,
        #293542 360deg
    )`;

    presetButtons.forEach(button => {
        button.classList.toggle(
            "active",
            Number(button.dataset.angle) === Number(angle)
        );
    });
}

slider.addEventListener("input", () => {
    updateDisplay(slider.value);
    message.textContent = "Target selected. Apply to move the servo.";
});

presetButtons.forEach(button => {
    button.addEventListener("click", () => {
        slider.value = button.dataset.angle;
        updateDisplay(slider.value);
        message.textContent = "Target selected. Apply to move the servo.";
    });
});

applyButton.addEventListener("click", async () => {
    if (busy) return;

    const angle = Number(slider.value);
    busy = true;
    applyButton.disabled = true;
    applyButton.textContent = "SENDING COMMAND...";
    message.textContent = "Sending command to Arduino...";

    try {
        const response = await fetch("/move?angle=" + angle);
        const result = await response.json();

        if (!response.ok || !result.success) {
            throw new Error(result.error || "Command failed");
        }

        appliedAngle = angle;
        message.textContent = "Command sent successfully · " + angle + "°";
    } catch (error) {
        message.textContent = "Error: " + error.message;
    } finally {
        busy = false;
        applyButton.disabled = false;
        applyButton.textContent = "APPLY POSITION ↗";
    }
});

updateDisplay(90);
</script>
</body>
</html>
"""


@app.route("/")
def home():
    return HTML


@app.route("/move")
def move():
    angle = request.args.get("angle", type=int)

    if angle is None or not 0 <= angle <= 180:
        return jsonify({
            "success": False,
            "error": "Angle must be between 0 and 180."
        }), 400

    try:
        arduino.write(f"{angle}\n".encode("utf-8"))
        arduino.flush()

        return jsonify({
            "success": True,
            "angle": angle
        })

    except serial.SerialException:
        return jsonify({
            "success": False,
            "error": "Arduino serial connection failed."
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
