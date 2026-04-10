import os

filepath = "src/pages/ResumeBuilderPage.jsx"
with open(filepath, "r", encoding="utf-8") as f:
    text = f.read()

# Find the second occurrence of "const TemplateMap = "
duplicate_start = "const TemplateMap = { classic: ClassicTemplate, modern: ModernTemplate, executive: ExecutiveTemplate };"
first_idx = text.find(duplicate_start)
if first_idx != -1:
    second_idx = text.find(duplicate_start, first_idx + len(duplicate_start))
    if second_idx != -1:
        # The duplication starts here. We want to cut off EVERYTHING from here downwards.
        # So we just keep the text up to `second_idx` safely.
        new_text = text[:second_idx].strip() + "\n"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_text)
        print("Removed duplication.")
    else:
        print("No second occurrence found.")
else:
    print("Could not find TemplateMap.")
