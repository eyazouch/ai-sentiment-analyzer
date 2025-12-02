from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pymongo
from datetime import datetime
import re

# Connexion MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["social_sentiment"]
collection = db["posts"]

# Initialisation des analyseurs
vader = SentimentIntensityAnalyzer()

def clean_text(text):
    """Nettoie le texte avant analyse"""
    # Supprimer les URLs
    text = re.sub(r'http\S+|www\S+', '', text)
    # Supprimer les mentions @
    text = re.sub(r'@\w+', '', text)
    # Supprimer les espaces multiples
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def analyze_sentiment(text):
    """Analyse le sentiment d'un texte"""
    # Nettoyage
    clean = clean_text(text)
    
    # Analyse TextBlob
    blob = TextBlob(clean)
    textblob_score = blob.sentiment.polarity
    
    # Analyse VADER
    vader_scores = vader.polarity_scores(clean)
    vader_score = vader_scores['compound']
    
    # Score final (moyenne pondérée)
    final_score = (textblob_score * 0.5) + (vader_score * 0.5)
    
    # Classification
    if final_score > 0.05:
        sentiment = "positive"
    elif final_score < -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    
    # Calcul de la confiance
    agreement = abs(textblob_score - vader_score)
    confidence = 1 - (agreement / 2)  # Plus ils sont d'accord, plus la confiance est haute
    
    return {
        "sentiment": sentiment,
        "score": round(final_score, 3),
        "textblob_score": round(textblob_score, 3),
        "vader_compound": round(vader_score, 3),
        "confidence": round(confidence, 3)
    }

def analyze_all_posts():
    """Analyse tous les posts dans MongoDB"""
    print("🧠 Analyse de sentiments en cours...")
    
    total = collection.count_documents({})
    print(f"📊 Total de posts à analyser : {total}")
    
    analyzed = 0
    errors = 0
    
    # Récupérer tous les posts
    posts = collection.find({})
    
    for post in posts:
        try:
            # Analyser le sentiment
            sentiment_data = analyze_sentiment(post['text'])
            
            # Mettre à jour le document MongoDB
            collection.update_one(
                {"_id": post["_id"]},
                {
                    "$set": {
                        "sentiment_analysis": sentiment_data,
                        "analyzed_at": datetime.now()
                    }
                }
            )
            
            analyzed += 1
            
            # Afficher la progression
            if analyzed % 500 == 0:
                print(f"  ✅ {analyzed}/{total} posts analysés...")
                
        except Exception as e:
            errors += 1
            print(f"  ❌ Erreur sur post {post.get('id', 'unknown')}: {str(e)}")
    
    print(f"\n✅ Analyse terminée !")
    print(f"  - Posts analysés : {analyzed}")
    print(f"  - Erreurs : {errors}")
    
    # Statistiques finales
    print("\n📊 DISTRIBUTION DES SENTIMENTS :")
    pipeline = [{"$group": {"_id": "$sentiment_analysis.sentiment", "count": {"$sum": 1}}}]
    for result in collection.aggregate(pipeline):
        sentiment = result['_id'] if result['_id'] else "Non analysé"
        count = result['count']
        percentage = (count / total) * 100
        print(f"  • {sentiment}: {count} ({percentage:.1f}%)")
    
    print("\n✨ Analyse de sentiments terminée !")

if __name__ == "__main__":
    analyze_all_posts()