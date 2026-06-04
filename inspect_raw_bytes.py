import subprocess

res = subprocess.run(['git', 'show', 'HEAD:match_intelligence/frontend/src/components/MatchDetail.jsx'], capture_output=True)
raw_bytes = res.stdout
print("Total bytes:", len(raw_bytes))
print("Bytes 100 to 150:", raw_bytes[100:150])
