path = '/home/shihuayue/codex_project/src/foamdesk/ui/main_window.py'
with open(path) as f:
    c = f.read()

# 1. Add button next to apply_domain_button
old_btn = "        apply_domain_button.clicked.connect(lambda _checked=False: self._apply_domain_template())"
new_btn = """        apply_domain_button.clicked.connect(lambda _checked=False: self._apply_domain_template())
        read_draw_btn = QPushButton("读取绘制几何")
        read_draw_btn.clicked.connect(lambda _checked=False: self._read_draw_geometry())"""
c = c.replace(old_btn, new_btn)

# 2. Add button to domain_row
old_row = "        domain_row.addWidget(apply_domain_button)"
new_row = "        domain_row.addWidget(apply_domain_button)\n        domain_row.addWidget(read_draw_btn)"
c = c.replace(old_row, new_row)

# 3. Add _read_draw_geometry method before _refresh_geometry_panel
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

with open(path, 'w') as f:
    f.write(c)
print('OK')
