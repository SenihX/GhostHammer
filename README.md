# 🚀 GhostHammer
 
GhostHammer is a powerful and anonymous HTTP Flooding tool that performs both GET and POST requests using the TOR network.
It works seamlessly on **Termux** and **Kali Linux**.

> 🧠 Educational purpose only. Do not use on unauthorized targets.

---

## 🔥 Features

- 🔁 Multi-threaded HTTP Flood (GET + POST)
- 🌍 Anonymity via TOR (with auto IP rotation)
- 🐧 Fully compatible with Termux and Linux
- 🧠 Built-in random User-Agent, Referer, Headers
- 🧱 Auto-config TOR if not already present

---

## 📦 Installation

### 📱 Termux

```bash
pkg update && pkg upgrade
pkg install python tor clang git -y
pip install requests stem
pip install requests[socks]
git clone https://github.com/SenihX/GhostHammer
cd GhostHammer
python ghosthammer.py
```

### 💻 Kali Linux

```bash
sudo apt update && sudo apt install python3 tor git -y
pip3 install requests stem
git clone https://github.com/YourSenihX/GhostHammer
cd GhostHammer
python3 ghosthammer.py
```

---

## 🛠️ Usage

```bash
python ghosthammer.py
```

Then enter:

- ✅ Target URL: `http://example.com` or `https://example.com`
- ❌ Wrong formats: `example.com`, `www.example.com`

👉 **URL must start with `http://` or `https://`**

- 🔁 Thread Count: Default is 700 (you can set more/less)
- ⏱️ IP Change Interval: Default is 3 seconds (auto TOR IP rotation)

---

## 📌 Examples

```
🌐 Target URL (must start with http/https): https://target.com
🔁 Number of threads [default=700]: 500
⏱️ IP change interval (sec) [default=3]: 5
```

You'll see logs like:

```
[Thread-3] GET 200
[Thread-3] POST 200
📊 Total: 40 | GET: 20 | POST: 20 | Failed: 0
```

---

## 🧠 Notes

- This tool auto-generates a TOR configuration if missing.
- If TOR is not running, it will attempt to launch it automatically.
- You can stop the attack anytime with `CTRL + C`.

---

## 👨‍💻 Developed By

**Mr.SenihX**
Cybersecurity Enthusiast – [GitHub]
https://github.com/SenihX
🛡️ *For educational use only. Use responsibly.*

---

## 📛 Disclaimer

This tool is intended for **educational and authorized testing** purposes only.
**Using this tool on targets without permission is illegal** and against GitHub policies.

---
