path = '/home/shihuayue/codex_project/src/foamdesk/ui/main_window.py'
with open(path) as f:
    c = f.read()

# 1. Add CSV import button to vertex row
old_v = "        vh.addWidget(add_v); vh.addWidget(del_v)"
new_v = """        csv_v = QPushButton("导入CSV")
        csv_v.clicked.connect(self._import_vertices_csv)
        vh.addWidget(add_v); vh.addWidget(del_v); vh.addWidget(csv_v)"""
c = c.replace(old_v, new_v)

# 2. Add CSV import button to edge row
old_e = "        ef.addWidget(ae); ef.addStretch(1)"
new_e = """        csv_e = QPushButton("导入CSV")
        csv_e.clicked.connect(self._import_edges_csv)
        ef.addWidget(ae); ef.addWidget(csv_e); ef.addStretch(1)"""
c = c.replace(old_e, new_e)

# 3. Add import methods before _add_vertex_row
marker = '\n    def _add_vertex_row(self, x=0.0, y=0.0, z=0.0):'
methods = """
    def _import_vertices_csv(self):
        fp, _ = QFileDialog.getOpenFileName(self, "导入顶点 CSV", "", "CSV (*.csv)")
        if not fp: return
        import csv
        with open(fp, newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                clean = [v.strip() for v in row if v.strip()]
                if len(clean) >= 3:
                    try:
                        x, y, z = float(clean[0]), float(clean[1]), float(clean[2])
                        self._add_vertex_row(x, y, z)
                    except ValueError:
                        continue
        self._save_vertex_table()
        self._refresh_draw_geo_preview()

    def _import_edges_csv(self):
        fp, _ = QFileDialog.getOpenFileName(self, "导入边 CSV", "", "CSV (*.csv)")
        if not fp: return
        import csv
        with open(fp, newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                clean = [v.strip() for v in row if v.strip()]
                if len(clean) < 3: continue
                etype = clean[0]
                if etype not in ("arc","spline","polyLine","BSpline"): continue
                try:
                    s = int(clean[1]); e = int(clean[2])
                    interp = " ".join(clean[3:]) if len(clean) > 3 else ""
                    self._edge_defs.append((etype, s, e, interp))
                except ValueError:
                    continue
        if self._geo_objects:
            self._geo_objects[self._active_obj_idx]["edges"] = list(self._edge_defs)
        self._update_edge_list()
        self._refresh_draw_geo_preview()

"""
c = c.replace(marker, methods + marker)

with open(path, 'w') as f:
    f.write(c)
print('OK')
