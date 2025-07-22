import pandas as pd
import matplotlib.pyplot as plt

def load_uploaded_data(file) -> pd.DataFrame:
    """
    Loads uploaded file and parses it into a cleaned DataFrame.
    Supports .csv, .json, .xls, .xlsx files.
    """
    if file.name.endswith(".json"):
        data = pd.read_json(file)
    elif file.name.endswith(".csv"):
        data = pd.read_csv(file)
    elif file.name.endswith((".xls", ".xlsx")):
        data = pd.read_excel(file)
    else:
        raise ValueError("❌ Unsupported file format. Please upload CSV, JSON, or Excel.")

    return clean_product_data(data)

def clean_product_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans product DataFrame by standardizing rating fields.
    """
    # Convert rating dict to columns if applicable
    if "rating" in df.columns and df["rating"].apply(lambda x: isinstance(x, dict)).any():
        df["rating_rate"] = df["rating"].apply(lambda x: x.get("rate", None) if isinstance(x, dict) else None)
        df["rating_count"] = df["rating"].apply(lambda x: x.get("count", None) if isinstance(x, dict) else None)
        df.drop("rating", axis=1, inplace=True)

    # Fallback: If dataset has rating_rate or rating columns separately
    elif "rating" in df.columns and "rating_rate" not in df.columns:
        df.rename(columns={"rating": "rating_rate"}, inplace=True)

    return df

    # Normalize column names: lowercase, no spaces
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Handle JSON-style nested rating dictionary
    if "rating" in df.columns and df["rating"].apply(lambda x: isinstance(x, dict)).any():
        df["rating_rate"] = df["rating"].apply(lambda x: x.get("rate", None) if isinstance(x, dict) else None)
        df["rating_count"] = df["rating"].apply(lambda x: x.get("count", None) if isinstance(x, dict) else None)
        df.drop("rating", axis=1, inplace=True)

    # Rename common alternate column names to match LLM logic
    rename_map = {
        "product_category": "category",
        "average_rating": "rating_rate",
        "number_of_items": "count"
    }
    df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns}, inplace=True)

    return df

def generate_llm_context(df: pd.DataFrame) -> str:
    """
    Generates a summarized string for LLM context from product data.
    Includes:
    - Product count per category
    - Average price per category
    - Average rating per category
    """
    try:
        if "category" not in df.columns:
            return "⚠️ 'category' column not found in the dataset."
        if "price" not in df.columns:
            return "⚠️ 'price' column not found in the dataset."

        rating_column = "rating_rate" if "rating_rate" in df.columns else (
            "average_rating" if "average_rating" in df.columns else None
        )

        avg_prices = df.groupby("category")["price"].mean().round(2).to_dict()
        avg_ratings = (
            df.groupby("category")[rating_column].mean().round(2).to_dict()
            if rating_column else {}
        )
        category_counts = df["category"].value_counts().to_dict()

        context_lines = ["Product Category Summary:\n"]
        for cat in category_counts:
            context_lines.append(
                f"- {cat}: {category_counts[cat]} items, "
                f"Average Price: ${avg_prices.get(cat, 'N/A')}, "
                f"Average Rating: {avg_ratings.get(cat, 'N/A')}"
            )
        return "\n".join(context_lines)

    except Exception as e:
        return f"⚠️ Error generating context: {e}"

# Optional: Standalone CLI test
if __name__ == "__main__":
    try:
        df = pd.read_json("products.json")
        df = clean_product_data(df)

        print("\n📊 Product count by category:")
        print(df['category'].value_counts())
        print("\n💰 Price statistics:")
        print(df['price'].describe())

        if "rating_rate" in df.columns:
            plt.figure(figsize=(8, 5))
            plt.scatter(df['rating_rate'], df['price'], alpha=0.6, color='teal')
            plt.title("Rating vs Price")
            plt.xlabel("Rating")
            plt.ylabel("Price")
            plt.grid(True)
            plt.tight_layout()
            plt.show()

        print("\n🧠 LLM Context:\n")
        print(generate_llm_context(df))

    except Exception as err:
        print(f"❌ Error: {err}")




