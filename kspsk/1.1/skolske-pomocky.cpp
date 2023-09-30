#include <bits/stdc++.h>
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

  ll t, n, m;
  cin >> t >> n >> m;
  vector<vector<pint>> items(t);
  for (int i = 0; i < n; i++) {
    ll ti, c, k;
    cin >> ti >> c >> k;
    items[ti - 1].push_back({c, k});
  }
  for (int i = 0; i < t; i++) {
    sort(items[i].begin(), items[i].end());
  }
  // {k, c, t}
  set<tuple<ll, ll, ll>> bestItems;
  vint indexes(t);
  ll cost = 0;
  for (int i = 0; i < t; i++) {
    if (items[i].size() == 0) {
      cout << 0 << nl;
      return 0;
    }

    bestItems.insert({items[i][0].second, items[i][0].first, i});
    cost += items[i][0].first;
  }
  if (cost > m) {
    cout << 0 << endl;
    return 0;
  }
  while (true) {
    auto worst = *bestItems.begin();
    ll k = get<0>(worst);
    ll c = get<1>(worst);
    ll ti = get<2>(worst);
    bestItems.erase(bestItems.begin());
    cost -= c;
    while (items[ti][indexes[ti]].second <= k) {
      indexes[ti]++;
      if (indexes[ti] >= items[ti].size()) {
        cout << k << endl;
        return 0;
      }
    }
    pint newItem = items[ti][indexes[ti]];
    bestItems.insert({newItem.second, newItem.first, ti});
    cost += newItem.first;
    if (cost > m) {
      cout << k << endl;
      return 0;
    }
  }

  return 0;
}
