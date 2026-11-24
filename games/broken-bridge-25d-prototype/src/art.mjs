// All primary scenery, characters and inspectable objects are authored raster assets.
export function loadArt(scene) {
  Object.entries(ART).forEach(([name, url]) => scene.load.image(name, url));
}

export function illustratedWorld(scene) {
  const add = (key,x,y,width,height,depth,originX=0,originY=0) =>
    scene.add.image(x,y,key).setOrigin(originX,originY).setDisplaySize(width,height).setDepth(depth);
  add('scenery-distance',-45,0,1150,540,-2).setScrollFactor(.91,1);
  add('scenery-bank',0,0,1060,540,0);
  const canopy=add('storm-canopy',-39,-38,425,165,582).setScrollFactor(1.08,1);
  add('storm-boulder',332,474,71,43,474,.5,1);
  const debris=add('storm-debris',397,430,81,31,428,.5,1);
  const current=add('current',209,272,596,137,1).setAlpha(.16);
  const water=scene.add.graphics().setDepth(2);
  const atmosphere=scene.add.graphics().setDepth(3);
  const frontLeft=add('front-left',0,445,266,95,550).setScrollFactor(1.035,1);
  const frontRight=add('front-right',830,450,230,90,550).setScrollFactor(1.035,1);
  const lamp=scene.add.ellipse(70,287,67,50,0xffb250,.014).setDepth(2);
  const bridge=add('bridge-damaged-v3',450,416,139,125,4,.5,1);
  const fill=[0,1].map(i=>add('bridge-patch-v3-'+i,450,416,139,125,5,.5,1).setVisible(false));
  const rack=add('rack-loaded',113,438,55,48,438,.5,1);
  const parcel=add('supplies',204,431,30,21,431,.5,1);
  add('depth',778,414,39,51,414,.5,1);
  add('sign',934,449,58,32,449,.5,1);
  const flags=[
    add('flag-0',954,415,21,40,415,.5,1).setFlipX(true),
    add('flag-1',857,310,18,34,310,.5,1),
  ];
  const actor = (role, height) => ({
    image: add(role+'-v3-0',0,0,height*160/192,height,20,.5,188/192),
    shadow: scene.add.ellipse(0,0,22,6,0x171b15,.50),
    penumbra: scene.add.ellipse(0,0,35,9,0x252317,.23),
    role,height, gait:0, direction:'right',
  });
  const carry=add('board',0,0,1,1,20,.5,.5).setVisible(false);
  return {current,water,atmosphere,frontLeft,frontRight,canopy,debris,lamp,bridge,fill,rack,flags,parcel,carry,
    ranger:actor('ranger',88), scout:actor('scout',81)};
}

export function paintWorld(art,time,state) {
  art.current.x=209+Math.sin(time*.78)*11;
  art.current.alpha=.12+.055*Math.sin(time*1.2);
  art.frontLeft.x=Math.sin(time*.82)*3;
  art.frontRight.x=830+Math.sin(time*.66)*3;
  art.frontLeft.rotation=Math.sin(time*.68)*.005;
  art.frontRight.rotation=Math.sin(time*.79)*.007;
  art.lamp.fillAlpha=.014+.008*Math.sin(time*1.9);
  art.canopy.setRotation(Math.sin(time*.64)*.013);
  art.water.clear();
  // Glints stay on individual open-water reaches, clear of stones and shore.
  const reaches=[[218,322,374,351],[231,351,421,377],[492,321,565,351],
    [504,371,769,385],[686,324,813,349],[721,351,869,369],[548,339,560,360]];
  reaches.forEach(([left,top,right,bottom],reach)=>{
    for(let i=0;i<7;i++){
      const phase=(time*(.19+reach*.01)+i*.143+reach*.061)%1;
      const x=right-phase*(right-left), y=top+((i*13+reach*7)%21)/21*(bottom-top);
      const light=Math.sin(phase*Math.PI);
      const length=(6+i%4*4)*light;
      art.water.lineStyle(1.15,reach<2?0xffdcb1:0xc6ede3,.31*light)
        .beginPath().moveTo(x,y).lineTo(x+length*.58,y+.8).lineTo(x+length,y+.15).strokePath();
    }
  });
  art.atmosphere.clear();
  for(let i=0;i<17;i++){
    const drift=(time*(3+i%3)+i*26)%158;
    const x=151+drift+(i%3)*19, y=150+i*13+Math.sin(time*.64+i)*6;
    const alpha=Math.sin(drift/158*Math.PI)*(.15+i%3*.065);
    art.atmosphere.fillStyle(0xffe2ae,alpha).fillCircle(x,y,.65+i%3*.38);
  }
  const repaired=state.delivered&&state.route==='bridge';
  art.debris.setVisible(!repaired);
  art.bridge.setTexture(repaired?'bridge-restored-v3':'bridge-damaged-v3').setDisplaySize(139,125);
  art.fill.forEach((image,i)=>image.setVisible(!repaired&&state.pieces.includes(['boardA','boardB'][i])));
  art.rack.setTexture(state.route==='bridge'?'rack':'rack-loaded').setDisplaySize(55,48);
  art.flags.forEach((flag,i)=>flag.setVisible(state.pieces.includes(['postA','postB'][i])));
}

export function figure(actor,x,y,{face=1,gesture=false,pose='',carrying=false}={}) {
  const dx=x-(actor.x??x),dy=y-(actor.y??y);
  const distance=Math.hypot(dx,dy);
  const moving=distance>.065&&distance<35;
  const scale=.83+(y-300)*.00118;
  if(moving) {
    const direction=Math.abs(dy)>Math.abs(dx)*.68?(dy<0?'up':'down'):(dx<0?'left':'right');
    if(direction!==actor.direction) {actor.gait=0;actor.direction=direction;}
    actor.gait=(actor.gait+distance/(63*scale))%1;
  } else actor.gait=0;
  actor.x=x;actor.y=y;
  const frame=Math.floor(actor.gait*6);
  const cycle=actor.role+'-v4-'+actor.direction+'-'+frame;
  const posed=actor.role+'-v4-'+(pose||(carrying?'hold':''));
  const resolvedPose=(pose||(!moving&&carrying))&&actor.image.scene.textures.exists(posed);
  const walking=moving&&actor.image.scene.textures.exists(cycle);
  const key=resolvedPose?posed:walking?cycle:actor.role+'-v3-'+(gesture?3:0);
  actor.key=key;
  actor.action=carrying?'carry':moving?'walk':pose|| (gesture?'gesture':'idle');
  actor.image.setTexture(key).setPosition(x,y)
    .setDisplaySize(actor.height*160/192*scale,actor.height*scale).setDepth(y+.3)
    .setFlipX(!walking&&face<0);
  const footShift=walking?Math.cos(frame*Math.PI/3)*2:0;
  actor.penumbra.setPosition(x+4,y+1).setDisplaySize(37*scale,10*scale).setDepth(y-.05);
  actor.shadow.setPosition(x+footShift,y).setDisplaySize(27*scale,6*scale).setDepth(y)
    .setAlpha(walking?(frame%3===0?.93:.76):1);
}
