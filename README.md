# GlossierPulse

GlossierPulse is a beginner-friendly Streamlit dashboard for beauty and ecommerce customer segmentation.
It clusters customers into 4 segments and uses Groq AI to generate marketing personas in a Glossier-style voice:
honest, skin-first, community-driven, never corporate.

## Project Files

- `app.py` - Main Streamlit app (upload data, segment customers, generate personas)
- `data_loader.py` - CSV loading and cleaning logic
- `segmentation.py` - K-Means segmentation and summary metrics
- `persona_generator.py` - Groq API integration for persona + campaign text
- `requirements.txt` - Python dependencies

## Expected CSV Columns

Your CSV should include:

- `customer_id`
- `age`
- `annual_income`
- `spending_score`
- `purchase_frequency`

## Setup

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your Groq key:

```bash
export GROQ_API_KEY="your_real_groq_api_key"
```

4. Run the Streamlit app:

```bash
streamlit run app.py
```

## Notes

- The app includes optional sample data so you can test quickly.
- Uploaded CSV data is cleaned automatically before clustering.
- If Groq key is missing, persona generation will show an error.
