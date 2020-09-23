#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <functional>

namespace NParserCSV {
    void skipDelimiter(std::stringstream &ss, const std::string &delimiter) {
        size_t num = delimiter.size();
        while (!ss.eof() && num > 0) {
            char skip;
            ss >> skip;
            num--;
            if (ss.tellg() == -1) {
                return;
            }
        }
    }

    template<typename T>
    std::vector<T> parse_csv_line(const std::string &inp, const std::string &delimiter) {
        std::vector<T> result;
        std::stringstream ss(inp);
        while (ss) {
            T cur;
            ss >> cur;
            result.push_back(cur);
            skipDelimiter(ss, delimiter);
            if (ss.tellg() == -1) {
                break;
            }
        }
        return result;
    }

    template<typename T>
    std::vector<std::vector<T>>
    parse_csv(std::istream &fin, const std::string &delimiter = ",", bool skipHeader = true) {
        std::vector<std::vector<T>> data;
        std::string str;
        if (skipHeader) {
            std::getline(fin, str);
        }
        while (std::getline(fin, str)) {
            data.emplace_back(parse_csv_line<T>(str, delimiter));
        }
        return data;
    }
}

/*namespace NDatasetNormalize {
    template<typename T>
    std::vector<std::pair<T, T>> min_max(const std::vector<std::vector<T>> &data) {
        if (data[0].size() < 2) return {};

        std::vector<std::pair<T, T>> result(data[0].size() - 1);
        for (size_t i = 0; i + 1 < data[0].size(); i++) {
            result[i] = {data[0][i], data[0][i]};
            for (size_t j = 0; j < data.size(); j++) {
                result[i].first = std::min(result[i].first, data[j][i]);
                result[i].second = std::max(result[i].second, data[j][i]);
            }
        }

        return result;
    }

    template<typename T>
    std::vector<std::vector<long double>> normalize(const std::vector<std::vector<T>> &data,
                                                    const std::vector<std::pair<T, T>> &minmax) {
        std::vector<std::vector<long double>> result;

        for (auto &row : data) {
            result.emplace_back();
            for (size_t i = 0; i + 1 < row.size(); i++) {
                result.back().push_back((row[i] * 1.0 - minmax[i].first)
                                 / (minmax[i].second * 1.0 - minmax[i].first));
            }
        }
        return result;
    }
}*/

template<typename T>
void print(const std::vector<std::vector<T>> &data) {
    for (auto &v : data) {
        for (const T &elem : v) {
            std::cout << elem << ' ';
        }
        std::cout << '\n';
    }
}

template<typename T>
void print(const std::vector<std::pair<T, T>> &data) {
    for (auto &v : data) {
        std::cout << v.first << ' ' << v.second << '\n';
    }
}

int main() {
    std::ifstream fin("heart-switzerland.csv");
    auto res = NParserCSV::parse_csv<double>(fin);
    //print(res);
    //auto minmax = NDatasetNormalize::min_max(res);
    //print(minmax);
    //auto normalized = NDatasetNormalize::normalize(res, minmax);
    //print(normalized);
    //auto target = NDatasetNormalize::normalize<double>({{5.0, 3.4, 1.6, 0.7}}, minmax);
    //print(target);
    return 0;
}
