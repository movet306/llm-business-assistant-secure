# 🧠 LLM Business Assistant

An AI-powered business assistant app that allows you to upload your product datasets and interact with them in natural language. Built with Streamlit, OpenAI API, and a fully customizable context pipeline.

![Streamlit Screenshot](https://llm-business-assistant-secure-9kg2r7csm7vzzem5che2tb.streamlit.app)

---

## 🔍 Use Case
This app is designed for business analysts, product managers, or entrepreneurs who want to:

- Quickly extract insights from product data
- Ask business questions in natural language
- Summarize key metrics for different stakeholders
- Download chat history in CSV or PDF

---

## ⚙️ Key Features

| Feature | Description |
|---------|-------------|
| 📂 Upload Product File | Upload `.csv`, `.json`, or `.xlsx` files |
| 🧠 LLM Integration | Ask business questions using GPT-4o, GPT-4, or GPT-3.5-turbo |
| ✅Dynamic system prompt customization (🧠 _Set Custom System Prompt_ box) 
| 📊 Context Generation | Dynamic context generation from uploaded dataset |
| 🛠️ Admin Panel | Reload default or uploaded data on demand |
| 📑 Export Options | Download entire chat as CSV or PDF |
| 🗂 Session Support | Isolated session history using UUID |
| 🔐 API Security | `.env` file ignored and API keys securely handled via Streamlit Cloud Secrets |

---

## 🗃️ Dataset Format
The app expects your product data to contain (at minimum) the following fields:

- `title`
- `category`
- `price`
- `rating.rate`
- `rating.count`

Example (JSON-like):
```json
{
  "title": "Gaming Mouse",
  "category": "electronics",
  "price": 49.99,
  "rating": {"rate": 4.5, "count": 234}
}
```

---

## 🧪 Usage

1. Launch app locally or on Streamlit Cloud
2. Upload your product dataset (`CSV`, `JSON`, `XLSX`)
3. Select a system prompt and LLM model
4. Ask business questions via chat or dropdowns
5. Download chat insights as PDF or CSV

💡 Tip: Use the system prompt to guide assistant behavior — e.g.:
```text
You are a helpful business assistant.
```

---

## 📁 File Structure
```
├── llm_dashboard.py         # Main Streamlit app
├── llm_agent.py             # Handles LLM API call and session history
├── product_analysis.py      # Cleans data and generates context
├── data_fetcher.py          # [optional] For future API integrations
├── products.json            # Default sample product data
├── .env                     # Contains your OpenAI API key
├── .gitignore               # Ignores .env and system files
```

---

## 🔐 API Key Handling

To prevent API key leaks (which caused the **initial project to be disabled**):

### ✅ What we did right in this version:
- `.env` file added to `.gitignore`
- `OPENAI_API_KEY` retrieved using `os.getenv()`
- On **Streamlit Cloud**, the API key is added manually under **Secrets**

```bash
# .env
OPENAI_API_KEY=sk-...
```

---

## 🧰 Technologies Used

| Tool / Library     | Purpose                          |
|--------------------|----------------------------------|
| Python             | Core programming language        |
| Streamlit          | Frontend web UI                  |
| OpenAI API (GPT-4o)| LLM-powered insights             |
| Pandas             | Data manipulation                |
| Matplotlib         | (Planned) basic visualizations   |
| FPDF               | Export to PDF                    |
| uuid               | Session management               |
| dotenv             | Secure environment variable load |

---

## 🧪 Sample Questions
- Which category is the most expensive?
- Which product has the highest rating?
- What is the average price of electronics?
- Which price range has the most products?

---

## 🧑‍💻 Local Deployment
```bash
# 1. Clone the repo
https://github.com/movet306/llm-business-assistant-secure.git

# 2. Create .env file
OPENAI_API_KEY= I put down the API KEY that I created from OpenAI

# 3. Install packages
pip install -r requirements.txt

# 4. Run app
streamlit run llm_dashboard.py
```

---

## ☁️ Streamlit Cloud Deployment
App is securely deployed here:
🔗 https://llm-business-assistant-secure-9kg2r7csm7vzzem5che2tb.streamlit.app/

Secrets set manually under **[App Settings > Secrets]**:
```ini
OPENAI_API_KEY = The API KEY that I created from OpenAI
```

---

## 🧠 Built With Purpose
This project was carefully built by **Mert Övet**, combining advanced LLM capabilities with business-facing analytics tools. It reflects hands-on experience in:

- Building production-ready LLM apps
- Handling API key security
- Debugging deployment pitfalls
- Crafting end-to-end user experiences

> _"This is more than a project — it's a full-stack AI solution for business users."_

---

## 📬 Contact
Feel free to reach out via [LinkedIn](https://www.linkedin.com/in/mertovet/) or open an issue on GitHub.

---

## 📄 License
MIT License
