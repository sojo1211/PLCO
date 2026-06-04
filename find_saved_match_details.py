import os

brain_dir = r"C:\Users\sungj\.gemini\antigravity\brain"
for root, dirs, files in os.walk(brain_dir):
    for file in files:
        if "MatchDetail" in file:
            path = os.path.join(root, file)
            print(f"Found file: {path} (size: {os.path.getsize(path)})")
