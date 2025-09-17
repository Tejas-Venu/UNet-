import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import NGO
import logging

logger = logging.getLogger(__name__)

def get_recommendations(ngo_name):
    logger.info(f"Received NGO name for recommendation: {ngo_name}")
    
    ngos = list(NGO.objects.all().values())
    total_ngos = len(ngos)
    logger.info(f"Number of NGOs fetched: {len(ngos)}")
    
    if not ngos:
        logger.warning("No NGOs available in the database.")
        return []

    df = pd.DataFrame(ngos)
    logger.info(f"DataFrame shape: {df.shape}")

    if df.empty:
        logger.warning("DataFrame is empty. Returning no recommendations.")
        return []

    df.fillna('', inplace=True)
    logger.info("Null values handled in DataFrame.")
    df['tags'] = (
        df['name'] + " " +
        df['purpose'] + " " +
        df['address'] + " " +
        df['contact_person']
    )
    df['tags'] = df['tags'].apply(lambda x: x.lower())
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(df['tags']).toarray()
    similarity = cosine_similarity(vectors)
    try:
        # Ensure case-insensitive matching for NGO name
        index = df[df['name'].str.lower() == ngo_name.lower()].index[0]
        
        # Calculate distances for similarity and sort them
        distances = sorted(
            list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1]
        )
        
        # Get top 10 recommended NGOs excluding the first one (itself)
        recommended_ngos = [
            {'id': df.iloc[i[0]]['id'], 'name': df.iloc[i[0]]['name']}
            for i in distances[0:total_ngos]
        ]
        print(recommended_ngos)
        return recommended_ngos

    except IndexError:
        # Handle case where the NGO name is not found in the DataFrame
        print(f"No matching NGO found for: {ngo_name}")
        return []