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
 
    std::vector<std::unordered_map<i64, i64>> distr(k1);
    std::vector<i64> by_x(k1, 0);
 
    for (size_t i = 0; i < n; ++i) {
        i64 x, y;
        std::cin >> x >> y;
        ++distr[x - 1][y - 1];
        ++by_x[x - 1];
    }
 
    ld entropy = 0;
    for (size_t x = 0; x < k1; ++x) {
        ld acc = 0;
        for (auto yp : distr[x]) {
            i64 y = yp.second;
            ld p = y * 1.0 / by_x[x];
            acc += p * log(p);
        }
        entropy += - by_x[x] * 1.0 / n * acc;
    }
 
    std::cout << std::fixed << std::setprecision(10);
    std::cout << entropy;
    return 0;
}
