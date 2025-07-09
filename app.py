from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample pantry and recipes
pantry = {"butter", "cheese", "pork loin"}
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

@app.route("/dialogflow", methods=["POST"])
def dialogflow_webhook():
    data = request.get_json()
    intent = data["queryResult"]["intent"]["displayName"]

    if intent == "SuggestRecipe":
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

        return jsonify({"fulfillmentText": reply})

    return jsonify({"fulfillmentText": "Sorry, I couldn't process your request."})

if __name__ == "__main__":
    app.run()
