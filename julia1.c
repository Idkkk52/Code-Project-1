#define UNICODE
#define _UNICODE
#include <windows.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <math.h>
#include <time.h>

static bool quit = false;

struct {
    int width;
    int height;
    uint32_t *pixels;
} frame = {0};

LRESULT CALLBACK WindowProcessMessage(HWND, UINT, WPARAM, LPARAM);
#if RAND_MAX == 32767
#define Rand32() ((rand() << 16) + (rand() << 1) + (rand() & 1))
#else
#define Rand32() rand()
#endif
int FRAMES = 0;
float FPS;
int START = 0;
double CONST_X = 2.0 / 700.0;
double CONST_Y = 2.0 / 700.0;
int X;
int Y;
double NORM_X;
double NORM_Y;
double X_N = 0.0;
double Y_N = 0.0;
double ZOOM = 2.0;
bool LEFT_BUTTON_DOWN = false;

static BITMAPINFO frame_bitmap_info;
static HBITMAP frame_bitmap = 0;
static HDC frame_device_context = 0;

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, PSTR pCmdLine, int nCmdShow) {
    const wchar_t window_class_name[] = L"My Window Class";
    static WNDCLASS window_class = { 0 };
    window_class.lpfnWndProc = WindowProcessMessage;
    window_class.hInstance = hInstance;
    window_class.lpszClassName = window_class_name;
    RegisterClass(&window_class);

    frame_bitmap_info.bmiHeader.biSize = sizeof(frame_bitmap_info.bmiHeader);
    frame_bitmap_info.bmiHeader.biPlanes = 1;
    frame_bitmap_info.bmiHeader.biBitCount = 32;
    frame_bitmap_info.bmiHeader.biCompression = BI_RGB;
    frame_device_context = CreateCompatibleDC(0);

    static HWND window_handle;
    window_handle = CreateWindow(window_class_name, L"Mandelbrot Fractal", WS_OVERLAPPEDWINDOW | WS_VISIBLE,
                                 0, 0, 600, 600, NULL, NULL, hInstance, NULL);
    if(window_handle == NULL) { return -1; }

void set_pixel(int x, int y, int r, int g, int b){
    if(r > 255) r = 255;
    if(g > 255) g = 255;
    if(b > 255) b = 255;
    if(0 <= x && x < frame.width && 0 <= y && y < frame.height) frame.pixels[y * frame.width + x] = r * 65536 + g * 256 + b; 
}

void julia(double x_m, double y_m, double zoom, float colors_r[127], float colors_g[127], float colors_b[127], double seed_x, double seed_y){
    double old_norm_x;
    double constant_x = zoom / frame.width;
    double constant_y = zoom / frame.height;
    double norm_x_c;
    double norm_y_c;
    double norm_x;
    double norm_y;
    double norm_x_sq;
    double norm_y_sq;
    for(int x = 0; x < frame.width; x++){
        for(int y = 0; y < frame.height; y++){
            norm_x = x_m + (x * 2.0 - frame.width) * constant_x;
            norm_y = y_m + (y * 2.0 - frame.height) * constant_y;
            for(int i = 0; i < 127; i++){
                old_norm_x = norm_x;
                norm_x_sq = norm_x * norm_x;
                norm_y_sq = norm_y * norm_y;
                norm_x = norm_x_sq - norm_y_sq + seed_x;
                norm_y = 2 * old_norm_x * norm_y + seed_y;
                if(norm_x_sq + norm_y_sq > 4.0){
                    int color = 40 + i * 1.7;
                    set_pixel(x, y, colors_r[i], colors_g[i], colors_b[i]);
                    //printf("%f, %f, %d\n", norm_x, norm_y, i);
                    break;
                }
                if(i == 126) {
                    set_pixel(x, y, 255, 255, 255);
                }
            }
        }
    }
}
    srand(time(NULL));
    START = time(NULL);
    int end2;
    float colors_r[127];
    float colors_g[127];
    float colors_b[127];
    for(int i = 0; i < 127; i++){
        colors_g[i] = i * 2;
        colors_r[i] = 10.0 + cos(i / 128.0) * 50.0;
        colors_b[i] = 30.0 + sqrt(i) * 20.0;
    }
    while(!quit) {
        //printf("%d, %d\n", X, Y);
        FRAMES++;
        //zoom *= 0.97;
        if(LEFT_BUTTON_DOWN) {
            X_N = (X * 2.0 - frame.width) / frame.width * 2.0;
            Y_N = (Y * 2.0 - frame.height) / frame.height * 2.0;
        }
        julia(0.0, 0.0, ZOOM, colors_r, colors_g, colors_b, X_N, Y_N);//
        
        /*if(FRAMES%30 == 0){
            end2 = time(NULL);
            //FPS = FRAMES / (end2 - START);
            //printf("FPS: %d TIME: %d seconds ZOOM: %lf\n", FRAMES / (end2 - START), end2 - START, zoom);
            
            SetWindowTextW(window_handle, L"Mandelbrot Fractal");
        }*/

        static MSG message = { 0 };
        while(PeekMessage(&message, NULL, 0, 0, PM_REMOVE)) { DispatchMessage(&message); }
        
        InvalidateRect(window_handle, NULL, FALSE);
        UpdateWindow(window_handle);
    }

    return 0;
}


LRESULT CALLBACK WindowProcessMessage(HWND window_handle, UINT message, WPARAM wParam, LPARAM lParam) {
    switch(message) {
        case WM_QUIT:
        case WM_DESTROY: {
            int end = time(NULL);
            printf("FPS: %d TIME: %d seconds", FRAMES / (end - START), end - START);
            quit = true;
        } break;

        case WM_PAINT: {
            static PAINTSTRUCT paint;
            static HDC device_context;
            device_context = BeginPaint(window_handle, &paint);
            BitBlt(device_context,
                   paint.rcPaint.left, paint.rcPaint.top,
                   paint.rcPaint.right - paint.rcPaint.left, paint.rcPaint.bottom - paint.rcPaint.top,
                   frame_device_context,
                   paint.rcPaint.left, paint.rcPaint.top,
                   SRCCOPY);
            EndPaint(window_handle, &paint);
        } break;

        case WM_SIZE: {
            frame_bitmap_info.bmiHeader.biWidth  = LOWORD(lParam);
            frame_bitmap_info.bmiHeader.biHeight = HIWORD(lParam);

            if(frame_bitmap) DeleteObject(frame_bitmap);
            frame_bitmap = CreateDIBSection(NULL, &frame_bitmap_info, DIB_RGB_COLORS, (void**)&frame.pixels, 0, 0);
            SelectObject(frame_device_context, frame_bitmap);

            frame.width = LOWORD(lParam);
            frame.height = HIWORD(lParam);
        } break;

        case WM_MOUSEMOVE: {
            POINT pt;
            GetCursorPos(&pt);
            RECT rect;
            GetWindowRect(window_handle, &rect);
            X = pt.x - rect.left;
            Y = pt.y - rect.top - 32;
        } break;

        case WM_LBUTTONDOWN: {
            LEFT_BUTTON_DOWN = true;
        } break;

        case WM_LBUTTONUP: {
            LEFT_BUTTON_DOWN = false;
        } break;

        default: {
            return DefWindowProc(window_handle, message, wParam, lParam);
        }
    }
    return 0;
}