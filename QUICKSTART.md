# 🚀 RÝCHLY ŠTART - Okamžité Spustenie

## ✅ Všetko je pripravené!

API kľúč je nakonfigurovaný a môžeš **ihneď spustiť** aplikáciu lokálne.

---

## 📥 Krok 1: Stiahni projekt

Stiahni celý priečinok `valueai` s všetkými súbormi.

---

## 🔧 Krok 2: Nainštaluj závislosti

Otvor terminál v priečinku `valueai` a spusti:

```bash
pip install -r requirements.txt
```

---

## ▶️ Krok 3: Spusti aplikáciu

```bash
streamlit run app.py
```

Aplikácia sa automaticky otvorí v prehliadači na:
```
http://localhost:8501
```

---

## 🔐 Krok 4: Prihlás sa

Použi jeden z demo kľúčov:

- **DEMO-KEY** - 3 kredity
- **TEST-KEY** - 10 kreditov
- **CLIENT-100** - 50 kreditov

---

## 📸 Krok 5: Otestuj

1. Nahraj alebo vyfot nejakú vec
2. Klikni "Analyze Item"
3. Počkaj 5-10 sekúnd
4. Uvidíš odhad cien a predajný popis

---

## ⚠️ DÔLEŽITÉ BEZPEČNOSTNÉ UPOZORNENIE!

Tvoj API kľúč bol zdieľaný v chate, čo znamená že je **kompromitovaný**.

### Po úspešnom otestovaní aplikácie MUSÍŠ:

1. Choď na: https://makersuite.google.com/app/apikey
2. **Vymaž** existujúci kľúč: `AIzaSyAZhT3KVOWS1UtkmN4d0HBFpFlsvELyf5Y`
3. **Vytvor nový** kľúč
4. **Uprav** `.streamlit/secrets.toml` s novým kľúčom

### Pre Streamlit Cloud:
Keď budeš nasadzovať na cloud, **MUSÍŠ** použiť nový (nepoužitý) kľúč!

---

## 📱 Prístup z mobilu (voliteľné)

Ak chceš otvoriť na mobile v rovnakej WiFi sieti:

1. Zisti svoju IP adresu:
   ```bash
   # Mac/Linux
   ifconfig | grep "inet "
   
   # Windows
   ipconfig
   ```

2. Na mobile otvor:
   ```
   http://192.168.X.X:8501
   ```
   (použi svoju IP adresu)

---

## 🎯 Ďalšie kroky:

- ✅ Otestuj lokálne
- 🔑 Regeneruj API kľúč
- ☁️ Nasaď na Streamlit Cloud (pozri DEPLOYMENT.md)
- 💳 Nastav Stripe platby (pozri STRIPE_SETUP.md)
- ⚙️ Otestuj admin panel (`streamlit run admin.py`)
- 💰 Začni predávať prístupy klientom

---

## 💳 Platobný Systém (Voliteľné)

Ak chceš povoliť online nákup kreditov:

1. Prečítaj **STRIPE_SETUP.md**
2. Vytvor Stripe účet
3. Pridaj API kľúč do secrets.toml
4. Klienti môžu kupovať kredity priamo v app

**Cenové plány:**
- Starter: €5 (10 kreditov)
- Professional: €20 (50 kreditov)
- Business: €50 (150 kreditov)
- Enterprise: €150 (500 kreditov)

---

## ⚙️ Admin Panel

Správa licencií a platieb:

```bash
streamlit run admin.py
```

**Funkcie:**
- Vytváranie nových licenčných kľúčov
- Úprava existujúcich kreditov
- Prezeranie payment history
- Export do CSV
- Systémové štatistiky

**Heslo:** Nastav v `.streamlit/secrets.toml` ako `ADMIN_PASSWORD`

---

## 🆘 Problémy?

### "Module not found"
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### "Port already in use"
```bash
streamlit run app.py --server.port 8502
```

### App sa neotvára
Manuálne otvor: http://localhost:8501

---

## 📊 Monitoring používania API

Google ti umožňuje sledovať:
- Počet API volaní
- Náklady (Flash model je veľmi lacný)
- Quota limity

Dashboard: https://console.cloud.google.com/apis/dashboard

---

Všetko funguje? Paráda! 🎉

Nejaký problém? Daj vedieť!
