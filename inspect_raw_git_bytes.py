import subprocess

try:
    cmd = ["git", "show", "49ab1da:match_intelligence/frontend/src/components/MatchDetail.jsx"]
    raw_bytes = subprocess.check_output(cmd)
    
    print("Total bytes:", len(raw_bytes))
    print("Raw bytes near 113:")
    print(raw_bytes[90:150])
    
except Exception as e:
    print("Error:", e)
