import boto3
import os
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# AWS REKOGNITION
# ----------------------------
client = boto3.client("rekognition", region_name="eu-west-1")

# ----------------------------
# FULL SÖKVÄG TILL BILDMAPP
# ----------------------------
IMAGE_FOLDER = r"C:\Users\KI\OneDrive\Desktop\AI IOT 1\Bilder"

# ----------------------------
# LISTA FÖR LABELS
# ----------------------------
all_labels = []

print("Startar bildanalys...")

# ----------------------------
# LOOPA IGENOM BILDER
# ----------------------------
for file in os.listdir(IMAGE_FOLDER):

    if file.lower().endswith((".jpg", ".jpeg", ".png")):

        full_path = os.path.join(IMAGE_FOLDER, file)

        print("Analyserar:", full_path)

        with open(full_path, "rb") as image:
            image_bytes = image.read()

        # ----------------------------
        # AWS LABEL DETECTION
        # ----------------------------
        response = client.detect_labels(
            Image={"Bytes": image_bytes},
            MaxLabels=10,
            MinConfidence=70
        )

        for label in response["Labels"]:
            all_labels.append(label["Name"])

# ----------------------------
# ANALYS
# ----------------------------
counts = pd.Series(all_labels).value_counts().head(10)

# ----------------------------
# DIAGRAM
# ----------------------------
plt.figure(figsize=(8, 8))
plt.pie(counts.values, labels=counts.index, autopct="%1.1f%%")
plt.title("Amazon Rekognition - Bildanalys")

# ----------------------------
# SPARA RESULTAT (FULL SÖKVÄG)
# ----------------------------
plt.savefig(r"C:\Users\KI\OneDrive\Desktop\AI IOT 1\resultat.png")

plt.show()

print("KLART! resultat.png skapad")