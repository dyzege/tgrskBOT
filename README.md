# Twitch Bot z panelem webowym (Python)

## Funkcje

- Obsługa komend na czacie: !k, !d, !kd, !res, !resm
- Statystyki kill/death z zapisem do pliku
- Webowy panel zarządzania (z opcjonalnym hasłem)
- Keep-alive przez Flask
- Kompatybilny z Replit, Render, Railway

## Uruchomienie

1. Skonfiguruj `.env` zgodnie ze swoimi danymi
2. Zainstaluj zależności:
```
pip install -r requirements.txt
```
3. Uruchom bota i panel:
```
python3 web.py
```

## Hosting

Polecane: [Replit.com](https://replit.com/) lub [Railway](https://railway.app)

- Pinguj `/` przez UptimeRobot aby utrzymać bota 24/7