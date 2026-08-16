path = '/home/shihuayue/codex_project/src/foamdesk/ui/main_window.py'
with open(path) as f:
    c = f.read()

# Fix _rebuild_obj_combo to use hasattr
old = '''        self._block_widget.setVisible(is_domain)
        self._boundary_widget.setVisible(is_domain)'''

new = '''        if hasattr(self, "_block_widget"):
            self._block_widget.setVisible(is_domain)
        if hasattr(self, "_boundary_widget"):
            self._boundary_widget.setVisible(is_domain)'''

c = c.replace(old, new)
with open(path, 'w') as f:
    f.write(c)
print('OK - fixed')
