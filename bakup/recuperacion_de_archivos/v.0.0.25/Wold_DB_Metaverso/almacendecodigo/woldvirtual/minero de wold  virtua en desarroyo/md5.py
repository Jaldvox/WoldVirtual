def _reset_form_fields(self):
    """Clear all input fields and reset form to initial state"""
    # Clear text entries
    self.entry_nombre.delete(0, tk.END)
    self.entry_descripcion.delete(0, tk.END)
    
    # Reset any error styling
    self.entry_nombre.configure(bg='white')
    self.entry_descripcion.configure(bg='white')
    
    # Clear any error messages
    if hasattr(self, 'error_label'):
        self.error_label.config(text='')
        
    # Reset focus to first field
    self.entry_nombre.focus()
    
    # Clear any selection or clipboard content
    self.entry_nombre.selection_clear()
    self.entry_descripcion.selection_clear()
    
    # Reset any validation states
    self.entry_nombre.config(state='normal')
    self.entry_descripcion.config(state='normal')
