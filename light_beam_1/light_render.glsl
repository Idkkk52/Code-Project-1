uniform vec2 source;
uniform vec2 direction;

void main() {
    vec2 cur = gl_FragCoord.xy - source.xy;
    float angle = atan(cur.x * direction.y - cur.y * direction.x, cur.x * direction.x + cur.y * direction.y);
    float dist = sqrt(cur.x * cur.x + cur.y * cur.y);
    float col = (1.0 - dist / 1000.0) - abs(angle) * 0.35;
    col *= col * col;
    gl_FragColor = vec4(col, col, col, 1.0);
}
