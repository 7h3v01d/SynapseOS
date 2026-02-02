def log_to_console(console, msg, is_error=False):
    tag = "error" if is_error else "info"
    console.insert("end", msg + "\n", tag)
    console.see("end")
    console.update_idletasks()

def filter_supported_models(models):
    return [m.name for m in models if "generateContent" in m.supported_generation_methods]