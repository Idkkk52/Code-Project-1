
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
Texture screen;
Sprite sprite;
Shader fract_render;
Vector2f C = {0.0, 0.0};

void update_screen() {
    window.clear();
    window.draw(sprite, &fract_render);
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
            sprite.setTexture(screen, true);
            sprite.setPosition(Vector2f(400.0 - WIDTH / 2.0, 400.0 - HEIGHT / 2.0));

            fract_render.setParameter("resolution", Vector2f(WIDTH, HEIGHT));

            change = true;
            // cout << event.size.width << ' ' << event.size.height << ' ' << window.getSize().x << ' ' << window.getSize().y << ' ' << screen.getSize().x << ' ' << screen.getSize().y << ' ' << WIDTH << ' ' << HEIGHT << endl;
        } break;
    }
}

int main() {
    fract_render.loadFromFile("fract_render.glsl", Shader::Fragment);

    float frames = 0.0;
    Clock clock;
    while (window.isOpen()) {
        sleep(milliseconds(33));
        ++frames;

        Event event;
        while (window.pollEvent(event))
            window_process_event(event);

        if (Mouse::isButtonPressed(Mouse::Left)) {
            C = (Vector2f)Mouse::getPosition() - (Vector2f)window.getPosition();
            // cout << C.x << ' ' << C.y << ' ';
            C = {(4.0f * C.x / WIDTH - 2.0f) * ratio, 4.0f * C.y / HEIGHT - 2.0f};
            // cout << C.x << ' ' << C.y << endl;
            fract_render.setParameter("C", C);
            change = true;
        }

        if (change) {
            update_screen();
            change = false;
        }

        if (clock.getElapsedTime().asMilliseconds() >= 1000) {
            window.setTitle("Julia Set Visualization (FPS: " + to_string(frames / ((float)clock.restart().asMilliseconds() / 1000.0)) + ')');
            frames = 0.0;
        }
    }

    return 0;
}
