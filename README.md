# 🎓 Projet NoSQL : Analyseur de Sentiments sur les Outils IA

**Projet académique - Cours NoSQL**

Analyse de sentiments en temps réel sur les outils d'Intelligence Artificielle en utilisant une architecture basée sur les bases de données NoSQL (MongoDB + Elasticsearch).

![Python](https://img.shields.io/badge/Python-3.12-blue)
![MongoDB](https://img.shields.io/badge/MongoDB-7.0-47A248)
![Elasticsearch](https://img.shields.io/badge/Elasticsearch-8.11-005571)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)

---

## 📚 Contexte académique

### Cours
**NoSQL et Big Data**

### Objectifs pédagogiques
- Comprendre les différences entre bases de données NoSQL
- Maîtriser MongoDB (base orientée documents)
- Maîtriser Elasticsearch (base orientée recherche)
- Implémenter un pipeline ETL
- Analyser des données non structurées
- Créer des visualisations de données

---

## 📋 Description du projet

Ce projet analyse les sentiments (positif, négatif, neutre) exprimés sur les réseaux sociaux concernant **25+ outils d'IA** populaires (ChatGPT, Claude, Midjourney, GitHub Copilot, etc.).

### 🎯 Problématique

Comment collecter, stocker et analyser efficacement les opinions sur les outils IA en utilisant des bases de données NoSQL ?

### 💡 Solution proposée

Une architecture complète utilisant :
- **MongoDB** pour le stockage flexible de posts avec sentiments
- **Elasticsearch** pour l'indexation et la recherche rapide
- **Kibana** pour la visualisation interactive
- **Python** pour le traitement et l'analyse NLP

---

## 🏗️ Architecture technique

```
┌──────────────────┐
│  Data Generator  │ ──► Génère 3000+ posts simulés
│    (Python)      │     avec Faker
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│    MongoDB       │ ──► Base NoSQL orientée documents
│  (Document DB)   │     Stockage flexible, schéma dynamique
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Sentiment NLP    │ ──► Analyse avec TextBlob + VADER
│    (Python)      │     Classification: pos/neg/neutral
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│   Python ETL     │ ──► Pipeline Extract-Transform-Load
│                  │     Transformation des données
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Elasticsearch    │ ──► Base NoSQL orientée recherche
│  (Search DB)     │     Indexation par date, agrégations
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│     Kibana       │ ──► Dashboards interactifs
│ (Visualization)  │     Analyse visuelle des données
└──────────────────┘
```

---

## 🔍 Choix des bases de données NoSQL

### Pourquoi MongoDB ?

**Type** : Base de données orientée documents (Document Store)

**Avantages pour ce projet** :
- ✅ Schéma flexible adapté aux posts de réseaux sociaux
- ✅ Stockage de documents JSON natif
- ✅ Requêtes et agrégations puissantes
- ✅ Scalabilité horizontale
- ✅ Facilité d'insertion de données hétérogènes

**Exemple de document** :
```json
{
  "_id": "ObjectId(...)",
  "text": "ChatGPT est incroyable !",
  "user": {
    "name": "Jean Dupont",
    "followers": 1250
  },
  "created_at": "2025-11-30T10:00:00Z",
  "sentiment_analysis": {
    "sentiment": "positive",
    "score": 0.85
  },
  "topic": "ChatGPT",
  "category": "Chatbots & LLMs"
}
```

### Pourquoi Elasticsearch ?

**Type** : Base de données orientée recherche (Search Engine)

**Avantages pour ce projet** :
- ✅ Recherche full-text ultra-rapide
- ✅ Agrégations en temps réel pour analytics
- ✅ Indexation optimisée par date
- ✅ Intégration native avec Kibana
- ✅ Queries complexes et filtres multiples

**Cas d'usage** :
- Recherche par mots-clés
- Agrégations (moyenne sentiment par outil)
- Analyse temporelle
- Filtres combinés (date + sentiment + catégorie)

---

## 🛠️ Technologies utilisées

### Bases de données NoSQL
- **MongoDB 7.0** - Document Store
- **Elasticsearch 8.11** - Search Engine

### Backend & Processing
- **Python 3.12** - Langage principal
- **TextBlob** - Analyse de sentiments
- **VADER Sentiment** - NLP pour réseaux sociaux
- **Faker** - Génération de données réalistes

### Visualisation
- **Kibana 8.11** - Dashboards interactifs

### DevOps
- **Docker Compose** - Orchestration des services

---

## 📦 Installation

### Prérequis

- Docker Desktop (8+ GB RAM allouée)
- Python 3.10+
- Git

### Installation complète

```bash
# 1. Cloner le repository
git clone https://github.com/eyazouch/ai-sentiment-analyzer.git
cd ai-sentiment-analyzer

# 2. Créer l'environnement virtuel Python
python -m venv venv
.\venv\Scripts\Activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. Installer les dépendances
pip install -r requirements.txt
python -m textblob.download_corpora

# 4. Démarrer l'infrastructure Docker
docker-compose up -d

# 5. Vérifier que tout fonctionne
# MongoDB : http://localhost:27017
# Elasticsearch : http://localhost:9200
# Kibana : http://localhost:5601
```

---

## 🚀 Utilisation

### Configuration initiale (une seule fois)

```powershell
# 1. Naviguer vers le projet
cd *your directory*\ai-sentiment-analyzer

# 2. Créer l'environnement virtuel Python
python -m venv venv

# 3. Activer l'environnement virtuel
.\venv\Scripts\Activate  # Windows PowerShell
# source venv/bin/activate  # Mac/Linux

# 4. Installer toutes les dépendances
.\venv\Scripts\pip install -r requirements.txt

# 5. Télécharger les modèles linguistiques NLP
.\venv\Scripts\python -m textblob.download_corpora

# 6. Démarrer l'infrastructure Docker
docker-compose up -d

# 7. Attendre 30 secondes que tout démarre
# Vérifier que les 4 containers sont actifs:
docker-compose ps
```

### Pipeline de données (workflow principal)

**⚠️ Important:** Exécuter ces commandes dans l'ordre !

```powershell
# Activer l'environnement virtuel (si pas déjà fait)
.\venv\Scripts\Activate

# Étape 1 : Générer 3000 posts simulés
.\venv\Scripts\python data\data_generator.py
# ✅ Crée 3000 posts sur les outils IA dans MongoDB

# Étape 2 : Analyser les sentiments (NLP)
.\venv\Scripts\python analysis\sentiment_analyzer.py
# ✅ Analyse chaque post avec TextBlob + VADER

# Étape 3 : Transférer vers Elasticsearch
.\venv\Scripts\python scripts\mongodb_to_elasticsearch.py
# ✅ Indexe les données pour Kibana

# Étape 4 : Visualiser dans Kibana
# Ouvrir http://localhost:5601 dans votre navigateur
```

### Configuration de Kibana (première utilisation)

1. **Ouvrir Kibana** : http://localhost:5601

2. **Créer une Data View** :
   - Menu ☰ → Management → Stack Management
   - Kibana → Data Views → Create data view
   - **Index pattern** : `ai-sentiment-*`
   - **Timestamp field** : `@timestamp`
   - Cliquer sur "Save data view to Kibana"

3. **Explorer les données** :
   - Menu ☰ → Analytics → Discover
   - Sélectionner "AI Sentiment Analysis"
   - **Ajuster le filtre temporel** : Cliquer "Last 15 minutes" → Choisir "Last 30 days"
   - Vous devriez voir **3000 documents** !

4. **Créer des visualisations** :
   - Menu ☰ → Analytics → Visualize Library
   - Exemples :
     - Pie chart : Distribution des sentiments
     - Bar chart : Top outils IA
     - Line chart : Évolution temporelle

### Commandes utiles

```powershell
# Vérifier les données dans MongoDB
docker exec -it sentiment_mongodb mongosh social_sentiment --eval "db.posts.countDocuments()"

# Vérifier les données dans Elasticsearch
Invoke-WebRequest -Uri "http://localhost:9200/ai-sentiment-*/_count" -UseBasicParsing | Select-Object -ExpandProperty Content

# Voir les logs Logstash
docker logs sentiment_logstash --tail 50

# Redémarrer un service
docker-compose restart logstash

# Effacer toutes les données MongoDB
docker exec -it sentiment_mongodb mongosh social_sentiment --eval "db.posts.deleteMany({})"

# Effacer les indices Elasticsearch
Invoke-WebRequest -Method DELETE -Uri "http://localhost:9200/ai-sentiment-*"
```

---

## 📊 Dataset généré

### Statistiques

- **Volume** : 3000+ documents
- **Outils IA** : 25+ (ChatGPT, Claude, Midjourney, GitHub Copilot, etc.)
- **Catégories** : 8 (Chatbots, Générateurs d'images, Coding assistants, etc.)
- **Distribution** : ~40% positif, ~30% négatif, ~30% neutre
- **Langues** : Français (60%), Anglais (40%)
- **Période** : 10 derniers jours glissants

### Structure des données

**MongoDB (Collection: posts)**
```javascript
{
  id: "uuid",
  text: "ChatGPT est incroyable !",
  user: { name, followers, location },
  created_at: ISODate,
  likes: 145,
  retweets: 23,
  topic: "ChatGPT",
  category: "Chatbots & LLMs",
  sentiment_analysis: {
    sentiment: "positive",
    score: 0.78,
    confidence: 0.92
  }
}
```

**Elasticsearch (Index: ai-sentiment-YYYY.MM.DD)**
```javascript
{
  "@timestamp": "2025-11-30T10:00:00Z",
  "text": "ChatGPT est incroyable !",
  "user_name": "Jean Dupont",
  "sentiment_label": "positive",
  "sentiment_score": 0.78,
  "topic": "ChatGPT",
  "category": "Chatbots & LLMs"
}
```

---

## 🔬 Analyse NLP

### Algorithmes utilisés

**TextBlob** : 
- Basé sur un dictionnaire de polarité
- Score : -1 (très négatif) à +1 (très positif)
- Meilleur pour textes formels

**VADER** :
- Spécialisé pour réseaux sociaux
- Comprend emojis, majuscules, ponctuation
- Meilleur pour textes informels

**Score final** : Moyenne pondérée des deux algorithmes

### Classification

```python
if score > 0.05:  → "positive"
if score < -0.05: → "negative"
else:             → "neutral"
```

---

## 📁 Structure du projet

```
ai-sentiment-analyzer/
├── data/
│   └── data_generator.py          # Génération 3000 posts
├── analysis/
│   └── sentiment_analyzer.py      # NLP (TextBlob + VADER)
├── scripts/
│   └── mongodb_to_elasticsearch.py # Pipeline ETL
├── logstash/
│   └── config/                    # Config (non utilisé finalement)
├── docker-compose.yml             # MongoDB + Elasticsearch + Kibana
├── requirements.txt               # Dépendances Python
└── README.md                      # Documentation
```

---

## 💡 Concepts NoSQL appliqués

### MongoDB

- ✅ **Schéma flexible** : Ajout de champs dynamiquement
- ✅ **Documents imbriqués** : user{}, sentiment_analysis{}
- ✅ **Index** : created_at, topic, sentiment
- ✅ **Agrégations** : $group, $match, $count

### Elasticsearch

- ✅ **Mapping** : Définition des types de champs
- ✅ **Index par date** : ai-sentiment-YYYY.MM.DD
- ✅ **Recherche full-text** : Analyse de texte
- ✅ **Agrégations** : Terms, Average, Date Histogram

---

## 📈 Dashboards Kibana (en cours)

- [ ] Vue d'ensemble (KPIs, distribution sentiments)
- [ ] Analyse temporelle (évolution dans le temps)
- [ ] Comparaison outils IA
- [ ] Analyse géographique
- [ ] Top influenceurs

---

## 🎓 Apprentissages

### Techniques
- Architecture NoSQL multi-bases
- Pipeline ETL complet
- Analyse de sentiments (NLP)
- Visualisation de données
- Docker & orchestration

### Théoriques
- Différences Document Store vs Search Engine
- Choix de la base selon le cas d'usage
- Scalabilité horizontale
- Indexation et performance

---

## 👥 Auteurs

**Eya Zouch**
- GitHub: [@eyazouch](https://github.com/eyazouch)

**Ahmed Messoudi**
- GitHub: 



---

## 📝 Licence

Projet académique - Tous droits réservés
