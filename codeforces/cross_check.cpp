#include <iostream>
#include <vector>
#include <cassert>
#include <iomanip>
#include <unordered_map>

using ui32 = uint32_t;

int main() {
    size_t n, m, k;
    std::cin >> n >> m >> k;

    std::unordered_map<size_t, std::vector<size_t>> classes;

    for (size_t i = 1; i <= n; i++) {
        size_t q;
        std::cin >> q;
        classes[q].push_back(i);
    }
    size_t p = 0;
    std::vector<std::vector<size_t>> parts(k);

    for (auto it = classes.begin(); it != classes.end(); it++) {
        for (size_t item : it->second) {
            parts[p].push_back(item);
            p = (p+1)%k;
        }
    }
    for (size_t i = 0; i < k; i++) {
        std::cout << parts[i].size() << ' ';
        for (size_t q : parts[i]) std::cout << q << ' ';
        std::cout << std::endl;
    }
    return 0;
}