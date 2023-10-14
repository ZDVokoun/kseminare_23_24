#include <bits/stdc++.h>
#define endl '\n'
#define nl '\n'

using namespace std;
typedef long long ll;
typedef vector<long long> vll;
typedef vector<int> vint;
typedef vector<bool> vbool;
typedef pair<int, int> pint;

struct {
  map<ll, int> color_count;
  map<int, set<ll>> count_color;
  int len = 0;

  void increase(ll n) {
    int n_count = color_count[n];
    count_color[n_count + 1].insert(n);
    count_color[n_count].erase(n);
    color_count[n]++;
    len++;
  }
  void decrease(ll n) {
    int n_count = color_count[n];
    count_color[n_count - 1].insert(n);
    count_color[n_count].erase(n);
    color_count[n]--;
    len--;
  }
  pair<ll, int> getMax() {
    auto it = count_color.rbegin();
    return make_pair(*(it->second.begin()), it->first);
  }
} Counter;

signed main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  int t, n, d;
  cin >> t >> n >> d;
  vll f(n);
  for (int i = 0; i < n; i++)
    cin >> f[i];
  int max_len = 0;
  pair<ll, int> max_res = {0, 0};
  pint max_ij = {0, 0};

  int i = 0, j = 0;
  auto cur = Counter.getMax();
  while (i < n) {
    Counter.increase(f[i]);
    cur = Counter.getMax();
    while (Counter.len - cur.second > d) {
      Counter.decrease(f[j]);
      j++;
      cur = Counter.getMax();
    }
    if (max_len < Counter.len) {
      max_len = Counter.len;
      max_res = Counter.getMax();
      max_ij = {i, j};
    }
    i++;
  }

  int k = 0;
  for (int i = max_ij.second; i <= max_ij.first; i++)
    if (f[i] != max_res.first)
      k++;
  if (max_len == n && d == 1 && k == 0) {
    cout << max_len - 1 << endl;
    if (t == 2) {
      if (f[0] == 0)
        cout << n - 1 << " " << 1 << endl;
      else
        cout << n - 1 << " " << 0 << endl;
    }
    return 0;
  }
  cout << max_len << endl;
  if (t == 1)
    return 0;
  for (int i = max_ij.second; i <= max_ij.first; i++)
    if (f[i] != max_res.first)
      cout << i << " " << max_res.first << endl;

  if (d > k) {
    ll startColor = max_res.first + 1;
    if (startColor + 2 > 10e9 - 1)
      startColor = 0;
    int toEnd = d - k;
    if (toEnd % 2 == 1) {
      cout << n - 1 << " " << startColor << endl;
      startColor++;
      toEnd--;
    }
    while (toEnd > 0) {
      cout << n - 1 << " " << startColor << endl;
      cout << n - 1 << " " << max_res.first << endl;
      toEnd -= 2;
    }
  }

  return 0;
}
