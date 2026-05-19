# Guide Power BI — Dashboard météo Maroc

## Connexion aux données

1. Ouvrir **Power BI Desktop**
2. **Accueil** → **Obtenir des données** → **JSON**
3. Parcourir vers :
   ```
   C:\Users\HP\Desktop\4IIR7\Decisionel POWER BI\weather_project\powerbi\weather_analytics.json
   ```
4. Sélectionner **Enregistrements** (tableau) → **Charger**

> Relancer `python scripts/run_pipeline.py` pour actualiser le fichier après chaque collecte.

## 4 visuels à créer (comme le rapport)

| Visuel | Type | Champ |
|--------|------|-------|
| Température par ville | Graphique en barres | Axe : `ville`, Valeur : `temperature` |
| Meilleure ville du jour | Carte (KPI) | Mesure : ville avec `classement` = 1 (ou MIN classement) |
| Classement | Table | `ville`, `score_meteo`, `classement`, `humidite` |
| Carte Maroc | Carte géographique | Emplacement : `ville`, Taille : `score_meteo` |

## Astuce carte géographique

Si les villes ne se placent pas automatiquement, ajouter une colonne **Latitude/Longitude** dans Power Query ou utiliser les villes reconnues par Bing Maps (Casablanca, Rabat, etc.).

## Sauvegarde

Enregistrer le rapport sous :
`Decisionel POWER BI\weather_project\powerbi\Dashboard_Meteo_Maroc.pbix`
