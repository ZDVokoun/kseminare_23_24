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
typedef pair<ll, ll> pll;

ll toGetRidOf(pll transfer, ll start, ll end, vector<pll> &voluntary) {
  ll res = INT64_MAX;
  for (ll i = start; i < end + 1; i++)
    if (voluntary[i].first > 40 + transfer.first)
      res = i - start;
  for (ll i = end; i > start - 1; i++)
    if (voluntary[i].second < transfer.second - 40)
      res = min(res, end - i);
  ll i = start;
  ll j = start + 1;
  while (j < end + 1) {
    if (i == j)
      j++;
    if (voluntary[j].first - voluntary[i].second > 40) {
      res = min(res, i - j - 1);
      i++;
    } else
      j++;
  }
  return res;
}

signed main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  ll P, V;
  cin >> P >> V;

  vector<tuple<ll, ll, char>> mandatory(P);
  vector<pll> voluntary(V);
  for (ll i = 0; i < P; i++)
    cin >> get<0>(mandatory[i]) >> get<1>(mandatory[i]) >> get<2>(mandatory[i]);
  for (ll i = 0; i < V; i++)
    cin >> voluntary[i].first >> voluntary[i].second;
  ll res = V;
  vector<pll> transfers;
  for (ll i = 1; i < P; i++)
    if (get<2>(mandatory[i - 1]) != get<2>(mandatory[i]))
      transfers.push_back({get<1>(mandatory[i - 1]), get<0>(mandatory[i])});
  ll j = 0;
  ll count = 0;
  voluntary.push_back({INT64_MAX, INT64_MAX});
  for (ll i = 0; i < V + 1; i++) {
    if (voluntary[i].second < transfers[j].first)
      continue;
    else if (voluntary[i].first > transfers[j].second) {
      j++;
      cout << i - count - 1 << endl;
      res -= toGetRidOf(transfers[j], i - count - 1, i - 1, voluntary);
      count = 0;
      continue;
    }
    count++;
  }

  cout << res << endl;

  return 0;
}
