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
 
    // using ld = long double;
    using i64 = int64_t;
 
    size_t k, n;
    std::cin >> k >> n;
 
    std::vector<i64> all_x(n);
    std::vector<std::vector<i64>> by_y(k);
 
    for (size_t i = 0; i < n; ++i) {
        i64 q, w;
        std::cin >> q >> w;
        all_x[i] = q;
        by_y[w - 1].push_back(q);
    }
    std::sort(all_x.begin(), all_x.end());
 
    i64 total = 0;
    i64 internal = 0.0;
    {
        i64 sum = 0.0;
        for (size_t i = 0; i < n; ++i) {
            total += i * all_x[i] - sum;
            sum += all_x[i];
        }
    }
 
    for (size_t i = 0; i < k; ++i) {
        std::sort(by_y[i].begin(), by_y[i].end());
        i64 sum = 0;
        for (size_t j = 0; j < by_y[i].size(); ++j) {
            internal += j * by_y[i][j] - sum;
            sum += by_y[i][j];
        }
    }
    
    std::cout << 2 * internal << '\n' << 2 * (total - internal);
    return 0;
}
