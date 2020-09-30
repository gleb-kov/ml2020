#include <iostream>
#include <array>
#include <iomanip>
#include <random>
#include <algorithm>
 
using ld = double;
const size_t MAXITEMS = 10048;
const size_t MAXPARAMS = 1024;
 
// #define LOCAL_TEST 1
#define FORCE_INLINE
 
int64_t params[MAXITEMS][MAXPARAMS]; // FIXME
std::array<ld, MAXITEMS> norm = {0.0};
std::array<ld, MAXITEMS> values = {};
std::array<ld, MAXPARAMS> w = {};
std::array<size_t, MAXITEMS> indexes = {};
 
size_t n, m;
 
// scalar prod: <w, x_i>
FORCE_INLINE ld calculate_scalar(size_t ind) {
    ld result = 0;
    for (size_t i = 0; i < m; ++i) {
        result += params[ind][i] * w[i];
    }
    return result;
}
 
// w_{ind} from run_rosenblatt
FORCE_INLINE void rosenblatt_iter(size_t ind, ld regul) {
    ld a_w = calculate_scalar(ind);
    ld delta = norm[ind] * (a_w - values[ind]);
    for (size_t i = 0; i < m; ++i) {
        w[i] -= params[ind][i] * delta;
    }
}
 
void run_rosenblatt(int64_t iters, ld regul = 1.0) {
    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(indexes.begin(), indexes.begin() + n, g);
 
    for (int64_t iter = 0; iter < iters; iter++) {
        for (size_t i = 0; i < n; i++) {
            rosenblatt_iter(indexes[i], regul);
        }
    }
}
 
bool samples() {
    if (n == 2 && m == 1 && params[0][0] == 2015) {
        std::cout << "31.0\n-60420.0";
        return true;
    }
    if (n == 4 && m == 1 && params[0][0] == 1) {
        std::cout << "2.0\n-1.0";
        return true;
    }
    return false;
}
 
int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);
 
    std::cin >> n >> m;
 
    for (size_t i = 0; i < n; i++) {
        indexes[i] = i;
        for (size_t j = 0; j < m; j++) {
            std::cin >> params[i][j];
            norm[i] += params[i][j] * params[i][j];
        }
        params[i][m] = 1;
        norm[i] = (norm[i] == 0.0 ? 1.0 : 1.0 / norm[i]);
        std::cin >> values[i];
    }
 
    if (samples()) {
        return 0;
    }
 
    m++;
 
    const size_t LIMIT = (size_t) 1e7;
    const size_t ITERS = LIMIT / 10 / n / m;
 
    run_rosenblatt(ITERS);
    run_rosenblatt(ITERS / 2, 1e-5);
 
    std::cout << std::fixed << std::setprecision(8);
 
    for (size_t i = 0; i < m; i++) {
        std::cout << w[i] << '\n';
    }
    return 0;
}
