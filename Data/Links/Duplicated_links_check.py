import pandas as pd



with open("links.txt", 'r', encoding='utf-8') as f:
    full_links1 = [line.strip() for line in f if line.strip()]
    
with open("links1.txt", 'r', encoding='utf-8') as f:
    full_links2 = [line.strip() for line in f if line.strip()]
    
    
all_links = list(dict.fromkeys(full_links1 + full_links2))

len(all_links)
link_df = pd.DataFrame(all_links)


print("Identical:", full_links1 == full_links2)
print("Same length:", len(full_links1) == len(full_links2))
print("Same set:", set(full_links1) == set(full_links2))