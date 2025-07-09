from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# In-memory pantry (add/remove in routes)
pantry = {"butter", "cheese", "pork loin", "eggs"}

# Sample recipe database
recipes = {
    "Grilled Cheese": {"bread", "cheese", "butter"},
    "Omelette": {"eggs", "milk", "cheese"},
    "Pork Stir Fry": {"pork loin", "soy sauce", "garlic"},
    "Mac and Cheese": {"pasta", "cheese", "butter"},
    "Smoothie": {"banana", "milk", "yogurt"}
}

@app.route("/")
def home():
    return "✅ KitchenBot is live on Render!"

# ✅ Add item to pantry
@app.route("/add_item", methods=["POST"])
def add_item():
    data = request.get_json()
    item = data.get("item", "").strip().lower()
    if item:
        pantry.add(item)
        return jsonify({"message": f"✅ {item} added to pantry", "pantry": list(pantry)})
    return jsonify({"error": "No item provided"}), 400

# ✅ Suggest recipes based on current pantry
@app.route("/recipe_suggest", methods=["GET", "POST"])
def recipe_suggest():
    suggestions = []
    for name, ingredients in recipes.items():
        match = pantry.intersection(ingredients)
        score = len(match) / len(ingredients)
        if score >= 0.5:
            suggestions.append(f"{name} (you have {len(match)}/{len(ingredients)} ingredients)")

    if suggestions:
        reply = "🍽️ You could make: " + "; ".join(suggestions)
    else:
        reply = "🤔 I couldn't find a recipe with your current ingredients."

    return jsonify({ "message": reply })

# ✅ Optional future routes: /remove_item, /get_pantry, etc.

# Flask port config for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
