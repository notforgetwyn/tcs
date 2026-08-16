"""WSL writer - copy to WSL /tmp then run"""
path = '/home/shihuayue/codex_project/src/foamdesk/ui/main_window.py'
with open(path) as f:
    c = f.read()

start = c.find('    def _build_draw_geometry_tab(self) -> QWidget:')
end = c.find('\n    def _build_geometry_tab(self) -> QWidget:')

with open('/tmp/method_v3.txt') as f:
    new_code = f.read()

c = c[:start] + new_code + c[end:]
with open(path, 'w') as f:
    f.write(c)
print('OK')
