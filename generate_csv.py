import pandas as pd

# Sample attendee IDs
data = {
    "attendee_id": [1, 2, 3, 4, 5]  # Modify as needed
}

# Create DataFrame
df = pd.DataFrame(data)

# Save as CSV
csv_filename = "attendees.csv"
df.to_csv(csv_filename, index=False)

print(f"Test CSV file '{csv_filename}' created successfully!")
