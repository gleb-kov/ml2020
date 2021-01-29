#include <iostream>
#include <vector>
#include <cassert>
#include <iomanip>

using ui32 = uint32_t;

template<typename T>
class matrix {
    std::vector<std::vector<T>> m;

public:
    matrix(size_t h, size_t w, T val = 0) : m(h, std::vector<T>(w, val)) {
        assert(h > 0);
        assert(w > 0);
    }

    matrix(const matrix<T> &) = default;

    matrix &operator=(const matrix &) = default;

    size_t height() const {
        return m.size();
    }

    size_t width() const {
        return m[0].size();
    }

    bool is_square() const {
        return m.size() == m[0].size();
    }

    void fill(T val) {
        for (size_t i = 0; i < height(); i++) {
            for (size_t j = 0; j < width(); j++) {
                m[i][j] = val;
            }
        }
    }

    std::vector<T> const &operator[](size_t ind) const {
        assert(ind < height());
        return m[ind];
    }

    std::vector<T> &operator[](size_t ind) {
        assert(ind < height());
        return m[ind];
    }

    friend std::istream &operator>>(std::istream &s, matrix<T> &rhs) {
        for (size_t i = 0; i < rhs.height(); i++) {
            for (size_t j = 0; j < rhs.width(); j++) {
                s >> rhs.m[i][j];
            }
        }
        return s;
    }

    friend std::ostream &operator<<(std::ostream &s, matrix const &rhs) {
        for (size_t i = 0; i < rhs.height(); i++) {
            for (size_t j = 0; j < rhs.width(); j++) {
                s << rhs.m[i][j] << ' ';
            }
            s << '\n';
        }
        return s;
    }
};

template<typename T>
class confusion_matrix {
    matrix<T> m;
    std::vector<T> TP; // true positive
    std::vector<T> FP; // false positive
    std::vector<T> FN; // false negative
    std::vector<T> TN; // true negative
    double all;
    size_t c;

private:
    void fill() {
        all = 0;
        for (size_t i = 0; i < c; i++) {
            for (size_t j = 0; j < c; j++) {
                all += m[i][j];
            }
        }
        fillTP();
        fillFP();
        fillFN();
        fillTN();
    }

    void fillTP() {
        TP.resize(c, 0);
        for (size_t i = 0; i < c; i++) {
            TP[i] = m[i][i];
        }
    }

    void fillFP() {
        FP.resize(c, 0);
        for (size_t i = 0; i < c; i++) {
            for (size_t j = 0; j < c; j++) {
                if (i != j) FP[j] += m[i][j];
            }
        }
    }

    void fillFN() {
        FN.resize(c, 0);
        for (size_t i = 0; i < c; i++) {
            for (size_t j = 0; j < c; j++) {
                if (i != j) FN[i] += m[i][j];
            }
        }
    }

    void fillTN() {
        TN.resize(c, 0);
        for (size_t i = 0; i < c; i++) {
            TN[i] = all - TP[i] - FP[i] - FN[i];
        }
    }

public:
    explicit confusion_matrix(const matrix<T> &rhs) : m(rhs), all(0), c(rhs.width()) {
        assert(m.is_square());
        fill();
    }

    std::pair<double, double> calc_score() {
        double micro_f = 0.0;
        double macro_f = 0.0;
        double recall_w = 0.0;
        double prec_w = 0.0;
        for (size_t i = 0; i < c; i++) {
            if (TP[i] == 0) continue;

            double cc = TP[i] + FN[i];
            double recall_i = TP[i] / cc;
            double prec_i = TP[i] / double(TP[i] + FP[i]);
            double f1 = 2.0 * recall_i * prec_i / (recall_i + prec_i);

            micro_f += f1 * cc / all;
            recall_w += double(TP[i]) / all;
            prec_w += prec_i * cc / all;
        }

        macro_f = 2.0 * prec_w * recall_w / (prec_w + recall_w);
        return {macro_f, micro_f};
    }
};

int main() {
    size_t k;
    std::cin >> k;
    matrix<ui32> m(k, k, 0);
    std::cin >> m;
    confusion_matrix cm(m);
    auto score = cm.calc_score();
    std::cout << std::fixed << std::setprecision(10);
    std::cout << score.first << std::endl << score.second;
    return 0;
}