#include <bits/stdc++.h>
#define endl '\n'
#define nl '\n'

using namespace std;
typedef long long ll;
typedef vector<long long> vll;
typedef vector<int> vint;
typedef vector<bool> vbool;
typedef pair<int, int> pint;
typedef pair<ll, ll> pll;

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
  ll res = 0;
  vector<pll> transfers;
  for (ll i = 1; i < P; i++)
    if (get<2>(mandatory[i - 1]) != get<2>(mandatory[i]))
      transfers.push_back({get<1>(mandatory[i - 1]), get<0>(mandatory[i])});

  cout << res << endl;

  return 0;
}
