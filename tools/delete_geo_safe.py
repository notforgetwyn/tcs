"""Safely remove geometry tab: delete tab+menu only, keep methods."""
path = '/home/shihuayue/codex_project/src/foamdesk/ui/main_window.py'
with open(path) as f:
    c = f.read()

# 1. Remove tab registration
old_tab = '        self._workspace_tabs.addTab(self._build_geometry_tab(), "几何/CAD")\n'
c = c.replace(old_tab, '')

# 2. Remove menu entries
for line in [
    '        geometry_menu = self._menu_bar.addMenu("几何/CAD")\n',
    '        geometry_menu.addAction("导入 STL 几何", self._import_stl_geometry)\n',
    '        geometry_menu.addAction("打开几何/CAD 页", self._open_geometry_tab)\n',
    '        geometry_menu.addAction("预览已导入 STL", self._preview_imported_stl)\n',
    '        geometry_menu.addAction("一键仿真流水线", self._run_simulation_pipeline)\n',
]:
    c = c.replace(line, '')

# 3. Shift setCurrentIndex: geometry was at index 2, so N>=3 -> N-1
import re
c, n = re.subn(
    r'self\._workspace_tabs\.setCurrentIndex\((\d+)\)',
    lambda m: 'self._workspace_tabs.setCurrentIndex(' + str(int(m.group(1)) - 1) + ')' if int(m.group(1)) >= 3 else m.group(0),
    c
)
print('Shifted ' + str(n) + ' indices')

with open(path, 'w') as f:
    f.write(c)
print('DONE')
