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

RenderWindow window(VideoMode({(unsigned int)WIDTH, (unsigned int)HEIGHT}), "Simple Light Beam");
View view = window.getDefaultView();
Texture screen;
Sprite sprite;
Shader light_render;

Vector2f source = Vector2f(WIDTH / 4.0, HEIGHT / 2.0);

void update_screen() {
    window.clear();
    sprite.setPosition(Vector2f(400.0 - WIDTH / 2.0, 400.0 - HEIGHT / 2.0));
    window.draw(sprite, &light_render);
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

            change = true;
            // cout << event.size.width << ' ' << event.size.height << ' ' << window.getSize().x << ' ' << window.getSize().y << ' ' << screen.getSize().x << ' ' << screen.getSize().y << ' ' << WIDTH << ' ' << HEIGHT << endl;
        } break;
    }
}

int main() {
    light_render.loadFromFile("light_render.glsl", Shader::Fragment);
    light_render.setParameter("source", source);
    light_render.setParameter("direction", Vector2f(1.0, 0.0));

    float frames = 0.0;
    Clock clock;
    while (window.isOpen()) {
        sleep(milliseconds(33));
        ++frames;

        Event event;
        while (window.pollEvent(event))
            window_process_event(event);

        if (Mouse::isButtonPressed(Mouse::Right)) {
            Vector2f cur = (Vector2f)Mouse::getPosition() - (Vector2f)window.getPosition();
            cur.y = HEIGHT - cur.y + 28.0;
            light_render.setParameter("direction", cur - source);
            change = true;

        } else if (Mouse::isButtonPressed(Mouse::Left)) {
            source = (Vector2f)Mouse::getPosition() - (Vector2f)window.getPosition();
            source.y = HEIGHT - source.y + 28.0;
            light_render.setParameter("source", source);
            change = true;
        }

        if (change) {
            update_screen();
            change = false;
        }

        if (clock.getElapsedTime().asMilliseconds() >= 1000) {
            window.setTitle("Simple Light Beam (FPS: " + to_string(frames / ((float)clock.restart().asMilliseconds() / 1000.0)) + ')');
            frames = 0.0;
        }
    }

    return 0;
}
