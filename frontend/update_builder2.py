import re

with open("src/pages/ResumeBuilderPage.jsx", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("hover:text-indigo-600 dark:text-cyan-400", "hover:text-indigo-600 dark:hover:text-cyan-400")
text = text.replace("text-white dark:text-slate-900 hover:bg-indigo-700 dark:hover:bg-cyan-400 text-slate-900", "text-white dark:text-slate-900 hover:bg-indigo-700 dark:hover:bg-cyan-400")
text = text.replace("bg-indigo-600 dark:bg-cyan-500 text-white dark:text-slate-900 hover:bg-indigo-700 dark:hover:bg-cyan-400 text-slate-900", "bg-indigo-600 dark:bg-cyan-500 text-white dark:text-slate-900 hover:bg-indigo-700 dark:hover:bg-cyan-400")
text = text.replace("text-indigo-600 hover:text-indigo-600 dark:hover:text-cyan-400", "text-slate-400 hover:text-indigo-600 dark:hover:text-cyan-400")

with open("src/pages/ResumeBuilderPage.jsx", "w", encoding="utf-8") as f:
    f.write(text)
