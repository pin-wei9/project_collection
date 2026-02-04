#include <iostream>
#include <string>
#include <deque>
#include <algorithm>
#include <iomanip>

// 定義資料結構
struct MoodEntry {
    std::string dateTime;
    int age;
    double sleepHours;
    double sleepQuality;
    double stressLevel;
    double emotionScore;
    double idealSleepHours;
};

// 全域變數與常數
std::deque<MoodEntry> moodEntries;
const int analysisWindow = 7;

// 根據年齡設定理想睡眠時數
double getIdealSleepHours(int age) {
    if (age >= 13 && age <= 18) return 9.0;
    else if (age >= 19 && age <= 64) return 7.5;
    else if (age >= 65) return 7.5;
    else return 8.0;
}

// 核心邏輯：判斷情緒標籤 (共用於每日與七日分析)
std::string determineMoodLabel(double deficit, double quality, double stress, double emotion) {
    if (deficit >= 3 && quality < 4 && emotion <= 3 && stress >= 8)
        return "暴走 Laifu";
    else if (deficit >= 2 && quality < 5 && emotion < 4)
        return "憂鬱 Laifu";
    else if (deficit >= 1.5 && quality < 6 && stress >= 6)
        return "疲憊 Laifu";
    else if ((stress >= 7 && emotion <= 5) || (quality < 6 && emotion <= 5))
        return "焦慮 Laifu";
    else if (deficit <= 0.5 && quality >= 7 && stress <= 4 && emotion >= 8)
        return "開心 Laifu";
    else
        return "平穩 Laifu";
}

// 顯示狀態輸出格式
void showMoobiState(const std::string& mood, double sleep, double stress, double emotion) {
    std::cout << "\n--- Laifu 綜合狀態：" << mood << " ---" << std::endl;
    std::cout << "平均睡眠時數：" << std::fixed << std::setprecision(1) << sleep << " 小時" << std::endl;
    std::cout << "平均壓力指數：" << stress << std::endl;
    std::cout << "平均情緒分數：" << emotion << std::endl;
}

// 顯示每日即時建議
void showMoobiFeedback(const MoodEntry& entry) {
    std::cout << "\n--- Laifu 今日回饋 ---" << std::endl;
    bool perfect = true;

    if (entry.sleepHours < entry.idealSleepHours) {
        std::cout << "[-] 睡眠偏少 (理想：" << entry.idealSleepHours << "h)，建議補眠。" << std::endl;
        perfect = false;
    }
    if (entry.sleepQuality < 6) {
        std::cout << "[-] 睡眠品質不佳，請檢查睡眠環境。" << std::endl;
        perfect = false;
    }
    if (entry.stressLevel > 7) {
        std::cout << "[!] 壓力過高，請試著深呼吸或運動放鬆。" << std::endl;
        perfect = false;
    }
    if (entry.emotionScore < 5) {
        std::cout << "[!] 心情低落，找人聊聊或做點喜歡的事吧！" << std::endl;
        perfect = false;
    }
    if (perfect) {
        std::cout << "[+] 狀態完美，請繼續保持！" << std::endl;
    }
}

// 執行七日趨勢分析
void performWeeklyAnalysis() {
    if (moodEntries.size() < analysisWindow) return;

    double tSleep = 0, tQuality = 0, tStress = 0, tEmotion = 0, tIdeal = 0;
    int startIdx = moodEntries.size() - analysisWindow;

    for (int i = startIdx; i < moodEntries.size(); ++i) {
        tSleep += moodEntries[i].sleepHours;
        tQuality += moodEntries[i].sleepQuality;
        tStress += moodEntries[i].stressLevel;
        tEmotion += moodEntries[i].emotionScore;
        tIdeal += moodEntries[i].idealSleepHours;
    }

    double avgSleep = tSleep / analysisWindow;
    double avgQuality = tQuality / analysisWindow;
    double avgStress = tStress / analysisWindow;
    double avgEmotion = tEmotion / analysisWindow;
    double avgDeficit = (tIdeal / analysisWindow) - avgSleep;

    std::string weeklyMood = determineMoodLabel(avgDeficit, avgQuality, avgStress, avgEmotion);
    
    std::cout << "\n================================";
    std::cout << "\n📊 七日趨勢綜合分析結果";
    showMoobiState(weeklyMood, avgSleep, avgStress, avgEmotion);
    std::cout << "================================\n";
}

// 新增資料功能
void addMoodEntry() {
    MoodEntry entry;
    std::cout << "\n[1] 輸入日期時間 (例 0204): ";
    std::getline(std::cin, entry.dateTime);
    
    std::cout << "[2] 您的年齡: ";
    std::cin >> entry.age;
    
    std::cout << "[3] 睡眠時數: ";
    std::cin >> entry.sleepHours;
    
    std::cout << "[4] 睡眠品質 (0-10): ";
    std::cin >> entry.sleepQuality;
    
    std::cout << "[5] 壓力指數 (0-10): ";
    std::cin >> entry.stressLevel;
    
    std::cout << "[6] 情緒分數 (0-10): ";
    std::cin >> entry.emotionScore;
    std::cin.ignore(); // 清除緩衝區以利下次 getline

    entry.idealSleepHours = getIdealSleepHours(entry.age);
    moodEntries.push_back(entry);

    // 顯示即時分析
    showMoobiFeedback(entry);
    double deficit = entry.idealSleepHours - entry.sleepHours;
    std::string dailyMood = determineMoodLabel(deficit, entry.sleepQuality, entry.stressLevel, entry.emotionScore);
    showMoobiState(dailyMood, entry.sleepHours, entry.stressLevel, entry.emotionScore);

    // 檢查是否足夠進行七日分析
    if (moodEntries.size() >= analysisWindow) {
        performWeeklyAnalysis();
    } else {
        std::cout << "\n(還需 " << (analysisWindow - moodEntries.size()) << " 天資料即可開啟七日趨勢分析)\n";
    }
}

// 主程式
int main() {
    int choice;
    std::cout << "歡迎使用 Laifu 情緒評估系統 v1.0\n";

    do {
        std::cout << "\n--- 主選單 ---\n";
        std::cout << "1. 填寫今日狀態紀錄\n";
        std::cout << "2. 結束程式\n";
        std::cout << "請輸入選擇: ";
        
        if (!(std::cin >> choice)) {
            std::cin.clear();
            std::cin.ignore(1000, '\n');
            continue;
        }
        std::cin.ignore();

        if (choice == 1) {
            addMoodEntry();
        }
    } while (choice != 2);

    std::cout << "\n感謝使用，祝您有美好的一天！\n";
    return 0;
}
