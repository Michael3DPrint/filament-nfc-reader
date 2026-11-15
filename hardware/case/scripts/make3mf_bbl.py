# Writes Bambu Studio 2.9-style 3MFs using the user's saved v8 file as the settings template
import sys, os, re, json, zipfile, numpy as np, trimesh
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from build_case import *
TPL=os.environ.get('BAMBU_TEMPLATE_DIR','/tmp/u8')   # folder holding an extracted, saved Bambu Studio 2.9 project (a .3mf unzipped); its settings are the template

def mesh_of(m):
    mm=m.to_mesh(); v=np.array(mm.vert_properties,dtype=np.float64)[:,:3]; f=np.array(mm.tri_verts)
    t=trimesh.Trimesh(v,f,process=False); t.merge_vertices()
    # drop zero-thickness slivers left by coincident faces, keep the real solid(s)
    parts=[c for c in t.split(only_watertight=False) if len(c.faces)>20]
    t=trimesh.util.concatenate(parts) if len(parts)>1 else parts[0]
    t.update_faces(t.nondegenerate_faces()); t.remove_unreferenced_vertices()
    if not t.is_watertight:                      # cleaning must never open the mesh: fall back to the raw Manifold mesh
        return v, f
    return np.array(t.vertices,dtype=np.float64), np.array(t.faces)


def single_black_pla(d, keep=1):
    """Reduce the template's 5 filament slots to one: Bambu PLA Basic (slot 2 of the template), black."""
    nf=len(d['filament_settings_id'])
    # variable-length per-filament groups (AMS drying lists): lengths per filament differ
    for k,v in list(d.items()):
        if not isinstance(v,list): continue
        L=len(v)
        if not (k.startswith(('filament','flush_volumes')) or L in (nf,nf*6)): continue
        if k=='flush_volumes_matrix':
            n2=L//(nf*nf); d[k]=[v[b*nf*nf+keep*nf+keep] for b in range(n2)]; continue
        if L%nf==0:
            per=L//nf; d[k]=v[keep*per:(keep+1)*per]
        elif k.startswith('filament_dev_'):
            # groups of 4/8 per Bambu filament, 1 for third-party; slot 0 and 1 are Bambu
            per=4 if L==17 else 8; d[k]=v[keep*per:(keep+1)*per]
    d['filament_colour']=['#000000']; d['filament_multi_colour']=['#000000']
    if 'filament_colour_type' in d: d['filament_colour_type']=['0']
    d['filament_map']=['1']
    if 'filament_self_index' in d: d['filament_self_index']=['1']*len(d['filament_self_index'])

