path = '/home/shihuayue/codex_project/src/foamdesk/ui/main_window.py'
with open(path) as f:
    c = f.read()

old = "        dv = [(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)]\n        self._geo_objects.append({\"name\":name,\"verts\":list(dv),\"edges\":[],\"is_domain\":False})"

new = """        domain_verts = self._geo_objects[0]["verts"]
        xs = [v[0] for v in domain_verts]; ys = [v[1] for v in domain_verts]; zs = [v[2] for v in domain_verts]
        s = 0.25  # half-size = 50% of domain = 0.25 from center
        dx = (max(xs)-min(xs))*s; dy = (max(ys)-min(ys))*s; dz = (max(zs)-min(zs))*s
        cx = (min(xs)+max(xs))/2; cy = (min(ys)+max(ys))/2; cz = (min(zs)+max(zs))/2
        dv = [(cx-dx,cy-dy,cz-dz),(cx+dx,cy-dy,cz-dz),(cx+dx,cy+dy,cz-dz),(cx-dx,cy+dy,cz-dz),
              (cx-dx,cy-dy,cz+dz),(cx+dx,cy-dy,cz+dz),(cx+dx,cy+dy,cz+dz),(cx-dx,cy+dy,cz+dz)]
        self._geo_objects.append({"name":name,"verts":list(dv),"edges":[],"is_domain":False})"""

c = c.replace(old, new)
with open(path, 'w') as f:
    f.write(c)
print('OK')
