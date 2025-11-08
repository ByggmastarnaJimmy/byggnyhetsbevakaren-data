# Byggnyhetsbevakaren – Automatiserad nyhetsinsamling

Detta projekt automatiserar insamling och sammanställning av byggnyheter från olika källor, uppdaterar en JSON-fil i GitHub och gör den tillgänglig för Power Automate.

## 📌 Översikt
- **Python-script (`generate_summary.py`)** hämtar nyheter från definierade källor, sammanfattar dem och sparar i `sammanfattning.json`.
- **Fallback med dummy-data** används om en källa inte svarar.
- **GitHub Action (`update-sammanfattning.yml`)** kör scriptet varje natt kl. 02:00 och pushar uppdaterad fil.
- **Power Automate** hämtar `sammanfattning.json` från GitHub Pages och skickar e-post med nyheterna.

## ✅ Flöde steg för steg
1. **Scriptet körs** via GitHub Action:
   - Hämtar nyheter från Byggfakta, Byggföretagen och Byggnads.
   - Skapar en JSON-struktur med kategorier och dagens pepp.
   - Sparar filen som `sammanfattning.json`.

2. **GitHub Action**:
   - Kör scriptet enligt cron-schema (varje natt kl. 02:00).
   - Commitar och pushar ändringar till din branch.

3. **Power Automate**:
   - Hämtar `sammanfattning.json` från GitHub Pages.
   - Skickar e-post med nyheterna.

## 🛠 Installation
1. Skapa mappstruktur:
   ```
   scripts/
   .github/workflows/
   ```
2. Lägg in:
   - `scripts/generate_summary.py`
   - `.github/workflows/update-sammanfattning.yml`
   - `sammanfattning.json` (första versionen eller dummy-data)

3. Aktivera GitHub Pages för din branch.

## 🔍 JSON-struktur
Exempel på `sammanfattning.json`:
```json
{
  "datum": "2025-11-08",
  "nyheter": {
    "Projekt": [
      {
        "titel": "Exempelprojekt i Stockholm",
        "källa": "Byggfakta",
        "url": "https://www.byggfakta.se/exempelprojekt"
      }
    ],
    "Bransch": [
      {
        "titel": "Byggföretagen satsar på hållbarhet",
        "källa": "Byggföretagen",
        "url": "https://www.byggforetagen.se/hallbarhet"
      }
    ],
    "Arbetsmarknad": [
      {
        "titel": "Byggnads lanserar nytt utbildningsprogram",
        "källa": "Byggnads",
        "url": "https://www.byggnads.se/utbildning"
      }
    ]
  },
  "dagens_pepp": "Byggbranschen växer – tillsammans bygger vi framtiden!"
}
```

## ⚠ Fallback med dummy-data
Om en källa inte svarar, lägger scriptet in fördefinierade nyheter så att filen alltid blir komplett.

## ▶ Manuell körning
Du kan köra workflow manuellt via GitHub:
- Gå till **Actions** → **update-sammanfattning.yml** → **Run workflow**.

## 🔗 Power Automate
Använd GitHub Pages-URL för `sammanfattning.json` som datakälla i ditt flöde.

---
Lycka till med Byggnyhetsbevakaren! 🚀
