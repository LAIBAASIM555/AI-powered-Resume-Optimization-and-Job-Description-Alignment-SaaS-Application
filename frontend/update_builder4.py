import re

with open("src/pages/ResumeBuilderPage.jsx", "r", encoding="utf-8") as f:
    text = f.read()

# Try exact string match first
broken_section = """  useEffect(() => {
    localStorage.setItem(DRAFT_KEY, JSON  // Print PDF
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
  }; { scale: 2, useCORS: true, letterRendering: true, logging: false },
      jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' }
    };"""

fixed_section = """  useEffect(() => {
    localStorage.setItem(DRAFT_KEY, JSON.stringify(data));
  }, [data]);

  const set = useCallback((field, value) => setData(d => ({ ...d, [field]: value })), []);
  const { score, checks } = calcATS(data);
  const PreviewTemplate = TemplateMap[template];
  const sectionsComplete = [
    !!(data.name && data.email),
    (data.summary || '').length > 10,
    data.skills.length >= 3,
    data.experience.some(e => e.title),
    data.education.some(e => e.school),
  ].filter(Boolean).length;

  // Print PDF
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

if broken_section in text:
    text = text.replace(broken_section, fixed_section)
else:
    # Use regex
    text = re.sub(r'  useEffect\(\(\) => \{\n    localStorage\.setItem\(DRAFT_KEY, JSON.*?jsPDF:\s*\{\s*unit:\s*\'mm\', format:\s*\'a4\', orientation:\s*\'portrait\'\s*\}\n\s*\};', fixed_section.replace('\\', '\\\\'), text, flags=re.DOTALL)

with open("src/pages/ResumeBuilderPage.jsx", "w", encoding="utf-8") as f:
    f.write(text)
