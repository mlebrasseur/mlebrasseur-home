#!/usr/bin/env python3
"""Build the self-contained offline viewer and four-scene GLB.

Python 3 standard library only. All inputs live in this folder.
Shared right-side geometry comes from v4. Sources: SRC-2026-104, 105.
"""
from pathlib import Path
import runpy
import base64
import copy
import hashlib
import json
import struct

HERE = Path(__file__).resolve().parent
OUT = HERE / 'dist'
I = .0254


def read_glb(path):
    raw = path.read_bytes()
    assert raw[:4] == b'glTF'
    size = struct.unpack_from('<I', raw, 12)[0]
    doc = json.loads(raw[20:20+size])
    return doc, raw[28+size:]


def encode_glb(doc, binary):
    doc = copy.deepcopy(doc)
    doc['buffers'] = [{'byteLength': len(binary)}]
    meta = json.dumps(doc, separators=(',', ':'), ensure_ascii=True).encode()
    meta += b' ' * (-len(meta) % 4)
    binary = bytes(binary) + b'\0' * (-len(binary) % 4)
    return (struct.pack('<4sII', b'glTF', 2, 28+len(meta)+len(binary))
            + struct.pack('<I4s', len(meta), b'JSON') + meta
            + struct.pack('<I4s', len(binary), b'BIN\0') + binary)


class Merger:
    """Copy only referenced resources and deduplicate identical data across scenes."""
    def __init__(self):
        self.doc = {k: [] for k in ['nodes', 'meshes', 'materials', 'accessors', 'bufferViews', 'images', 'textures', 'samplers']}
        self.binary = bytearray()
        self.cache = {k: {} for k in self.doc}
        self.memo = {}

    def item(self, category, value):
        key = json.dumps(value, sort_keys=True, separators=(',', ':'))
        if key not in self.cache[category]:
            self.cache[category][key] = len(self.doc[category])
            self.doc[category].append(value)
        return self.cache[category][key]

    def resource(self, source, category, index):
        token = (id(source), category, index)
        if token in self.memo:
            return self.memo[token]
        doc, binary = source
        value = copy.deepcopy(doc[category][index])
        if category == 'bufferViews':
            start = value.get('byteOffset', 0)
            data = binary[start:start+value['byteLength']]
            # glTF requires an explicit stride when multiple vertex accessors
            # share a view, including identical position/normal byte sequences.
            if value.get('target') == 34962:
                users = [a for a in doc['accessors'] if a.get('bufferView') == index]
                assert users and all(a['componentType'] == 5126 for a in users)
                strides = {4 * {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4}[a['type']] for a in users}
                assert len(strides) == 1
                value['byteStride'] = value.get('byteStride', strides.pop())
            key = (data, value.get('target'), value.get('byteStride'))
            cache = self.cache['bufferViews']
            if key not in cache:
                self.binary.extend(b'\0' * (-len(self.binary) % 4))
                value['buffer'], value['byteOffset'] = 0, len(self.binary)
                self.binary.extend(data)
                cache[key] = len(self.doc['bufferViews'])
                self.doc['bufferViews'].append(value)
            result = cache[key]
        else:
            if category in ('accessors', 'images'):
                value['bufferView'] = self.resource(source, 'bufferViews', value['bufferView'])
            elif category == 'textures':
                value['source'] = self.resource(source, 'images', value['source'])
                if 'sampler' in value:
                    value['sampler'] = self.resource(source, 'samplers', value['sampler'])
            elif category == 'materials':
                pbr = value.get('pbrMetallicRoughness', {})
                for owner, key in [(pbr, 'baseColorTexture'), (pbr, 'metallicRoughnessTexture'), (value, 'normalTexture'), (value, 'occlusionTexture'), (value, 'emissiveTexture')]:
                    if key in owner:
                        owner[key]['index'] = self.resource(source, 'textures', owner[key]['index'])
            elif category == 'meshes':
                for primitive in value['primitives']:
                    primitive['attributes'] = {k: self.resource(source, 'accessors', v) for k, v in primitive['attributes'].items()}
                    if 'indices' in primitive:
                        primitive['indices'] = self.resource(source, 'accessors', primitive['indices'])
                    primitive['material'] = self.resource(source, 'materials', primitive['material'])
            result = self.item(category, value)
        self.memo[token] = result
        return result

    def node(self, source, original, shared=False):
        node = copy.deepcopy(original)
        assert 'children' not in node and 'matrix' not in node, 'Input meshes must use baked coordinates'
        node['mesh'] = self.resource(source, 'meshes', node['mesh'])
        name = node['name']
        if name.startswith(('Shaker door ', 'Weiser Breton ', 'Door hinge door leaf')):
            node['extras']['group'] = 'entrance_door'
        if shared:
            node['extras']['sharedRightSide'] = 'v4'
        return self.item('nodes', node)


