path = '/home/shihuayue/codex_project/src/foamdesk/ui/main_window.py'
with open(path) as f:
    c = f.read()

# 1. Add clear vertex button in UI row
old_v = "vh.addWidget(del_v); vh.addWidget(csv_v)"
new_v = "clear_v = QPushButton(\"清空\"); clear_v.clicked.connect(self._clear_all_vertices); vh.addWidget(del_v); vh.addWidget(clear_v); vh.addWidget(csv_v)"
c = c.replace(old_v, new_v)

# 2. Add clear edge button
old_e = "de_btn = QPushButton(\"删除选中边\")\n        de_btn.clicked.connect(self._delete_selected_edge)\n        layout.addWidget(de_btn)"
new_e = "de_btn = QPushButton(\"删除选中边\")\n        de_btn.clicked.connect(self._delete_selected_edge)\n        clr_e = QPushButton(\"清空边\")\n        clr_e.clicked.connect(self._clear_all_edges)\n        er = QHBoxLayout(); er.setSpacing(6)\n        er.addWidget(de_btn); er.addWidget(clr_e); er.addStretch(1)\n        layout.addLayout(er)"
c = c.replace(old_e, new_e)

# 3. Add clear methods before _add_vertex_row
marker = '\n    def _add_vertex_row(self, x=0.0, y=0.0, z=0.0):'
methods = """
    def _clear_all_vertices(self):
        self._vertex_table.blockSignals(True)
        while self._vertex_table.rowCount() > 0:
            self._vertex_table.removeRow(0)
        self._vertex_table.blockSignals(False)
        self._save_vertex_table()
        self._refresh_draw_geo_preview()

    def _clear_all_edges(self):
        self._edge_defs = []
        if self._geo_objects:
            self._geo_objects[self._active_obj_idx]["edges"] = []
        self._update_edge_list()
        self._refresh_draw_geo_preview()

"""
c = c.replace(marker, methods + marker)

with open(path, 'w') as f:
    f.write(c)
print('OK')
