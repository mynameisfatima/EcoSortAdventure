import pickle
import os
from classifier import classify_trash  # Import the function from the new file

# Make sure 'models' folder exists
os.makedirs("models", exist_ok=True)

# Save the function as a pickle file
with open("models/simple_classifier.pkl", "wb") as f:
    pickle.dump(classify_trash, f)

print("✅ simple_classifier.pkl has been created.")
