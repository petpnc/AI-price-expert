# 💳 STRIPE PLATOBNÁ BRÁNA - Kompletný Návod

## 🎯 Čo získaš

✅ **Automatické platby** - Klienti kupujú kredity kartou  
✅ **Bezpečné** - PCI compliant, používa Stripe  
✅ **Automatické licencie** - Generuje sa unikátny kľúč  
✅ **Email notifikácie** - Klient dostane kľúč na email  
✅ **Admin panel** - Správa kľúčov a platieb  
✅ **4 cenové plány** - Od €5 do €150  

---

## 📋 Krok za Krokom Setup (15 minút)

### 1️⃣ Vytvor Stripe Účet

1. Choď na: **https://dashboard.stripe.com/register**
2. Zaregistruj sa (zadarmo)
3. Potvrď email
4. Vyplň základné info o firme

**💡 Tip:** Môžeš začať v testovom režime (test mode) a neskôr aktivovať production.

---

### 2️⃣ Získaj API Kľúče

1. V Stripe Dashboard choď na: **Developers → API keys**
2. Uvidíš 2 kľúče:
   - **Publishable key** (pk_test_...) - verejný, netreba
   - **Secret key** (sk_test_...) - tento potrebuješ! 🔑

3. **Skopíruj Secret key** (klikni "Reveal test key")

**⚠️ DÔLEŽITÉ:** Secret key NIKDY nezdieľaj verejne!

---

### 3️⃣ Nastav v Streamlit Secrets

V Streamlit Cloud (Settings → Secrets) alebo v lokálnom `.streamlit/secrets.toml` pridaj:

```toml
# Stripe Secret Key
STRIPE_SECRET_KEY = "sk_test_..." # tvoj kľúč sem

# Success/Cancel URLs (upravte pre vašu doménu)
STRIPE_SUCCESS_URL = "https://tvoja-app.streamlit.app?payment=success"
STRIPE_CANCEL_URL = "https://tvoja-app.streamlit.app?payment=cancel"

# Admin heslo (zmeň!)
ADMIN_PASSWORD = "super-tajne-heslo-123"
```

**Pre lokálne testovanie:**
```toml
STRIPE_SUCCESS_URL = "http://localhost:8501?payment=success"
STRIPE_CANCEL_URL = "http://localhost:8501?payment=cancel"
```

---

### 4️⃣ Nainštaluj Stripe Knižnicu

```bash
pip install stripe==7.9.0
```

(Už je v `requirements.txt`, ale ak máš problémy spusti to manuálne)

---

### 5️⃣ Otestuj Platby (Test Mode)

1. Spusti aplikáciu
2. Klikni "Buy Credits Now"
3. Vyber cenový plán
4. Použi testovacie karty:

**Úspešná platba:**
```
Číslo karty: 4242 4242 4242 4242
CVC: ľubovoľné 3 čísla
Dátum: ľubovoľný budúci dátum
```

**Zamietnutá platba:**
```
Číslo karty: 4000 0000 0000 0002
```

5. Po úspešnej platbe dostaneš licenčný kľúč
6. Prihlás sa s novým kľúčom

**💡 Tip:** Všetky testovacie platby vidíš v Stripe Dashboard → Payments

---

### 6️⃣ Aktivuj Production Mode

Keď si pripravený akceptovať skutočné platby:

1. V Stripe Dashboard prepni **"Test mode" → OFF**
2. Vyplň business details
3. Pridaj banku account info
4. Prejdi verifikáciou
5. Získaj **production API key** (sk_live_...)
6. Uprav secrets.toml s production kľúčom

**⚠️ DÔLEŽITÉ:** 
- Test kľúče (sk_test_...) nefungujú v production
- Production kľúče (sk_live_...) akceptujú skutočné platby
- VŽDY použi test mode pri vývoji!

---

## 💰 Cenové Plány (Upraviteľné)

V súbore `payments.py` nájdeš sekciu `PRICING_PLANS`:

```python
PRICING_PLANS = {
    "starter": {
        "credits": 10,
        "price_eur": 5.00,
        ...
    },
    "professional": {
        "credits": 50,
        "price_eur": 20.00,
        ...
    }
}
```

**Môžeš zmeniť:**
- Počet kreditov
- Cenu
- Názvy plánov
- Popis a features

---

## ⚙️ Admin Panel

Spusti admin panel:

```bash
streamlit run admin.py
```

**Prihlasovacie heslo:** Nastav v secrets.toml (`ADMIN_PASSWORD`)

**Admin môže:**
- ✅ Vytvoriť nové licenčné kľúče
- ✅ Upraviť kredity existujúcich kľúčov
- ✅ Vymazať kľúče
- ✅ Vidieť históriu platieb
- ✅ Exportovať payment log do CSV
- ✅ Monitorovať systém status

---

## 📧 Email Notifikácie (Automatické)

Stripe automaticky posiela emaily:

1. **Payment receipt** - Potvrdenie platby
2. **Invoice** - Faktúra (ak ju povoliš)

Licenčný kľúč sa zobrazí po platbe na success page.