def node_bounds(doc, node):
    a = doc['accessors'][doc['meshes'][node['mesh']]['primitives'][0]['attributes']['POSITION']]
    return a['min'], a['max']


def right_side(doc, node):
    # The entrance's hinge and trim belong to its configuration, even where
    # they extend beyond the right jamb. Everything fully beyond that jamb
    # otherwise comes from v4: shower, right wall, toilet/storage and fittings.
    if node['name'].startswith(('Shaker door ', 'Weiser Breton ', 'Door hinge ', 'Entrance ', 'Casing ')):
        return False
    return node_bounds(doc, node)[0][0] / I >= 48.3


def envelope(doc, ids, prefix):
    values = [node_bounds(doc, doc['nodes'][i]) for i in ids if doc['nodes'][i]['name'].startswith(prefix)]
    assert values, prefix
    return ([min(b[0][j] for b in values) for j in range(3)],
            [max(b[1][j] for b in values) for j in range(3)])


def configuration(doc, ids, index, source_doc):
    mirror_name = 'ALEX' if index < 2 else 'BIBO'
    lo, hi = envelope(doc, ids, mirror_name+' reflective surface')
    centre = [(lo[j]+hi[j])/2 for j in range(3)]
    c = -centre[2]/I
    labels = []
    for text, prefix in [
        ('Alder · 48″ floor vanity' if index < 2 else 'Madison · 36″ floating vanity' if index == 2 else 'Alder · 36″ floor vanity', ('VF4818', 'VW3620', 'VF3618')),
        ('16″ floating linen' if index == 2 else '16″ floor linen', ('LF1614', 'LW1614')),
        (mirror_name+' · '+('36 × 28″' if index < 2 else '24 × 28″'), mirror_name+' reflective surface'),
        ('Sterilite hamper', 'Sterilite upper rim'), ('Vanity outlet · location TBC', ('Vanity-side tool outlet plate', 'Rear-wall tool outlet plate')),
        ('Ducted vent · size TBC', 'Rectangular ventilation grille frame')]:
        a,b = envelope(doc,ids,prefix)
        labels.append([text,[(a[0]+b[0])/2/I,b[1]/I+2,-(a[2]+b[2])/2/I]])
    labels += [['GANSJÖN bin',[82,12,55.5]],['Robe hook · above bin',[87,67,55.5]],['Alaska · 48 × 36″',[71,8,25]],['Chormtok shower stool',[71,20,8.8]],['Niche · vertical 12 × 24″',[89,66,24]],['Toledo · provisional',[67,31,71]],['Storage · provisional',[86,38,71]]]
    if index:
        labels.append(['Light dimmer / vent switch',[7.625,51,1]])
    summaries = [
        '48-inch Alder at the rear · floor linen near entrance · ALEX mirror · door opens inward-left.',
        '48-inch Alder beside rear-left floor linen · front-left hamper · ALEX mirror · door opens toward shower.',
        '36-inch Madison floating furniture and polymarble top · equal 5.10-inch vanity gaps · BIBO mirror aligned with linen.',
        '36-inch Alder and Saxe porcelain · floor linen · equal 4.80-inch vanity gaps · BIBO mirror aligned with linen.',
    ]
    findings = [
        'V1 uses v4’s complete right side. Entrance and linen-door opening paths overlap; close the entrance before fully opening linen doors. Actual site and hinge clearances remain to verify.',
        'V2 retains its rear-hinged linen-door conflict with the rear wall and assumed window/towel fittings. Cabinet spacing needs review.',
        'V3 has a 5-inch linen rear gap. Its lower BIBO placement leaves only 0.18 inch static depth clearance to the faucet lever; actual lever motion needs checking.',
        'V4 has a 5-inch linen rear gap, 4.80-inch gaps around the vanity, and 4.10-inch vertical clearance above the static faucet lever. Actual hinges, plumbing and site fit remain to verify.',
    ]
    notes = [n for n in source_doc['extras']['assumptions'] if not n.startswith(('Canac 88001678 door', 'Square shower fixture'))]
    notes.insert(0,'Combined comparison: this configuration keeps its left-side arrangement and uses v4’s complete right-side fixtures, finishes and positions. All four configurations are maintained in this single viewer.')
    notes.append('Entrance is closed initially, with animated Open/Close and angle slider in all four configurations. V1 opens inward-left about assumed X=17.7 / Z=0.9 inches; V2–V4 inward-right about X=47.8 / Z=0.9 inches. Door remains visible in wall cutaways. Actual hinges and installation clearances are unverified. Downloads retain closed geometry.')
    return {'id':f'v{index+1}','name':f'V{index+1}', 'summary':summaries[index], 'finding':findings[index],
            'notes':notes,'centre':c,'labels':labels,'mirror':{'name':mirror_name+' reflective surface','width':hi[2]-lo[2],'height':hi[1]-lo[1],'position':[hi[0]+.01*I,centre[1],centre[2]]},
            'doorPivot':[17.7 if index==0 else 47.8,0,.9], 'doorSign':1 if index==0 else -1}


