"""Replace _refresh_draw_geo_preview, _apply_draw_geometry, _reset_draw_geometry"""
path = '/home/shihuayue/codex_project/src/foamdesk/ui/main_window.py'
with open(path) as f:
    c = f.read()

# 1. Replace _refresh_draw_geo_preview
old_pv = c.find('    def _refresh_draw_geo_preview(self):')
old_next = c.find('    def _draw_edge_in_preview(self, axes, verts, etype, start, end, interp_str):')

new_pv = '''
    def _draw_edge_in_preview(self, axes, verts, etype, start, end, interp_str):
        if start >= len(verts) or end >= len(verts): return
        p0 = np.array(verts[start]); p1 = np.array(verts[end])
        try: coords = [float(v) for v in interp_str.split()]
        except ValueError: coords = []
        if etype == "arc" and len(coords) >= 3:
            interp = np.array(coords[:3])
            mid = (p0+p1)/2.0; offset = interp - mid
            t = np.linspace(0,1,60)
            pts = (1-t)[:,None]*p0 + t[:,None]*p1 + np.sin(t*np.pi)[:,None]*offset
            axes.plot(pts[:,0],pts[:,1],pts[:,2], color="#4fc1ff", linewidth=1.4, alpha=0.9)
        elif etype in ("spline","polyLine","BSpline") and len(coords) >= 3:
            ctrl = [p0]
            for k in range(len(coords)//3):
                ctrl.append(np.array(coords[k*3:(k+1)*3]))
            ctrl.append(p1); ctrl = np.array(ctrl)
            t = np.linspace(0,1,60); n = len(ctrl)-1; pts = np.zeros((len(t),3))
            import math
            for k in range(n+1):
                pts += math.comb(n,k) * (t**k)[:,None] * ((1-t)**(n-k))[:,None] * ctrl[k]
            axes.plot(pts[:,0],pts[:,1],pts[:,2], color="#4fc1ff", linewidth=1.4, alpha=0.9)
        else:
            axes.plot([p0[0],p1[0]],[p0[1],p1[1]],[p0[2],p1[2]], color="#4fc1ff", linewidth=1.4, alpha=0.9)

    def _refresh_draw_geo_preview(self):
        if not hasattr(self,"_geo_preview_fig") or not hasattr(self,"_geo_preview_canvas"): return
        self._geo_preview_fig.clear()
        axes = self._geo_preview_fig.add_subplot(111, projection="3d", facecolor="#1e1e1e")
        axes.set_title("Geometry Preview", color="#d4d4d4", pad=10)
        axes.set_axis_off()
        if not self._geo_objects:
            self._geo_preview_canvas.draw(); return

        all_pts = []
        for oi, obj in enumerate(self._geo_objects):
            verts = obj.get("verts", [])
            if not verts: continue
            corners = np.array(verts, dtype=float)
            all_pts.append(corners)
            is_domain = (oi == 0)
            is_active = (oi == self._active_obj_idx)

            if is_domain:
                axes.scatter(corners[:,0],corners[:,1],corners[:,2], c="#ff9944", s=30, alpha=0.9)
                for i,v in enumerate(verts):
                    axes.text(v[0],v[1],v[2], str(i), color="#ff9944", fontsize=8)
                for edef in obj.get("edges",[]):
                    self._draw_edge_in_preview(axes, verts, edef[0],edef[1],edef[2],edef[3])
                bv = obj.get("block_v",[0,1,2,3,4,5,6,7])
                if all(v < len(verts) for v in bv):
                    faces = [[0,3,7,4],[1,5,6,2],[0,1,2,3],[4,5,6,7],[0,1,5,4],[3,2,6,7]]
                    fc = [(0.537,0.820,0.522,0.25),(0.957,0.529,0.443,0.25)] + [(0.310,0.757,1.000,0.08)]*4
                    ec = [(0.537,0.820,0.522,0.50),(0.957,0.529,0.443,0.50)] + [(0.310,0.757,1.000,0.30)]*4
                    for face,fcol,ecol in zip(faces,fc,ec):
                        vs = [corners[bv[i]] for i in face]
                        axes.add_collection3d(Poly3DCollection([vs], facecolors=[fcol], edgecolors=[ecol], linewidths=1.2))
                    axes.text(corners[bv[0],0],corners[bv[0],1],corners[bv[0],2], "inlet", color="#89d185")
                    axes.text(corners[bv[1],0],corners[bv[1],1],corners[bv[1],2], "outlet", color="#f48771")
            else:
                alpha = 0.65 if is_active else 0.35
                ec = (1.0,0.6,0.2,0.9) if is_active else (0.5,0.5,0.5,0.6)
                fc = (1.0,0.6,0.2,0.30) if is_active else (0.5,0.5,0.5,0.15)
                if len(verts) >= 8:
                    esc = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
                    for s,e in esc:
                        if s<len(verts) and e<len(verts):
                            axes.plot([corners[s,0],corners[e,0]],[corners[s,1],corners[e,1]],[corners[s,2],corners[e,2]], color=ec, linewidth=1.5, alpha=0.9)
                    faces = [[0,3,7,4],[1,5,6,2],[0,1,2,3],[4,5,6,7],[0,1,5,4],[3,2,6,7]]
                    for face in faces:
                        if all(v<len(verts) for v in face):
                            vs = [corners[v] for v in face]
                            axes.add_collection3d(Poly3DCollection([vs], facecolors=[fc], edgecolors=[ec], linewidths=1.0))

        if all_pts:
            ap = np.vstack(all_pts)
            mn = ap.min(axis=0); mx = ap.max(axis=0)
            ct = (mn+mx)/2.0
            rad = max(float((mx-mn).max())/2.0, 0.55)
            axes.set_xlim(ct[0]-rad, ct[0]+rad)
            axes.set_ylim(ct[1]-rad, ct[1]+rad)
            axes.set_zlim(ct[2]-rad, ct[2]+rad)
        axes.view_init(elev=24, azim=-55)
        self._geo_preview_canvas.draw()

'''

