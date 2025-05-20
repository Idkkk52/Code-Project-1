#include <SFML/Graphics.hpp>
#include <random>
#include <iostream>

using namespace std;
using namespace sf;

mt19937 rnd(time(NULL));

const unsigned int WIDTH = 600,
                   HEIGHT = 600;

bool Left = false,
     Right = false;

RenderWindow window(VideoMode({WIDTH, HEIGHT}), "Ping-pong Game", Style::Close);

void window_process_event(const Event& event) {
    switch(event.type) {
        case Event::Closed: {
            window.close();
        } break;

        case Event::KeyPressed: {
            switch (event.key.code) {
                case Keyboard::Left: {
                    Left = true;
                } break;

                case Keyboard::Right: {
                    Right = true;
                } break;
            }
        } break;

        case Event::KeyReleased: {
            switch (event.key.code) {
                case Keyboard::Left: {
                    Left = false;
                } break;

                case Keyboard::Right: {
                    Right = false;
                } break;
            }
        }
    }
}

int main() {
    unsigned int ball_radius = 10,
                 tile_width = 150,
                 tile_height = 5;
    Color ball_color = {255, 255, 0},
          tile_color = {255, 0, 0},
          text_color = {255, 255, 255};

    CircleShape ball(ball_radius);
    ball.setFillColor(ball_color);
    RectangleShape tile({(float)tile_width, (float)tile_height});
    tile.setFillColor(tile_color);

    Font font; font.loadFromFile("Hack-Regular.ttf");
    Text score_text("score: 0", font, 20),
         game_over_text("Game over!", font, 40);
    score_text.setFillColor(text_color);
    game_over_text.setFillColor(text_color);

    Vector2f ball_coord = {(float)(rnd() % WIDTH), (float)(rnd() % (HEIGHT / 2))},
             tile_coord = {225.0, 570.0},
             ball_speed = {-0.6, 0.0},
             tile_speed = {0.6, 0.0},
             ball_accel = {0.0, 0.0015};

    ball.setPosition(ball_coord);
    tile.setPosition(tile_coord);
        
    bool game_over = false;
    unsigned int score = 0;
    float game_over_time, dt;

    Clock clock;

    while (window.isOpen()) {
        Event event;
        while (window.pollEvent(event))
            window_process_event(event);

        window.clear();

        if (!game_over) {
            dt = clock.restart().asMicroseconds() / 1000.0;

            if (Left && tile_coord.x >= 0.0) {
                tile.move(-tile_speed * dt);
                tile_coord -= tile_speed * dt;
                // cout << 'l' << endl;
            } else if (Right && tile_coord.x <= WIDTH - tile_width) {
                tile.move(tile_speed * dt);
                tile_coord += tile_speed * dt;
                // cout << 'r' << endl;
            }
    
            ball_coord += ball_speed * dt;
            ball_speed += ball_accel * dt;

            if (ball_coord.x - (float)ball_radius <= 0) {
                ball_coord.x = (float)ball_radius - ball_coord.x;
                ball_speed.x = -ball_speed.x;
            } else if (ball_coord.x + (float)ball_radius >= (float)WIDTH) {
                ball_coord.x = (float)(WIDTH - ball_radius) * 2.0 - ball_coord.x;
                ball_speed.x = -ball_speed.x;
            }
            
            if (ball_coord.y - (float)ball_radius <= 0) {
                ball_coord.y = (float)ball_radius - ball_coord.y;
                ball_speed.y = -ball_speed.y;
            } else if (ball_coord.y + (float)ball_radius >= tile_coord.y && ball_coord.x >= tile_coord.x && ball_coord.x <= tile_coord.x + (float)tile_width) {
                ball_coord.y = (tile_coord.y - (float)ball_radius) * 2.0 - ball_coord.y;
                ball_speed.y = -ball_speed.y;
                ++score;
                score_text.setString("score: " + to_string(score));
            } else if (ball_coord.y + (float)ball_radius >= (float)HEIGHT) {
                ball_coord.y = (float)(HEIGHT - ball_radius) * 2.0 - ball_coord.y;
                ball_speed.y = -ball_speed.y;
                game_over = true;
                score = 0;
                score_text.setString("score: 0");
                clock.restart();
            }
    
            ball.setPosition(ball_coord);
    
            window.draw(tile);
            window.draw(ball);
            window.draw(score_text);

        } else {
            window.draw(game_over_text);

            if (clock.getElapsedTime().asSeconds() > 3.0) {
                game_over = false;

                ball_coord = {(float)(rnd() % WIDTH), (float)(rnd() % (HEIGHT / 2))},
                tile_coord = {225.0, 570.0},
                ball_speed = {-0.6, 0.0},
                tile_speed = {0.6, 0.0},
                ball_accel = {0.0, 0.001};

                ball.setPosition(ball_coord);
                tile.setPosition(tile_coord);

                clock.restart();
            }
            // cout << clock.getElapsedTime().asSeconds() << endl;
        }

        window.display();
    }

    return 0;
}