**Voliteľné:** Môžeš pridať vlastný email systém (SendGrid, AWS SES)

---

## 🔄 Workflow Celého Procesu

```
1. Klient klikne "Buy Credits"
   ↓
2. Vybrať cenový plán
   ↓
3. Stripe Checkout (bezpečná platba)
   ↓
4. Platba úspešná ✓
   ↓
5. Vygeneruje sa unikátny licenčný kľúč
   ↓
6. Kľúč sa pridá do systému s kreditmi
   ↓
7. Klient vidí svoj kľúč
   ↓
8. Prihlási sa a začne používať
```

---

## 📊 Monitorovanie a Štatistiky

### Stripe Dashboard

Môžeš sledovať:
- Počet transakcií
- Úspešnosť platieb
- Refundy
- Chargebacky
- Výnosy (daily/monthly)

### Admin Panel

Sleduj:
- Koľko licencií je aktívnych
- Celkový počet kreditov v systéme
- Payment history s exportom

---

## 💡 Pokročilé Funkcie (Voliteľné)

### 1. Subscription Model

Namiesto jednorazových platieb môžeš pridať mesačné predplatné:

```python
# V payments.py
mode='subscription'  # namiesto 'payment'
```

### 2. Discount Kódy

V Stripe Dashboard → Products → Coupons vytvoriť zľavové kódy.

### 3. Webhooks

Pre pokročilé tracking platieb nastav webhook:

1. Stripe Dashboard → Developers → Webhooks
2. Pridaj endpoint URL
3. Vyber eventy (checkout.session.completed)
4. Pridaj webhook handling do kódu

### 4. Vlastné Faktúry

Stripe môže generovať PDF faktúry automaticky.

---

## 🔒 Bezpečnosť

✅ **PCI Compliant** - Stripe je certifikovaný  
✅ **Secret keys** - Nikdy v kóde, len v secrets  
✅ **HTTPS** - Streamlit Cloud má automatic SSL  
✅ **Payment validation** - Verifikácia pred aktiváciou  
✅ **Test mode** - Vždy testuj pred production  

---

## 💸 Poplatky

**Stripe Fees (Europa):**
- **1.4% + €0.25** za transakciu (European cards)
- **2.9% + €0.25** za transakciu (non-European cards)

**Príklad:**
- Klient platí €20
- Stripe fee: €0.53
- Dostaneš: €19.47

**💡 Tip:** Môžeš zahrnúť fees do ceny alebo pridať "processing fee" pri checkout.

---

## 🆘 Časté Problémy

### ❌ "Stripe module not found"
```bash
pip install stripe==7.9.0
```

### ❌ "Invalid API key"
- Skontroluj že kľúč začína `sk_test_` alebo `sk_live_`
- Skontroluj že je v secrets.toml správne
- Bez medzier

### ❌ "Payment succeeded but no license created"
- Skontroluj logs v Streamlit
- Skontroluj že `save_credits()` funguje
- Možno problém s file permissions

### ❌ "Redirect URLs not working"
- URL musí byť PRESNE ako v secrets
- Obsahuje `?payment=success`
- Pre local dev: `http://localhost:8501?payment=success`
- Pre cloud: `https://tvoja-app.streamlit.app?payment=success`

---

## 📈 Optimalizácia Konverzií

**Tipy pre viac predajov:**

1. **Jasné ceny** - Zobraz hodnotu (€/credit)
2. **Social proof** - "100+ spokojných klientov"
3. **Urgency** - "Limitovaná ponuka"
4. **Risk reversal** - "14-day money back guarantee"
5. **Free trial** - DEMO-KEY so 3 kreditmi
6. **Bundle discount** - "Save 40% with Enterprise plan"

---

## 🎯 Checklist Pred Spustením

- [ ] Stripe účet vytvorený
- [ ] API kľúče získané
- [ ] Secrets.toml nakonfigurovaný
- [ ] Testovacia platba úspešná
- [ ] Admin panel funguje
- [ ] Production mode aktivovaný (keď si pripravený)
- [ ] Banku account info v Stripe
- [ ] Terms & Conditions pridané
- [ ] Privacy Policy pridaná
- [ ] Email support nastavený

---

## 📞 Support

**Stripe Support:**
- Email: support@stripe.com
- Chat v Dashboard
- Docs: https://stripe.com/docs

**ValueAI Support:**
- Admin panel pre správu
- Stripe Dashboard pre transakcie
- Payment log pre audity

---

## 🎉 Všetko Funguje?

Gratulujem! Máš teraz:

✅ Plne funkčnú platobnú bránu  
✅ Automatické generovanie licencií  
✅ Admin panel pre správu  
✅ 4 cenové plány  
✅ Bezpečné platby cez Stripe  

**Ďalšie kroky:**
1. Zdieľaj odkaz s prvými klientmi
2. Monitoruj platby v Stripe Dashboard
3. Optimalizuj ceny podľa dopytu
4. Pridaj marketing (social media, ads)

Veľa úspechov s predajom! 💰🚀
