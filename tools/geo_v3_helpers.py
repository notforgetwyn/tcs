"""Add helper methods to draw geometry page."""
path = '/home/shihuayue/codex_project/src/foamdesk/ui/main_window.py'
with open(path) as f:
    c = f.read()

# Find insertion point: right before _apply_draw_geometry
marker = '\n    def _apply_draw_geometry(self):'

helpers = '''
    # --- Object management ---
    def _rebuild_obj_combo(self):
        self._obj_combo.blockSignals(True)
        self._obj_combo.clear()
        for obj in self._geo_objects:
            self._obj_combo.addItem(obj["name"])
        self._obj_combo.setCurrentIndex(self._active_obj_idx)
        self._obj_combo.blockSignals(False)
        is_domain = (self._active_obj_idx == 0)
        self._block_widget.setVisible(is_domain)
        self._boundary_widget.setVisible(is_domain)

    def _save_current_object(self):
        if not self._geo_objects: return
        obj = self._geo_objects[self._active_obj_idx]
        obj["verts"] = self._read_draw_geo_vertices()
        obj["edges"] = list(self._edge_defs)
        if self._active_obj_idx == 0:
            obj["block_v"] = [sb.value() for sb in self._block_vert_inputs]
            obj["nx"] = self._geo_nx.value()
            obj["ny"] = self._geo_ny.value()
            obj["nz"] = self._geo_nz.value()
            obj["grading"] = self._geo_grading.text().strip() or "1 1 1"

    def _switch_active_object(self, idx):
        if idx < 0 or idx >= len(self._geo_objects): return
        self._save_current_object()
        self._active_obj_idx = idx
        self._load_active_object_to_ui()
        self._rebuild_obj_combo()
        self._refresh_draw_geo_preview()

    def _load_active_object_to_ui(self):
        obj = self._geo_objects[self._active_obj_idx]
        self._edge_defs = list(obj.get("edges", []))
        self._vertex_table.blockSignals(True)
        while self._vertex_table.rowCount() > 0:
            self._vertex_table.removeRow(0)
        for x,y,z in obj["verts"]:
            self._add_vertex_row(x,y,z)
        self._vertex_table.blockSignals(False)
        self._update_edge_list()
        if self._active_obj_idx == 0:
            bv = obj.get("block_v",[0,1,2,3,4,5,6,7])
            for i,sb in enumerate(self._block_vert_inputs):
                sb.setValue(bv[i] if i<len(bv) else i)
            self._geo_nx.setValue(obj.get("nx",10))
            self._geo_ny.setValue(obj.get("ny",10))
            self._geo_nz.setValue(obj.get("nz",10))
            self._geo_grading.setText(obj.get("grading","1 1 1"))

    def _new_geo_object(self):
        self._save_current_object()
        name = "几何体" + str(len(self._geo_objects))
        dv = [(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)]
        self._geo_objects.append({"name":name,"verts":list(dv),"edges":[],"is_domain":False})
        self._active_obj_idx = len(self._geo_objects) - 1
        self._load_active_object_to_ui()
        self._rebuild_obj_combo()
        self._refresh_draw_geo_preview()

    def _delete_geo_object(self):
        if self._active_obj_idx == 0:
            self._show_error("不能删除计算域。")
            return
        self._geo_objects.pop(self._active_obj_idx)
        self._active_obj_idx = 0
        self._load_active_object_to_ui()
        self._rebuild_obj_combo()
        self._refresh_draw_geo_preview()

    # --- Vertex helpers ---
    def _add_vertex_row(self, x=0.0, y=0.0, z=0.0):
        r = self._vertex_table.rowCount()
        self._vertex_table.insertRow(r)
        for j,v in enumerate([x,y,z]):
            self._vertex_table.setItem(r, j, QTableWidgetItem(str(float(v))))

    def _read_draw_geo_vertices(self):
        verts = []
        for i in range(self._vertex_table.rowCount()):
            row = []
            for j in range(3):
                item = self._vertex_table.item(i,j)
                try: row.append(float(item.text()) if item else 0.0)
                except ValueError: row.append(0.0)
            verts.append(tuple(row))
        return verts

    def _save_vertex_table(self):
        if self._geo_objects:
            self._geo_objects[self._active_obj_idx]["verts"] = self._read_draw_geo_vertices()

    def _on_vertex_table_changed(self):
        self._save_vertex_table()
        self._refresh_draw_geo_preview()

    def _delete_selected_vertex(self):
        rows = set(i.row() for i in self._vertex_table.selectedIndexes())
        for r in sorted(rows, reverse=True):
            self._vertex_table.removeRow(r)
        self._save_vertex_table()
        self._refresh_draw_geo_preview()

    # --- Edge helpers ---
    def _add_edge_to_current(self):
        et = self._edge_type_combo.currentText()
        s = self._edge_start.value(); e = self._edge_end.value()
        ip = self._edge_interp.text().strip()
        self._edge_defs.append((et,s,e,ip))
        if self._geo_objects:
            self._geo_objects[self._active_obj_idx]["edges"] = list(self._edge_defs)
        self._update_edge_list()
        self._refresh_draw_geo_preview()

    def _update_edge_list(self):
        lines = []
        for et,s,e,ip in self._edge_defs:
            lines.append(et + " " + str(s) + " " + str(e) + (" (" + ip + ")" if ip else ""))
        self._edge_list.setPlainText("\\n".join(lines))

    def _delete_selected_edge(self):
        cur = self._edge_list.textCursor()
        if cur.hasSelection():
            st = cur.selectionStart(); ed = cur.selectionEnd()
            text = self._edge_list.toPlainText()
            lines = text.split("\\n")
            pos = 0; rm = []
            for i,line in enumerate(lines):
                le = pos + len(line)
                if st < le and ed > pos: rm.append(i)
                pos = le + 1
            for i in sorted(rm, reverse=True):
                if i < len(lines): lines.pop(i)
                if i < len(self._edge_defs): self._edge_defs.pop(i)
            if self._geo_objects:
                self._geo_objects[self._active_obj_idx]["edges"] = list(self._edge_defs)
            self._edge_list.setPlainText("\\n".join(lines))
            self._refresh_draw_geo_preview()

    # --- Block helpers ---
    def _on_block_vert_changed(self):
        if self._geo_objects and self._active_obj_idx == 0:
            self._geo_objects[0]["block_v"] = [sb.value() for sb in self._block_vert_inputs]
        self._refresh_draw_geo_preview()

    def _on_cell_changed(self):
        if self._geo_objects and self._active_obj_idx == 0:
            obj = self._geo_objects[0]
            obj["nx"] = self._geo_nx.value()
            obj["ny"] = self._geo_ny.value()
            obj["nz"] = self._geo_nz.value()

    def _on_grading_changed(self):
        if self._geo_objects and self._active_obj_idx == 0:
            self._geo_objects[0]["grading"] = self._geo_grading.text().strip() or "1 1 1"

'''

# Replace _apply_draw_geometry and _refresh_draw_geo_preview and add new helpers
# Find _apply_draw_geometry
old_apply = c.find('    def _apply_draw_geometry(self):')
# Find _reset_draw_geometry
old_reset = c.find('    def _reset_draw_geometry(self):')

# Keep only from _apply onwards
c = c[:old_apply] + helpers + c[old_apply:]

with open(path, 'w') as f:
    f.write(c)
print('OK - helpers added')
