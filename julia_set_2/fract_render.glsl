
uniform vec2 C;
uniform vec2 resolution;

void main() {
    vec2 Z = (gl_FragCoord.xy / resolution.xy) * 4.0 - 2.0, old_Z;
    Z.x *= (resolution.x / resolution.y);
    float i = 0.01;
    for (; Z.x * Z.x + Z.y * Z.y < 4.0 && i < 1.0; i += 0.01) {
        old_Z = Z;
        Z.x = old_Z.x * old_Z.x - old_Z.y * old_Z.y + C.x;
        Z.y = 2.0 * old_Z.x * old_Z.y + C.y;
    }

    gl_FragColor = vec4(i * 4.0, 0.1 + sin(i), 0.2 + sqrt(i) * 0.5, 1.0);
}
