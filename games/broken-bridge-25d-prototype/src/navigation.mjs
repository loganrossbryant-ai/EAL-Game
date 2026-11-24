// Foot-space regions traced against the clearing plate. Points are 1060×540 world units.
const nearTrail = [
  [55,418],[106,409],[167,407],[238,404],[347,404],[445,403],
  [560,406],[689,408],[830,414],[928,413],[1005,417],
  [1005,480],[945,484],[859,481],[780,488],[670,488],[566,486],
  [466,487],[355,487],[255,485],[154,489],[55,482],
];
const lookoutTrail = [
  [265,278],[331,270],[405,270],[461,267],[510,274],[581,275],
  [649,281],[716,282],[776,285],[828,282],[873,288],[933,292],[977,301],
  [969,315],[896,313],[850,312],[799,307],[737,306],[677,302],
  [617,301],[550,296],[482,293],[439,296],[366,288],[307,289],[265,287],
];

export const crossingPaths = {
  bridge: [[450,417],[450,288]],
  ford: [[969,420],[953,401],[933,378],[910,358],[886,339],[853,318],[829,299]],
};
const safeStart=[278,449];
const distance=(a,b)=>Math.hypot(a[0]-b[0],a[1]-b[1]);

function projectSegment(point,a,b) {
  const dx=b[0]-a[0], dy=b[1]-a[1];
  const t=Math.max(0,Math.min(1,((point[0]-a[0])*dx+(point[1]-a[1])*dy)/(dx*dx+dy*dy)));
  return [a[0]+t*dx,a[1]+t*dy];
}
function inRegion(point,polygon) {
  let inside=false;
  const [x,y]=point;
  for(let i=0,j=polygon.length-1;i<polygon.length;j=i++) {
    const a=polygon[j],b=polygon[i];
    if(distance(point,projectSegment(point,a,b))<.001)return true;
    if((a[1]>y)!==(b[1]>y)&&x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]) inside=!inside;
  }
  return inside;
}
function opened(state) {
  return ['bridge','ford'].includes(state.route) &&
    (state.delivered || state.route==='ford'&&state.pieces.includes('postA'));
}
export function onLookout(state,x,y) {
  return opened(state)&&inRegion([x,y],lookoutTrail);
}
export function canWalk(state,x,y) {
  const point=[x,y];
  if(inRegion(point,nearTrail))return true;
  if(!opened(state))return false;
  if(inRegion(point,lookoutTrail))return true;
  const path=crossingPaths[state.route];
  const radius=state.route==='bridge'?15:11;
  return path.slice(1).some((end,i)=>distance(point,projectSegment(point,path[i],end))<=radius);
}
function closestEdge(point,polygon) {
  return polygon.reduce((best,end,i)=>{
    const next=projectSegment(point,polygon[(i+polygon.length-1)%polygon.length],end);
    return !best||distance(point,next)<distance(point,best)?next:best;
  },null);
}
export function recoverFoot(state,x,y) {
  if(!Number.isFinite(x)||!Number.isFinite(y))return safeStart;
  if(canWalk(state,x,y))return [x,y];
  const point=[x,y];
  const near=closestEdge(point,nearTrail);
  if(!opened(state))return near;
  const far=closestEdge(point,lookoutTrail);
  return distance(point,far)<distance(point,near)?far:near;
}
export function targetFoot(state,x,y) {
  if(!Number.isFinite(x)||!Number.isFinite(y))return null;
  if(canWalk(state,x,y))return [x,y];
  if(y<386)return null;
  const point=closestEdge([x,y],nearTrail);
  return distance(point,[x,y])<=43?point:null;
}
export function canTravel(state,a,b) {
  const count=Math.ceil(distance(a,b)/3);
  for(let i=1;i<=count;i++) {
    const progress=i/count;
    if(!canWalk(state,a[0]+(b[0]-a[0])*progress,a[1]+(b[1]-a[1])*progress))return false;
  }
  return true;
}
export function pathTo(state,start,end) {
  if(!end)return null;
  if(canTravel(state,start,end))return [end];
  const nodes=[start,end,...nearTrail];
  if(opened(state))nodes.push(...lookoutTrail,...crossingPaths[state.route]);
  const scores=nodes.map((_,i)=>i?Infinity:0),parent=[],closed=new Set();
  while(closed.size<nodes.length) {
    let best=-1;
    for(let i=0;i<nodes.length;i++)if(!closed.has(i)&&Number.isFinite(scores[i])&&(best<0||scores[i]<scores[best]))best=i;
    if(best<0)return null;
    if(best===1) {
      const route=[];
      for(let i=1;i!==0;i=parent[i])route.unshift(nodes[i]);
      return route;
    }
    closed.add(best);
    for(let i=1;i<nodes.length;i++) {
      if(closed.has(i))continue;
      const cost=scores[best]+distance(nodes[best],nodes[i]);
      if(cost<scores[i]&&canTravel(state,nodes[best],nodes[i])) {
        scores[i]=cost;parent[i]=best;
      }
    }
  }
  return null;
}
