import {sites} from './content.mjs';
import {canTravel,canWalk,crossingPaths,onLookout,pathTo,recoverFoot,targetFoot} from './navigation.mjs';
import {figure, illustratedWorld, loadArt, paintWorld} from './art.mjs';

const deliverySchedules={
  bridge:{walk:1410, inspect:460, cross:1370, deliver:620, back:1570},
  ford:{walk:4010, inspect:460, cross:2000, deliver:620, back:4710},
};

export function rangerDeliveryDuration(route) {
  return Object.values(deliverySchedules[route]??deliverySchedules.bridge).reduce((sum,part)=>sum+part,0);
}

function crossingPose(route,elapsed) {
  const ranger=sites.ranger;
  const path=crossingPaths[route];
  const {walk,inspect,cross,deliver,back}=deliverySchedules[route];
  const start=[ranger.x,ranger.y], abutment=path[0], far=path.at(-1);
  const lerp=(a,b,t)=>a.map((v,index)=>v+(b[index]-v)*Math.max(0,Math.min(1,t)));
  const stones=(t)=>{
    const progress=Math.max(0,Math.min(1,t))*(path.length-1);
    const segment=Math.min(path.length-2,Math.floor(progress));
    return lerp(path[segment],path[segment+1],progress-segment);
  };
  if(elapsed<walk)return {point:lerp(start,abutment,elapsed/walk)};
  if(elapsed<walk+inspect)return {point:abutment,pose:'inspect'};
  const arrival=walk+inspect+cross;
  if(elapsed<arrival)return {point:stones((elapsed-walk-inspect)/cross)};
  if(elapsed<arrival+deliver)return {point:far,pose:'handoff',dropped:elapsed>arrival+deliver*.43};
  const returning=(elapsed-arrival-deliver)/back;
  const fordPart=route==='bridge'?.38:.29;
  return {point:returning<fordPart?stones(1-returning/fordPart):lerp(abutment,start,(returning-fordPart)/(1-fordPart)),dropped:true};
}

