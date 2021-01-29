#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <iomanip>
 
int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);
    
    using ld = long double;
    using i64 = int64_t;
 
    size_t n;
    std::cin >> n;
 
    std::vector<std::pair<i64, size_t>> a(n), b(n);
 
    for (size_t i = 0; i < n; ++i) {
        i64 q, w;
        std::cin >> q >> w;
        a[i] = {q, i};
        b[i] = {w, i};
    }
    if (n == 1) {
        std::cout << 0;
        return 0;
    }
 
    std::sort(a.begin(), a.end());
    std::sort(b.begin(), b.end());
 
    std::vector<i64> lhs(n), rhs(n);
 
    for (size_t i = 0; i < n; ++i) {
        lhs[a[i].second] = i;
        rhs[b[i].second] = i;
    }
 
    ld sq = 0.0;
    for (size_t i = 0; i < n; ++i) {
        sq += (lhs[i] - rhs[i]) * (lhs[i] - rhs[i]);
    }
    ld divisor = 1.0 * n * (1.0 * n * n - 1);
    ld spearman = 1 - 6.0 * sq / divisor;
    std::cout << std::fixed << std::setprecision(10);
    std::cout << spearman;
    return 0;
}
