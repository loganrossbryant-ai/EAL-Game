import {sites} from './content.mjs';
import {figure, illustratedWorld, paintWorld} from './art.mjs';

export function mountWorld(Phaser, host, app) {
  const clamp = Phaser.Math.Clamp;
  const nearBank = [[0,339],[84,344],[155,364],[231,358],[306,362],[380,355],[458,346],[520,353],
    [597,364],[689,380],[777,404],[858,421],[940,413],[1060,382]];
  const farBank = [[0,245],[75,239],[130,251],[225,253],[340,244],[437,229],[540,243],
    [641,251],[743,268],[863,294],[946,312],[1060,302]];
  const bankAt = (bank,x) => {
    const i = bank.findIndex(([edge]) => edge >= x);
    const [a,b] = [bank[i-1],bank[i]];
    return a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0]);
  };
  const walkLimit = x => bankAt(nearBank,x)+8;
  const farLimit = x => bankAt(farBank,x)-5;
  const routes = { bridge: [[438,371],[451,218]], ford: [[947,435],[910,284]] };
  const canWalk = (state,x,y) => {
    if(y>=walkLimit(x) && y<=489) return true;
    if(!state.delivered) return false;
    if(y>=202 && y<=farLimit(x)) return true;
    const [[nx,ny],[fx,fy]]=routes[state.route];
    const center=nx+(fx-nx)*(ny-y)/(ny-fy);
    return y>=fy && y<=ny && Math.abs(x-center)<(state.route==='bridge'?21:13);
  };
  class Forest extends Phaser.Scene {
    create() {
      this.art = illustratedWorld(this);
      this.people = this.add.graphics().setDepth(20);
      this.goal = null;
      this.face = 1;
      this.step = 0;
      this.deliveryElapsed = app.state().delivered ? 4300 : 0;
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
        if (event.code === 'KeyE') app.interact(app.near());
      });
      this.input.keyboard.on('keyup', event => this.keys.delete(event.code));
      window.addEventListener('blur', () => this.keys.clear());
      app.ready(this);
    }
    walk(x,y,id) {
      const state=app.state();
      x=clamp(x,55,1005);y=clamp(y,202,489);
      const far=state.delivered && y<=farLimit(x);
      if(!far && !canWalk(state,x,y)) y=clamp(y,walkLimit(x),489);
      const positions=[];
      if(state.delivered) {
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
      return state.delivered && state.y<=farLimit(state.x);
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
      const zoom=Math.min(Math.max(camera.height/540, camera.width/1060),camera.height/370);
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
          this.step+=dt*17;
          this.moving=true;
          if (!this.savedAt || performance.now()-this.savedAt>175) {
            this.savedAt=performance.now(); app.save();
          }
        } else if(this.moving) { this.moving=false; app.save(); }
      }
      camera.centerOn(half>=530?530:clamp(state.x,half,1060-half),camera.height/zoom<540?540-camera.height/(2*zoom):270);
      const motion=app.motion();
      const time=motion?performance.now()/1000:0;
      const worldState=state.id+':'+state.pieces.join(',');
      if(this.lastFrame!==worldState || this.lastPaint==null || (motion && time-this.lastPaint>.023) || this.lastMotion!==motion) {
        paintWorld(this.art,time,state);
        this.lastPaint=time; this.lastMotion=motion; this.lastFrame=worldState;
      }
      this.people.clear();
      const ranger=sites.ranger;
      let rx=ranger.x,ry=ranger.y,step=0,pack=!state.delivered;
      if(this.deliverySession!==state.id) {
        this.deliverySession=state.id;
        this.deliveryElapsed=state.delivered?4300:0;
      }
      if(state.delivered&&!state.complete&&motion) {
        if(!app.paused()) this.deliveryElapsed=Math.min(this.deliveryElapsed+dt*1000,4300);
        const elapsed=this.deliveryElapsed;
        const outgoing=elapsed<2300;
        const p=outgoing?elapsed/2300:1-clamp((elapsed-2700)/1600,0,1);
        const path=state.route==='bridge'?[[246,376],[440,373],[449,223]]:[[246,376],[940,437],[912,306]];
        const section=p<.64?0:1;
        const ratio=section===0?p/.64:(p-.64)/.36;
        rx=Phaser.Math.Linear(path[section][0],path[section+1][0],ratio);
        ry=Phaser.Math.Linear(path[section][1],path[section+1][1],ratio);
        pack=outgoing;
        step=(elapsed<2300||elapsed>2700&&elapsed<4300)?elapsed*.017:0;
      }
      figure(this.people,rx,ry,{ranger:true,step,pack,face:Math.sign(state.x-rx)||1});
      figure(this.people,state.x,state.y,{step:motion&&this.moving?this.step:0,face:this.face});
      app.placePins(this);
    }
  }
  return new Phaser.Game({
    type:Phaser.CANVAS, parent:host, backgroundColor:'#142b32', banner:false,
    scale:{mode:Phaser.Scale.RESIZE,width:host.clientWidth,height:host.clientHeight},
    scene:[Forest], audio:{noAudio:true}, render:{antialias:true},
  });
}
