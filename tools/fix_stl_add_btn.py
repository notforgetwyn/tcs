path = '/home/shihuayue/codex_project/src/foamdesk/ui/main_window.py'
with open(path) as f:
    c = f.read()

# 1. Fix STL binary format: write normal once per triangle, not per vertex
old_stl = """                    sf.write(_struct.pack("<3f", *n))
                        sf.write(_struct.pack("<3f", *vert))
                    sf.write(_struct.pack("<H", 0))"""
new_stl = """                    sf.write(_struct.pack("<3f", *n))
                    for vert in (v0,v1,v2):
                        sf.write(_struct.pack("<3f", *vert))
                    sf.write(_struct.pack("<H", 0))"""

# Wait, the old_stl has a problem - the for loop should be AFTER the normal
# Actually looking at it more carefully:
# Current: for vert in (v0,v1,v2): sf.write(n); sf.write(vert) — writes normal 3x
# Fixed: sf.write(n); for vert in (v0,v1,v2): sf.write(vert)

# Find the actual indented code
old_stl_real = """                for v0,v1,v2 in tris:
                    u = _np.array(v1)-_np.array(v0); v = _np.array(v2)-_np.array(v0)
                    n = _np.cross(u,v); n = n/(_np.linalg.norm(n)+1e-12)
                    for vert in (v0,v1,v2):
                        sf.write(_struct.pack("<3f", *n))
                        sf.write(_struct.pack("<3f", *vert))
                    sf.write(_struct.pack("<H", 0))"""

new_stl_real = """                for v0,v1,v2 in tris:
                    u = _np.array(v1)-_np.array(v0); v = _np.array(v2)-_np.array(v0)
                    n = _np.cross(u,v); n = n/(_np.linalg.norm(n)+1e-12)
                    sf.write(_struct.pack("<3f", *n))
                    sf.write(_struct.pack("<3f", *v0))
                    sf.write(_struct.pack("<3f", *v1))
                    sf.write(_struct.pack("<3f", *v2))
                    sf.write(_struct.pack("<H", 0))"""

c = c.replace(old_stl_real, new_stl_real)
print('1. STL fixed')

# 2. Add "读取绘制几何" button + method
# 2a. Add button next to apply_domain_button
old_btn = "        apply_domain_button.clicked.connect(lambda _checked=False: self._apply_domain_template())"
new_btn = """        apply_domain_button.clicked.connect(lambda _checked=False: self._apply_domain_template())
        read_draw_btn = QPushButton("读取绘制几何")
        read_draw_btn.clicked.connect(lambda _checked=False: self._read_draw_geometry())"""
c = c.replace(old_btn, new_btn)

# 2b. Add button to layout
old_row = "        domain_row.addWidget(apply_domain_button)"
new_row = "        domain_row.addWidget(apply_domain_button)\n        domain_row.addWidget(read_draw_btn)"
c = c.replace(old_row, new_row)

# 2c. Add _read_draw_geometry method before _refresh_geometry_panel
marker = '\n    def _refresh_geometry_panel(self) -> None:'
method = """
    def _read_draw_geometry(self):
        if self._current_project is None:
            self._show_error("请先新建或打开项目。"); return
        dc_path = self._current_project.case_dir / "system" / "domain_config.json"
        if not dc_path.exists():
            self._show_error("未找到 domain_config.json，请先在绘制几何页生成 blockMeshDict。"); return
        import json
        try:
            payload = json.loads(dc_path.read_text(encoding="utf-8"))
        except Exception as e:
            self._show_error("读取失败：" + str(e)); return
        if payload.get("key") != "custom_domain":
            self._show_error("domain_config.json 不是绘制几何生成的自定义域。"); return
        idx = self._domain_template_combo.findData("custom_domain")
        if idx < 0:
            self._domain_template_combo.addItem("手工绘制", "custom_domain")
            self._domain_template_combo.setCurrentIndex(self._domain_template_combo.count()-1)
        else:
            self._domain_template_combo.setCurrentIndex(idx)
        self._load_domain_template_into_form()
        self._geometry_text.setPlainText(self._context.geometry_import_service.format_assets(self._current_project))
        self._refresh_domain_preview()
        stl_dir = self._current_project.case_dir / "constant" / "triSurface"
        count = 0
        for stl_path in sorted(stl_dir.glob("body_*.stl")):
            try:
                self._context.geometry_import_service.import_stl(self._current_project, stl_path)
                count += 1
            except Exception:
                pass
        if count > 0:
            self._geometry_text.setPlainText(self._context.geometry_import_service.format_assets(self._current_project))
            self._refresh_domain_preview()
            self._append_log("读取绘制几何：{} 个几何体已导入。".format(count))
        self._set_status("已读取绘制几何。" + (" + {} 个 STL。".format(count) if count > 0 else ""))
        self._append_log("读取绘制几何：计算域 " + str(payload.get("name", "手工绘制")))

"""
c = c.replace(marker, method + marker)
print('2. read draw geo button added')

with open(path, 'w') as f:
    f.write(c)
print('DONE')
