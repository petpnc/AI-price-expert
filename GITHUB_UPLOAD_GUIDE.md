# 📤 GitHub Upload - Web Interface Návod

## ✅ KROK ZA KROKOM (5 minút)

Tvoje repo: https://github.com/petpnc/AI-price-expert

---

## 📋 KROK 1: Príprava Súborov

### ✅ NAHRAJ TIETO SÚBORY:

**Python Aplikácie:**
- ✅ `app.py`
- ✅ `payments.py`
- ✅ `admin.py`

**Konfigurácia:**
- ✅ `requirements.txt`
- ✅ `.gitignore`
- ✅ `secrets.toml.example`

**Dokumentácia:**
- ✅ `README.md`
- ✅ `QUICKSTART.md`
- ✅ `DEPLOYMENT.md`
- ✅ `DEPLOYMENT_CHECKLIST.md`
- ✅ `STRIPE_SETUP.md`
- ✅ `FEATURES.md`
- ✅ `PROJECT_OVERVIEW.md`

**Štartovacie Skripty:**
- ✅ `start.sh`
- ✅ `start.bat`

**Demo Data:**
- ✅ `credits.json`

---

### ❌ NENAHRAJ TIETO SÚBORY (OBSAHUJÚ API KĽÚČE!):

- ❌ `.streamlit/secrets.toml` - OBSAHUJE API KĽÚČ!
- ❌ `payment_log.json` - lokálne dáta

**⚠️ DÔLEŽITÉ:** Súbor `.streamlit/secrets.toml` obsahuje tvoj API kľúč, NIKDY ho nenahrávaj na GitHub!

---

## 📤 KROK 2: Nahranie na GitHub (Web)

### 1️⃣ Otvor svoje repo
Choď na: https://github.com/petpnc/AI-price-expert

### 2️⃣ Klikni "Add file" → "Upload files"
(Tlačidlo je vpravo hore)

### 3️⃣ Pretiahni súbory
Môžeš:
- **Pretiahni** všetky súbory naraz z priečinka valueai
- Alebo **"choose your files"** a vyber ich

**⚠️ POZOR:** 
- Pretiahni všetko OKREM `.streamlit/secrets.toml`!
- GitHub automaticky ignoruje súbory uvedené v `.gitignore`

### 4️⃣ Napíš commit message
```
Initial commit - ValueAI with payments
```

### 5️⃣ Klikni "Commit changes"

---

## 🗂️ KROK 3: Vytvor .streamlit priečinok (ak ešte neexistuje)

GitHub neumožňuje nahrať prázdne priečinky, tak musíme vytvoriť `.streamlit` s placeholder súborom:

### 1️⃣ V tvojom repo klikni "Add file" → "Create new file"

### 2️⃣ Do "Name your file" napíš:
```
.streamlit/.gitkeep
```
(tým vytvoríš priečinok .streamlit)

### 3️⃣ Do obsahu súboru napíš:
```
# Placeholder file to keep directory in git
# Add your secrets.toml file here locally (do not commit!)
```

### 4️⃣ Klikni "Commit changes"

---

## 🔐 KROK 4: Nastavenie Secrets (Pre Streamlit Cloud)

Keď budeš nasadzovať na Streamlit Cloud:

### V Streamlit Cloud Dashboard → Settings → Secrets

Skopíruj obsah z `secrets.toml.example` a uprav:

```toml
# Google Gemini API Key (VYTVOR NOVÝ!)
GOOGLE_API_KEY = "tvoj-novy-api-kluc"

# Stripe Secret Key
STRIPE_SECRET_KEY = "sk_test_..."

# URLs
STRIPE_SUCCESS_URL = "https://ai-price-expert.streamlit.app?payment=success"
STRIPE_CANCEL_URL = "https://ai-price-expert.streamlit.app?payment=cancel"

# Admin Password
ADMIN_PASSWORD = "tvoje-silne-heslo"

# Credits
[credits]
DEMO-KEY = 3
TEST-KEY = 10
CLIENT-100 = 50
PREMIUM-2024 = 100
```

**⚠️ NEZABUDNI:**
1. Vytvoriť NOVÝ Google API kľúč (starý bol kompromitovaný)
2. Získať Stripe API kľúč
3. Zmeniť admin heslo
4. Upraviť URLs na tvoju doménu

---

## ✅ KROK 5: Overenie

Po nahratí skontroluj že máš:

```
AI-price-expert/
├── .gitignore
├── .streamlit/
│   └── .gitkeep
├── DEPLOYMENT.md
├── DEPLOYMENT_CHECKLIST.md
├── FEATURES.md
├── PROJECT_OVERVIEW.md
├── QUICKSTART.md
├── README.md
├── STRIPE_SETUP.md
├── admin.py
├── app.py
├── credits.json
├── payments.py
├── requirements.txt
├── secrets.toml.example
├── start.bat
└── start.sh
```

**Chýba:** `.streamlit/secrets.toml` - a to je OK! (bezpečnosť)

---

## 🚀 KROK 6: Nasadenie na Streamlit Cloud

Teraz môžeš nasadiť:

### 1️⃣ Choď na: https://streamlit.io/cloud

### 2️⃣ Klikni "New app"

### 3️⃣ Vyplň:
- **Repository:** `petpnc/AI-price-expert`
- **Branch:** `main`
- **Main file path:** `app.py`

### 4️⃣ Klikni "Deploy!"

### 5️⃣ Nastav Secrets (Settings → Secrets)
Vlož konfiguráciu z KROKU 4 vyššie

### 6️⃣ Počkaj ~2 minúty

**Tvoja app bude na:**
```
https://ai-price-expert.streamlit.app
```
(alebo podobná URL)

---

## 🎉 HOTOVO!

Máš teraz:
✅ Kód na GitHube
✅ Bezpečné secrets (nie v gite)
✅ Pripravené na cloud deploy

---

## 🆘 Časté Problémy

### ❌ "File too large"
GitHub má limit 100MB na súbor. Všetky naše súbory sú malé, takže by to nemalo byť problém.

### ❌ "Secrets not working"
Skontroluj že si v Streamlit Cloud Settings → Secrets správne nakopíroval konfiguráciu.

### ❌ "App not deploying"
Skontroluj že `requirements.txt` je nahratý správne.

---

## 📞 Ďalšie Kroky

1. ✅ Súbory nahrané na GitHub
2. 🔑 Vytvor nový Google API kľúč
3. 💳 Nastav Stripe
4. ☁️ Nasaď na Streamlit Cloud
5. 🎉 Začni predávať!

---

**Potrebuješ pomoc?** Daj vedieť kde si zastal!
