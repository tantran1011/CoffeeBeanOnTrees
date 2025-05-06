import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # đường đến src/services
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "ai_model.pt")

# Normalize đường dẫn lại
MODEL_PATH = os.path.normpath(MODEL_PATH)

img_test = 'src/models/test1.jpg'
