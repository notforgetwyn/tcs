"""Delete entire geometry/CAD tab and all related methods."""
path = '/home/shihuayue/codex_project/src/foamdesk/ui/main_window.py'
with open(path) as f:
    c = f.read()

# 1. Remove tab registration
c = c.replace('''        self._workspace_tabs.addTab(self._build_geometry_tab(), "几何/CAD")\n''', '')

# 2. Remove _build_geometry_tab method - find its range
start = c.find('    def _build_geometry_tab(self) -> QWidget:')
# Find next top-level method after it
end = c.find('\n    def _build_settings_tab(self) -> QWidget:')
if end < 0:
    end = c.find('\n    def _build_results_tab(self) -> QWidget:')
if end < 0:
    end = c.find('\n    def _build_environment_tab(self) -> QWidget:')

if start > 0 and end > start:
    c = c[:start] + c[end:]
    print('1. _build_geometry_tab removed')
else:
    print('1. SKIPPED (start=' + str(start) + ' end=' + str(end) + ')')

# 3. Remove geometry-specific methods. Each method to remove:
methods_to_remove = [
    '_open_geometry_tab', '_import_stl_geometry', '_read_stl_transform_dialog',
    '_draw_stl_transform_preview', '_apply_domain_template', '_apply_custom_domain',
    '_apply_boundary_conditions', '_refresh_geometry_panel', '_load_domain_template_into_form',
    '_load_custom_domain_inputs', '_load_boundary_conditions_into_form',
    '_refresh_domain_template_hint', '_update_domain_apply_state_label',
    '_domain_template_stl_hint', '_refresh_domain_preview', '_current_domain_template',
    '_selected_domain_template', '_draw_domain_template_wireframe', '_draw_domain_wireframe',
    '_draw_unit_domain_wireframe', '_draw_pipe_domain_wireframe', '_draw_bend_domain_wireframe',
    '_style_domain_preview_axes', '_read_stl_preview_mesh', '_read_draw_geometry',
    '_import_template_stl', '_template_stl_path', '_edit_imported_stl_transform',
    '_preview_imported_stl', '_show_cad_import_limitations',
    '_generate_snappy_hex_mesh_dict', '_select_stl_asset_for_snappy',
    '_run_snappy_hex_mesh', '_run_check_mesh', '_run_preprocess_pipeline',
    '_run_simulation_pipeline', '_run_preflight_check',
    '_load_snappy_settings_into_form', '_pick_stl_asset_dialog',
    '_open_domain_preview_dialog'
]

count = 0
for name in methods_to_remove:
    pattern = '\n    def ' + name + '(self'
    idx = c.find(pattern)
    if idx < 0:
        # Try with type hints
        pattern = '\n    def ' + name + '(self)'
        idx = c.find(pattern)
    if idx > 0:
        # Find the end of this method (next top-level def at same indent)
        nxt = c.find('\n    def ', idx + 1)
        if nxt > 0:
            c = c[:idx] + c[nxt:]
            count += 1
    else:
        # Try broader search
        idx2 = c.find('def ' + name + '(')
        if idx2 > 0 and ('\n    def ' in c[max(0,idx2-10):idx2+10] or '    def ' in c[max(0,idx2-10):idx2+10]):
            nxt = c.find('\n    def ', idx2 + 1)
            if nxt > 0:
                c = c[:c.rfind('\n    def ', 0, idx2)] + c[nxt:]
                count += 1

print('2. Removed ' + str(count) + ' geometry methods')

# 4. Remove menu entries
c = c.replace('        geometry_menu = self._menu_bar.addMenu("几何/CAD")\n', '')
c = c.replace('        geometry_menu.addAction("导入 STL 几何", self._import_stl_geometry)\n', '')
c = c.replace('        geometry_menu.addAction("打开几何/CAD 页", self._open_geometry_tab)\n', '')
c = c.replace('        geometry_menu.addAction("预览已导入 STL", self._preview_imported_stl)\n', '')

# Remove menu creation lines that reference geometry
for line_to_remove in [
    '        geometry_menu = self._menu_bar.addMenu("几何/CAD")\n',
    '        geometry_menu.addAction("导入 STL 几何", self._import_stl_geometry)\n',
    '        geometry_menu.addAction("一键仿真流水线", self._run_simulation_pipeline)\n',
]:
    c = c.replace(line_to_remove, '')
print('3. Menu entries removed')

# 5. Shift setCurrentIndex: now geometry (index 2) is gone, so N >= 3 becomes N-1
import re
def shift_geo(m):
    idx = int(m.group(1))
    # Tab order: 0:项目主页 1:绘制几何 2:求解器选择 3:仿真参数 4:求解运行 5:环境检查 6:设置 7:结果
    # After removing geometry (was at old index 2):
    # 0:项目主页 1:绘制几何 2:求解器选择 3:仿真参数 4:求解运行 5:环境检查 6:设置 7:结果
    # N was already shifted for geometry (old 2→1), now geometry is gone
    # Old mapping: 3→2, 4→3, 5→4, 6→5, 7→6
    if idx >= 3:
        return 'self._workspace_tabs.setCurrentIndex(' + str(idx - 1) + ')'
    return m.group(0)

# Wait, the indices are already shifted from when we moved geometry to index 1.
# Current state: 0:项目主页 1:绘制几何 2:几何/CAD 3:求解器选择 ...
# After removal: 0:项目主页 1:绘制几何 2:求解器选择 3:仿真参数 ...
# So N >= 3 becomes N-1, N=2 was geometry which should be gone
c, n = re.subn(r'self\._workspace_tabs\.setCurrentIndex\((\d+)\)', shift_geo, c)
print('4. Shifted ' + str(n) + ' setCurrentIndex calls')

with open(path, 'w') as f:
    f.write(c)
print('DONE')
