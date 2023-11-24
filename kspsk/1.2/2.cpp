#include <bits/stdc++.h>
#include <unordered_map>
#define endl '\n'
#define nl '\n'

using namespace std;
typedef long long ll;
typedef vector<long long> vll;
typedef vector<int> vint;
typedef vector<bool> vbool;
typedef pair<int, int> pint;

signed main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  ll t;
  cin >> t;
  for (ll i = 0; i < t; i++) {
    unordered_map<char, int> signs;
    vector<int> numbers;
    string in;
    cin >> in;
    for (char ch : in) {
      auto it = signs.find(ch);
      if (it == signs.end()) {
        if (signs.size() == 0)
          signs[ch] = 1;
        else if (signs.size() == 1)
          signs[ch] = 0;
        else
          signs[ch] = signs.size();
      }
    }
    ll res = 0;
    ll power = 1;
    ll base = signs.size();
    if (base == 1)
      base++;
    for (int i = in.size() - 1; i >= 0; i--) {
      // cout << power << endl;
      res += power * signs[in[i]];
      power *= base;
    }
    cout << res << endl;
  }

  return 0;
}
