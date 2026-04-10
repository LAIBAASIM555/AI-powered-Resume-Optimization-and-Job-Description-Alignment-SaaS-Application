import re

with open("src/pages/ResumeBuilderPage.jsx", "r", encoding="utf-8") as f:
    text = f.read()

# Replace full screen black background and fixed nav
text = text.replace(
    '<div className="min-h-screen bg-[#030712] text-white font-sans">',
    '<div className="min-h-screen bg-slate-50 dark:bg-[#030712] transition-colors duration-500 text-slate-900 dark:text-slate-300 font-sans pt-20 pb-12 overflow-hidden">'
)

# Remove the fixed top bar and make it relative
text = text.replace(
    '<div className="fixed top-0 left-0 right-0 z-50 border-b border-white/10 bg-slate-900/80 backdrop-blur-xl flex items-center justify-between px-4 h-14">',
    '<div className="max-w-7xl mx-auto flex items-center justify-between px-6 py-4 mb-4 bg-white/70 dark:bg-slate-900/40 backdrop-blur-xl rounded-2xl shadow-sm border border-slate-200 dark:border-white/10">'
)

text = text.replace(
    '<div className="fixed top-14 left-0 right-0 z-40 bg-slate-900/80 backdrop-blur-xl border-b border-white/10 px-4 py-3">',
    '<div className="max-w-7xl mx-auto px-6 py-4 mb-8 bg-white/70 dark:bg-slate-900/40 backdrop-blur-xl rounded-2xl shadow-sm border border-slate-200 dark:border-white/10">'
)

# Update layout container
text = text.replace(
    '<div className="flex min-h-screen pt-[122px]">',
    '<div className="flex flex-col lg:flex-row max-w-7xl mx-auto gap-8 px-4 sm:px-6 lg:px-8">'
)

# Left column
text = text.replace(
    '<div className="flex-1 max-w-xl p-6 overflow-y-auto">',
    '<div className="flex-1 px-2">'
)
text = text.replace(
    '<div className="bg-slate-900/60 border border-white/10 rounded-2xl p-5 mb-6">',
    '<div className="bg-white/70 dark:bg-slate-900/40 backdrop-blur-xl rounded-3xl shadow-xl dark:shadow-none border border-slate-200 dark:border-white/10 p-6 md:p-8 mb-6">'
)

# Right column
text = text.replace(
    '<div className="w-[420px] border-l border-white/10 bg-slate-900/40 p-4 flex flex-col sticky top-[122px] h-[calc(100vh-122px)] overflow-y-auto">',
    '<div className="w-full lg:w-[460px] bg-white/70 dark:bg-slate-900/40 backdrop-blur-xl rounded-3xl shadow-xl dark:shadow-none border border-slate-200 dark:border-white/10 p-6 flex flex-col sticky top-24 h-[calc(100vh-120px)] overflow-y-auto">'
)

# Template picker styling
text = text.replace(
    "border-teal-500 shadow-lg shadow-teal-500/20",
    "border-indigo-500 dark:border-cyan-500 shadow-lg shadow-indigo-500/20 dark:shadow-cyan-500/20"
)
text = text.replace(
    "bg-teal-500 text-slate-900",
    "bg-indigo-600 dark:bg-cyan-500 text-white dark:text-slate-900 hover:bg-indigo-700 dark:hover:bg-cyan-400"
)
text = text.replace(
    "hover:bg-teal-400",
    "hover:bg-indigo-700 dark:hover:bg-cyan-400"
)
text = text.replace(
    "bg-teal-500/20 text-teal-400",
    "bg-indigo-100 dark:bg-cyan-500/20 text-indigo-700 dark:text-cyan-400"
)
text = text.replace(
    "text-teal-400",
    "text-indigo-600 dark:text-cyan-400"
)

# Inputs and Labels
text = text.replace(
    "const inp = 'w-full bg-slate-800/80 border border-white/10 rounded-xl px-3 py-2.5 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-teal-500/60 focus:ring-1 focus:ring-teal-500/20 transition-all';",
    "const inp = 'w-full bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-white/10 rounded-xl px-3 py-2.5 text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 text-sm focus:outline-none focus:border-indigo-500/60 dark:focus:border-cyan-500/60 focus:ring-1 focus:ring-indigo-500/20 dark:focus:ring-cyan-500/20 transition-all';"
)
text = text.replace(
    "const lbl = 'block text-xs font-semibold text-slate-400 mb-1';",
    "const lbl = 'block text-xs font-semibold text-slate-700 dark:text-slate-400 mb-1';"
)

text = text.replace(
    'text-slate-400 text-sm mb-6',
    'text-slate-600 dark:text-slate-400 text-sm mb-6'
)
text = text.replace(
    'text-xs font-bold uppercase tracking-widest text-slate-400 mb-3',
    'text-xs font-bold uppercase tracking-widest text-slate-500 dark:text-slate-400 mb-3'
)
text = text.replace(
    'text-center text-xs text-slate-500 mt-3',
    'text-center text-xs text-slate-500 mt-3'
)

# Accent color changes
text = text.replace("accent-teal-500", "accent-indigo-600 dark:accent-cyan-500")
text = text.replace("bg-teal-500", "bg-indigo-600 dark:bg-cyan-500 text-white dark:text-slate-900")
text = text.replace("text-slate-900 font-bold", "font-bold shadow-sm")

# Preview text
text = text.replace(
    '<p className="text-xs font-bold text-white">Live Preview</p>',
    '<p className="text-xs font-bold text-slate-900 dark:text-white">Live Preview</p>'
)
text = text.replace(
    '<span className="text-xs font-bold text-slate-300">ATS Score</span>',
    '<span className="text-xs font-bold text-slate-900 dark:text-slate-300">ATS Score</span>'
)
text = text.replace(
    '<div className="bg-slate-900 border border-white/10 rounded-2xl p-4">',
    '<div className="bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-white/10 rounded-2xl p-4 mt-4 shadow-sm dark:shadow-none">'
)

text = text.replace(
    "bg-slate-800/40 border border-white/10",
    "bg-slate-50 dark:bg-slate-800/40 border border-slate-200 dark:border-white/10"
)

text = text.replace(
    "bg-slate-800 border border-white/10 rounded-xl",
    "bg-white dark:bg-slate-800 border border-slate-200 dark:border-white/10 shadow-sm rounded-xl"
)

text = text.replace(
    "text-slate-900 dark:text-slate-900 font-bold shadow-sm",
    "text-white dark:text-slate-900 font-bold shadow-sm"
)

# Checklists in preview
text = text.replace(
    "className={done?'text-slate-300':'text-slate-500'}",
    "className={done?'text-slate-700 dark:text-slate-300':'text-slate-400 dark:text-slate-500'}"
)

# Re-update bg-slate-800 classes that were used generally for buttons
text = text.replace(
    "bg-slate-800 border border-white/10 rounded-xl",
    "bg-white dark:bg-slate-800 border border-slate-200 dark:border-white/10 shadow-sm rounded-xl"
)

with open("src/pages/ResumeBuilderPage.jsx", "w", encoding="utf-8") as f:
    f.write(text)

