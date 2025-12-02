import random
from datetime import datetime, timedelta
from faker import Faker
import pymongo
import uuid

# ========== BASE DE DONNÉES DES OUTILS IA ==========

AI_TOOLS = [
    {"name": "ChatGPT", "category": "Chatbots & LLMs", "company": "OpenAI"},
    {"name": "Claude", "category": "Chatbots & LLMs", "company": "Anthropic"},
    {"name": "Gemini", "category": "Chatbots & LLMs", "company": "Google"},
    {"name": "Copilot", "category": "Chatbots & LLMs", "company": "Microsoft"},
    {"name": "Llama", "category": "Chatbots & LLMs", "company": "Meta"},
    {"name": "Midjourney", "category": "Generateurs Images", "company": "Midjourney"},
    {"name": "DALL-E", "category": "Generateurs Images", "company": "OpenAI"},
    {"name": "Stable Diffusion", "category": "Generateurs Images", "company": "Stability AI"},
    {"name": "Leonardo AI", "category": "Generateurs Images", "company": "Leonardo"},
    {"name": "Firefly", "category": "Generateurs Images", "company": "Adobe"},
    {"name": "GitHub Copilot", "category": "Coding Assistants", "company": "GitHub"},
    {"name": "Cursor", "category": "Coding Assistants", "company": "Cursor"},
    {"name": "Tabnine", "category": "Coding Assistants", "company": "Tabnine"},
    {"name": "Codeium", "category": "Coding Assistants", "company": "Codeium"},
    {"name": "Runway", "category": "Generateurs Video", "company": "Runway"},
    {"name": "Pika", "category": "Generateurs Video", "company": "Pika Labs"},
    {"name": "Synthesia", "category": "Generateurs Video", "company": "Synthesia"},
    {"name": "Notion AI", "category": "Productivite", "company": "Notion"},
    {"name": "Jasper", "category": "Productivite", "company": "Jasper"},
    {"name": "Copy.ai", "category": "Productivite", "company": "Copy.ai"},
    {"name": "ElevenLabs", "category": "Audio", "company": "ElevenLabs"},
    {"name": "Murf AI", "category": "Audio", "company": "Murf"},
    {"name": "Canva AI", "category": "Design", "company": "Canva"},
    {"name": "Uizard", "category": "Design", "company": "Uizard"},
    {"name": "Perplexity", "category": "Recherche", "company": "Perplexity"},
    {"name": "You.com", "category": "Recherche", "company": "You.com"},
]

POSITIVE_TEMPLATES = [
    "{tool} est incroyable pour la productivité !",
    "Je suis impressionné par {tool}, vraiment bluffant",
    "{tool} m'a fait gagner tellement de temps",
    "Excellente expérience avec {tool}",
    "{tool} dépasse mes attentes",
]

NEGATIVE_TEMPLATES = [
    "{tool} est décevant, trop de bugs",
    "Je ne recommande pas {tool}, pas fiable",
    "{tool} ne fonctionne pas comme prévu",
    "Déçu par {tool}, beaucoup de problèmes",
    "{tool} n'est pas à la hauteur",
]

NEUTRAL_TEMPLATES = [
    "Quelqu'un a testé {tool} ?",
    "Que pensez-vous de {tool} ?",
    "J'hésite entre {tool} et d'autres outils",
    "{tool} semble intéressant",
    "Des avis sur {tool} ?",
]

LOCATIONS = [
    "Paris, France", "Lyon, France", "Marseille, France",
    "London, UK", "New York, USA", "San Francisco, USA",
    "Berlin, Germany", "Tokyo, Japan", "Toronto, Canada",
]

# ========== GÉNÉRATEUR DE DONNÉES ==========

fake = Faker(['fr_FR', 'en_US'])
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["social_sentiment"]
collection = db["posts"]

def generate_user():
    followers = random.choice([
        random.randint(10, 100),
        random.randint(100, 1000),
        random.randint(1000, 10000),
        random.randint(10000, 100000)
    ])
    
    return {
        "name": fake.name(),
        "screen_name": fake.user_name(),
        "followers": followers,
        "location": random.choice(LOCATIONS),
        "verified": followers > 10000 and random.random() < 0.3,
        "created_at": fake.date_time_between(start_date="-5y", end_date="-1y")
    }

def generate_post(days_back=10):
    tool = random.choice(AI_TOOLS)
    
    sentiment_choice = random.choices(
        ['positive', 'negative', 'neutral'],
        weights=[40, 30, 30]
    )[0]
    
    if sentiment_choice == 'positive':
        text = random.choice(POSITIVE_TEMPLATES).format(tool=tool['name'])
    elif sentiment_choice == 'negative':
        text = random.choice(NEGATIVE_TEMPLATES).format(tool=tool['name'])
    else:
        text = random.choice(NEUTRAL_TEMPLATES).format(tool=tool['name'])
    
    user = generate_user()
    
    created_at = datetime.now() - timedelta(
        days=random.randint(0, days_back),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )
    
    base_engagement = user['followers'] * random.uniform(0.02, 0.05)
    sentiment_multiplier = {'positive': 1.5, 'negative': 1.2, 'neutral': 0.8}
    
    likes = int(base_engagement * sentiment_multiplier[sentiment_choice] * random.uniform(0.5, 2))
    retweets = int(likes * random.uniform(0.1, 0.3))
    replies = int(likes * random.uniform(0.05, 0.15))
    
    hashtags = [tool['name'], "AI", tool['category'].replace(" ", "")]
    
    post = {
        "id": str(uuid.uuid4()),
        "text": text,
        "user": user,
        "created_at": created_at,
        "likes": likes,
        "retweets": retweets,
        "replies": replies,
        "hashtags": hashtags,
        "topic": tool['name'],
        "category": tool['category'],
        "language": "fr" if random.random() < 0.6 else "en",
        "source": "simulated",
        "text_length": len(text),
        "word_count": len(text.split()),
        "has_url": False,
        "has_media": False,
        "collected_at": datetime.now()
    }
    
    return post

def generate_dataset(num_posts=3000, days_back=10):
    print(f"🎲 Génération de {num_posts} posts...")
    
    posts = []
    for i in range(num_posts):
        post = generate_post(days_back)
        posts.append(post)
        
        if (i + 1) % 500 == 0:
            print(f"  ✅ {i + 1}/{num_posts} posts générés...")
    
    print(f"💾 Insertion dans MongoDB...")
    collection.delete_many({})
    collection.insert_many(posts)
    
    print(f"✅ {num_posts} posts insérés avec succès !")
    
    print("\n📊 STATISTIQUES DU DATASET :")
    print(f"  - Total posts : {collection.count_documents({})}")
    
    pipeline = [{"$group": {"_id": "$category", "count": {"$sum": 1}}}]
    print("\n  - Par catégorie :")
    for cat in collection.aggregate(pipeline):
        print(f"    • {cat['_id']}: {cat['count']}")
    
    pipeline = [{"$group": {"_id": "$language", "count": {"$sum": 1}}}]
    print("\n  - Par langue :")
    for lang in collection.aggregate(pipeline):
        print(f"    • {lang['_id']}: {lang['count']}")
    
    print("\n✨ Dataset prêt pour l'analyse !")

if __name__ == "__main__":
    generate_dataset(num_posts=3000, days_back=10)