import os
import pandas as pd
import pdfplumber
import re

input_folder = r"D:\CIVR\Reports"
output_file = os.path.join(input_folder, "chat_feedback_summary.csv")

all_data = []

for filename in os.listdir(input_folder):
    if filename.lower().endswith(".pdf"):
        file_path = os.path.join(input_folder, filename)
        print(f"\n📄 Reading {filename}...")
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if not text:
                        continue

                    # Split text into lines
                    lines = text.split("\n")
                    i = 0
                    while i < len(lines) - 1:
                        line1 = lines[i].strip()
                        line2 = lines[i + 1].strip()

                        if re.match(r'^\d{8}\s+\S+\s+\d+\s+\S+\s+', line2):
                            parts = line2.split()
                            if len(parts) >= 5:
                                entry = {
                                    "Source File": filename,
                                    "Page Name": line1,
                                    "Day": parts[0],
                                    "ChatWindowID": parts[1],
                                    "Feedback Rating": parts[2], #Actual rating value
                                    "Transcript": parts[3], #Y/N flag
                                    "Comment": " ".join(parts[4:]) #Actual user comment
                                }
                                all_data.append(entry)
                                print(f"✅ Parsed: {entry}")
                            i += 2  # Move to next pair
                        else:
                            i += 1  # Skip ahead if no match

        except Exception as e:
            print(f"⚠️ Error processing {filename}: {e}")

df = pd.DataFrame(all_data)
df.to_csv(output_file, index=False)
print(f"\n✅ Saved {len(df)} rows to {output_file}")