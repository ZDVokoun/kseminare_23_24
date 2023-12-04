#include <bits/stdc++.h>
#include <cstdint>
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

  ll Q, P;
  cin >> Q >> P;
  map<int, list<pint>> graph;
  vector<ll> customers;
  ll W = INT64_MAX, C = 0;
  for (int i = 0; i < P; i++) {
    ll t;
    char com;
    cin >> t >> com;
    if (com == 'N') {
      customers.push_back(t);
    } else if (com == 'P') {
      ll j, k;
      cin >> j >> k;
      graph[j].push_back({k, t});
    } else if (com == 'V') {
      ll j;
      cin >> j;
      graph[j].push_back({-1, t});
    }
  }
  for (ll start : customers) {
    if (start == 0)
      continue;
    int v = 0;
    ll t = start;
    while (v != -1 && graph[v].size() != 0) {
      t = graph[v].front().second;
      int tempV = graph[v].front().first;
      graph[v].pop_front();
      v = tempV;
    }
    if (v == -1 && t - start + 2 < W) {
      W = t - start + 2;
      C = start - 1;
    }
  }
  cout << W << " " << C << endl;

  return 0;
}
