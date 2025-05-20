
#include <SFML/Graphics.hpp>
#include <iostream>
#include <cmath>

#pragma GCC optimize("unroll-loops,Ofast")

using namespace std;
using namespace sf;

float WIDTH = 800.0,
      HEIGHT = 800.0,
      ratio = 1.0;
bool change = false;

RenderWindow window(VideoMode({(unsigned int)WIDTH, (unsigned int)HEIGHT}), "Julia Set Visualization");
View view = window.getDefaultView();
Uint8* bitmap = (Uint8*)malloc((unsigned int)WIDTH * (unsigned int)HEIGHT * 4);
Texture screen;
Sprite sprite;
Vector2f C = {0.0, 0.0};
Color cols[256];

Color render_pixel(const float& x, const float& y) {
    Vector2f Z = {(4.0f * x / WIDTH - 2.0f) * ratio, 4.0f * y / HEIGHT - 2.0f},
             old_Z;

    int i = 0;
    for (; i < 255 && Z.x * Z.x + Z.y * Z.y < 4.0; ++i) {
        old_Z = Z;
        Z.x = old_Z.x * old_Z.x - old_Z.y * old_Z.y + C.x;
        Z.y = 2.0 * old_Z.x * old_Z.y + C.y;
    }

    return cols[i];
}

void update_screen() {
    for (int y = 0; y < (int)HEIGHT; ++y) {
        for (int x = 0; x < (int)WIDTH; ++x) {
            const Color col = render_pixel((float)x, (float)y);
            bitmap[(y * (int)WIDTH + x) * 4] = col.r;
            bitmap[(y * (int)WIDTH + x) * 4 + 1] = col.g;
            bitmap[(y * (int)WIDTH + x) * 4 + 2] = col.b;
            bitmap[(y * (int)WIDTH + x) * 4 + 3] = col.a;
        }
    }
    screen.update(bitmap);
    sprite.setTexture(screen, true);
    sprite.setPosition({400.0f - WIDTH / 2.0f, 400.0f - HEIGHT / 2.0f});
    window.draw(sprite);
    window.display();
}

void window_process_event(const Event& event) {
    switch(event.type) {
        case Event::Closed: {
            window.close();
        } break;

        case Event::Resized: {
            WIDTH = event.size.width;
            HEIGHT = event.size.height;
            ratio = WIDTH / HEIGHT;

            view.setSize({WIDTH, HEIGHT});
            window.setView(view);
            screen.create(event.size.width, event.size.height);
            bitmap = (Uint8*)realloc(bitmap, event.size.width * event.size.height * 4);
            change = true;
            // cout << event.size.width << ' ' << event.size.height << ' ' << window.getSize().x << ' ' << window.getSize().y << ' ' << screen.getSize().x << ' ' << screen.getSize().y << ' ' << WIDTH << ' ' << HEIGHT << endl;
        } break;
    }
}

int main() {
    for (int i = 0; i < 255; ++i) {
        cols[i] = {
            (Uint8)(sqrt(i) * 16.0),
            (Uint8)((float)i * log2(i) / 8.0),
            (Uint8)(1000.0 / (float)(i + 10))
        };
    }

    float frames = 0.0;
    Clock clock;
    while (window.isOpen()) {
        ++frames;

        Event event;
        while (window.pollEvent(event))
            window_process_event(event);

        if (Mouse::isButtonPressed(Mouse::Left)) {
            C = (Vector2f)Mouse::getPosition() - (Vector2f)window.getPosition();
            // cout << C.x << ' ' << C.y << ' ';
            C = {(4.0f * C.x / WIDTH - 2.0f) * ratio, 4.0f * C.y / HEIGHT - 2.0f};
            // cout << C.x << ' ' << C.y << endl;
            change = true;
        }

        if (change) {
            update_screen();
            change = false;
        } else {
            sleep(milliseconds(40));
        }

        if (clock.getElapsedTime().asMilliseconds() >= 1000) {
            window.setTitle("Julia Set Visualization (FPS: " + to_string(frames / ((float)clock.restart().asMilliseconds() / 1000.0)) + ')');
            frames = 0.0;
        }
    }

    return 0;
}
