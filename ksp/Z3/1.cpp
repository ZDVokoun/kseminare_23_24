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

  ll N, J;
  cin >> N >> J;
  ll res = INT64_MAX;
  for (ll i = 0; i < N; i++) {
    ll k, l;
    cin >> k >> l;
    res = min(res, k + J * l);
  }
  cout << res << nl;

  return 0;
}
