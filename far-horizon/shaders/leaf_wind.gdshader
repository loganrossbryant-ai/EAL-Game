shader_type canvas_item;
render_mode unshaded;
uniform float clock = 0.0;
uniform float phase = 0.0;
void vertex() {
    float leaf = max(0.0, (0.64 - UV.y) / 0.64);
    VERTEX.x += (sin(clock * 1.22 + phase + UV.y * 5.0) * 10.0 + sin(clock * 2.31 + UV.x * 8.0 + phase) * 3.0) * leaf * leaf;
    VERTEX.y += sin(clock * 1.22 + UV.x * 5.0 + phase) * 2.5 * leaf * leaf;
}
