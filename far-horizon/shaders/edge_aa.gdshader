shader_type canvas_item;
render_mode unshaded;
// A small edge filter on the 3D picture. Projected text and portraits stay sharp.
void fragment(){
 vec2 p=TEXTURE_PIXEL_SIZE;
 vec4 center=texture(TEXTURE,UV);
 vec3 left=texture(TEXTURE,UV-vec2(p.x,0.0)).rgb;
 vec3 right=texture(TEXTURE,UV+vec2(p.x,0.0)).rgb;
 vec3 above=texture(TEXTURE,UV-vec2(0.0,p.y)).rgb;
 vec3 below=texture(TEXTURE,UV+vec2(0.0,p.y)).rgb;
 vec3 luma=vec3(0.2126,0.7152,0.0722);
 float c=dot(center.rgb,luma);
 float low=min(c,min(min(dot(left,luma),dot(right,luma)),min(dot(above,luma),dot(below,luma))));
 float high=max(c,max(max(dot(left,luma),dot(right,luma)),max(dot(above,luma),dot(below,luma))));
 float edge=smoothstep(0.08,0.24,high-low);
 vec3 filtered=center.rgb*0.6+(left+right+above+below)*0.1;
 COLOR=vec4(mix(center.rgb,filtered,edge*0.65),center.a);
}
