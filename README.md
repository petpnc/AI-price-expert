# 💎 ValueAI - Inteligentné Oceňovanie Predmetov

AI aplikácia na okamžité ocenenie predmetov pomocou Google Gemini AI.

## 🚀 Rýchly Štart

### 1. Nainštaluj závislosti

```bash
pip install -r requirements.txt
```

### 2. Získaj Google API kľúč

1. Otvor: https://makersuite.google.com/app/apikey
2. Prihlás sa Google účtom
3. Klikni **"Create API Key"**
4. Skopíruj vygenerovaný kľúč

### 3. Nastav API kľúč

Otvor súbor `.streamlit/secrets.toml` a nahraď:

```toml
GOOGLE_API_KEY = "tvoj-api-kluc-sem"
```

### 4. Spusti aplikáciu

```bash
streamlit run app.py
```

Aplikácia sa otvorí na: `http://localhost:8501`

## 🔐 Demo Prihlasovacie Kľúče

Po spustení použi jeden z týchto kľúčov:

- `DEMO-KEY` - 3 kredity
- `TEST-KEY` - 10 kreditov
- `CLIENT-100` - 50 kreditov
- `PREMIUM-2024` - 100 kreditov

## ➕ Pridanie Nových Licenčných Kľúčov

Otvor `credits.json` a pridaj nový riadok:

```json
{
  "DEMO-KEY": 3,
  "NOVY-KLIENT": 50,  ← pridaj tu
  "PREMIUM-2024": 100
}
```

Formát: `"NAZOV-KLUCA": pocet_kreditov`

## 📱 Prístup z Mobilu

Ak chceš otvoriť na mobile v rovnakej sieti:

1. Zisti svoju lokálnu IP adresu:
   - Mac/Linux: `ifconfig`
   - Windows: `ipconfig`

2. Na mobile otvor:
   ```
   http://192.168.X.X:8501
   ```
   (použi svoju IP adresu)

## ✨ Funkcie

✅ Autentifikácia pomocou licenčných kľúčov
✅ Nahranie fotky alebo fotenie cez kameru
✅ AI analýza pomocou Google Gemini
✅ Odhad cien (nové/použité/zberateľské)
✅ Vygenerovaný predajný popis
✅ Mobilne responzívne
✅ Správa kreditov
✅ **💳 Platobná brána (Stripe)**
✅ **⚙️ Admin panel pre správu**
✅ **💰 4 cenové plány (€5 - €150)**
✅ **📊 Payment tracking a reporting**

## 📁 Štruktúra Projektu

```
valueai/
├── app.py                    # Hlavná aplikácia
├── payments.py               # Platobný systém (Stripe)
├── admin.py                  # Admin panel
├── credits.json              # Databáza licenčných kľúčov
├── payment_log.json          # História platieb (generuje sa automaticky)
├── requirements.txt          # Python závislosti
├── .streamlit/
│   └── secrets.toml         # Konfigurácia API kľúčov
├── README.md                # Tento súbor
├── STRIPE_SETUP.md          # Návod na Stripe setup
└── DEPLOYMENT.md            # Návod na cloud deploy
```

## 💡 Tipy Pre Najlepšie Výsledky

- Použi dobré osvetlenie
- Fotka celého predmetu
- Ukáž značky a logo
- Vyhni rozmazaným fotkám

## 🆘 Problémy?

Ak niečo nefunguje:

1. **Chyba API kľúča**: Skontroluj `.streamlit/secrets.toml`
2. **Nemôžem sa prihlásiť**: Skontroluj `credits.json`
3. **Chyba inštalácie**: Skús `pip install --upgrade pip` a potom znova `pip install -r requirements.txt`

## 📄 Licencia

Pre komerčné použitie kontaktuj autora.

---

## 💳 Platobný Systém

ValueAI obsahuje kompletný platobný systém pomocou Stripe:

### Cenové Plány

- **Starter** (€5) - 10 kreditov
- **Professional** (€20) - 50 kreditov  
- **Business** (€50) - 150 kreditov
- **Enterprise** (€150) - 500 kreditov

### Setup Stripe

1. Prečítaj si **STRIPE_SETUP.md** pre kompletný návod
2. Vytvor Stripe účet na https://dashboard.stripe.com
3. Získaj API kľúč
4. Pridaj do `.streamlit/secrets.toml`
5. Otestuj s testovacími kartami

### Funkcie

✅ Automatické generovanie licenčných kľúčov  
✅ Bezpečné platby cez Stripe  
✅ Email notifikácie  
✅ Payment tracking  
✅ Test mode pre development  

---

## ⚙️ Admin Panel

Spravuj licencie a platby cez admin panel:

```bash
streamlit run admin.py
```

**Admin funkcie:**
- Vytvorenie/úprava/vymazanie licenčných kľúčov
- Prezeranie histórie platieb
- Export payment logu do CSV
- Systémové štatistiky
- Monitoring API statusu

**Prihlasovacie heslo:** Nastav v `secrets.toml` (`ADMIN_PASSWORD`)

---

Vytvoril: Claude + p
Dátum: December 2024
