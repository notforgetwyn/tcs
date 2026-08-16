path = '/home/shihuayue/codex_project/src/foamdesk/ui/main_window.py'
with open(path) as f:
    c = f.read()

# Replace _import_draw_geometry_domain with file dialog version
old = '''    def _import_draw_geometry_domain(self):
        if self._current_project is None:
            self._show_error("请先新建或打开项目。"); return
        dc_path = self._current_project.case_dir / "system" / "domain_config.json"
        if not dc_path.exists():
            self._show_error("未找到 domain_config.json，请先在绘制几何页生成 blockMeshDict。"); return
        import json
        try:
            payload = json.loads(dc_path.read_text(encoding="utf-8"))
        except Exception as e:
            self._show_error("读取 domain_config.json 失败：" + str(e)); return
        key = payload.get("key", "")
        if key == "custom_domain":
            self._load_domain_template_into_form()
            self._refresh_geometry_panel()
            # Also import body STLs from draw geometry
            stl_dir = self._current_project.case_dir / "constant" / "triSurface"
            count = 0
            for stl_path in sorted(stl_dir.glob("body_*.stl")):
                try:
                    self._context.geometry_import_service.import_stl(self._current_project, stl_path)
                    count += 1
                except Exception:
                    pass
            if count > 0:
                self._append_log("从绘制几何导入 {} 个几何体 STL。".format(count))
                self._refresh_geometry_panel()
            self._set_status("已从绘制几何导入计算域" + (" + {} 个几何体。".format(count) if count > 0 else "。"))
            self._append_log("从绘制几何导入计算域：" + str(payload.get("name", "手工绘制")))
        else:
            self._show_error("当前 domain_config.json 不是绘制几何生成的自定义域。")'''

new = '''    def _import_draw_geometry_domain(self):
        if self._current_project is None:
            self._show_error("请先新建或打开项目。"); return
        start_dir = str(self._current_project.case_dir / "system")
        fp, _ = QFileDialog.getOpenFileName(self, "选择 domain_config.json", start_dir, "JSON (*.json)")
        if not fp: return
        dc_path = Path(fp)
        import json
        try:
            payload = json.loads(dc_path.read_text(encoding="utf-8"))
        except Exception as e:
            self._show_error("读取失败：" + str(e)); return
        key = payload.get("key", "")
        if key != "custom_domain":
            self._show_error("所选文件不是绘制几何生成的自定义域。"); return
        self._load_domain_template_into_form()
        self._refresh_geometry_panel()
        # Import body STLs from same project
        stl_dir = dc_path.parent.parent / "constant" / "triSurface"
        count = 0
        if stl_dir.exists():
            for stl_path in sorted(stl_dir.glob("body_*.stl")):
                try:
                    self._context.geometry_import_service.import_stl(self._current_project, stl_path)
                    count += 1
                except Exception:
                    pass
        if count > 0:
            self._append_log("从绘制几何导入 {} 个几何体 STL。".format(count))
            self._refresh_geometry_panel()
        self._set_status("已从绘制几何导入计算域" + (" + {} 个几何体。".format(count) if count > 0 else "。"))
        self._append_log("从绘制几何导入计算域：" + str(payload.get("name", "手工绘制")))'''

c = c.replace(old, new)
with open(path, 'w') as f:
    f.write(c)
print('OK')
