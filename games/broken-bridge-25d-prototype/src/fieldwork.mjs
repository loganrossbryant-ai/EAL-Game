import {operate} from './state.mjs';

// Item position, destination and safe working stance are distinct. The scout
// works from the intact abutment while the gap remains closed to walking.
export const FIELD_ITEMS = {
  bridge: [
    { id:'boardA', name:'First board', asset:'board', at:[83,436], pickup:[83,451],
      target:'Lower deck socket', anchor:[443,373], stand:[438,413] },
    { id:'boardB', name:'Second board', asset:'board', at:[119,429], pickup:[119,451],
      target:'Upper deck socket', anchor:[455,335], stand:[450,413] },
    { id:'rope', name:'Rope', asset:'rope', at:[155,441], pickup:[155,452],
      target:'Anchor cleat', anchor:[481,397], stand:[474,422] },
  ],
  ford: [
    { id:'postA', name:'Near marker', asset:'flag-0', at:[903,438], pickup:[903,449],
      target:'Near white stone', anchor:[958,407], stand:[956,425], bearing:3 },
    { id:'postB', name:'Far marker', asset:'flag-1', at:[939,438], pickup:[939,451],
      target:'Far white stone', anchor:[851,301], stand:[829,299], bearing:1 },
    { id:'pack', name:'Supply pack', asset:'supplies', at:[204,430], pickup:[205,451],
      target:'Loading spot', anchor:[977,430], stand:[975,437] },
  ],
};
const BEARINGS = ['↗ Northeast','↘ Southeast','↙ Southwest','↖ Northwest'];
const BOARD_ANGLES = ['Across the deck', 'Skewed clockwise', 'Along the deck', 'Skewed counterclockwise'];
const ROPE_CLEAT = {name:'Tension cleat', anchor:[467,351], stand:[468,416]};
const actionId = (type, index) => `field-${type}${index}`;
const distanceTo = (current, [x,y]) => Math.hypot(current.x-x,current.y-y);

function createMarker(layer,type,item,index,texture,activate) {
  const marker=document.createElement('button');
  marker.type='button';
  marker.className='field-marker field-'+type;
  marker.dataset.action=type+index;
  marker.setAttribute('aria-label',type==='pick'?'Pick up '+item.name.toLowerCase():item.target);
  if(type==='pick') {
    const art=document.createElement('img');
    art.src=texture[item.asset]; art.alt=''; art.draggable=false;
    marker.append(art);
  } else {
    const focus=document.createElement('span');
    focus.className='field-socket-dot'; focus.setAttribute('aria-hidden','true');
    marker.append(focus);
  }
  marker.addEventListener('click',()=>activate(actionId(type,index)));
  layer.append(marker);
  return marker;
}

