import {sites} from './content.mjs';
import {figure, illustratedWorld, loadArt, paintWorld} from './art.mjs';

export const RANGER_DELIVERY_MS=5100;

export function mountWorld(Phaser, host, app) {
  const clamp = Phaser.Math.Clamp;
  const nearBank = [[0,395],[125,396],[246,395],[440,395],[650,397],[850,402],[947,403],[1060,408]];
  const farBank = [[0,288],[200,289],[335,292],[451,300],[650,308],[850,315],[1060,327]];
  const bankAt = (bank,x) => {
    const i = bank.findIndex(([edge]) => edge >= x);
    const [a,b] = [bank[i-1],bank[i]];
    return a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0]);
  };
  const walkLimit = x => bankAt(nearBank,x)+8;
  const farLimit = x => bankAt(farBank,x)-5;
  const routes = { bridge: [[450,417],[450,288]], ford: [[969,420],[829,299]] };
  const crossingOpen=state=>state.delivered || (state.route==='ford'&&state.pieces.includes('postA'));
  const canWalk = (state,x,y) => {
    if(y>=walkLimit(x) && y<=489) return true;
    if(!crossingOpen(state)) return false;
    if(y>=202 && y<=farLimit(x)) return true;
    const [[nx,ny],[fx,fy]]=routes[state.route];
    const center=nx+(fx-nx)*(ny-y)/(ny-fy);
    return y>=fy && y<=ny && Math.abs(x-center)<(state.route==='bridge'?21:13);
  };
  class Forest extends Phaser.Scene {
    preload() { loadArt(this); }
    create() {
      this.art = illustratedWorld(this);
      this.goal = null;
      this.face = 1;
      this.deliveryElapsed = app.state().delivered ? RANGER_DELIVERY_MS : 0;
      this.deliverySession = app.state().id;
      this.keys = new Set();
      this.input.on('pointerdown', pointer => {
        if (!app.paused()) this.walk(pointer.worldX, pointer.worldY);
      });
      this.input.keyboard.on('keydown', event => {
        if (app.paused() || event.target.closest?.('button,input,textarea,select')) return;
        if (['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','KeyA','KeyD','KeyW','KeyS'].includes(event.code)) {
          event.preventDefault(); this.keys.add(event.code);
        }
        if (event.code === 'KeyE' && !app.fieldworkKey()) app.interact(app.near());
        if (event.code === 'KeyR') app.fieldworkTurn();
      });
      this.input.keyboard.on('keyup', event => this.keys.delete(event.code));
      window.addEventListener('blur', () => this.keys.clear());
      app.ready(this);
    }
    walk(x,y,id) {
      const state=app.state();
      x=clamp(x,55,1005);y=clamp(y,202,489);
      const far=crossingOpen(state) && y<=farLimit(x);
      if(!far && !canWalk(state,x,y)) y=clamp(y,walkLimit(x),489);
      const positions=[];
      if(crossingOpen(state)) {
        const onNear=state.y>=walkLimit(state.x), wantsNear=y>=walkLimit(x);
        const onFar=state.y<=farLimit(state.x);
        const [nearEdge,farEdge]=routes[state.route];
        if(onNear && far) positions.push(nearEdge,farEdge);
        else if(onFar && wantsNear) positions.push(farEdge,nearEdge);
        else if(!onNear && !onFar && far) positions.push(farEdge);
        else if(!onNear && !onFar && wantsNear) positions.push(nearEdge);
      }
      this.goal={id,positions:[...positions,[x,y]]};
    }
    onFarBank() {
      const state=app.state();
      return crossingOpen(state) && state.y<=farLimit(state.x);
    }
    useCrossing() {
      const state=app.state();
      if(!state.delivered)return;
      const [nearEdge,farEdge]=routes[state.route];
      const point=this.onFarBank()?nearEdge:farEdge;
      this.walk(...point);
      this.goal.crossing=true;
    }
    project(x,y) {
      const camera=this.cameras.main;
      return [(x-camera.midPoint.x)*camera.zoom+camera.width/2,(y-camera.midPoint.y)*camera.zoom+camera.height/2];
    }
    update(_,delta) {
      const state=app.state();
      const dt=Math.min(delta,40)/1000;
      const camera=this.cameras.main;
      const portrait=camera.width<camera.height;
      const talking=app.conversation();
      const baseZoom=Math.min(Math.max(camera.height/540,camera.width/1060),camera.height/370);
      const closeBridge=state.route==='bridge'&&!state.delivered&&Math.abs(state.x-450)<57;
      const desiredZoom=baseZoom*(talking?(portrait?1.22:1.36):closeBridge&&!portrait?1.12:1);
      const blend=app.motion()?Math.min(1,dt*7):1;
      const zoom=this.cameraReady?Phaser.Math.Linear(camera.zoom,desiredZoom,blend):desiredZoom;
      camera.setZoom(zoom);
      const half=camera.width/(2*zoom);
      if(!canWalk(state,state.x,state.y)) state.y=walkLimit(state.x);
      let dx=0,dy=0;
      if (!app.paused()) {
        const key=(a,b)=>this.keys.has(a)||this.keys.has(b);
        dx=Number(key('ArrowRight','KeyD'))-Number(key('ArrowLeft','KeyA'));
        dy=Number(key('ArrowDown','KeyS'))-Number(key('ArrowUp','KeyW'));
        if(dx||dy) this.goal=null;
        if(this.goal) {
          const [tx,ty]=this.goal.positions[0];
          const x=tx-state.x,y=ty-state.y;
          const distance=Math.hypot(x,y);
          if(distance<5){
            const {id,positions}=this.goal;
            positions.shift();
            if(!positions.length) {
              this.goal=null; app.save();
              if(id) app.interact(id);
            }
          } else {
            dx=x/distance; dy=y/distance;
            const look=clamp(state.x+dx*7,55,1005);
            if(state.y>=walkLimit(state.x) && state.y<walkLimit(look) && ty>=walkLimit(tx) && Math.abs(x)>6) dy=Math.max(dy,.45);
            if(state.delivered && state.y<=farLimit(state.x) && state.y>farLimit(look) && ty<=farLimit(tx) && Math.abs(x)>6) dy=Math.min(dy,-.45);
          }
        }
        if(dx||dy) {
          const len=Math.max(1,Math.hypot(dx,dy));
          const speed=this.goal?194:152;
          const nextX=clamp(state.x+dx*dt*speed/len,55,1005);
          const nextY=clamp(state.y+dy*dt*speed/len,202,489);
          if(canWalk(state,nextX,nextY)) {state.x=nextX;state.y=nextY;}
          else if(canWalk(state,nextX,state.y)) state.x=nextX;
          else if(canWalk(state,state.x,nextY)) state.y=nextY;
          this.face=dx?Math.sign(dx):this.face;
          this.moving=true;
          if (!this.savedAt || performance.now()-this.savedAt>175) {
            this.savedAt=performance.now(); app.save();
          }
        } else if(this.moving) { this.moving=false; app.save(); }
      }
      const opening=portrait&&!state.question&&state.x<375;
      const centerX=talking?(portrait?sites.ranger.x:sites.ranger.x+115):
        opening?Math.max(355,state.x):state.x;
      const centerY=talking&&portrait?533:camera.height/zoom<540?540-camera.height/(2*zoom):270;
      const targetX=half>=530?530:clamp(centerX,half,1060-half);
      camera.centerOn(this.cameraReady?Phaser.Math.Linear(camera.midPoint.x,targetX,blend):targetX,
        this.cameraReady?Phaser.Math.Linear(camera.midPoint.y,centerY,blend):centerY);
      this.cameraReady=true;
      const motion=app.motion();
      const time=motion?performance.now()/1000:0;
      const worldState=state.id+':'+state.pieces.join(',');
      if(this.lastFrame!==worldState || this.lastPaint==null || (motion && time-this.lastPaint>.023) || this.lastMotion!==motion) {
        paintWorld(this.art,time,state);
        this.lastPaint=time; this.lastMotion=motion; this.lastFrame=worldState;
      }
      const ranger=sites.ranger;
      const greeting=talking&&!state.delivered&&Math.hypot(state.x-ranger.x,state.y-ranger.y)<48;
      const dxToScout=Math.sign(state.x-ranger.x)||1;
      const mark=greeting?dxToScout*6:0;
      const oldShift=this.rangerShift??0;
      this.rangerShift=Phaser.Math.Linear(oldShift,mark,blend);
      let rx=ranger.x+this.rangerShift,ry=ranger.y,rangerPose='';
      if(this.deliverySession!==state.id) {
        this.deliverySession=state.id;
        this.deliveryElapsed=state.delivered?RANGER_DELIVERY_MS:0;
      }
      if(state.delivered&&!state.complete&&motion) {
        if(!app.paused()) this.deliveryElapsed=Math.min(this.deliveryElapsed+dt*1000,RANGER_DELIVERY_MS);
        const elapsed=this.deliveryElapsed;
        const path=[[ranger.x,ranger.y],...routes[state.route]];
        // Pause at the abutment for the inspection before committing to the deck.
        const inspection=elapsed>=1320&&elapsed<1760;
        const handoff=elapsed>=3060&&elapsed<3630;
        const phase=elapsed<1320?elapsed/1320*.64:elapsed<1760?.64:
          elapsed<3060?.64+(elapsed-1760)/1300*.36:elapsed<3630?1:
          1-clamp((elapsed-3630)/(RANGER_DELIVERY_MS-3630),0,1);
        if(inspection) rangerPose='inspect';
        if(handoff) rangerPose='handoff';
        const section=phase<.64?0:1;
        const ratio=section===0?phase/.64:(phase-.64)/.36;
        rx=Phaser.Math.Linear(path[section][0],path[section+1][0],ratio);
        ry=Phaser.Math.Linear(path[section][1],path[section+1][1],ratio);
      }
      if(state.delivered){
        if(motion&&!state.complete&&this.deliveryElapsed<3370) {
          this.art.parcel.setPosition(rx+8,ry-21).setDepth(ry+.6).setDisplaySize(19,14);
        } else {
          const [x,y]=routes[state.route][1];
          this.art.parcel.setPosition(x+19,y+1).setDepth(y+1).setDisplaySize(23,16);
        }
      } else this.art.parcel.setPosition(204,431).setDepth(431).setDisplaySize(30,21);
      const carried=app.carry();
      const speaking=talking&&app.voicePlaying();
      figure(this.art.ranger,rx,ry,{face:Math.sign(state.x-rx)||1,
        pose:rangerPose|| (talking&&!speaking?'listen':''),gesture:speaking});
      figure(this.art.scout,state.x,state.y,{face:talking?Math.sign(rx-state.x)||this.face:this.face,
        pose:app.installing()?'fit':'',gesture:talking,carrying:Boolean(carried)});
      for(const actor of [this.art.scout,this.art.ranger]) {
        const data=this.game.canvas.dataset, prefix=actor.role;
        if(data[prefix+'Frame']!==actor.key) data[prefix+'Frame']=actor.key;
        if(data[prefix+'Action']!==actor.action) data[prefix+'Action']=actor.action;
        if(data[prefix+'Direction']!==actor.direction) data[prefix+'Direction']=actor.direction;
      }
      this.art.parcel.setVisible(state.delivered||carried?.item.id!=='pack');
      if(carried){
        const asset=carried.item.asset;
        const height=asset.startsWith('flag-')?35:asset==='rope'?14:18;
        const heading=this.art.scout.direction;
        const shift=this.art.scout.gait&&['up','down'].includes(heading)?0:13*this.face;
        this.art.carry.setTexture(asset).setDisplaySize(height*this.textures.get(asset).getSourceImage().width/
          this.textures.get(asset).getSourceImage().height,height)
          .setPosition(state.x+shift,state.y-29).setDepth(state.y+(heading==='up'?.18:.7))
          .setAngle(carried.angle??(carried.item.bearing===undefined?0:carried.bearing*90)).setVisible(true);
      } else this.art.carry.setVisible(false);
      app.placePins(this);
    }
  }
  return new Phaser.Game({
    type:Phaser.CANVAS, parent:host, backgroundColor:'#142b32', banner:false,
    scale:{mode:Phaser.Scale.RESIZE,width:host.clientWidth,height:host.clientHeight},
    scene:[Forest], audio:{noAudio:true}, render:{antialias:true},
  });
}
