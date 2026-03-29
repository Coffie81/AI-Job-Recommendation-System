from flask import Flask, render_template, request
from database import initialize_database, add_user, save_recommendations, get_connection
from model import get_recommendations

app = Flask(__name__)

# Initialize database when app starts
initialize_database()


@app.route("/", methods=["GET"])
def index():
    """Render the home page with the input form."""
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend():

    # Get form data
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    skills = request.form.get("skills", "").strip()
    experience = request.form.get("experience", "0").strip()

    # Basic validation
    if not name or not email or not skills:
        error = "Please fill in all required fields."
        return render_template("index.html", error=error)

    try:
        experience = int(experience)
    except ValueError:
        experience = 0

    # Check if email already exists in database
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, skills FROM users WHERE email = ?", (email,))
    existing_user = cursor.fetchone()
    conn.close()

    if existing_user:
        # Show a warning and ask if they want to continue with updated skills
        return render_template(
            "index.html",
            error=f" The email '{email}' is already registered to another name. "
                  f"Please use a different email or click below to get new recommendations with updated skills.",
            prefill_name=name,
            prefill_email=email,
            prefill_skills=skills,
            prefill_experience=experience,
            existing_user_id=existing_user["id"]
        )

    #  Save new user to database
    user_id = add_user(name, email, skills, experience)

    # Run ML model
    recommendations = get_recommendations(skills, top_n=5)

    # Save recommendations
    if recommendations:
        save_recommendations(user_id, recommendations)

    return render_template(
        "results.html",
        name=name,
        skills=skills,
        experience=experience,
        recommendations=recommendations
    )


@app.route("/recommend-existing", methods=["POST"])
def recommend_existing():
  
    user_id = request.form.get("existing_user_id")
    name = request.form.get("name", "").strip()
    skills = request.form.get("skills", "").strip()
    experience = request.form.get("experience", "0").strip()

    try:
        experience = int(experience)
    except ValueError:
        experience = 0

    # Run ML model with new/updated skills
    recommendations = get_recommendations(skills, top_n=5)

    # Save new recommendations for existing user
    if recommendations:
        save_recommendations(user_id, recommendations)

    return render_template(
        "results.html",
        name=name,
        skills=skills,
        experience=experience,
        recommendations=recommendations
    )

if __name__ == "__main__":
    app.run(debug=True)    