def write_bbl(path, items, title, enable_support=True):
    """items: list of (name, manifold, (x,y) plate centre)"""
    objs=[]; res=[]; build=[]; cfg=[]; plate=[]; assem=[]
    n=len(items)
    for i,(name,m,(cx,cy)) in enumerate(items):
        oid_comp=2*i+1; oid=2*i+2
        v,t=mesh_of(m); lo,hi=v.min(0),v.max(0); ctr=(lo+hi)/2; half=(hi[2]-lo[2])/2
        v=v-ctr
        vs="\n".join(f'     <vertex x="{a:.7f}" y="{b:.7f}" z="{c_:.7f}"/>' for a,b,c_ in v)
        ts="\n".join(f'     <triangle v1="{a}" v2="{b}" v3="{c_}"/>' for a,b,c_ in t)
        objs.append((f'3D/Objects/object_{i+1}.model', f'''<?xml version="1.0" encoding="UTF-8"?>
<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p">
 <metadata name="BambuStudio:3mfVersion">1</metadata>
 <resources>
  <object id="{oid_comp}" p:UUID="{i+1:04d}0000-81cb-4c03-9d28-80fed5dfa1dc" type="model">
   <mesh>
    <vertices>
{vs}
    </vertices>
    <triangles>
{ts}
    </triangles>
   </mesh>
  </object>
 </resources>
 <build/>
</model>'''))
        res.append(f'''  <object id="{oid}" p:UUID="{i+1:08d}-61cb-4c03-9d28-80fed5dfa1dc" type="model">
   <components>
    <component p:path="/3D/Objects/object_{i+1}.model" objectid="{oid_comp}" p:UUID="{i+1:04d}0000-b206-40ff-9872-83e8017abed1" transform="1 0 0 0 1 0 0 0 1 0 0 0"/>
   </components>
  </object>''')
        build.append(f'  <item objectid="{oid}" p:UUID="{i+1:08d}-b1ec-4553-aec9-835e5b724bb4" transform="1 0 0 0 1 0 0 0 1 {cx:.6f} {cy:.6f} {half:.6f}" printable="1"/>')
        cfg.append(f'''  <object id="{oid}">
    <metadata key="name" value="{name}"/>
    <metadata key="extruder" value="1"/>
    <metadata face_count="{len(t)}"/>
    <part id="{oid_comp}" subtype="normal_part">
      <metadata key="name" value="{name}"/>
      <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>
      <mesh_stat face_count="{len(t)}" edges_fixed="0" degenerate_facets="0" facets_removed="0" facets_reversed="0" backwards_edges="0"/>
    </part>
  </object>''')
        plate.append(f'''    <model_instance>
      <metadata key="object_id" value="{oid}"/>
      <metadata key="instance_id" value="0"/>
      <metadata key="identify_id" value="{100+i*22}"/>
    </model_instance>''')
        assem.append(f'   <assemble_item object_id="{oid}" instance_id="0" transform="1 0 0 0 1 0 0 0 1 {cx:.6f} {cy:.6f} {half:.6f}" offset="0 0 0" />\n   <assemble_item object_id="{oid}" volume_id="0" transform="1 0 0 0 1 0 0 0 1 0 0 0" />')
    model=f'''<?xml version="1.0" encoding="UTF-8"?>
<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p">
 <metadata name="Application">BambuStudio-02.09.01.70</metadata>
 <metadata name="BambuStudio:3mfVersion">1</metadata>
 <metadata name="Copyright"></metadata>
 <metadata name="CreationDate">2026-11-14</metadata>
 <metadata name="Description"></metadata>
 <metadata name="Designer"></metadata>
 <metadata name="DesignerCover"></metadata>
 <metadata name="DesignerUserId"></metadata>
 <metadata name="License"></metadata>
 <metadata name="ModificationDate">2026-11-14</metadata>
 <metadata name="Origin"></metadata>
 <metadata name="ProfileCover"></metadata>
 <metadata name="ProfileDescription"></metadata>
 <metadata name="ProfileTitle"></metadata>
 <metadata name="Title">{title}</metadata>
 <resources>
{chr(10).join(res)}
 </resources>
 <build p:UUID="2c7c17d8-22b5-4d84-8835-1976022ea369">
{chr(10).join(build)}
 </build>
</model>'''
    settings=f'''<?xml version="1.0" encoding="UTF-8"?>
<config>
{chr(10).join(cfg)}
  <plate>
    <metadata key="plater_id" value="1"/>
    <metadata key="plater_name" value=""/>
    <metadata key="locked" value="false"/>
    <metadata key="filament_map_mode" value="Auto For Flush"/>
{chr(10).join(plate)}
  </plate>
  <assemble>
{chr(10).join(assem)}
  </assemble>
</config>'''
    ps=open(f'{TPL}/Metadata/project_settings.config').read()
    d=json.loads(ps)
    d['curr_bed_type']='Textured PEI Plate'
    single_black_pla(d)
    if enable_support: d['enable_support']='1'
    ps=json.dumps(d,indent=4)
    cut='<?xml version="1.0" encoding="utf-8"?>\n<objects>\n'+''.join(f' <object id="{2*i+1}">\n  <cut_id id="0" check_sum="1" connectors_cnt="0"/>\n </object>\n' for i in range(n))+'</objects>'
    rels='<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'+''.join(f' <Relationship Target="/3D/Objects/object_{i+1}.model" Id="rel-{i+1}" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>\n' for i in range(n))+'</Relationships>'
    root_rels='<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n <Relationship Target="/3D/3dmodel.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>\n</Relationships>'
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml',open(f'{TPL}/[Content_Types].xml').read())
        z.writestr('_rels/.rels',root_rels)
        z.writestr('3D/3dmodel.model',model)
        z.writestr('3D/_rels/3dmodel.model.rels',rels)
        for p,c in objs: z.writestr(p,c)
        z.writestr('Metadata/model_settings.config',settings)
        z.writestr('Metadata/project_settings.config',ps)
        z.writestr('Metadata/slice_info.config',open(f'{TPL}/Metadata/slice_info.config').read())
        z.writestr('Metadata/cut_information.xml',cut)
        z.writestr('Metadata/filament_sequence.json',open(f'{TPL}/Metadata/filament_sequence.json').read())

write_bbl('filament_nfc_v20_rigid_parts.3mf',[
    ('Case_Body',body,(68,75)),
    ('NFC_Arm',arm_print,(215,75)),
    ('Faceplate',fp_print,(118,200)),
    ('NFC_Top_Lid',lid_print,(215,150)),
    ('Spine_Cover',cover_print,(156,80))],
    'Filament NFC reader v20 - rigid parts (body, NFC arm, faceplate, NFC lid, spine cover)', enable_support=False)
print('ok')
