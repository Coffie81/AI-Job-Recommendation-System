from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as nump
from database import get_all_jobs


def preprocess_text(text):
    """
    Clean and standardize text.
    Converts to lowercase and strips extra spaces.
    """
    return text.lower().strip()


def get_recommendations(user_skills, top_n=5):
    """
    Generate job recommendations based on user skills.
    Matches user skills against full job descriptions using TF-IDF + cosine similarity.

    Parameters:
        user_skills (str): Skills entered by the user (comma or space separated).
        top_n (int): Number of top job recommendations to return.

    Returns:
        List of dictionaries with job details and match scores.
    """

    # Fetch all jobs from the database
    jobs = get_all_jobs()

    if not jobs:
        print(" No jobs found in the database.")
        return []

    #Extract job data into lists
    job_ids = []
    job_titles = []
    job_descriptions = []

    for job in jobs:
        job_ids.append(job["id"])
        job_titles.append(job["job_title"])
        job_descriptions.append(preprocess_text(job["description"]))

    #  Preprocess user skills
    cleaned_user_skills = preprocess_text(user_skills)

    # Combine user skills + all job descriptions into one list for TF-IDF
    # The model compares user skills against full job descriptions
    # since skills are embedded inside the descriptions in your dataset
    all_text = [cleaned_user_skills] + job_descriptions

    # Apply TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
    tfidf_matrix = vectorizer.fit_transform(all_text)

    # Compute cosine similarity between user skills and each job description
    user_vector = tfidf_matrix[0]
    job_vectors = tfidf_matrix[1:]

    similarity_scores = cosine_similarity(user_vector, job_vectors).flatten()

    #Rank jobs by similarity score (highest first)
    ranked_indices = nump.argsort(similarity_scores)[::-1]

    # Build results list for top N jobs
    recommendations = []
    for i in ranked_indices[:top_n]:
        score = round(float(similarity_scores[i]) * 100, 2)
        recommendations.append({
            "job_id": job_ids[i],
            "job_title": job_titles[i],
            "description": job_descriptions[i][:300] + "...",  # Trim long descriptions
            "score": score
        })

    return recommendations


# Test the model directly
if __name__ == "__main__":
    test_skills = "Python Machine Learning SQL"
    print(f"\n Finding jobs for skills: {test_skills}\n")

    results = get_recommendations(test_skills, top_n=5)

    if results:
        print("Top Job Recommendations:\n")
        for i, job in enumerate(results, 1):
            print(f"{i}. {job['job_title']}")
            print(f"   Match Score : {job['score']}%")
            print(f"   Description : {job['description']}")
            print()
    else:
        print("No recommendations found.")