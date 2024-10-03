# test_roadmap.py
import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.utils.content import Roadmap  # Adjust the import accordingly

if __name__ == "__main__":
    roadmap = Roadmap()  # Test initialization
    print("Roadmap initialized successfully.")
