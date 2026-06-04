import subprocess

res = subprocess.run(["git", "diff", "HEAD", "--", "match_intelligence/frontend/src/components/MatchDetail.jsx"], capture_output=True)
diff_text = res.stdout.decode('utf-8', errors='ignore')
print("Diff length:", len(diff_text))
print("First 300 characters of diff:")
print(diff_text[:300])
