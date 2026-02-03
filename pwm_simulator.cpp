#include <iostream>
#include <cmath>
#include <fstream>    // for file output
#include <thread>     // for sleep
#include <chrono>     // for sleep
using namespace std;

char highChar = '#';
char lowChar = '-';

// 函數：輸出一段 PWM 波形
void printPWMBlock(int period, int duty, ostream &out, bool delay = false) {
    int highTime = round((duty / 100.0) * period);
    int lowTime = period - highTime;

    out << "[";
    for (int i = 0; i < highTime; i++) {
        out << highChar;
        if (delay) {
            cout << highChar << flush;
            this_thread::sleep_for(chrono::milliseconds(100));
        }
    }
    for (int i = 0; i < lowTime; i++) {
        out << lowChar;
        if (delay) {
            cout << lowChar << flush;
            this_thread::sleep_for(chrono::milliseconds(100));
        }
    }
    out << "]";
    if (delay) cout << "]";
}

int main() {
    int period, duty, cycles;
    string filename;

    // 使用者輸入
    cout << "輸入週期長度（整數）：";
    cin >> period;

    cout << "輸入佔空比（0~100）：";
    cin >> duty;

    if (duty < 0 || duty > 100) {
        cout << "錯誤：佔空比必須在 0~100 之間。" << endl;
        return 1;
    }

    cout << "輸入週期數：";
    cin >> cycles;

    // 自訂高/低符號
    cout << "輸入高電平符號（預設為 #）：";
    cin >> highChar;
    cout << "輸入低電平符號（預設為 -）：";
    cin >> lowChar;

    // 檔案儲存
    cout << "請輸入輸出檔名（例如 output.txt）：";
    cin >> filename;
    ofstream fout(filename);
    if (!fout.is_open()) {
        cout << "無法開啟檔案 " << filename << endl;
        return 1;
    }

    // 輸出波形
    cout << "\n模擬 PWM 波形：" << endl;
    for (int i = 0; i < cycles; i++) {
        printPWMBlock(period, duty, cout);
        printPWMBlock(period, duty, fout);
    }
    cout << endl;

    // 漸變 PWM + 寫入檔案
    cout << "\n模擬 PWM 亮度漸變（從亮到暗）：" << endl;
    fout << "\n模擬 PWM 亮度漸變（從亮到暗）：" << endl;
    for (int d = 100; d >= 0; d -= 10) {
        printPWMBlock(period, d, cout);
        cout << " (" << d << "%)" << endl;
        printPWMBlock(period, d, fout);
        fout << " (" << d << "%)" << endl;
    }

    // 動畫
    cout << "\n動畫模擬 PWM（慢速播放）：" << endl;
    for (int i = 0; i < cycles; i++) {
        printPWMBlock(period, duty, cout, true);
        cout << " ";
    }
    cout << endl;

    fout.close();
    cout << "\n波形已儲存到檔案：" << filename << endl;

    return 0;
}