c = c[:old_pv] + new_pv + c[old_next:]

# 2. Replace _apply_draw_geometry
old_apply = c.find('    def _apply_draw_geometry(self):')
old_apply_end = c.find('    def _reset_draw_geometry(self):')

new_apply = '''    def _apply_draw_geometry(self):
        if self._current_project is None:
            self._show_error("请先新建或打开项目。"); return
        self._save_current_object()
        domain = self._geo_objects[0]
        verts = domain.get("verts", [])
        if len(verts) < 8:
            self._show_error("计算域至少需要 8 个顶点。"); return
        nx = domain.get("nx",10); ny = domain.get("ny",10); nz = domain.get("nz",10)
        grading = domain.get("grading","1 1 1")
        bv = domain.get("block_v",[0,1,2,3,4,5,6,7])
        vl = "\\n".join("    ({} {} {})".format(x,y,z) for x,y,z in verts)
        el = ""
        for et,s,e,ip in domain.get("edges",[]):
            el += "    {} {} {} ({})\\n".format(et,s,e,ip) if ip else "    {} {} {}\\n".format(et,s,e)
        bl_line = "    hex ({}) ({} {} {}) simpleGrading ({})\\n".format(" ".join(str(v) for v in bv), nx, ny, nz, grading)
        il = self._geo_inlet.text().strip() or "inlet"
        ol = self._geo_outlet.text().strip() or "outlet"
        wl = self._geo_walls.text().strip() or "fixedWalls"
        bm = ("FoamFile\\n{{\\n    version     2.0;\\n    format      ascii;\\n"
              "    class       dictionary;\\n    object      blockMeshDict;\\n}}\\n\\n"
              "convertToMeters 1;\\n\\nvertices\\n(\\n{});\\n\\n"
              "blocks\\n(\\n{});\\n\\nedges\\n(\\n{});\\n\\n"
              "boundary\\n(\\n    {} {{ type patch; faces ((0 4 7 3)); }}\\n"
              "    {} {{ type patch; faces ((1 2 6 5)); }}\\n"
              "    {} {{ type wall; faces ((0 1 5 4) (0 3 2 1) (4 5 6 7) (3 7 6 2)); }}\\n);\\n\\n"
              "mergePatchPairs\\n(\\n);\\n").format(vl, bl_line, el, il, ol, wl)
        bp = self._current_project.case_dir / "system" / "blockMeshDict"
        bp.parent.mkdir(parents=True, exist_ok=True)
        bp.write_text(bm, encoding="utf-8")
        xs = [v[0] for v in verts]; ys = [v[1] for v in verts]; zs = [v[2] for v in verts]
        size = (max(xs)-min(xs), max(ys)-min(ys), max(zs)-min(zs))
        import json as _json
        dc_path = self._current_project.case_dir / "system" / "domain_config.json"
        dc_path.write_text(_json.dumps({"key":"custom_domain","name":"手工绘制","size":[round(v,4) for v in size],"cells":[nx,ny,nz],"suggested_location_in_mesh":[round(size[0]*0.1,4),round(size[1]*0.5,4),round(size[2]*0.5,4)],"shape":"box"}, ensure_ascii=False, indent=2), encoding="utf-8")
        self._append_log("blockMeshDict 已生成 (domain): {} 顶点 {}x{}x{}".format(len(verts), nx, ny, nz))

        import struct as _struct
        stl_dir = self._current_project.case_dir / "constant" / "triSurface"
        stl_dir.mkdir(parents=True, exist_ok=True)
        for bi, body in enumerate(self._geo_objects[1:], 1):
            bverts = body.get("verts", [])
            if len(bverts) < 8: continue
            tris = []
            vv = [(float(x),float(y),float(z)) for x,y,z in bverts]
            faces_b = [(0,3,1),(1,3,2),(4,5,7),(5,6,7),(0,1,5),(0,5,4),(3,7,6),(3,6,2),(0,4,7),(0,7,3),(1,2,6),(1,6,5)]
            for f in faces_b:
                if all(idx < len(vv) for idx in f):
                    tris.append((vv[f[0]], vv[f[1]], vv[f[2]]))
            if not tris: continue
            import numpy as _np
            stl_name = "body_{}_{}.stl".format(bi, body["name"])
            stl_path = stl_dir / stl_name
            with open(stl_path, "wb") as sf:
                sf.write(b"\\x00"*80)
                sf.write(_struct.pack("<I", len(tris)))
                for v0,v1,v2 in tris:
                    u = _np.array(v1)-_np.array(v0); v = _np.array(v2)-_np.array(v0)
                    n = _np.cross(u,v); n = n/(_np.linalg.norm(n)+1e-12)
                    for vert in (v0,v1,v2):
                        sf.write(_struct.pack("<3f", *n))
                        sf.write(_struct.pack("<3f", *vert))
                    sf.write(_struct.pack("<H", 0))
            self._append_log("STL 已导出: " + stl_name + " (" + str(len(tris)) + " 三角形)")
        self._set_status("blockMeshDict + STL 已生成。")

'''

c = c[:old_apply] + new_apply + c[old_apply_end:]

# 3. Replace _reset_draw_geometry
old_reset = c.find('    def _reset_draw_geometry(self):')
old_reset_end = len(c)  # last method

new_reset = '''    def _reset_draw_geometry(self):
        dv = [(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)]
        self._geo_objects = [{"name":"计算域","verts":list(dv),"edges":[],"block_v":[0,1,2,3,4,5,6,7],"is_domain":True,"nx":10,"ny":10,"nz":10,"grading":"1 1 1"}]
        self._active_obj_idx = 0
        self._edge_defs = []
        self._geo_inlet.setText("inlet")
        self._geo_outlet.setText("outlet")
        self._geo_walls.setText("fixedWalls")
        self._rebuild_obj_combo()
        self._load_active_object_to_ui()
        self._refresh_draw_geo_preview()
'''

c = c[:old_reset] + new_reset

with open(path, 'w') as f:
    f.write(c)
print('OK - final methods updated')
