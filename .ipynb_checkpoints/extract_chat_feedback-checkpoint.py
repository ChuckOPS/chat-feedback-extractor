import pandas as pd
import tabula

# Directory where all PDFs are stored (e.g., your USB stick)
input_folder = r"E:\CIVR\Reports"
output_file = os.path.join(input_folder, "chat_feedback_summary.csv")

# Holds all extracted rows
all_data = []

# Loop through all PDF files
for filename in os.listdir(input_folder):
    if filename.endswith(".pdf"):
        file_path = os.path.join(input_folder, filename)
        
        try:
            # Extract tables from PDF
            tables = tabula.read_pdf(file_path, pages='all', multiple_tables=True)
            
            for table in tables:
                # Optional: Clean/normalize columns if needed
                if table.shape[1] >= 5:
                    for index, row in table.iterrows():
                        entry = {
                            "Source File": filename,
                            "Page Name": row.iloc[0],
                            "Day": row.iloc[1],
                            "Feedback Rating": row.iloc[3],
                            "Comment": row.iloc[4]
                        }
                        all_data.append(entry)
        
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

# Convert to DataFrame and export
df = pd.DataFrame(all_data)
df.to_csv(output_file, index=False)
print(f"Extracted data saved to {output_file}")