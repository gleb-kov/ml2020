#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>
 
int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);
    
    using ld = long double;
    size_t n;
    std::cin >> n;
    std::vector<int64_t> a(n), b(n);
 
    int64_t a_avg = 0, b_avg = 0;
 
    for (size_t i = 0; i < n; ++i) {
        std::cin >> a[i] >> b[i];
        a_avg += a[i];
        b_avg += b[i];
    }
    a_avg /= n, b_avg /= n;
 
    int64_t psum = 0, asq = 0, bsq = 0;
 
    for (size_t i = 0; i < n; ++i) {
        asq += (a[i] - a_avg) * (a[i] - a_avg);
        bsq += (b[i] - b_avg) * (b[i] - b_avg);
        psum += (a[i] - a_avg) * (b[i] - b_avg);
    }
    ld sq = 1.0 * asq * bsq;
    sq = (sq <= 0 ? 0.0 : psum / sqrtl(sq));
    std::cout << std::fixed << std::setprecision(10) << sq;
    return 0;
}
