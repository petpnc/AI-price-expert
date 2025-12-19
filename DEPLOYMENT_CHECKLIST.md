# ✅ STREAMLIT CLOUD - Deployment Checklist

## 📦 Súbory na Upload na GitHub:

✅ app.py
✅ requirements.txt
✅ README.md
✅ .gitignore
❌ .streamlit/secrets.toml (NENAHRAJ - nastav v Streamlit Cloud UI!)
❌ credits.json (NENAHRAJ - vytvorí sa automaticky)

## 🔑 Kľúče ktoré potrebuješ:

1. **GitHub účet** → https://github.com/signup
2. **Google Gemini API kľúč** → https://makersuite.google.com/app/apikey
3. **Streamlit Cloud účet** → https://streamlit.io/cloud

## 📝 Postup (5 krokov):

### Krok 1: GitHub
- [ ] Vytvor nové repository (napr. "valueai")
- [ ] Nahraj súbory: app.py, requirements.txt, README.md, .gitignore

### Krok 2: Google API
- [ ] Získaj Gemini API kľúč
- [ ] Skopíruj si ho (budeš ho potrebovať!)

### Krok 3: Streamlit Cloud
- [ ] Zaregistruj sa (použi GitHub login)
- [ ] Klikni "New app"
- [ ] Vyber tvoje valueai repository

### Krok 4: Secrets
- [ ] Choď do Settings → Secrets
- [ ] Vlož obsah z `secrets.toml.example`
- [ ] Nahraď "your-google-api-key-here" skutočným API kľúčom
- [ ] Save

### Krok 5: Test
- [ ] Počkaj kým sa app nasadí (~2 min)
- [ ] Otvor URL (napr. https://valueai-abc123.streamlit.app)
- [ ] Prihlás sa: DEMO-KEY
- [ ] Otestuj analýzu fotky

## 🎉 Hotovo!

Tvoja app je live na internete!

## 📱 Ďalšie kroky:

- Zdieľaj URL s klientmi
- Vytvor nové licenčné kľúče v Secrets
- Uprav dizajn podľa potreby

## 🆘 Problémy?

Prečítaj si `DEPLOYMENT.md` pre detailný návod!
