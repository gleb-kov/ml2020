#include <iostream>
#include <vector>
#include <cmath>
#include <unordered_map>
#include <algorithm>
 
using ld = long double;
 
struct Item {
    std::vector<int64_t> x;
    size_t y;
};
 
using Dataset = std::vector<Item>;
 
struct Node {
    size_t id = 0;
    size_t f_or_d = 0;
    ld b = 0.0; // TODO: pack to front
 
    Node *left = nullptr;
    Node *right = nullptr;
    // packed
    char type = 'C';
};
 
class PrettyPrinter {
private:
    size_t node_id = 0;
    Node *root_;
 
private:
    void Numerate(Node *root) {
        if (root == nullptr) return;
        root->id = ++node_id;
        Numerate(root->left);
        Numerate(root->right);
    }
 
    static void Print(std::ostream &s, Node *n) {
        if (n == nullptr) return;
        if (n->type == 'C') {
            s << "C " << n->f_or_d;
        } else {
            s << "Q " << n->f_or_d << ' ' << n->b << ' '
              << n->left->id << ' ' << n->right->id;
        }
        s << '\n';
        Print(s, n->left);
        Print(s, n->right);
    }
 
public:
    explicit PrettyPrinter(Node *root) : root_(root) {
        Numerate(root_);
    }
 
    void Print(std::ostream &s) const {
        s << node_id << std::endl;
        Print(s, root_);
    }
};
 
std::ostream &operator<<(std::ostream &s, const PrettyPrinter &pp) {
    pp.Print(s);
    return s;
}
 
///////////////////////////////////////////////////////////////////////////////
 
class DecisionTree {
private:
    using ptr = Node *;
 
    size_t features;
    size_t max_depth;
    size_t class_cnt;
 
private:
    [[nodiscard]] static bool IsSameClass(const Dataset &ds) {
        for (size_t i = 1; i < ds.size(); ++i) {
            if (ds[i].y != ds[i - 1].y) {
                return false;
            }
        }
        return true;
    }
 
    [[nodiscard]] static size_t MostFrequentClass(const Dataset &ds) {
        std::unordered_map<size_t, size_t> cnt;
        for (const auto &elem : ds) {
            cnt[elem.y]++;
        }
        size_t best = 0, best_cnt = 0;
        for (auto &it : cnt) {
            if (it.second > best_cnt) {
                best = it.first;
                best_cnt = it.second;
            }
        }
        return best;
    }
 
    [[nodiscard]] std::pair<ld, ld> Split(Dataset ds, size_t x_idx) const {
        // TODO: stable_sort is faster
        std::sort(ds.begin(), ds.end(),
                  [x_idx](const Item &lhs, const Item &rhs) { return lhs.x[x_idx] < rhs.x[x_idx]; });
 
        std::vector<size_t> leftPart(class_cnt + 1), rightPart(class_cnt + 1);
        for (const Item &t : ds) {
            ++rightPart[t.y];
        }
 
        // TODO: ugly
        ld full_score = CountScore(rightPart, ds.size());
        ld best_score = -100000000;
        ld x_border = 0, prev_x_border = ds[0].x[x_idx];
 
        for (size_t i = 0; i < ds.size(); ++i) {
            ld x = ds[i].x[x_idx];
            // TODO: shitty cmp
            if (x != prev_x_border) {
                ld p = 1.0 * i / ds.size();
                // TODO: recalc in O(1)
                ld l = CountScore(leftPart, i);
                ld r = CountScore(rightPart, ds.size() - i);
                ld score = full_score - p * l - (1.0 - p) * r;
                if (score > best_score) {
                    best_score = score;
                    x_border = x + prev_x_border;
                }
                prev_x_border = x;
            }
            ++leftPart[ds[i].y];
            --rightPart[ds[i].y];
        }
 
        return {best_score, x_border / 2};
    }
 
    [[nodiscard]] ptr TrainImpl(const Dataset &ds, size_t depth) {
        if (depth >= max_depth || IsSameClass(ds)) {
            // TODO: ugly
            Node *leaf = new Node{};
            leaf->f_or_d = MostFrequentClass(ds);
            leaf->type = 'C';
            return leaf;
        }
        // TODO: ugly
        ld best_score = -100000000;
        size_t x_idx = 0;
        ld delimiter = 0;
 
        for (size_t i = 0; i < features; ++i) {
            auto spl = Split(ds, i);
            if (spl.first > best_score) {
                best_score = spl.first;
                x_idx = i;
                delimiter = spl.second;
            }
        }
 
        // TODO: ugly
        Dataset lhs, rhs;
        for (const auto &d : ds) {
            if (d.x[x_idx] < delimiter) {
                lhs.push_back(d);
            } else {
                rhs.push_back(d);
            }
        }
 
        ptr left = TrainImpl(lhs, depth + 1);
        ptr right = TrainImpl(rhs, depth + 1);
        return new Node{0, x_idx + 1, delimiter, left, right, 'Q'};
    }
 
    [[nodiscard]] static ld CountScore(const std::vector<size_t> &freq, size_t size) {
        ld result = 0;
        // TODO: ugly
        for (size_t f : freq) {
            if (f == 0) continue;
            ld p = 1.0 * f / size;
            ld pr = 1.0 * size / f;
            result += p * log(pr);
        }
        return result;
    }
 
public:
    explicit DecisionTree(size_t features, size_t max_depth, size_t class_cnt)
            : features(features), max_depth(max_depth), class_cnt(class_cnt) {}
 
    [[nodiscard]] ptr Train(const Dataset &ds) {
        return TrainImpl(ds, 0);
    }
};
 
int main() {
    size_t m, k, h;
    std::cin >> m >> k >> h;
    size_t n;
    std::cin >> n;
 
    Dataset input(n);
    for (size_t i = 0; i < n; ++i) {
        input[i].x.resize(m);
        for (size_t j = 0; j < m; ++j) {
            std::cin >> input[i].x[j];
        }
        std::cin >> input[i].y;
    }
 
    Node *root = DecisionTree(m, h, k).Train(input);
    std::cout << PrettyPrinter(root);
    return 0;
}
