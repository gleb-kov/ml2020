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
 
    size_t k, n;
    std::cin >> k >> n;
 
    std::vector<std::vector<i64>> by_x(k);
 
    for (size_t i = 0; i < n; ++i) {
        i64 q, w;
        std::cin >> q >> w;
        by_x[q - 1].push_back(w);
    }
 
    ld variance = 0.0;
    for (const auto &d : by_x) {
        size_t dn = d.size();
        if (dn == 0) continue;
        ld sum = 0.0, sq_sum = 0;
        for (long j : d) {
            sum += j;
            sq_sum += j * j;
        }
        sum /= dn;
        sq_sum /= dn;
        variance += dn * (sq_sum - sum * sum) / n;
    }
    std::cout << std::fixed << std::setprecision(10);
    std::cout << variance;
    return 0;
}
