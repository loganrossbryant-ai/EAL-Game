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

export function createFieldwork({stage,state,paused,walk,notify,onPlaced,onDelivered,texture}) {
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

  const belt=document.createElement('section');
  belt.className='field-belt';
  belt.setAttribute('aria-label','Work equipment and directions');
  belt.innerHTML=`
    <span class="field-belt-copy"><strong id="field-holding"></strong><small id="field-instruction"></small></span>
    <button type="button" id="field-guide" class="field-control"></button>
    <button type="button" id="field-rotate" class="field-control" hidden>Turn marker clockwise</button>
    <button type="button" id="field-drop" class="field-control" hidden>Return material</button>`;
  layer.append(belt);
  stage.append(layer);

  let carriedIndex=null, markedRoute=null, actorState=null, bearing=0;
  let markers=[];
  const holding=belt.querySelector('#field-holding');
  const instruction=belt.querySelector('#field-instruction');
  const guide=belt.querySelector('#field-guide');
  const rotate=belt.querySelector('#field-rotate');
  const drop=belt.querySelector('#field-drop');
  const items=()=>FIELD_ITEMS[state()?.route]??[];
  const isActive=()=>Boolean(state()?.route && !state().delivered);
  const carried=()=>carriedIndex===null?null:items()[carriedIndex]??null;
  const carriedPose=()=>carried()?{item:carried(),bearing}:null;
  const isPlaced=item=>state().pieces.includes(item.id);
  const setText=(node, text)=>{ if(node.textContent!==text) node.textContent=text; };

  function resetIfNeeded() {
    if(state()===actorState && state()?.route===markedRoute)return;
    actorState=state(); markedRoute=state()?.route;
    carriedIndex=null; bearing=0;
    for(const {pick,target} of markers){pick.remove();target.remove();}
    markers=items().map((item,index)=>{
      const pick=createMarker(layer,'pick',item,index,texture,activate);
      const target=createMarker(layer,'place',item,index,texture,activate);
      target.addEventListener('dragover',event=>{if(carried())event.preventDefault();});
      target.addEventListener('drop',event=>{
        event.preventDefault();
        if(event.dataTransfer.getData('text/plain')===carried()?.id) activate(actionId('place',index));
      });
      return {pick,target};
    });
  }

  function describe(id) {
    const match=/^field-(pick|place)([0-2])$/.exec(id??'');
    const item=match&&items()[Number(match[2])];
    if(!item)return '';
    if(match[1]==='pick') return 'Pick up '+item.name.toLowerCase();
    return item.id==='rope'?'Secure rope at '+item.target.toLowerCase():'Place at '+item.target.toLowerCase();
  }

  function available(type,index,item) {
    if(isPlaced(item))return false;
    return type==='pick'?carriedIndex!==index:carriedIndex!==null;
  }
  const mismatch=(item)=>`The ${carried().name.toLowerCase()} does not fit the ${item.target.toLowerCase()}. Try the matching position.`;

  function activate(id) {
    if(!isActive()||paused())return;
    const match=/^field-(pick|place)([0-2])$/.exec(id);
    if(!match)return;
    const [, type, index]=match, item=items()[Number(index)];
    if(!item||!available(type,Number(index),item))return;
    if(type==='place'&&item.id==='postB'&&!state().pieces.includes('postA')) {
      notify(carriedIndex!==Number(index)?mismatch(item):'Plant the near marker first. It marks the safe entrance to the stones.');
      return;
    }
    const point=type==='pick'?item.pickup:item.stand;
    if(distanceTo(state(),point)>17)walk(...point,id);
    else interact(id);
  }

  function interact(id) {
    if(!id?.startsWith('field-'))return false;
    if(!isActive()||paused())return true;
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
      notify(previous
        ?`Returned ${previous.name.toLowerCase()}. Carrying ${item.name.toLowerCase()}.`
        :`Carrying ${item.name.toLowerCase()}.`);
      return true;
    }
    if(carriedIndex!==index) {
      notify(mismatch(item));
      return true;
    }
    if(item.id==='postB'&&!state().pieces.includes('postA')) {
      notify('Plant the near marker first to mark the safe entrance.');
      return true;
    }
    if(item.bearing!==undefined&&bearing!==item.bearing) {
      notify(item.bearing===3
        ?'Turn the near marker northwest, toward the far white stone.'
        :'Turn the far marker southeast, back toward the near white stone.');
      return true;
    }
    if(!operate(state(),item.id)) {
      notify(state().route==='bridge'?'Fit both boards before securing the rope.':'Plant both markers before delivering the pack.');
      return true;
    }
    carriedIndex=null;
    bearing=0;
    onPlaced(item);
    if(state().delivered)onDelivered();
    else notify(state().route==='bridge'?'Board seated.':'Marker planted.');
    return true;
  }

  function next() {
    if(carriedIndex!==null)return ['place',carriedIndex];
    const index=items().findIndex(item=>!isPlaced(item));
    return index<0?null:['pick',index];
  }

  function near() {
    if(!isActive()||paused())return null;
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
    const command=next();
    if(command)activate(actionId(...command));
  });
  function turn() {
    if(!isActive()||paused()||carried()?.bearing===undefined)return false;
    bearing=(bearing+1)%4;
    notify('Marker points '+BEARINGS[bearing]+'.');
    return true;
  }
  rotate.addEventListener('click',turn);
  carrySprite.addEventListener('dragstart',event=>{
    const item=carried();
    if(!item||paused()){event.preventDefault();return;}
    event.dataTransfer.setData('text/plain',item.id);
    event.dataTransfer.effectAllowed='move';
  });
  drop.addEventListener('click',()=>{
    const item=carried();
    if(!item)return;
    carriedIndex=null; bearing=0;
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
    layer.hidden=!isActive()||paused();
    if(layer.hidden)return;

    const item=carried();
    setText(holding,item?'Carrying '+item.name.toLowerCase():'Crossing materials');
    setText(instruction,item
      ?item.bearing===undefined?'Walk to '+item.target.toLowerCase()+'.':'Turn the flag, then plant it at '+item.target.toLowerCase()+'.'
      :state().route==='bridge'?'Collect and carry one piece at a time.':'Collect the flags and mark the crossing.');
    const command=next();
    const suggested=command&&items()[command[1]];
    if(suggested){
      const close=distanceTo(state(),command[0]==='pick'?suggested.pickup:suggested.stand)<=17;
      setText(guide,command[0]==='pick'
        ?(close?'Pick up ':'Walk to ')+suggested.name.toLowerCase()
        :close?(suggested.id==='rope'?'Secure rope':'Place '+suggested.name.toLowerCase())
          :'Walk to '+suggested.target.toLowerCase());
    }
    rotate.hidden=item?.bearing===undefined;
    drop.hidden=!item;

    markers.forEach(({pick,target},index)=>{
      const fieldItem=items()[index];
      if(available('pick',index,fieldItem)) project(pick,world,fieldItem.at); else pick.hidden=true;
      if(available('place',index,fieldItem)) project(target,world,fieldItem.anchor); else target.hidden=true;
      target.dataset.compatible=String(carriedIndex===index);
    });
    if(item){
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
    } else carrySprite.hidden=true;
  }
  function inspect() {
    if(!isActive()||paused())return false;
    notify(carried()?'Choose a crossing position for the piece you are carrying.':'Start by collecting a material.');
    return true;
  }

  return {render,interact,near,describe,carriedPose,inspect,isActive,turn};
}
