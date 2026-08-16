path = '/home/shihuayue/codex_project/src/foamdesk/ui/main_window.py'
with open(path) as f:
    c = f.read()

# 1. Delete custom domain section
old_custom = """        custom_domain_size_row = QHBoxLayout()
        custom_domain_size_row.setSpacing(8)
        custom_domain_cells_row = QHBoxLayout()
        custom_domain_cells_row.setSpacing(8)
        self._domain_length_x_input = QDoubleSpinBox()
        self._domain_length_y_input = QDoubleSpinBox()
        self._domain_length_z_input = QDoubleSpinBox()
        for input_widget in (
            self._domain_length_x_input,
            self._domain_length_y_input,
            self._domain_length_z_input,
        ):
            input_widget.setRange(0.01, 100000.0)
            input_widget.setDecimals(3)
            input_widget.setSingleStep(0.5)
            input_widget.setValue(1.0)
        self._domain_cells_x_input = QSpinBox()
        self._domain_cells_y_input = QSpinBox()
        self._domain_cells_z_input = QSpinBox()
        for input_widget in (
            self._domain_cells_x_input,
            self._domain_cells_y_input,
            self._domain_cells_z_input,
        ):
            input_widget.setRange(1, 100000)
            input_widget.setValue(10)
        apply_custom_domain_button = QPushButton("应用自定义计算域")
        apply_custom_domain_button.clicked.connect(lambda _checked=False: self._apply_custom_domain())
        for label, input_widget in (
            ("Lx", self._domain_length_x_input),
            ("Ly", self._domain_length_y_input),
            ("Lz", self._domain_length_z_input),
        ):
            input_widget.setMinimumWidth(96)
            custom_domain_size_row.addWidget(QLabel(label))
            custom_domain_size_row.addWidget(input_widget)
        custom_domain_size_row.addStretch(1)
        for label, input_widget in (
            ("Nx", self._domain_cells_x_input),
            ("Ny", self._domain_cells_y_input),
            ("Nz", self._domain_cells_z_input),
        ):
            input_widget.setMinimumWidth(96)
            custom_domain_cells_row.addWidget(QLabel(label))
            custom_domain_cells_row.addWidget(input_widget)
        custom_domain_cells_row.addWidget(apply_custom_domain_button)
        custom_domain_cells_row.addStretch(1)
        custom_domain_widget = QWidget()
        custom_domain_layout = QVBoxLayout(custom_domain_widget)
        custom_domain_layout.setContentsMargins(0, 0, 0, 0)
        custom_domain_layout.setSpacing(6)
        custom_domain_layout.addLayout(custom_domain_size_row)
        custom_domain_layout.addLayout(custom_domain_cells_row)
        domain_form.addRow("自定义尺寸/网格", custom_domain_widget)"""

c = c.replace(old_custom, "")
print('1. custom domain section removed')

# 2. Add import button next to apply_domain_button
old_btn = "        apply_domain_button.clicked.connect(lambda _checked=False: self._apply_domain_template())"
new_btn = """        import_draw_btn = QPushButton("从绘制几何导入")
        import_draw_btn.clicked.connect(lambda _checked=False: self._import_draw_geometry_domain())
        apply_domain_button.clicked.connect(lambda _checked=False: self._apply_domain_template())"""
c = c.replace(old_btn, new_btn)

# 3. Add import button to domain_row
old_domain_row = "        domain_row.addWidget(import_template_stl_button)"
new_domain_row = "        domain_row.addWidget(import_draw_btn)\n        domain_row.addWidget(import_template_stl_button)"
c = c.replace(old_domain_row, new_domain_row)

# 4. Add _import_draw_geometry_domain method
# Find a good spot - before _apply_domain_template
marker = '\n    def _apply_domain_template(self):'
method = """
    def _import_draw_geometry_domain(self):
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
            self._set_status("已从绘制几何导入计算域。")
            self._append_log("从绘制几何导入计算域：" + str(payload.get("name", "手工绘制")))
        else:
            self._show_error("当前 domain_config.json 不是绘制几何生成的自定义域。")

"""
c = c.replace(marker, method + marker)

with open(path, 'w') as f:
    f.write(c)
print('OK')
