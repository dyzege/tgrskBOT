import socket
import os
import time
import json
from dotenv import load_dotenv

load_dotenv()

HOST = "irc.chat.twitch.tv"
PORT = 6667
NICK = os.getenv("TWITCH_BOT_NICK")
CHANNEL = os.getenv("TWITCH_CHANNEL")
PASS = os.getenv("TWITCH_OAUTH_TOKEN")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
STATS_FILE = "stats.json"

def debug(msg):
    if DEBUG:
        print("[DEBUG]", msg)
    with open("log.txt", "a") as log:
        log.write(f"{time.ctime()} - {msg}\n")

def load_stats():
    try:
        with open(STATS_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {"kills": 0, "deaths": 0}

def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)

def handle_command(msg, stats):
    if msg == "!k":
        stats["kills"] += 1
    elif msg == "!d":
        stats["deaths"] += 1
    elif msg == "!kd":
        kd = stats["kills"] / stats["deaths"] if stats["deaths"] > 0 else stats["kills"]
        return f"Kills: {stats['kills']} | Deaths: {stats['deaths']} | K/D: {kd:.2f}"
    elif msg == "!res":
        stats["kills"] = 0
        stats["deaths"] = 0
    elif msg == "!resm":
        stats = {"kills": 0, "deaths": 0}
    save_stats(stats)
    return None

def run_bot():
    try:
        sock = socket.socket()
        sock.connect((HOST, PORT))
        sock.send(f"PASS {PASS}\n".encode())
        sock.send(f"NICK {NICK}\n".encode())
        sock.send(f"JOIN #{CHANNEL}\n".encode())

        stats = load_stats()

        while True:
            resp = sock.recv(2048).decode("utf-8", errors="ignore")
            if resp.startswith("PING"):
                sock.send("PONG :tmi.twitch.tv\n".encode())
                continue

            debug(resp)

            if "PRIVMSG" in resp:
                parts = resp.split(":", 2)
                if len(parts) < 3:
                    continue
                username = parts[1].split("!")[0]
                message = parts[2].strip()
                debug(f"{username}: {message}")

                response = handle_command(message, stats)
                if response:
                    sock.send(f"PRIVMSG #{CHANNEL} :{response}\n".encode())

    except Exception as e:
        debug(f"ERROR: {e}")
        time.sleep(5)
        run_bot()

if __name__ == "__main__":
    run_bot()