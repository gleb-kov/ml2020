#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <iomanip>
 
using namespace std;
using ll = int64_t;
using ld = long double;
 
vector<ll> class_size;
vector<unordered_map<string, ll>> texts_with_word;
unordered_set<string> all_words;
 
ld a;
ll numb;
 
ld pr(ll c) {
    return class_size[c] * 1.0 / numb;
}
 
ld pr(const string &s, ll c) {
    ll cnt = 0;
    auto it = texts_with_word[c].find(s);
    if (it != texts_with_word[c].end()) {
        cnt = it->second;
    }
    return (1.0 * cnt + a) / (class_size[c] + 2.0 * a);
}
 
ld adjusted(const string &s, ll c) {
    ld p = pr(s, c);
    return p / (1.0 - p);
}
 
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    ll k;
    cin >> k;
 
    vector<ll> lambda(k);
    texts_with_word.resize(k);
    class_size.resize(k, 0);
 
    for (ll i = 0; i < k; ++i) {
        cin >> lambda[i];
    }
    cin >> a >> numb;

    for (ll i = 0; i < numb; i++) {
        ll c, cnt;
        cin >> c >> cnt;
        --c;
        class_size[c]++;
 
 
        unordered_set<string> msg;
        for (ll j = 0; j < cnt; j++) {
            string s;
            cin >> s;
            if (msg.find(s) != msg.end()) continue;
            msg.insert(s);
            texts_with_word[c][s]++;
            all_words.insert(s);
        }
    }
 
    vector<ld> negated_table(k, 1.0);
 
    for (ll i = 0; i < k; i++) {
        negated_table[i] = pr(i);
        for (const string &s : all_words) {
            long double p = pr(s, i);
            negated_table[i] *= (1.0 - p);
        }
    }
 
    ll m;
    cin >> m;

    for (ll i = 0; i < m; i++) {
        ll cnt;
        cin >> cnt;
 
        unordered_set<string> was_in_msg;
 
        vector<ld> results(k);
        for (ll cl_index = 0; cl_index < k; cl_index++) {
            results[cl_index] = lambda[cl_index] * negated_table[cl_index];
        }
 
        for (ll j = 0; j < cnt; j++) {
            string s;
            cin >> s;
            if (was_in_msg.find(s) != was_in_msg.end()) continue;
            if (all_words.find(s) == all_words.end()) continue;
            was_in_msg.insert(s);
 
            for (ll cl_index = 0; cl_index < k; cl_index++) {
                results[cl_index] *= adjusted(s, cl_index);
            }
        }
        ld sum = 0;
        for (ll cl_index = 0; cl_index < k; cl_index++) {
            sum += results[cl_index];
        }
        /*for (ll cl_index = 0; cl_index < k; cl_index++) {
            cout << fixed << setprecision(10) << results[cl_index] / sum << ' ';
        }*/
        ll best_class = 0;
        for (ll cl_index = 0; cl_index < k; cl_index++) {
            if (results[cl_index] > results[best_class]) {
                best_class = cl_index;
            }
        }
        std::cout << best_class + 1 << '\n'; // DIFF: decide best class inplace by argmax
        // cout << '\n';
    }
    return 0;
}

