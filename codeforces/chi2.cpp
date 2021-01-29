#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <iomanip>
#include <map>
#include <unordered_map>
 
int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);
    
    using ld = long double;
    using i64 = int64_t;
 
    size_t k1, k2, n;
    std::cin >> k1 >> k2 >> n;
 
    std::map<std::pair<i64, i64>, i64> point_cnt;
    std::vector<i64> x_cnt(k1, 0), y_cnt(k2, 0);
 
    for (size_t i = 0; i < n; ++i) {
        i64 q, w;
        std::cin >> q >> w;
        ++x_cnt[q - 1];
        ++y_cnt[w - 1];
        point_cnt[{q - 1, w - 1}]++;
    }
    ld answer = n;
    for (auto & it : point_cnt) {
        auto point = it.first;
        i64 x = point.first, y = point.second;
        ld p_real = 1.0 * x_cnt[x] * y_cnt[y] / n;
        ld sq = (p_real - it.second);
        answer += (sq * sq) / p_real - p_real;
    }
    std::cout << std::fixed << std::setprecision(10);
    std::cout << answer;
    return 0;
}
