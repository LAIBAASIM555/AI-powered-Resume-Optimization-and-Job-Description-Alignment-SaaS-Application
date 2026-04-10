import re

with open("src/pages/ResumeBuilderPage.jsx", "r", encoding="utf-8") as f:
    text = f.read()

# I am completely overriding handlePrint with the simplest native JS implementation 
# and stripping ANY previous failed python remnants.

start_marker = "  // Print PDF"
end_marker = "  return ("

if start_marker in text and end_marker in text:
    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker)
    
    clean_handle_print = """  // Print PDF
  const handlePrint = () => {
    const element = printRef.current;
    if (!element) return;
    const win = window.open('', '_blank');
    win.document.write(`<html><head><title>${data.name || 'Resume'}</title>
      <style>body{margin:0;padding:20px;font-family:sans-serif;font-size:11px;color:#111;}
      @page{size:A4;margin:15mm;} *{box-sizing:border-box;}</style></head><body>`);
    win.document.write(element.innerHTML);
    win.document.write('</body></html>');
    win.document.close();
    win.focus();
    setTimeout(() => { win.print(); win.close(); }, 400);
  };

"""
    new_text = text[:start_idx] + clean_handle_print + text[end_idx:]
    
    with open("src/pages/ResumeBuilderPage.jsx", "w", encoding="utf-8") as f:
        f.write(new_text)
    print("Successfully replaced handlePrint block.")
else:
    print("Could not find markers.")
