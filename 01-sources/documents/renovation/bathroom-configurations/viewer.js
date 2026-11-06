import * as THREE from 'three';
import {OrbitControls} from 'orbit';
import {Reflector} from 'reflector';
const I=.0254, viewport=document.querySelector('#viewport'), canvas=document.querySelector('#canvas');
window.__modelReady=false;
try {
const raw=Uint8Array.from(atob(document.querySelector('#model-data').textContent.trim()),c=>c.charCodeAt(0));
const dv=new DataView(raw.buffer),jl=dv.getUint32(12,true),doc=JSON.parse(new TextDecoder().decode(raw.subarray(20,20+jl))),bin=raw.subarray(28+jl);
const urls=[];
function bufferView(id){const v=doc.bufferViews[id];return bin.slice(v.byteOffset||0,(v.byteOffset||0)+v.byteLength)}
function accessor(id){const a=doc.accessors[id],v=bufferView(a.bufferView);return new Float32Array(v.buffer,a.byteOffset||0,a.count*({VEC2:2,VEC3:3}[a.type]))}
const textures=await Promise.all(doc.textures.map(async t=>{const im=doc.images[t.source],url=URL.createObjectURL(new Blob([bufferView(im.bufferView)],{type:im.mimeType}));urls.push(url);const tex=await new THREE.TextureLoader().loadAsync(url);tex.colorSpace=THREE.SRGBColorSpace;tex.wrapS=tex.wrapT=THREE.RepeatWrapping;tex.flipY=false;tex.anisotropy=4;return tex}));
const mats=doc.materials.map(m=>{const p=m.pbrMetallicRoughness,c=p.baseColorFactor;return new THREE.MeshStandardMaterial({name:m.name,color:new THREE.Color(c[0],c[1],c[2]),opacity:c[3],transparent:c[3]<1,roughness:p.roughnessFactor,metalness:p.metallicFactor,side:THREE.DoubleSide,depthWrite:c[3]===1,map:p.baseColorTexture?textures[p.baseColorTexture.index]:null,emissive:m.emissiveFactor?new THREE.Color(...m.emissiveFactor):new THREE.Color(0)})});
const scene=new THREE.Scene();scene.background=new THREE.Color('#e9e9e2');
const configs=doc.extras.configurations;
const geometryCache=new Map();
function makeMesh(id){
 const node=doc.nodes[id],prim=doc.meshes[node.mesh].primitives[0];
 let geo=geometryCache.get(node.mesh);
 if(!geo){geo=new THREE.BufferGeometry();for(const [key,value] of Object.entries(prim.attributes)){const values=accessor(value);geo.setAttribute({POSITION:'position',NORMAL:'normal',TEXCOORD_0:'uv'}[key],new THREE.BufferAttribute(values,key==='TEXCOORD_0'?2:3))}geometryCache.set(node.mesh,geo)}
 const obj=new THREE.Mesh(geo,mats[prim.material]);obj.name=node.name;obj.userData={...node.extras,nodeId:id};obj.castShadow=obj.material.opacity===1;obj.receiveShadow=true;return obj;
}
const layouts=doc.scenes.map((definition,index)=>{
 const root=new THREE.Group(),groups={},pivot=new THREE.Group();root.name=configs[index].id;root.visible=false;scene.add(root);
 for(const id of definition.nodes){const obj=makeMesh(id);root.add(obj);(groups[obj.userData.group]??=[]).push(obj)}
 const p=configs[index].doorPivot;pivot.position.set(p[0]*I,p[1]*I,-p[2]*I);root.add(pivot);root.updateMatrixWorld(true);
 for(const obj of groups.entrance_door||[])pivot.attach(obj);
 return {root,groups,pivot,doorAngle:0};
});
let active=3,room=layouts[3].root,groups=layouts[3].groups,doorPivot=layouts[3].pivot;
let doorAngle=0, doorTarget=0, doorMotion=null;
const doorSlider=document.querySelector('#doorangle'), doorToggle=document.querySelector('#doortoggle');
const reducedMotion=matchMedia('(prefers-reduced-motion: reduce)');
function renderDoorAngle(angle){doorAngle=angle;doorPivot.rotation.y=configs[active].doorSign*angle*Math.PI/180;layouts[active].doorAngle=angle;doorSlider.value=String(Math.round(angle));document.querySelector('#doorvalue').value=Math.round(angle)+'°';}
function setDoorAngle(angle){doorMotion=null;doorTarget=Math.max(0,Math.min(90,angle));renderDoorAngle(doorTarget);doorToggle.textContent=doorTarget<45?'Open door':'Close door';}
function animateDoor(target){doorTarget=target;doorToggle.textContent=target===90?'Close door':'Open door';if(reducedMotion.matches){setDoorAngle(target);return;}doorMotion={from:doorAngle,to:target,start:performance.now(),duration:Math.max(180,900*Math.abs(target-doorAngle)/90)};}
function updateDoor(now){if(!doorMotion)return;const t=Math.min(1,(now-doorMotion.start)/doorMotion.duration),ease=t*t*(3-2*t);renderDoorAngle(doorMotion.from+(doorMotion.to-doorMotion.from)*ease);if(t===1)doorMotion=null;}
doorSlider.oninput=e=>setDoorAngle(Number(e.target.value));
doorToggle.onclick=()=>animateDoor(doorTarget>=45?0:90);
const renderer=new THREE.WebGLRenderer({canvas,antialias:true,preserveDrawingBuffer:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.0;
const camera=new THREE.PerspectiveCamera(43,1,.01,60);
let baseFov=43;function updateLens(){camera.fov=Math.min(110,THREE.MathUtils.radToDeg(2*Math.atan(Math.tan(THREE.MathUtils.degToRad(baseFov/2))/Math.min(1,camera.aspect))));camera.updateProjectionMatrix()}
const controls=new OrbitControls(camera,canvas);controls.enableDamping=true;controls.dampingFactor=.075;controls.minDistance=.28;controls.maxDistance=12;controls.maxPolarAngle=Math.PI*.49;controls.autoRotateSpeed=.6;controls.enablePan=true;
scene.add(new THREE.HemisphereLight(0xf4f6ff,0xa8a18e,1.7));
const sun=new THREE.DirectionalLight(0xfff4dc,2.5);sun.position.set(20*I,145*I,-62*I);sun.target.position.set(45*I,0,-40*I);sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);Object.assign(sun.shadow.camera,{left:-2,right:2,top:2,bottom:-2,near:.1,far:9});sun.shadow.bias=-.0003;sun.shadow.normalBias=.015;sun.shadow.radius=3;scene.add(sun,sun.target);
const fill=new THREE.DirectionalLight(0xe4eeff,1.25);fill.position.set(90*I,70*I,70*I);scene.add(fill);
const mirrorLight=new THREE.PointLight(0xfff1d9,5,2,2);scene.add(mirrorLight);
const platform=new THREE.Mesh(new THREE.PlaneGeometry(200,200),new THREE.MeshStandardMaterial({color:0xdadcd3,roughness:1}));platform.rotation.x=-Math.PI/2;platform.position.y=-4.05*I;platform.receiveShadow=true;scene.add(platform);
// One live reflector is resized and repositioned for the selected configuration.
const reflection=new Reflector(new THREE.PlaneGeometry(.6,.7),{color:0xc8d0d0,textureWidth:768,textureHeight:768,clipBias:0});reflection.rotation.y=Math.PI/2;reflection.name='Live mirror reflection';scene.add(reflection);
let exportedMirror=null,labels=[];
function setLabels(spec){
 document.querySelector('#labels').replaceChildren();
 labels=spec.map(([text,p])=>{const el=document.createElement('div');el.className='label';el.textContent=text;document.querySelector('#labels').append(el);return {el,p:new THREE.Vector3(...p.map((v,i)=>v*I*(i===2?-1:1)))}});
}
let wallMode='auto', glassVisible=true, ceilingVisible=false, labelVisible=false;
function setVisibility(){const p=camera.position;const hidden={wall_front:p.z>0,wall_back:p.z< -86.5*I,wall_left:p.x<0,wall_right:p.x>89*I};for(const [group,objects] of Object.entries(groups)){const show=group==='ceiling'?ceilingVisible:group==='glass'?glassVisible:group.startsWith('wall_')?(wallMode==='show'||(wallMode==='auto'&&!hidden[group])):true;for(const obj of objects)obj.visible=show}exportedMirror.visible=false;reflection.visible=p.x>configs[active].mirror.position[0];}
const presets={overview:{p:[87,155,-136],t:[44.5,22,39],f:43},doorway:{p:[32.75,63,-12],t:[43,40,66],f:69},top:{p:[44.5,225,43.15],t:[44.5,0,43.25],f:43},vanity:{p:[48,55,configs[active].centre],t:[3,43,configs[active].centre],f:80},shower:{p:[24,63,62],t:[73,43,12],f:67}};
function view(name){const v=presets[name];controls.autoRotate=false;document.querySelector('#rotate').checked=false;camera.position.set(...v.p.map((n,i)=>n*I*(i===2?-1:1)));controls.target.set(...v.t.map((n,i)=>n*I*(i===2?-1:1)));baseFov=v.f;updateLens();controls.update();for(const b of document.querySelectorAll('[data-view]'))b.setAttribute('aria-pressed',String(b.dataset.view===name));setVisibility()}
for(const b of document.querySelectorAll('[data-view]'))b.onclick=()=>view(b.dataset.view);
document.querySelector('#walls').onchange=e=>{wallMode=e.target.value;setVisibility()};document.querySelector('#glass').onchange=e=>{glassVisible=e.target.checked;setVisibility()};document.querySelector('#ceiling').onchange=e=>{ceilingVisible=e.target.checked;setVisibility()};document.querySelector('#labeltoggle').onchange=e=>labelVisible=e.target.checked;document.querySelector('#rotate').onchange=e=>controls.autoRotate=e.target.checked;
function zoom(f){const offset=camera.position.clone().sub(controls.target);offset.setLength(THREE.MathUtils.clamp(offset.length()*f,controls.minDistance,controls.maxDistance));camera.position.copy(controls.target).add(offset);controls.update()};document.querySelector('#zoomin').onclick=()=>zoom(.83);document.querySelector('#zoomout').onclick=()=>zoom(1.2);
canvas.addEventListener('keydown',e=>{if(['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','+','=','-','r','R'].includes(e.key)){e.preventDefault();if(e.key==='r'||e.key==='R')view('overview');else if('+=-'.includes(e.key))zoom(e.key==='-'?1.15:.87);else{const s=new THREE.Spherical().setFromVector3(camera.position.clone().sub(controls.target));s.theta+=e.key==='ArrowLeft'?.1:e.key==='ArrowRight'?-.1:0;s.phi=THREE.MathUtils.clamp(s.phi+(e.key==='ArrowUp'?-.1:e.key==='ArrowDown'?.1:0),.01,Math.PI*.49);camera.position.copy(controls.target).add(new THREE.Vector3().setFromSpherical(s));controls.update()}}});
// Export only the selected scene and its referenced resources, keeping closed geometry.
function selectedGLB(index){
 const out={asset:{...doc.asset},scene:0,scenes:[{name:doc.scenes[index].name,nodes:[]}],extras:{source:doc.extras.source,configuration:configs[index].id,rightSideSource:'v4',doorPose:'closed',assumptions:configs[index].notes}};
 for(const key of ['nodes','meshes','materials','accessors','bufferViews','images','textures','samplers'])out[key]=[];
 const maps={},chunks=[];let length=0;
 const clone=v=>JSON.parse(JSON.stringify(v));
 function copy(category,id){
  const map=maps[category]??=new Map();if(map.has(id))return map.get(id);
  const value=clone(doc[category][id]);
  if(category==='nodes')value.mesh=copy('meshes',value.mesh);
  else if(category==='meshes')for(const p of value.primitives){for(const key of Object.keys(p.attributes))p.attributes[key]=copy('accessors',p.attributes[key]);if(p.indices!==undefined)p.indices=copy('accessors',p.indices);p.material=copy('materials',p.material)}
  else if(category==='accessors'||category==='images')value.bufferView=copy('bufferViews',value.bufferView);
  else if(category==='textures'){value.source=copy('images',value.source);if(value.sampler!==undefined)value.sampler=copy('samplers',value.sampler)}
  else if(category==='materials'){
   const p=value.pbrMetallicRoughness||{};
   for(const [owner,key] of [[p,'baseColorTexture'],[p,'metallicRoughnessTexture'],[value,'normalTexture'],[value,'occlusionTexture'],[value,'emissiveTexture']])if(owner[key])owner[key].index=copy('textures',owner[key].index);
  }else if(category==='bufferViews'){
   const data=bufferView(id),pad=(4-length%4)%4;if(pad){chunks.push(new Uint8Array(pad));length+=pad}
   value.buffer=0;value.byteOffset=length;chunks.push(data);length+=data.byteLength;
  }
  const next=out[category].length;map.set(id,next);out[category].push(value);return next;
 }
 out.scenes[0].nodes=doc.scenes[index].nodes.map(id=>copy('nodes',id));out.buffers=[{byteLength:length}];
 const json=new TextEncoder().encode(JSON.stringify(out)),jl=(json.length+3)&~3,bl=(length+3)&~3;
 const bytes=new Uint8Array(28+jl+bl),view=new DataView(bytes.buffer);view.setUint32(0,0x46546c67,true);view.setUint32(4,2,true);view.setUint32(8,bytes.length,true);view.setUint32(12,jl,true);view.setUint32(16,0x4e4f534a,true);bytes.fill(32,20,20+jl);bytes.set(json,20);view.setUint32(20+jl,bl,true);view.setUint32(24+jl,0x004e4942,true);let offset=28+jl;for(const chunk of chunks){bytes.set(chunk,offset);offset+=chunk.length}return bytes;
}
const downloads=new Map(),download=document.querySelector('#download');
const allURL=URL.createObjectURL(new Blob([raw],{type:'model/gltf-binary'}));urls.push(allURL);document.querySelector('#download-all').href=allURL;document.querySelector('#download-all').download='bathroom-configurations.glb';
function selectConfiguration(id){
 const index=configs.findIndex(c=>c.id===id);if(index<0)throw new Error('Unknown configuration '+id);
 // Stop an in-flight door at its current pose; each layout remembers its own angle.
 doorMotion=null;layouts[active].root.visible=false;active=index;
 const state=layouts[active],config=configs[active];room=state.root;groups=state.groups;doorPivot=state.pivot;room.visible=true;setDoorAngle(state.doorAngle);
 exportedMirror=room.getObjectByName(config.mirror.name);exportedMirror.castShadow=false;
 reflection.geometry.dispose();reflection.geometry=new THREE.PlaneGeometry(config.mirror.width,config.mirror.height);reflection.position.set(...config.mirror.position);
 mirrorLight.position.set(10*I,config.mirror.position[1],config.mirror.position[2]);
 presets.vanity={p:[48,55,config.centre],t:[3,43,config.centre],f:80};setLabels(config.labels);
 document.querySelector('#configuration').value=id;document.querySelector('#configuration-title').textContent=config.name;
 document.querySelector('#configuration-summary').textContent=config.summary;document.querySelector('#layout-finding').textContent=config.finding;
 document.querySelector('#countertop-finish').textContent=active===2?'Gloss white cabinetry & polymarble':'Gloss white cabinetry & porcelain';
 document.querySelector('#configuration-notes').replaceChildren(...config.notes.map(text=>{const p=document.createElement('p');p.textContent=text;return p}));
 for(const button of document.querySelectorAll('[data-view]'))button.setAttribute('aria-pressed','false');
 if(!downloads.has(index)){const url=URL.createObjectURL(new Blob([selectedGLB(index)],{type:'model/gltf-binary'}));urls.push(url);downloads.set(index,url)}
 download.href=downloads.get(index);download.download='basement-bathroom-'+id+'.glb';setVisibility();
}
document.querySelector('#configuration').onchange=e=>selectConfiguration(e.target.value);
document.querySelector('#saveimage').onclick=()=>{const capturedConfiguration=configs[active].id;setVisibility();renderer.render(scene,camera);canvas.toBlob(blob=>{if(!blob)return;const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='basement-bathroom-'+capturedConfiguration+'.png';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),3000)},'image/png')};
function resize(){const w=viewport.clientWidth,h=viewport.clientHeight;renderer.setSize(w,h,false);camera.aspect=w/h;updateLens()}new ResizeObserver(resize).observe(viewport);resize();selectConfiguration('v4');view('overview');
let frames=0;function animate(){requestAnimationFrame(animate);updateDoor(performance.now());controls.update();setVisibility();renderer.render(scene,camera);for(const item of labels){const v=item.p.clone().project(camera);item.el.hidden=!labelVisible||v.z>1||v.z< -1||Math.abs(v.x)>1||Math.abs(v.y)>1;item.el.style.left=(v.x*.5+.5)*viewport.clientWidth+'px';item.el.style.top=(-v.y*.5+.5)*viewport.clientHeight+'px'}frames++;}
animate();document.querySelector('#loading').hidden=true;window.__modelReady=true;
// Read-only diagnostics used for verification; no browser services or network calls.
window.__bathroom={doc,scene,camera,controls,renderer,layouts,configs,reflection,selectConfiguration,selectedGLB,get groups(){return groups},view,get doorPivot(){return doorPivot},get activeConfiguration(){return configs[active].id},setDoorAngle,animateDoor,get doorAngle(){return doorAngle},get doorAnimating(){return doorMotion!==null},get frames(){return frames},get wallMode(){return wallMode}};
window.addEventListener('pagehide',()=>{for(const u of urls)URL.revokeObjectURL(u)});
canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();document.querySelector('#loading').hidden=false;document.querySelector('#error').textContent='The graphics context was interrupted. Reload this file to restore the model.'});
} catch(error){console.error(error);document.querySelector('#error').textContent='The 3D view could not start. Open this HTML in a current WebGL-enabled browser, or open bathroom-configurations.glb in a 3D viewer. Details: '+error.message;}
