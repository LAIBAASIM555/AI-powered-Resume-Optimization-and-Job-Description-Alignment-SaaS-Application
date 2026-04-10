import os

filepath = "src/pages/ResumeBuilderPage.jsx"
with open(filepath, "r", encoding="utf-8") as f:
    text = f.read()

# The duplicates start when ModernTemplate is declared a second time
modern_decl = "function ModernTemplate({ data }) {"
first_idx = text.find(modern_decl)
if first_idx != -1:
    second_idx = text.find(modern_decl, first_idx + 1)
    if second_idx != -1:
        # We cut EVERYTHING from second_modern onwards
        clean_text = text[:second_idx].strip()
        # The cut likely severed the final closing brackets of ResumeBuilderPage Component
        clean_text += "\n  );\n}\n"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(clean_text)
        print("Truncated file at duplicate ModernTemplate and sealed.")
    else:
        print("No second occurrence found.")
else:
    print("Could not find ModernTemplate.")
