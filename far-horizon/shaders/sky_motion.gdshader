shader_type canvas_item;
render_mode unshaded;
uniform float clock = 0.0;
uniform float strength = 0.11;
uniform vec4 mist_color : source_color = vec4(0.94, 0.97, 1.0, 1.0);
uniform vec4 mask_bounds = vec4(0.0, 0.0, 2172.0, 724.0);
varying vec2 scene_point;

float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
float noise(vec2 p) {
    vec2 i = floor(p), f = fract(p);
    f = f*f*(3.0-2.0*f);
    return mix(mix(hash(i),hash(i+vec2(1,0)),f.x),mix(hash(i+vec2(0,1)),hash(i+vec2(1,1)),f.x),f.y);
}
void vertex() { scene_point = VERTEX; }
void fragment() {
    vec2 p = scene_point / vec2(180.0, 44.0) - vec2(clock * 0.07, clock * 0.003);
    float n = noise(p) * 0.63 + noise(p * 2.1) * 0.27 + noise(p * 4.2) * 0.1;
    float clouds = smoothstep(0.44, 0.78, n);
    vec2 edge_distance = min(scene_point - mask_bounds.xy, mask_bounds.zw - scene_point);
    float edge = smoothstep(0.0, 18.0, min(edge_distance.x, edge_distance.y));
    COLOR = vec4(mist_color.rgb, clouds * strength * edge);
}
