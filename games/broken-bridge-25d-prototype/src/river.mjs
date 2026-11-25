// Registration follows the original 1060 × 540 scenery plate. The bank
// and the exposed faces of the rocks remain on the static plate.
const riverBounds={x:193,y:290,w:867,h:120};
const waterline=[
  [202,295],[281,297],[347,298],[403,300],[475,304],[544,306],[620,309],
  [700,311],[767,313],[828,314],[879,318],[950,321],[1059,325],
  [1059,395],[1036,398],[990,402],[949,405],[907,404],[862,402],
  [824,399],[787,397],[757,394],[727,391],[677,397],[626,397],
  [581,396],[541,395],[509,391],[469,389],[424,386],[392,380],
  [356,377],[326,374],[300,367],[274,363],[244,354],[207,345],
];
const midstreamRocks=[
  [[329,347],[339,339],[357,334],[379,338],[394,347],[402,355],[375,358],[326,356]],
  [[560,354],[577,341],[585,332],[607,322],[624,322],[647,331],[662,343],
    [677,356],[667,366],[637,367],[598,365],[573,362]],
  [[689,396],[709,385],[727,382],[746,387],[765,397],[752,405],[704,404]],
  [[804,376],[822,367],[839,368],[853,376],[853,383],[808,383]],
  [[1000,402],[1011,391],[1028,386],[1052,388],[1059,399],[1059,408],[995,408]],
];
const steppingStones=[
  [846,318,17,6],[858,324,18,6],[872,330,20,7],[886,338,22,7],
  [901,348,23,8],[913,358,25,9],[932,370,27,10],[945,384,31,11],[952,399,37,12],
];

function tracePolygon(context,polygon){
  context.beginPath();
  polygon.forEach(([x,y],index)=>{
    if(index===0)context.moveTo(x,y);
    else context.lineTo(x,y);
  });
  context.closePath();
  context.fill();
}

function waterCoverage(context,width,height,{x,y,w,h}){
  context.save();
  context.scale(width/w,height/h);
  context.translate(-x,-y);
  tracePolygon(context,waterline);
  context.globalCompositeOperation='destination-out';
  midstreamRocks.forEach(rock=>tracePolygon(context,rock));
  for(const [cx,cy,rx,ry] of steppingStones){
    context.beginPath();
    context.ellipse(cx,cy,rx,ry,0,0,Math.PI*2);
    context.fill();
  }
  context.restore();
  const {data}=context.getImageData(0,0,width,height);

  // Feather into the water. Areas within the rocks and on the dry banks
  // retain zero coverage even after the neighbouring pixels are softened.
  const feather=5;
  const horizontal=new Uint16Array(width*height);
  for(let y=0;y<height;y++){
    const row=y*width;
    let sum=0;
    for(let x=-feather;x<width;x++){
      if(x+feather<width)sum+=data[(row+x+feather)*4+3];
      if(x-feather-1>=0)sum-=data[(row+x-feather-1)*4+3];
      if(x>=0)horizontal[row+x]=sum;
    }
  }
  const coverage=new Uint8Array(width*height);
  const area=(2*feather+1)**2;
  for(let x=0;x<width;x++){
    let sum=0;
    for(let y=-feather;y<height;y++){
      if(y+feather<height)sum+=horizontal[(y+feather)*width+x];
      if(y-feather-1>=0)sum-=horizontal[(y-feather-1)*width+x];
      if(y<0)continue;
      const index=y*width+x;
      const softened=Math.max(0,Math.min(1,(sum/(255*area)-.51)/.49));
      coverage[index]=Math.round(softened*softened*(3-2*softened)*data[index*4+3]);
    }
  }
  return coverage;
}

