#include <windows.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <math.h>
#include <time.h>
#define UNICODE
#define _UNICODE




static bool quit = false;

struct {
    int width;
    int height;
    uint32_t *pixels;
} frame = {0};

static BITMAPINFO frame_bitmap_info;
static HBITMAP frame_bitmap = 0;
static HDC frame_device_context = 0;

POINT pt;
RECT rect;




long long frame_count = 0;
int start_time = 0;
long double zoom_x = 2.0 / 700.0,
            zoom_y = 2.0 / 700.0,
            WtoH = 1.0,
            normalized_mouse_x,
            normalized_mouse_y,
            julia_C_x = 0.0,
            julia_C_y = 0.0, 
            
            fractal_center_x = 0.0,
            fractal_center_y = 0.0,
            
            zoom = 2.0, 
            
            temp, temp2;

int mouse_x,
    mouse_y;

float colors_r[127],
      colors_g[127],
      colors_b[127];

bool change = true, 
     lmb_down = false;




// event-handler
LRESULT CALLBACK WindowProcessMessage(HWND window_handle, UINT message, WPARAM wParam, LPARAM lParam) {
    switch(message) {
        case WM_QUIT:
        case WM_DESTROY: {
            int time_passed = time(NULL) - start_time;
            printf("FPS: %lf TIME: %d seconds", (float)frame_count / (float)(time_passed), time_passed);
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


            zoom_x = zoom / frame.width;
            zoom_y = zoom / frame.height;
            normalized_mouse_x = fractal_center_x + (long double)(mouse_x * 2 - frame.width) / (long double)frame.width * zoom;
            normalized_mouse_y = fractal_center_y + (long double)(mouse_y * 2 - frame.height) / (long double)frame.height * zoom;
            WtoH = (long double)frame.width / (long double)(frame.height);
            change = true;
            GetWindowRect(window_handle, &rect);
            //printf("%lf, %lf\n", normalized_x_Z, normalized_y_Z);
        } break;



        case WM_MOVE: {
            GetWindowRect(window_handle, &rect);
        } break;



        case WM_MOUSEMOVE: {
            GetCursorPos(&pt);
            mouse_x = pt.x - rect.left - 8;
            mouse_y = pt.y - rect.top - 32;
            normalized_mouse_x = fractal_center_x + (long double)(mouse_x * 2 - frame.width) * zoom_x;
            normalized_mouse_y = fractal_center_y + (long double)(mouse_y * 2 - frame.height) * -zoom_y;
            //printf("%lf, %lf\n", normalized_x_Z, normalized_y_Z);
        } break;



        case WM_MOUSEWHEEL: {
            if((int)wParam > 0) {
                temp = 7000000.0 / wParam;
                zoom *= temp;
                temp2 = 1.0 - temp;
                fractal_center_x += (normalized_mouse_x - fractal_center_x) * temp2;
                fractal_center_y += (normalized_mouse_y - fractal_center_y) * temp2;
            }

            if((int)wParam < 0) {
                temp = 7000000.0 / -wParam;
                zoom /= temp;
                temp2 = 1.0 - temp;
                fractal_center_x -= (normalized_mouse_x - fractal_center_x) * temp2;
                fractal_center_y -= (normalized_mouse_y - fractal_center_y) * temp2;
            }

            //printf("%d\n", wParam);

            zoom_x = zoom / (long double)frame.width;
            zoom_y = zoom / (long double)frame.height;
            change = true;
            //printf("%lf, %lf\n", normalized_x_Z, normalized_y_Z);
        } break;


 
        case WM_LBUTTONDOWN: {
            lmb_down = true;
        } break;
        
        case WM_LBUTTONUP: {
            lmb_down = false;
        } break;



        default: {
            return DefWindowProc(window_handle, message, wParam, lParam);
        }
    }

    if(lmb_down) {
        julia_C_x = normalized_mouse_x;
        julia_C_y = normalized_mouse_y;
        change = true;
    }

    return 0;
}






// set_pixel
void set_pixel(int x, int y, int r, int g, int b) {
    if(r > 255) r = 255;
    if(g > 255) g = 255;
    if(b > 255) b = 255;
    if(0 <= x && x < frame.width && 0 <= y && y < frame.height) frame.pixels[y * frame.width + x] = (r << 16) + (g << 8) + b; 
}






// fractal drawing function
void fractal_julia() {
    long double normalized_x_C,
                normalized_y_C,
                normalized_x_Z,
                normalized_y_Z,
                normalized_x_Z_squared,
                normalized_y_Z_squared;

    for(int x = 0; x < frame.width; x++) {
        for(int y = 0; y < frame.height; y++) {
            normalized_x_C = julia_C_x;
            normalized_y_C = julia_C_y;
            normalized_x_Z = fractal_center_x + (x * 2.0 - frame.width) * zoom_x * WtoH;
            normalized_y_Z = fractal_center_y + (y * 2.0 - frame.height) * zoom_y;

            for(int i = 0; i < 127; i++) {
                temp = normalized_x_Z;
                normalized_x_Z_squared = normalized_x_Z * normalized_x_Z;
                normalized_y_Z_squared = normalized_y_Z * normalized_y_Z;

                normalized_x_Z = (normalized_x_Z_squared - normalized_y_Z_squared + normalized_x_C);
                normalized_y_Z = (2 * temp * normalized_y_Z + normalized_y_C);

                if(normalized_x_Z_squared + normalized_y_Z_squared > 4.0) {
                    int color = 40 + i * 1.7;
                    set_pixel(x, y, colors_r[i], colors_g[i], colors_b[i]);
                    //printf("%f, %f, %d\n", normalized_x_Z, normalized_y_Z, i);
                    break;
                }

                if(i == 126) 
                    set_pixel(x, y, 255, 255, 255);
            }
        }
    }
}






// main()
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
    window_handle = CreateWindow(window_class_name, 
                                 "Mandelbrot Set Visualization", 
                                 WS_OVERLAPPEDWINDOW | WS_VISIBLE,
                                 0, 0, 
                                 700, 700, 
                                 NULL, 
                                 NULL, 
                                 hInstance, 
                                 NULL);

    if(window_handle == NULL) return -1;




    srand(time(NULL));
    start_time = time(NULL);

    for(float i = 0; i < 127; ++i) {
        colors_g[(int)i] = i * log2(i + 1.0) / 2.0;
        colors_r[(int)i] = sqrt(i) * 22.0;
        colors_b[(int)i] = 75.0 + cos(i / 5.0) * 25.0;
    }




    while(!quit) {
        if(change) {
            ++frame_count;
            fractal_julia();
            change = false;
        }
        
        static MSG message = { 0 };
        while(PeekMessage(&message, NULL, 0, 0, PM_REMOVE)) { DispatchMessage(&message); }
        
        InvalidateRect(window_handle, NULL, FALSE);
        UpdateWindow(window_handle);
    }




    return 0;
}