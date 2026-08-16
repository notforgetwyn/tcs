path = '/home/shihuayue/codex_project/src/foamdesk/ui/main_window.py'
with open(path) as f:
    c = f.read()

old = '''        if key == "custom_domain":
            self._load_domain_template_into_form()
            self._refresh_geometry_panel()
            self._set_status("已从绘制几何导入计算域。")
            self._append_log("从绘制几何导入计算域：" + str(payload.get("name", "手工绘制")))
        else:
            self._show_error("当前 domain_config.json 不是绘制几何生成的自定义域。")'''

new = '''        if key == "custom_domain":
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

c = c.replace(old, new)
with open(path, 'w') as f:
    f.write(c)
print('OK')
