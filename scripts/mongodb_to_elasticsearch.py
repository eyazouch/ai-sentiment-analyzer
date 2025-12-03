#!/usr/bin/env python3
"""
MongoDB to Elasticsearch ETL Pipeline
Transfers sentiment-analyzed posts from MongoDB to Elasticsearch
"""

import sys
from datetime import datetime
from pymongo import MongoClient
from elasticsearch import Elasticsearch, helpers
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def connect_mongodb(host='localhost', port=27017, db_name='social_sentiment'):
    """Connect to MongoDB"""
    try:
        client = MongoClient(host, port, serverSelectionTimeoutMS=5000)
        # Test connection
        client.server_info()
        db = client[db_name]
        logger.info(f"✅ Connected to MongoDB: {host}:{port}/{db_name}")
        return db
    except Exception as e:
        logger.error(f"❌ Failed to connect to MongoDB: {e}")
        sys.exit(1)


def connect_elasticsearch(host='localhost', port=9200):
    """Connect to Elasticsearch"""
    try:
        es = Elasticsearch([f"http://{host}:{port}"])
        # Test connection
        if es.ping():
            logger.info(f"✅ Connected to Elasticsearch: {host}:{port}")
            logger.info(f"   Cluster: {es.info()['cluster_name']}")
            logger.info(f"   Version: {es.info()['version']['number']}")
            return es
        else:
            logger.error("❌ Elasticsearch is not responding")
            sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Failed to connect to Elasticsearch: {e}")
        sys.exit(1)


def transform_document(doc):
    """
    Transform MongoDB document to Elasticsearch format
    """
    try:
        # Create base document
        es_doc = {
            '@timestamp': doc.get('created_at', datetime.now()),
            'text': doc.get('text', ''),
            'topic': doc.get('topic', ''),
            'category': doc.get('category', ''),
            'likes': doc.get('likes', 0),
            'retweets': doc.get('retweets', 0),
        }
        
        # Extract user fields
        if 'user' in doc and isinstance(doc['user'], dict):
            es_doc['user_name'] = doc['user'].get('name', '')
            es_doc['user_location'] = doc['user'].get('location', '')
            es_doc['user_followers'] = doc['user'].get('followers', 0)
        
        # Extract sentiment analysis fields
        if 'sentiment_analysis' in doc and isinstance(doc['sentiment_analysis'], dict):
            es_doc['sentiment_label'] = doc['sentiment_analysis'].get('sentiment', 'neutral')
            es_doc['sentiment_score'] = doc['sentiment_analysis'].get('score', 0.0)
            es_doc['sentiment_confidence'] = doc['sentiment_analysis'].get('confidence', 0.0)
        
        return es_doc
    except Exception as e:
        logger.warning(f"⚠️ Error transforming document: {e}")
        return None


def generate_bulk_actions(mongodb_docs, index_name):
    """
    Generator for bulk indexing in Elasticsearch
    """
    for doc in mongodb_docs:
        es_doc = transform_document(doc)
        if es_doc:
            # Extract date for dynamic index naming: ai-sentiment-YYYY.MM.DD
            timestamp = es_doc.get('@timestamp', datetime.now())
            if isinstance(timestamp, str):
                try:
                    timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                except:
                    timestamp = datetime.now()
            
            index_with_date = f"{index_name}-{timestamp.strftime('%Y.%m.%d')}"
            
            yield {
                '_index': index_with_date,
                '_source': es_doc
            }


def transfer_data(mongodb_db, es_client, collection_name='posts', index_prefix='ai-sentiment'):
    """
    Transfer data from MongoDB to Elasticsearch
    """
    try:
        # Get collection
        collection = mongodb_db[collection_name]
        
        # Count documents
        total_docs = collection.count_documents({})
        logger.info(f"📊 Found {total_docs} documents in MongoDB collection '{collection_name}'")
        
        if total_docs == 0:
            logger.warning("⚠️ No documents to transfer!")
            return
        
        # Fetch all documents
        logger.info("📥 Fetching documents from MongoDB...")
        docs = list(collection.find())
        
        # Bulk index to Elasticsearch
        logger.info("📤 Transferring to Elasticsearch...")
        success_count = 0
        error_count = 0
        
        # Use bulk helper for efficient indexing
        for ok, response in helpers.streaming_bulk(
            es_client,
            generate_bulk_actions(docs, index_prefix),
            chunk_size=500,
            raise_on_error=False
        ):
            if ok:
                success_count += 1
            else:
                error_count += 1
                logger.warning(f"⚠️ Error indexing document: {response}")
        
        logger.info(f"✅ Transfer complete!")
        logger.info(f"   ✓ Successfully indexed: {success_count}")
        if error_count > 0:
            logger.warning(f"   ✗ Failed: {error_count}")
        
        # Show created indices
        logger.info("\n📋 Created Elasticsearch indices:")
        indices = es_client.cat.indices(index=f"{index_prefix}-*", format='json')
        for idx in indices:
            logger.info(f"   • {idx['index']} ({idx['docs.count']} docs, {idx['store.size']})")
            
    except Exception as e:
        logger.error(f"❌ Error during transfer: {e}")
        raise


def main():
    """Main ETL pipeline"""
    logger.info("=" * 60)
    logger.info("🚀 MongoDB → Elasticsearch ETL Pipeline")
    logger.info("=" * 60)
    logger.info("")
    
    # Connect to databases
    mongodb = connect_mongodb(
        host='localhost',
        port=27017,
        db_name='social_sentiment'
    )
    
    es = connect_elasticsearch(
        host='localhost',
        port=9200
    )
    
    logger.info("")
    
    # Transfer data
    transfer_data(
        mongodb_db=mongodb,
        es_client=es,
        collection_name='posts',
        index_prefix='ai-sentiment'
    )
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("✅ ETL Pipeline completed successfully!")
    logger.info("=" * 60)
    logger.info("")
    logger.info("🎯 Next steps:")
    logger.info("   1. Open Kibana: http://localhost:5601")
    logger.info("   2. Go to Management → Stack Management → Index Management")
    logger.info("   3. Create index pattern: ai-sentiment-*")
    logger.info("   4. Go to Analytics → Discover to explore your data!")
    logger.info("")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n⚠️ Process interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"\n❌ Fatal error: {e}")
        sys.exit(1)
