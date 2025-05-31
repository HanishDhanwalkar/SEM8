import os
import re

files = os.listdir()
slides = {}

print(files)
# for file in files:
    
#     if file.endswith(".pdf"):
#         filename, extension = os.path.splitext(file)
#         for item in ["CS769_2025", "Intro", "annotated", "-", "_"]:
#             filename = filename.strip(item)
#             filename = re.search(r'\d+', filename).group()
#         # print(filename)
#         slides[file] = f"Lecture_{filename}"
#         # print(file)
        
# for i, (key, item) in enumerate(slides.items()):
#     os.rename(key, item)
#     print(i,key, ":\t\t", item)

for file in files:
    if file.endswith(".py"):
        continue
    else:
        print(file)
        os.rename(file, f"{file}.pdf")