export function createFieldwork({stage,state,paused,walk,notify,onPlaced,onDelivered,texture,
  motion=()=>true,onActivity=()=>{},onGuideVoice,onRig}) {
  const layer=document.createElement('div');
  layer.className='field-layer';
  layer.setAttribute('aria-label','Work on the crossing');
  layer.hidden=true;
  const carrySprite=document.createElement('span');
  carrySprite.className='field-carried';
  carrySprite.id='field-carried';
  carrySprite.setAttribute('aria-hidden','true');
  carrySprite.draggable=true;
  carrySprite.hidden=true;
  layer.append(carrySprite);
  function preview(className) {
    const image=document.createElement('img');
    image.className='field-preview '+className;
    image.alt='';
    image.hidden=true;
    layer.append(image);
    return image;
  }
  const ghost=preview('field-ghost');
  const hooked=preview('field-hooked');
  const glide=preview('field-glide');
  const tension=document.createElement('button');
  tension.type='button';
  tension.dataset.action='tension';
  tension.className='field-marker field-tension';
  tension.setAttribute('aria-label','Tension the rope');
  tension.innerHTML='<span class="field-socket-dot" aria-hidden="true"></span>';
  tension.hidden=true;
  layer.append(tension);

  const belt=document.createElement('section');
  belt.className='field-belt';
  belt.setAttribute('aria-label','Work equipment and directions');
  belt.innerHTML=`
    <span class="field-belt-brief">
      <span class="field-belt-copy"><strong id="field-holding"></strong><small id="field-instruction"></small></span>
      <button type="button" id="field-listen" class="field-control" aria-label="Hear instructions" title="Hear instructions" ${onGuideVoice?'':'hidden'}>▶</button>
    </span>
    <button type="button" id="field-guide" class="field-control" title="Use guided assistance"></button>
    <button type="button" id="field-rotate" class="field-control" hidden>Turn marker clockwise</button>
    <button type="button" id="field-drop" class="field-control" hidden>Return material</button>`;
  layer.append(belt);
  stage.append(layer);

  let carriedIndex=null, markedRoute=null, actorState=null, bearing=0;
  let ropeHooked=false, hookAssisted=false, moving=null, queued=null, rejected=null, dragPoint=null, contactUntil=0;
  let markers=[];
  const holding=belt.querySelector('#field-holding');
  const instruction=belt.querySelector('#field-instruction');
  const guide=belt.querySelector('#field-guide');
  const rotate=belt.querySelector('#field-rotate');
  const drop=belt.querySelector('#field-drop');
  const items=()=>FIELD_ITEMS[state()?.route]??[];
  const isActive=()=>Boolean(state()?.route && !state().delivered);
  const carried=()=>carriedIndex===null?null:items()[carriedIndex]??null;
  const isBoard=item=>item?.asset==='board';
  const angleOf=item=>isBoard(item)?bearing*45:item?.bearing===undefined?0:bearing*90;
  const carriedPose=()=>carried()&&!moving&&!ropeHooked?{item:carried(),bearing,angle:angleOf(carried())}:null;
  const isPlaced=item=>state().pieces.includes(item.id);
  const setText=(node, text)=>{ if(node.textContent!==text) node.textContent=text; };

  function resetIfNeeded() {
    if(state()===actorState && state()?.route===markedRoute)return;
    actorState=state(); markedRoute=state()?.route;
    carriedIndex=null; bearing=0;
    ropeHooked=false;hookAssisted=false;moving=null;queued=null;rejected=null;dragPoint=null;contactUntil=0;
    for(const {pick,target} of markers){pick.remove();target.remove();}
    markers=items().map((item,index)=>{
      const pick=createMarker(layer,'pick',item,index,texture,activate);
      const target=createMarker(layer,'place',item,index,texture,activate);
      target.addEventListener('dragover',event=>{if(carried())event.preventDefault();});
      target.addEventListener('drop',event=>{
        event.preventDefault();
        event.stopPropagation();
        dragPoint=null;
        if(event.dataTransfer.getData('text/plain')===carried()?.id) activate(actionId('place',index),'drag');
      });
      return {pick,target};
    });
  }

  function describe(id) {
    if(id==='field-tension')return 'Tension the rope';
    const match=/^field-(pick|place)([0-2])$/.exec(id??'');
    const item=match&&items()[Number(match[2])];
    if(!item)return '';
    if(match[1]==='pick') return 'Pick up '+item.name.toLowerCase();
    return item.id==='rope'?'Secure rope at '+item.target.toLowerCase():'Place at '+item.target.toLowerCase();
  }

  function available(type,index,item) {
    if(isPlaced(item)||moving)return false;
    if(type==='pick')return !ropeHooked&&carriedIndex!==index;
    return !ropeHooked&&carriedIndex!==null;
  }
  const mismatch=(item)=>`The ${carried().name.toLowerCase()} does not fit the ${item.target.toLowerCase()}. Try the matching position.`;
  function report(action,item,method,assisted) {
    onActivity({action,piece:item.id,method,assisted,route:state().route});
  }
  function reject(item,message,method,assisted,targetIndex) {
    rejected={index:targetIndex,until:performance.now()+660};
    report('contact-rejected',item,method,assisted);
    notify(message);
  }

  function activate(id,method='tap') {
    if(!isActive()||paused()||moving)return;
    if(id==='field-tension'){
      if(!ropeHooked)return;
      const auto=distanceTo(state(),ROPE_CLEAT.stand)>17;
      const access={method,assisted:method==='guide'||auto};
      if(auto){queued={id,...access};walk(...ROPE_CLEAT.stand,id);}
      else interact(id,access);
      return;
    }
    const match=/^field-(pick|place)([0-2])$/.exec(id);
    if(!match)return;
    const [, type, index]=match, item=items()[Number(index)];
    if(!item||!available(type,Number(index),item))return;
    if(type==='place'&&item.id==='postB'&&!state().pieces.includes('postA')) {
      reject(carried(),carriedIndex!==Number(index)?mismatch(item):'Plant the near marker first. It marks the safe entrance to the stones.',
        method,method==='guide',Number(index));
      return;
    }
    const point=type==='pick'?item.pickup:item.stand;
    const auto=distanceTo(state(),point)>17;
    const access={method,assisted:method==='guide'||auto};
    if(auto){queued={id,...access};walk(...point,id);}
    else interact(id,access);
  }

  function interact(id,access) {
    if(!id?.startsWith('field-'))return false;
    if(!isActive()||paused()||moving)return true;
    const {method='keyboard',assisted=false}=access??(queued?.id===id?queued:{});
    queued=null;
    if(id==='field-tension') {
      if(!ropeHooked||distanceTo(state(),ROPE_CLEAT.stand)>19)return true;
      const rope=carried();
      const tensionRope=(rigAssisted=false)=>snap(rope,items()[2].anchor,ROPE_CLEAT.anchor,()=>{
        report('rope-tensioned',rope,method,assisted||hookAssisted||rigAssisted);
        complete(rope,method,assisted||hookAssisted||rigAssisted);
      });
      if(state().fieldEdition===6&&onRig)onRig(tensionRope);
      else tensionRope();
      return true;
    }
    const match=/^field-(pick|place)([0-2])$/.exec(id);
    if(!match)return true;
    const [, type, rawIndex]=match, index=Number(rawIndex), item=items()[index];
    if(!item||!available(type,index,item))return true;
    const point=type==='pick'?item.pickup:item.stand;
    if(distanceTo(state(),point)>19)return true;
    if(type==='pick') {
      const previous=carried();
      // A two-handed carry takes one piece. The previous item goes back to
      // its supply point, so a wrong pickup cannot strand the puzzle.
      carriedIndex=index; bearing=0;
      report('collected',item,method,assisted);
      notify(previous
        ?`Returned ${previous.name.toLowerCase()}. Carrying ${item.name.toLowerCase()}.`
        :`Carrying ${item.name.toLowerCase()}.`);
      return true;
    }
    if(carriedIndex!==index) {
      reject(carried(),mismatch(item),method,assisted,index);
      return true;
    }
    if(item.id==='postB'&&!state().pieces.includes('postA')) {
      reject(item,'Plant the near marker first to mark the safe entrance.',method,assisted,index);
      return true;
    }
    if(item.bearing!==undefined&&bearing!==item.bearing) {
      reject(item,item.bearing===3
        ?'Turn the near marker northwest, toward the far white stone.'
        :'Turn the far marker southeast, back toward the near white stone.',method,assisted,index);
      return true;
    }
    if(isBoard(item)&&bearing!==0) {
      reject(item,'Turn the board across the deck to line it up with both sockets.',method,assisted,index);
      return true;
    }
    if(index===2&&state().pieces.length!==2) {
      reject(item,state().route==='bridge'?'Fit both boards before securing the rope.':'Plant both markers before delivering the pack.',method,assisted,index);
      return true;
    }
    const from=[state().x, state().y-28];
    if(item.id==='rope') {
      snap(item,from,item.anchor,()=>{
        ropeHooked=true;hookAssisted=assisted;
        report('rope-hooked',item,method,assisted);
        notify('Rope hooked. Pull it to the second cleat to tension it.');
      });
      return true;
    }
    snap(item,from,item.anchor,()=>complete(item,method,assisted));
    return true;
  }

  function complete(item,method,assisted) {
    if(!operate(state(),item.id))return;
    carriedIndex=null;
    bearing=0;
    ropeHooked=false;
    hookAssisted=false;
    report('placed',item,method,assisted);
    onPlaced(item);
    if(state().delivered)onDelivered();
    else notify(state().route==='bridge'?'Board seated.':'Marker planted.');
  }

  function snap(item,from,to,finish) {
    const now=performance.now();
    if(!motion()){contactUntil=now+170;finish();return;}
    moving={item,from,to,angle:angleOf(item),finish,started:now};
  }

  function next() {
    if(carriedIndex!==null)return ['place',carriedIndex];
    const index=items().findIndex(item=>!isPlaced(item));
    return index<0?null:['pick',index];
  }

  function near() {
    if(!isActive()||paused())return null;
    if(ropeHooked)return distanceTo(state(),ROPE_CLEAT.stand)<18?'field-tension':null;
    const held=carried();
    if(held && distanceTo(state(),held.stand)<18)return actionId('place',carriedIndex);
    let best=null, distance=18;
    const preference=carriedIndex===null?'pick':'place';
    items().forEach((item,index)=>{
      if(!available(preference,index,item))return;
      const candidate=distanceTo(state(),preference==='pick'?item.pickup:item.stand);
      if(candidate<distance) {best=actionId(preference,index);distance=candidate;}
    });
    return best;
  }

  guide.addEventListener('click',()=>{
    if(ropeHooked){activate('field-tension','guide');return;}
    const command=next();
    if(command)activate(actionId(...command),'guide');
  });
  belt.querySelector('#field-listen').addEventListener('click',()=>{
    if(!isActive()||paused())return;
    const nextItem=items()[next()?.[1]];
    const id=state().route==='ford'?'guideFord':nextItem?.id==='rope'?'guideRope':'guideBoard';
    onGuideVoice?.(id);
  });
  tension.addEventListener('click',()=>activate('field-tension'));
  tension.addEventListener('dragover',event=>{if(ropeHooked)event.preventDefault();});
  tension.addEventListener('drop',event=>{
    event.preventDefault();event.stopPropagation();dragPoint=null;
    if(event.dataTransfer.getData('text/plain')==='rope')activate('field-tension','drag');
  });
  function turn() {
    const item=carried();
    if(!isActive()||paused()||moving||(!isBoard(item)&&item?.bearing===undefined))return false;
    bearing=(bearing+1)%4;
    notify(isBoard(item)?'Board alignment: '+BOARD_ANGLES[bearing]+'.':'Marker points '+BEARINGS[bearing]+'.');
    return true;
  }
  rotate.addEventListener('click',turn);
  carrySprite.addEventListener('dragstart',event=>{
    const item=carried();
    if(!item||paused()){event.preventDefault();return;}
    event.dataTransfer.setData('text/plain',item.id);
    event.dataTransfer.effectAllowed='move';
  });
  carrySprite.addEventListener('dragend',()=>{dragPoint=null;});
  stage.addEventListener('dragover',event=>{
    if(!carried()||paused()||moving)return;
    event.preventDefault();
    const rect=stage.getBoundingClientRect();
    const target=event.target.closest?.('.field-place');
    dragPoint=[event.clientX-rect.left,event.clientY-rect.top,target?Number(target.dataset.action.at(-1)):null];
  });
  stage.addEventListener('dragleave',event=>{
    if(!(event.relatedTarget instanceof Node)||!stage.contains(event.relatedTarget))dragPoint=null;
  });
  stage.addEventListener('drop',event=>{
    if(!dragPoint||event.dataTransfer.getData('text/plain')!==carried()?.id)return;
    event.preventDefault();dragPoint=null;
    notify(ropeHooked?'The rope stays hooked. Pull it to the lit second cleat.'
      :'The material stays in your hands. Aim for a lit socket.');
  });
  drop.addEventListener('click',()=>{
    const item=carried();
    if(!item||moving)return;
    carriedIndex=null; bearing=0;
    ropeHooked=false;hookAssisted=false;
    notify('Returned '+item.name.toLowerCase()+'.');
  });

  function project(node,world,point) {
    const [x,y]=world.project(...point);
    const margin=node===carrySprite?0:22;
    if(x<margin||x>stage.clientWidth-margin||y<margin||y>stage.clientHeight-margin){
      node.hidden=true;return;
    }
    node.style.left=x+'px';node.style.top=y+'px';
    node.hidden=false;
  }

  function render(world) {
    resetIfNeeded();
    const now=performance.now();
    if(moving&&now-moving.started>=250&&!paused()) {
      const {finish}=moving;
      moving=null;
      finish();
    }
    layer.hidden=!isActive()||paused();
    if(layer.hidden)return;

    const item=carried();
    setText(holding,ropeHooked?'Rope hooked':item?'Carrying '+item.name.toLowerCase():'Crossing materials');
    setText(instruction,ropeHooked?'Use the second cleat to tension the rope.':item
      ?isBoard(item)?BOARD_ANGLES[bearing]+'. Aim for the lit socket.'
        :item.bearing===undefined?'Walk to '+item.target.toLowerCase()+'.':'Turn the flag, then plant it at '+item.target.toLowerCase()+'.'
      :state().route==='bridge'?'Collect and carry one piece at a time.':'Collect the flags and mark the crossing.');
    const command=next();
    const suggested=command&&items()[command[1]];
    if(ropeHooked)setText(guide,'Tension the rope');
    else if(suggested){
      const close=distanceTo(state(),command[0]==='pick'?suggested.pickup:suggested.stand)<=17;
      setText(guide,command[0]==='pick'
        ?(close?'Pick up ':'Walk to ')+suggested.name.toLowerCase()
        :close?(suggested.id==='rope'?'Secure rope':'Place '+suggested.name.toLowerCase())
          :'Walk to '+suggested.target.toLowerCase());
    }
    guide.disabled=Boolean(moving);
    rotate.hidden=!isBoard(item)&&item?.bearing===undefined;
    setText(rotate,isBoard(item)?'Turn board clockwise':'Turn marker clockwise');
    drop.hidden=!item;drop.disabled=Boolean(moving);

    markers.forEach(({pick,target},index)=>{
      const fieldItem=items()[index];
      if(available('pick',index,fieldItem)) project(pick,world,fieldItem.at); else pick.hidden=true;
      if(available('place',index,fieldItem)) project(target,world,fieldItem.anchor); else target.hidden=true;
      target.dataset.compatible=String(carriedIndex===index);
      target.dataset.rejected=String(rejected?.index===index&&now<rejected.until);
    });
    if(item&&!moving&&!ropeHooked){
      carrySprite.dataset.asset=item.asset;
      const x=state().x+13*(world.face||1), y=state().y-29;
      const [screenX,screenY]=world.project(x,y);
      const overlaps=items().some((target,index)=>{
        if(!available('place',index,target))return false;
        const [tx,ty]=world.project(...target.anchor);
        return Math.abs(tx-screenX)<12 && Math.abs(ty-screenY)<12;
      });
      // Keep the center of each socket tap-through while the scout's hand
      // is directly over it. The small drag handle stays on the held sprite.
      project(carrySprite,world,[x,overlaps?y-14:y]);
    } else if(ropeHooked&&!moving)project(carrySprite,world,items()[2].anchor);
    else carrySprite.hidden=true;
    renderPreview(world,item,now);
  }

  function putImage(node,item,angle) {
    if(node.dataset.asset!==item.asset){node.dataset.asset=item.asset;node.src=texture[item.asset];}
    node.style.setProperty('--field-angle',angle+'deg');
  }

  function renderPreview(world,item,now) {
    ghost.hidden=true;hooked.hidden=true;glide.hidden=true;tension.hidden=true;
    if(ropeHooked) {
      putImage(hooked,item,0);
      project(hooked,world,items()[2].anchor);
      if(!moving)project(tension,world,ROPE_CLEAT.anchor);
    }
    if(moving) {
      const p=Math.min((now-moving.started)/250,1), ease=1-(1-p)**3;
      putImage(glide,moving.item,moving.angle*(1-ease));
      project(glide,world,moving.from.map((start,i)=>start+(moving.to[i]-start)*ease));
    } else if(item&&(!ropeHooked||dragPoint)) {
      putImage(ghost,item,angleOf(item));
      if(dragPoint){
        ghost.style.left=dragPoint[0]+'px';
        ghost.style.top=dragPoint[1]+'px';
        ghost.hidden=false;
      } else if(distanceTo(state(),item.stand)<31) {
        project(ghost,world,item.anchor);
      }
      const aligned=isBoard(item)?bearing===0:item.bearing===undefined||bearing===item.bearing;
      ghost.dataset.aligned=String(aligned&&(dragPoint?.[2]==null||dragPoint[2]===carriedIndex));
    }
  }
  function inspect() {
    if(!isActive()||paused())return false;
    notify(carried()?'Choose a crossing position for the piece you are carrying.':'Start by collecting a material.');
    return true;
  }

  return {render,interact,near,describe,carriedPose,inspect,isActive,turn,
    installing:()=>Boolean(moving)||performance.now()<contactUntil};
}
