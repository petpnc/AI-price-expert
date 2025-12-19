# 🚀 NÁVOD: Nasadenie ValueAI na Streamlit Cloud

## ✨ Prečo Streamlit Cloud?

✅ **Zadarmo** - Free tier navždy
✅ **Automatické updaty** - Push to GitHub = automatický deploy
✅ **HTTPS** - Bezpečné pripojenie zadarmo
✅ **Verejná URL** - Zdieľaj odkaz s klientmi
✅ **Mobilný prístup** - Funguje odkiaľkoľvek

---

## 📋 Krok za krokom (10 minút)

### 1️⃣ Vytvor GitHub účet (ak nemáš)

1. Choď na: **https://github.com/signup**
2. Zaregistruj sa (zadarmo)
3. Potvrď email

### 2️⃣ Vytvor nové GitHub repository

1. Prihlás sa na GitHub
2. Klikni na **"+"** vpravo hore → **"New repository"**
3. Vyplň:
   - **Repository name**: `valueai`
   - **Description**: "AI Item Valuation App"
   - **Public** alebo **Private** (obe fungujú)
   - ✅ Zaškrtni **"Add a README file"**
4. Klikni **"Create repository"**

### 3️⃣ Nahraj súbory na GitHub

**Možnosť A - Cez Web (jednoduchšie):**

1. V tvojom repository klikni **"Add file"** → **"Upload files"**
2. Pretiahni všetky súbory OKREM:
   - ❌ `.streamlit/secrets.toml` (tento nastavíme osobitne)
   - ❌ `credits.json` (vytvorí sa automaticky)
3. Nahraj:
   - ✅ `app.py`
   - ✅ `requirements.txt`
   - ✅ `README.md`
   - ✅ `.gitignore`
4. Klikni **"Commit changes"**

**Možnosť B - Cez Git (pokročilé):**

```bash
cd valueai
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/TVOJE-MENO/valueai.git
git push -u origin main
```

### 4️⃣ Získaj Google Gemini API kľúč

1. Otvor: **https://makersuite.google.com/app/apikey**
2. Prihlás sa Google účtom
3. Klikni **"Create API Key"**
4. **Skopíruj kľúč** (budeš ho potrebovať o chvíľu!)

### 5️⃣ Vytvor Streamlit Cloud účet

1. Choď na: **https://streamlit.io/cloud**
2. Klikni **"Sign up"**
3. Prihlás sa cez **GitHub účet** (odporúčané)
4. Autorizuj Streamlit prístup k tvojim repositories

### 6️⃣ Nasaď aplikáciu

1. Po prihlásení klikni **"New app"**
2. Vyplň:
   - **Repository**: Vyber `valueai`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. Klikni **"Deploy!"**

### 7️⃣ Nastav API kľúč (DÔLEŽITÉ!)

**Aplikácia bude mať chybu, to je OK! Musíme nastaviť API kľúč:**

1. Po deployi klikni na **"⚙️ Settings"** (vpravo dole)
2. Klikni na záložku **"Secrets"**
3. Do textového poľa vlož:
   ```toml
   GOOGLE_API_KEY = "tvoj-skopírovany-api-kluc-sem"
   ```
   (nahraď `tvoj-skopírovany-api-kluc-sem` skutočným kľúčom!)
4. Klikni **"Save"**
5. Aplikácia sa automaticky reštartuje

### 8️⃣ Otestuj aplikáciu

1. Počkaj 30 sekúnd kým sa app reštartuje
2. Tvoja app bude na URL typu:
   ```
   https://valueai-nazov.streamlit.app
   ```
3. Prihlás sa s demo kľúčom: `DEMO-KEY`
4. Nahraj testovú fotku
5. Funguje? 🎉

---

## 🔑 Správa Licenčných Kľúčov na Cloude

### Problém:
`credits.json` sa na cloude po reštarte zmaže (containerizované prostredie).

### Riešenie:
Použi Streamlit Secrets aj pre kredity!

**Upravená verzia - Nastav v Secrets:**