def build_configuration(version):
    namespace = runpy.run_path(str(HERE / 'geometry.py'), init_globals={'VERSION': version})
    raw = namespace['build_glb']()
    size = struct.unpack_from('<I', raw, 12)[0]
    return json.loads(raw[20:20+size]), raw[28+size:]


def main():
    sources = [build_configuration(version) for version in range(1, 5)]
    merger = Merger()
    common = [merger.node(sources[3],n,True) for n in sources[3][0]['nodes'] if right_side(sources[3][0],n)]
    scenes, configs = [], []
    for i,source in enumerate(sources):
        ids = [merger.node(source,n) for n in source[0]['nodes'] if not right_side(source[0],n)] + common
        scenes.append({'name':f'V{i+1} · '+['48-inch Alder rear layout','48-inch Alder rear linen','36-inch floating Madison','36-inch floor Alder / Saxe'][i], 'nodes':ids})
        configs.append(configuration(merger.doc,ids,i,source[0]))
    doc=merger.doc
    doc.update({'asset':{'version':'2.0','generator':'Bathroom configurations · SRC-2026-104','copyright':'Homeowner concept; viewer libraries Three.js MIT'},'scene':3,'scenes':scenes,
                'extras':{'source':'SRC-2026-104','units':'metres','authoringUnit':'inch','rightSideSource':'v4','configurations':configs,'defaultConfiguration':'v4','downloadDoorPose':'closed'}})
    raw=encode_glb(doc,merger.binary)
    template=(HERE/'viewer.html').read_text().replace('__VIEWER__',(HERE/'viewer.js').read_text())
    libraries=json.loads((HERE/'vendor/imports.json').read_text())
    imports={name:'data:text/javascript;base64,'+base64.b64encode((HERE/'vendor'/filename).read_bytes()).decode() for name,filename in libraries.items()}
    page=template.replace('__IMPORTMAP__',json.dumps({'imports':imports})).replace('__MODEL__',base64.b64encode(raw).decode())
    assert '__PLACEMENT__' not in page
    OUT.mkdir(exist_ok=True)
    (OUT/'bathroom-configurations.glb').write_bytes(raw)
    (OUT/'index.html').write_text(page)
    manifest={'source':'SRC-2026-104','sharedRightNodeCount':len(common),'defaultScene':3,'scenes':[{'id':c['id'],'nodes':len(s['nodes']),'doorPivotInches':c['doorPivot'],'doorSign':c['doorSign'],'mirror':c['mirror']} for c,s in zip(configs,scenes)],'inputs':{str(path.relative_to(HERE)):hashlib.sha256(path.read_bytes()).hexdigest() for path in [HERE/'generate.py', HERE/'geometry.py', HERE/'viewer.html', HERE/'viewer.js', *sorted((HERE/'vendor').glob('*'))]},'artifacts':{name:{'bytes':(OUT/name).stat().st_size,'sha256':hashlib.sha256((OUT/name).read_bytes()).hexdigest()} for name in ['index.html','bathroom-configurations.glb']}}
    (HERE/'references/build-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'sharedRightNodes':len(common),'meshes':len(doc['meshes']),'nodes':len(doc['nodes']),'artifacts':manifest['artifacts']},indent=2))


if __name__=='__main__':
    main()
