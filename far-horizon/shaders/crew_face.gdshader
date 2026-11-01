shader_type spatial;
render_mode diffuse_burley, specular_schlick_ggx;
uniform sampler2D face_atlas : source_color, filter_linear_mipmap_anisotropic, repeat_disable;
uniform vec2 cell = vec2(0.0);
uniform vec4 base_skin : source_color = vec4(0.6,0.4,0.3,1.0);
uniform vec4 fit = vec4(1.0,0.0,1.0,0.0);
void fragment(){
	vec2 projected=vec2(UV.x*fit.x+fit.y,UV.y*fit.z+fit.w);
	vec2 face_uv=clamp(projected,vec2(0.004),vec2(0.996));
	vec3 detail=texture(face_atlas,(face_uv+cell)/3.0).rgb;
	float feather=smoothstep(0.03,0.17,projected.x)*smoothstep(0.03,0.17,1.0-projected.x);
	feather*=smoothstep(0.01,0.09,projected.y)*smoothstep(0.01,0.11,1.0-projected.y);
	ALBEDO=mix(base_skin.rgb,detail,feather);
	ROUGHNESS=0.64;
	SPECULAR=0.32;
}