```toml
GOOGLE_API_KEY = "tvoj-api-kluc"

# Licenčné kľúče a kredity
[credits]
DEMO-KEY = 3
CLIENT-100 = 50
PREMIUM-2024 = 100
TEST-KEY = 10
NOVY-KLIENT = 25
```

**Potom upravíme `app.py`** (tu je opravená funkcia):

Nahraď funkciu `load_credits()` v `app.py` takto:

```python
def load_credits():
    """Load credits from Streamlit secrets (cloud) or JSON file (local)."""
    try:
        # Try to load from Streamlit secrets (for cloud deployment)
        if "credits" in st.secrets:
            return dict(st.secrets["credits"])
    except:
        pass
    
    # Fallback to local JSON file
    if not os.path.exists(CREDITS_FILE):
        default_credits = {
            "DEMO-KEY": 3,
            "CLIENT-100": 50,
            "PREMIUM-2024": 100
        }
        save_credits(default_credits)
        return default_credits
    
    try:
        with open(CREDITS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading credits: {e}")
        return {}
```

---

## 📱 Zdieľanie s Klientmi

Tvoja app je teraz verejne dostupná na:
```
https://valueai-XYZ.streamlit.app
```

**Môžeš:**
- Zdieľať link s klientmi
- Vytvoriť QR kód pre ľahký prístup
- Pridať do svojho webu cez iframe
- Zdieľať na sociálnych sieťach

**Licenčné kľúče:**
- Každému klientovi dáš iný kľúč
- Nastavíš kredity v Secrets
- Klient sa prihlási svojím kľúčom

---

## 🔄 Ako Updatovať Aplikáciu

1. Uprav kód lokálne v `app.py`
2. Nahraj nový súbor na GitHub (cez web alebo git push)
3. Streamlit Cloud automaticky zdetekuje zmenu
4. App sa sama updatuje za ~1 minútu

---

## ⚙️ Pokročilé Nastavenia

### Vlastná Doména
Streamlit Cloud podporuje vlastné domény (napr. `valueai.tvojadomena.sk`):
1. Settings → Custom domain
2. Pridaj CNAME záznam v DNS

### Monitoring
- Dashboard ukazuje počet návštev
- Logy pre debugging
- Resource usage

### Password Protection
V Settings môžeš pridať heslo pre celú app.

---

## 🆘 Časté Problémy

### ❌ "Error loading API key"
- Skontroluj že API kľúč je správne v Secrets
- Bez medzier okolo `=`
- V úvodzovkách

### ❌ "Module not found"
- Skontroluj `requirements.txt`
- Verzie musia byť kompatibilné

### ❌ Kredity sa resetujú
- Použi Secrets pre kredity (nie JSON súbor)
- JSON funguje len lokálne

### ❌ App je pomalá
- Gemini Flash je rýchly, ale prvý cold start trvá
- Po prvom použití je rýchla

---

## 💰 Ceny Streamlit Cloud

**Free Tier (zadarmo navždy):**
- 1 súkromná app
- Neobmedzené verejné apps
- 1 GB RAM
- Dostatočné pre ValueAI

**Paid Tier (ak potrebuješ viac):**
- Od $20/mesiac
- Viac RAM a CPU
- Priority support

---

## 🎯 Checklist Pred Spustením

- [ ] GitHub repository vytvorené
- [ ] Súbory nahrané (app.py, requirements.txt, README.md)
- [ ] Streamlit Cloud účet vytvorený
- [ ] App nasadená
- [ ] Google API kľúč v Secrets
- [ ] Kredity nastavené v Secrets
- [ ] Testovacia analýza funguje
- [ ] URL zdieľaná s prvým klientom

---

## 🚀 Ďalšie Kroky

Po úspešnom nasadení môžeš:

1. **Pridať Analytics** - Google Analytics tracking
2. **Pridať Platby** - Stripe/PayPal integrácia
3. **Custom Branding** - Logo, farby, font
4. **Multi-language** - Angličtina, nemčina, atď.
5. **Admin Panel** - Správa kľúčov cez UI

---

Máš otázky? Píš mi!
