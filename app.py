import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

st.title("🤖 TechStore AI Kundtjänst (Förbättrad RAG)")

# 📦 FAQ / kunskapsbas
documents = [
    "Returpolicy: Kunden har 30 dagar på sig att returnera en produkt. Produkten måste vara oanvänd och i originalförpackning.",
    "Frakt: Leveranstid är 2–5 arbetsdagar inom Sverige. Beställningar skickas vardagar.",
    "Fraktkostnad: Standardfrakt kostar 49 kr, fri frakt över 500 kr.",
    "Garanti: Alla produkter har 1 års garanti som täcker fabrikationsfel.",
    "Reklamation: Om en produkt är trasig kan den reklameras inom garantiperioden genom att kontakta kundtjänst.",
    "Betalning: Vi accepterar kort, Klarna, Swish och PayPal.",
    "Beställning: Din order bekräftas direkt efter köp via e-post.",
    "Orderändring: Beställningar kan ändras inom 1 timme efter att de lagts.",
    "Leveransproblem: Om paketet är försenat kan du kontakta kundtjänst för spårning.",
    "Support: Kundtjänst är öppen vardagar 08–17 via chat och e-post.",
    "Byte av vara: Du kan byta produkt inom 30 dagar om den är oanvänd.",
    "Avbeställning: Order kan avbeställas innan den har skickats från lagret.",
    "Färg och modellbyte: Kontakta support så snart som möjligt om du vill ändra färg eller modell.",
    "Spårning: Du kan spåra ditt paket via spårningslänk som skickas via e-post.",
    "Återbetalning: Återbetalning sker inom 5–10 arbetsdagar efter godkänd retur.",
    "Rabattkoder: Rabattkoder kan användas i kassan innan betalning.",
    "Företagsinfo: TechStore är en svensk e-handelsbutik som säljer elektronik och tillbehör.",
    "Kontakt: Du kan nå oss via kundtjänst@techstore.se eller chatten på hemsidan.",
    "Lagerstatus: Produkter som visas på hemsidan finns normalt i lager.",
    "Presentkort: Vi erbjuder digitala presentkort som skickas via e-post."
]

# 🧠 AI-modell
model = SentenceTransformer('all-MiniLM-L6-v2')
doc_embeddings = model.encode(documents)

st.subheader("Ställ din fråga")

user_input = st.text_input("Skriv här:")

# 🔍 Förbättrad matchning (TOP 3)
def get_best_match(question):
    question_embedding = model.encode([question])
    similarities = cosine_similarity(question_embedding, doc_embeddings)[0]

    top_indices = similarities.argsort()[-3:][::-1]  # topp 3
    best_score = similarities[top_indices[0]]

    top_docs = [documents[i] for i in top_indices]

    return top_docs, best_score

if st.button("Skicka"):

    if user_input.strip() == "":
        st.write("Skriv en fråga först.")
    else:
        best_docs, score = get_best_match(user_input)

        # 🧠 smartare tröskel (mindre “ingen info” problem)
        if score < 0.15:
            st.write("❌ Ingen tydlig information hittades.")
        else:
            st.write("🤖 Här är de mest relevanta svaren:")

            for i, doc in enumerate(best_docs, 1):
                st.write(f"{i}. {doc}")

        st.caption(f"Matchningsscore: {score:.2f}")