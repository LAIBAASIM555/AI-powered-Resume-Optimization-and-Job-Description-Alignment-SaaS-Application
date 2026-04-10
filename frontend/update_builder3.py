import re

with open("src/pages/ResumeBuilderPage.jsx", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update padding for header
text = text.replace(
    'pt-20 pb-12 overflow-hidden',
    'pt-28 pb-12 overflow-hidden'
)

# 2. Fix the print function
old_print = """  // Print PDF
  const handlePrint = () => {
    const win = window.open('', '_blank');
    win.document.write(`<html><head><title>${data.name || 'Resume'}</title>
      <style>body{margin:0;padding:20px;font-family:sans-serif;font-size:11px;color:#111;}
      @page{size:A4;margin:15mm;} *{box-sizing:border-box;}</style></head><body>`);
    win.document.write(printRef.current.innerHTML);
    win.document.write('</body></html>');
    win.document.close();
    win.focus();
    setTimeout(() => { win.print(); win.close(); }, 400);
  };"""

new_print = """  // Print PDF
  const handlePrint = async () => {
    const element = printRef.current;
    if (!element) return;
    
    // Convert lucide icons to images or remove them for html2canvas if needed, but it handles SVGs okay usually
    const toastId = toast.loading('Generating high-quality ATS-friendly PDF...');

    const opt = {
      margin:       [10, 10, 10, 10],
      filename:     `${data.name ? data.name.replace(/\\s+/g, '_') : 'resume'}_optimized.pdf`,
      image:        { type: 'jpeg', quality: 1.0 },
      html2canvas:  { scale: 2, useCORS: true, letterRendering: true, logging: false },
      jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' }
    };

    try {
      const html2pdf = (await import('html2pdf.js')).default;
      await html2pdf().set(opt).from(element).save();
      toast.success('Downloaded successfully!', { id: toastId });
    } catch (e) {
      console.error(e);
      toast.error('Failed to generate PDF', { id: toastId });
    }
  };"""
if old_print in text:
    text = text.replace(old_print, new_print)

# 3. Add AI Suggest
if "handleSuggestSkillsAI" not in text:
    ai_suggest_func = """  const handleSuggestSkillsAI = () => {
    setIsGenerating(true);
    const toastId = toast.loading('AI analyzing job role...');
    setTimeout(() => {
      const suggest = ['Strategic Leadership', 'Cross-functional Collaboration', 'Process Optimization'];
      const newSkills = suggest.filter(s => !data.skills.includes(s));
      if (newSkills.length > 0) {
        set('skills', [...data.skills, ...newSkills]);
        toast.success(`AI added highly relevant skills!`, { id: toastId });
      } else {
        toast.success('Your skills are already well-optimized!', { id: toastId });
      }
      setIsGenerating(false);
    }, 1500);
  };"""
    text = text.replace("  /* ─── Step content ─── */", ai_suggest_func + "\n\n  /* ─── Step content ─── */")

# 4. Replace Skills Header
old_skills_header = """<p className="text-xs font-semibold text-slate-700 dark:text-slate-400 mb-1">Your Skills</p>"""
new_skills_header = """<div className="flex justify-between items-center mb-1">
            <p className="text-xs font-semibold text-slate-700 dark:text-slate-400">Skills Highlights</p>
            <button onClick={handleSuggestSkillsAI} disabled={isGenerating} className="flex items-center gap-1.5 px-3 py-1.5 bg-gradient-to-r from-purple-500/10 to-indigo-500/10 hover:from-purple-500/20 hover:to-indigo-500/20 border border-purple-500/20 text-purple-600 dark:text-purple-400 rounded-lg text-xs font-bold transition-all disabled:opacity-50">
              {isGenerating ? <div className="w-3 h-3 border-2 border-purple-400 border-t-transparent rounded-full animate-spin" /> : <Sparkles className="w-3.5 h-3.5" />}
              Suggest with AI
            </button>
          </div>"""
text = text.replace(old_skills_header, new_skills_header)

# 5. Replace Add Experience button
old_add_exp = """<button onClick={addExp} className="w-full py-2.5 border border-dashed border-white/20 rounded-xl text-slate-400 text-sm hover:border-teal-500/40 hover:text-indigo-600 dark:hover:text-cyan-400 transition-all flex items-center justify-center gap-1"><Plus className="w-4 h-4"/>Add Work Experience</button>"""
new_add_exp = """<button onClick={addExp} className="group relative w-full py-3 overflow-hidden rounded-xl bg-slate-100 dark:bg-slate-800/60 border border-dashed border-slate-300 dark:border-white/20 hover:border-indigo-500/50 dark:hover:border-cyan-500/50 transition-all flex items-center justify-center gap-2 mt-4">
          <div className="absolute inset-0 w-full h-full bg-gradient-to-r from-transparent via-indigo-500/5 dark:via-cyan-500/10 to-transparent -translate-x-full group-hover:animate-[shimmer_1.5s_infinite]" />
          <Plus className="w-4 h-4 text-slate-500 group-hover:text-indigo-600 dark:group-hover:text-cyan-400 transition-colors"/>
          <span className="text-sm font-bold text-slate-600 dark:text-slate-400 group-hover:text-indigo-600 dark:group-hover:text-cyan-400 transition-colors">Add Experience Module</span>
        </button>"""
text = text.replace(old_add_exp, new_add_exp)

# 6. Replace Add Education button
old_add_edu = """<button onClick={addEdu} className="w-full py-2.5 border border-dashed border-white/20 rounded-xl text-slate-400 text-sm hover:border-teal-500/40 hover:text-indigo-600 dark:hover:text-cyan-400 transition-all flex items-center justify-center gap-1"><Plus className="w-4 h-4"/>Add Education</button>"""
new_add_edu = """<button onClick={addEdu} className="group relative w-full py-3 overflow-hidden rounded-xl bg-slate-100 dark:bg-slate-800/60 border border-dashed border-slate-300 dark:border-white/20 hover:border-purple-500/50 dark:hover:border-purple-500/50 transition-all flex items-center justify-center gap-2 mt-4">
          <div className="absolute inset-0 w-full h-full bg-gradient-to-r from-transparent via-purple-500/5 dark:via-purple-500/10 to-transparent -translate-x-full group-hover:animate-[shimmer_1.5s_infinite]" />
          <Plus className="w-4 h-4 text-slate-500 group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors"/>
          <span className="text-sm font-bold text-slate-600 dark:text-slate-400 group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors">Add Credential</span>
        </button>"""
text = text.replace(old_add_edu, new_add_edu)

# 7. Add imports needed for the extra components (Globe, LayoutGrid) if not present
if "Globe," not in text:
    text = text.replace("Award", "Award, Globe, LayoutGrid")

# 8. Extra section
old_extra = """    if (step === 6) {
      const addCert = () => set('certifications', [...(data.certifications||[]), '']);
      const updateCert = (i, v) => { const c=[...data.certifications]; c[i]=v; set('certifications',c); };
      return (
        <div className="space-y-5">
          <div>
            <div className="flex justify-between items-center mb-2">
              <p className="text-sm font-semibold text-slate-300">Certifications</p>
              <button onClick={addCert} className="flex items-center gap-1 text-indigo-600 dark:text-cyan-400 text-xs hover:text-teal-300"><Plus className="w-3 h-3"/>Add</button>
            </div>
            {(data.certifications||[]).map((c,i)=>(
              <input key={i} className={`${inp} mb-2`} placeholder="e.g., Google UX Design Certificate" value={c} onChange={e=>updateCert(i,e.target.value)} />
            ))}
          </div>
          <div>
            <p className="text-sm font-semibold text-slate-300 mb-2">Languages</p>
            <input className={inp} placeholder="e.g., English (Native), Urdu (Fluent)" value={data.languages} onChange={e=>set('languages',e.target.value)} />
          </div>
          <div>
            <p className="text-sm font-semibold text-slate-300 mb-2">Projects</p>
            <textarea rows={3} className={`${inp} resize-none`} placeholder="e.g., Portfolio Website — Built with React & Tailwind..." value={data.projects||''} onChange={e=>set('projects',e.target.value)} />
          </div>
        </div>
      );
    }"""

new_extra = """    if (step === 6) {
      const addCert = () => set('certifications', [...(data.certifications||[]), '']);
      const updateCert = (i, v) => { const c=[...data.certifications]; c[i]=v; set('certifications',c); };
      const removeCert = (i) => { const c=[...data.certifications]; c.splice(i,1); set('certifications',c); };
      
      const addProj = () => set('projects', [...(data.projects||[]), '']);
      const updateProj = (i, v) => { const c=[...data.projects||[]]; c[i]=v; set('projects',c); };
      const removeProj = (i) => { const c=[...data.projects||[]]; c.splice(i,1); set('projects',c); };
      
      return (
        <div className="space-y-8">
          <div className="bg-slate-50 dark:bg-slate-800/30 p-5 rounded-2xl border border-slate-200 dark:border-white/5 relative overflow-hidden">
            <div className="absolute top-0 right-0 p-4 opacity-5 pointer-events-none"><Award className="w-24 h-24" /></div>
            <div className="flex justify-between items-center mb-4 relative z-10">
              <div className="flex items-center gap-2"><Award className="w-4 h-4 text-amber-500" /><p className="text-sm font-bold text-slate-800 dark:text-white">Certifications</p></div>
              <button onClick={addCert} className="flex items-center gap-1 text-amber-600 dark:text-amber-400 text-xs font-bold hover:text-amber-500"><Plus className="w-3 h-3"/>Add</button>
            </div>
            <div className="space-y-3 relative z-10">
            {(data.certifications||[]).map((c,i)=>(
              <div key={i} className="flex items-center gap-2">
                <input className={`${inp} flex-1`} placeholder="e.g., Google UX Design Certificate" value={c} onChange={e=>updateCert(i,e.target.value)} />
                <button onClick={()=>removeCert(i)} className="p-2 text-slate-400 hover:text-rose-500 transition-colors bg-white dark:bg-slate-800 border border-slate-200 dark:border-white/10 rounded-xl"><Trash2 className="w-4 h-4" /></button>
              </div>
            ))}
            {(data.certifications||[]).length === 0 && <p className="text-xs text-slate-500 text-center py-2">No certifications added yet.</p>}
            </div>
          </div>
          
          <div className="bg-slate-50 dark:bg-slate-800/30 p-5 rounded-2xl border border-slate-200 dark:border-white/5 relative overflow-hidden">
             <div className="absolute top-0 right-0 p-4 opacity-5 pointer-events-none"><Globe className="w-24 h-24" /></div>
             <div className="flex items-center gap-2 mb-3 relative z-10"><Globe className="w-4 h-4 text-blue-500 dark:text-blue-400" /><p className="text-sm font-bold text-slate-800 dark:text-white">Languages</p></div>
            <input className={`${inp} relative z-10`} placeholder="e.g., English (Native), Spanish (Fluent)" value={data.languages} onChange={e=>set('languages',e.target.value)} />
          </div>
          
          <div className="bg-slate-50 dark:bg-slate-800/30 p-5 rounded-2xl border border-slate-200 dark:border-white/5 relative overflow-hidden">
            <div className="absolute top-0 right-0 p-4 opacity-5 pointer-events-none"><LayoutGrid className="w-24 h-24" /></div>
            <div className="flex justify-between items-center mb-4 relative z-10">
              <div className="flex items-center gap-2"><LayoutGrid className="w-4 h-4 text-emerald-500 dark:text-emerald-400" /><p className="text-sm font-bold text-slate-800 dark:text-white">Key Projects</p></div>
              <button onClick={addProj} className="flex items-center gap-1 text-emerald-600 dark:text-emerald-400 text-xs font-bold hover:text-emerald-500"><Plus className="w-3 h-3"/>Add</button>
            </div>
            
            <div className="space-y-3 relative z-10">
            {(data.projects||[]).map((c,i)=>(
              <div key={i} className="flex gap-2">
                <textarea rows={2} className={`${inp} flex-1 resize-none`} placeholder="Describe project and tech stack..." value={c} onChange={e=>updateProj(i,e.target.value)} />
                <button onClick={()=>removeProj(i)} className="p-2 text-slate-400 hover:text-rose-500 transition-colors bg-white dark:bg-slate-800 border border-slate-200 dark:border-white/10 rounded-xl h-fit"><Trash2 className="w-4 h-4" /></button>
              </div>
            ))}
            {(data.projects||[]).length === 0 && <p className="text-xs text-slate-500 text-center py-2">No projects added yet.</p>}
            </div>
            
          </div>
        </div>
      );
    }"""
text = text.replace(old_extra, new_extra)

with open("src/pages/ResumeBuilderPage.jsx", "w", encoding="utf-8") as f:
    f.write(text)