export function mountWorld(Phaser, host, app) {
  const clamp = Phaser.Math.Clamp;
  const routes=crossingPaths;
  class Forest extends Phaser.Scene {
    preload() { loadArt(this); }
    create() {
      this.art = illustratedWorld(this);
      this.goal = null;
      this.face = 1;
      this.deliveryElapsed = app.state().delivered ? rangerDeliveryDuration(app.state().route) : 0;
      this.splashes=[];
      this.noticeElapsed=null;
      this.noticePhase='';
      this.footfalls={};
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
      const point=targetFoot(state,x,y);
      const positions=pathTo(state,[state.x,state.y],point);
      if(!positions)return false;
      this.goal={id,positions};
      return true;
    }
    onFarBank() {
      const state=app.state();
      return onLookout(state,state.x,state.y);
    }
    useCrossing() {
      const state=app.state();
      if(!state.delivered)return;
      const crossing=routes[state.route];
      const point=this.onFarBank()?crossing[0]:crossing.at(-1);
      if(this.walk(...point)) this.goal.crossing=true;
    }
    stageNotice() {
      this.noticeElapsed=0;
      this.noticePhase='';
    }
    stepSound(actor,x,y,time,state,action) {
      const previous=this.footfalls[actor]??{x,y,travel:0};
      const movement=Math.hypot(x-previous.x,y-previous.y);
      previous.x=x;previous.y=y;
      if(action!=='walk'&&action!=='carry'){previous.travel=0;this.footfalls[actor]=previous;return;}
      previous.travel+=movement<28?movement:0;
      if(previous.travel>=31){
        previous.travel%=31;
        let surface='gravel';
        if(state.route==='bridge'&&state.delivered&&Math.abs(x-450)<=15&&y>=296&&y<=407)surface='wood';
        if(state.route==='ford'&&state.pieces.includes('postA')&&y>=310&&y<=412&&canWalk(state,x,y))surface='stone';
        app.soundFoot(surface,x,actor==='scout'?.60:.39);
        if(surface==='stone'&&time>0){
          this.splashes.push({x,y,at:time});
        }
      }
      this.footfalls[actor]=previous;
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
      const focus=app.focus();
      const fieldShot=focus==='depth'?778:focus==='rig'?450:null;
      const noticeShot=this.noticeElapsed!==null&&!app.paused()&&app.motion();
      const baseZoom=Math.min(Math.max(camera.height/540,camera.width/1060),camera.height/370);
      const closeBridge=state.route==='bridge'&&!state.delivered&&Math.abs(state.x-450)<57;
      const desiredZoom=baseZoom*(fieldShot?(portrait?1.13:1.36):
        talking?(portrait?1.22:1.36):noticeShot&&!portrait?1.17:closeBridge&&!portrait?1.19:1);
      const blend=app.motion()?Math.min(1,dt*7):1;
      const zoom=this.cameraReady?Phaser.Math.Linear(camera.zoom,desiredZoom,blend):desiredZoom;
      camera.setZoom(zoom);
      const half=camera.width/(2*zoom);
      if(!canWalk(state,state.x,state.y)) [state.x,state.y]=recoverFoot(state,state.x,state.y);
      let dx=0,dy=0,remaining=Infinity;
      if (!app.paused()) {
        const key=(a,b)=>this.keys.has(a)||this.keys.has(b);
        dx=Number(key('ArrowRight','KeyD'))-Number(key('ArrowLeft','KeyA'));
        dy=Number(key('ArrowDown','KeyS'))-Number(key('ArrowUp','KeyW'));
        if(dx||dy) this.goal=null;
        if(this.goal) {
          const [tx,ty]=this.goal.positions[0];
          const x=tx-state.x,y=ty-state.y;
          const distance=Math.hypot(x,y);
          if(distance<.01){
            const {id,positions}=this.goal;
            positions.shift();
            if(!positions.length) {
              this.goal=null; app.save();
              if(id) app.interact(id);
            }
          } else {
            dx=x/distance; dy=y/distance; remaining=distance;
          }
        }
        if(dx||dy) {
          const len=Math.max(1,Math.hypot(dx,dy));
          const step=Math.min(remaining,dt*(this.goal?194:152));
          const nextX=clamp(state.x+dx*step/len,55,1005);
          const nextY=clamp(state.y+dy*step/len,202,489);
          if(canTravel(state,[state.x,state.y],[nextX,nextY])) {state.x=nextX;state.y=nextY;}
          else if(canTravel(state,[state.x,state.y],[nextX,state.y])) state.x=nextX;
          else if(canTravel(state,[state.x,state.y],[state.x,nextY])) state.y=nextY;
          this.face=dx?Math.sign(dx):this.face;
          this.moving=true;
          if (!this.savedAt || performance.now()-this.savedAt>175) {
            this.savedAt=performance.now(); app.save();
          }
        } else if(this.moving) { this.moving=false; app.save(); }
      }
      const opening=portrait&&!state.question&&state.x<375;
      const centerX=fieldShot?(portrait?fieldShot:fieldShot+102):
        talking?(portrait?sites.ranger.x:sites.ranger.x+115):
        noticeShot?(portrait?295:395):opening?Math.max(355,state.x):state.x;
      const centerY=(talking||fieldShot)&&portrait?515:camera.height/zoom<540?540-camera.height/(2*zoom):270;
      const targetX=half>=530?530:clamp(centerX,half,1060-half);
      camera.centerOn(this.cameraReady?Phaser.Math.Linear(camera.midPoint.x,targetX,blend):targetX,
        this.cameraReady?Phaser.Math.Linear(camera.midPoint.y,centerY,blend):centerY);
      this.cameraReady=true;
      const motion=app.motion();
      const time=motion?performance.now()/1000:0;
      const worldState=state.id+':'+state.pieces.join(',')+':'+state.survey.corrected;
      const noticeMode=this.noticeElapsed!==null&&this.noticeElapsed<980&&motion?'pending':'open';
      if(this.lastFrame!==worldState || this.lastPaint==null || (motion && time-this.lastPaint>.023) || this.lastMotion!==motion) {
        this.splashes=this.splashes.filter(ripple=>time>=ripple.at&&time-ripple.at<.80);
        paintWorld(this.art,time,state,this.splashes,noticeMode);
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
        this.deliveryElapsed=state.delivered?rangerDeliveryDuration(state.route):0;
        this.noticeElapsed=null;
        this.deliveryPose='';
      }
      if(this.noticeElapsed!==null){
        if(!motion)this.noticeElapsed=null;
        else if(!app.paused()){
          this.noticeElapsed+=dt*1000;
          const t=this.noticeElapsed;
          const offset=t<580?t/580:t<1370?1:Math.max(0,1-(t-1370)/690);
          rx=ranger.x+56*offset;
          ry=ranger.y-5*offset;
          if(t>=580&&t<1370)rangerPose=t<980?'inspect':'handoff';
          if(t>=980&&this.noticePhase!=='turned'){
            this.noticePhase='turned';
            app.worldSound('notice-turn',316,.67);
          }
          if(t>=2060)this.noticeElapsed=null;
        }
      }
      if(state.delivered){
        const end=rangerDeliveryDuration(state.route);
        let dropped=true;
        if(!state.complete&&motion){
          if(!app.paused())this.deliveryElapsed=Math.min(this.deliveryElapsed+dt*1000,end);
          const delivery=crossingPose(state.route,this.deliveryElapsed);
          [rx,ry]=delivery.point;
          rangerPose=delivery.pose??'';
          dropped=Boolean(delivery.dropped);
          if(rangerPose&&rangerPose!==this.deliveryPose){
            app.worldSound(rangerPose==='inspect'&&state.route==='bridge'?'bridge-creak':'gear-handoff',rx,.58);
          }
          this.deliveryPose=rangerPose;
        }
        if(dropped){
          const [x,y]=routes[state.route].at(-1);
          this.art.parcel.setPosition(x+19,y+1).setDepth(y+1).setDisplaySize(23,16);
        } else this.art.parcel.setPosition(rx+8,ry-26).setDepth(ry+.6).setDisplaySize(19,14);
      } else this.art.parcel.setPosition(204,431).setDepth(431).setDisplaySize(30,21);
      const carried=app.carry();
      const speaking=talking&&app.voicePlaying();
      figure(this.art.ranger,rx,ry,{face:Math.sign(state.x-rx)||1,
        pose:rangerPose|| (talking&&!speaking?'listen':''),gesture:speaking});
      figure(this.art.scout,state.x,state.y,{face:talking?Math.sign(rx-state.x)||this.face:this.face,
        pose:app.installing()?'fit':'',gesture:talking,carrying:Boolean(carried)});
      app.soundAt(state.x,state.y,performance.now()/1000);
      this.stepSound('scout',state.x,state.y,time,state,this.art.scout.action);
      this.stepSound('ranger',rx,ry,time,state,this.art.ranger.action);
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
          .setPosition(state.x+shift,state.y-37).setDepth(state.y+(heading==='up'?.18:.7))
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
