# Imports and calls the key functions from notebooks 1, 2, and 3 in sequence.
# Reads a --date argument or grabs yesterday’s date automatically.


# Next Steps:
    
#     run.sh
#         #!/usr/bin/env bash
#         DATE=${1:-$(date -d "yesterday" +%F)}
#         python final.py --date $DATE

#     README
#         “Install requirements: pip install -r requirements.txt”
#         “Run daily: bash run.sh 2025-05-04”
#         “Outputs: data/processed/recommended_prices_2025-05-04.csv”