export function makeRiver(scene){
  const source=scene.textures.get('scenery-bank').getSourceImage();
  const sx=source.width/1060, sy=source.height/540;
  const left=Math.floor(riverBounds.x*sx), top=Math.floor(riverBounds.y*sy);
  const width=Math.ceil((riverBounds.x+riverBounds.w)*sx)-left;
  const height=Math.ceil((riverBounds.y+riverBounds.h)*sy)-top;
  const x=left/sx, y=top/sy, w=width/sx, h=height/sy;
  const scratch=document.createElement('canvas');
  scratch.width=width;
  scratch.height=height;
  const input=scratch.getContext('2d',{willReadFrequently:true});
  // Copy native texels on whole-pixel boundaries to keep the fine foam and
  // riverbed detail. The layer is registered back to the same world coordinates.
  input.drawImage(source,left,top,width,height,0,0,width,height);
  const pixels=input.getImageData(0,0,width,height).data;
  input.clearRect(0,0,width,height);
  const coverage=waterCoverage(input,width,height,{x,y,w,h});
  const waterPixels=coverage.reduce((count,alpha)=>count+Number(alpha>0),0);
  const indexes=new Uint32Array(waterPixels);
  const waves=new Float32Array(waterPixels*6);
  const strength=new Float32Array(waterPixels);
  const texture=scene.textures.createCanvas('river-refractions',width,height);
  const output=texture.getContext();
  const frame=output.createImageData(width,height);
  const image=scene.add.image(x,y,texture).setOrigin(0).setDisplaySize(w,h).setDepth(1.5).setVisible(false);

  // Cache the spatial phases. Crests move downstream, with slightly
  // different angles and sizes so neighbouring reflections break apart.
  for(let index=0,row=0;index<coverage.length;index++){
    const alpha=coverage[index];
    if(!alpha)continue;
    const localX=index%width/sx;
    const localY=Math.floor(index/width)/sy;
    const a=localX*.089+localY*.46+.79*Math.sin(localX*.044+localY*.124);
    const b=localX*.051-localY*.29+.62*Math.sin(localX*.071-localY*.16);
    const c=localX*.161+localY*.19+.82*Math.cos(localX*.057+localY*.212);
    const offset=row*6;
    waves.set([Math.sin(a),Math.cos(a),Math.sin(b),Math.cos(b),Math.sin(c),Math.cos(c)],offset);
    indexes[row]=index;
    strength[row]=(alpha/255)*(.46+localY/h*.40);
    frame.data[index*4+3]=alpha;
    row++;
  }
  let rendered=-1;
  return function paintRiver(time,splashes){
    image.setVisible(time>0);
    if(!time)return;
    const tick=Math.floor(time*18);
    if(tick===rendered)return;
    rendered=tick;
    const [ca,sa,cb,sb,cc,sc]=[4.05,2.45,5.95].flatMap(rate=>[Math.cos(time*rate),Math.sin(time*rate)]);
    const wakes=splashes.map(splash=>{
      const age=time-splash.at;
      return {x:(splash.x-x+age*11)*sx,y:(splash.y-y+2)*sy,
        radius:(4+age*33)*sx, strength:Math.max(0,1-age/.8)};
    });
    for(let n=0,offset=0;n<indexes.length;n++,offset+=6){
      const index=indexes[n];
      const px=index%width, py=Math.floor(index/width);
      const a=waves[offset]*ca-waves[offset+1]*sa;
      const b=waves[offset+2]*cb-waves[offset+3]*sb;
      const c=waves[offset+4]*cc-waves[offset+5]*sc;
      let dx=2.35*a+1.42*b+.62*c;
      let dy=.81*a-.58*b+.36*c;
      for(const wake of wakes){
        const wx=px-wake.x, wy=(py-wake.y)*2.5;
        if(Math.abs(wx)>wake.radius+6||Math.abs(wy)>wake.radius+6)continue;
        const distance=Math.hypot(wx,wy);
        const envelope=Math.max(0,1-Math.abs(distance-wake.radius)/6)*wake.strength;
        const displacement=envelope*Math.sin((distance-wake.radius)*.63);
        dx+=displacement*wx/Math.max(1,distance)*1.8;
        dy+=displacement*wy/Math.max(1,distance)*.8;
      }
      const u=Math.max(0,Math.min(width-1.001,px+dx*strength[n]*sx));
      const v=Math.max(0,Math.min(height-1.001,py+dy*strength[n]*sy));
      const col=Math.floor(u), row=Math.floor(v);
      const fx=u-col, fy=v-row;
      const upper=(row*width+col)*4, lower=upper+width*4;
      const dest=index*4;
      for(let channel=0;channel<3;channel++){
        const top=pixels[upper+channel]*(1-fx)+pixels[upper+channel+4]*fx;
        const bottom=pixels[lower+channel]*(1-fx)+pixels[lower+channel+4]*fx;
        frame.data[dest+channel]=top*(1-fy)+bottom*fy;
      }
    }
    output.putImageData(frame,0,0);
    // Phaser's Canvas renderer reads the updated canvas directly.
  };
}
