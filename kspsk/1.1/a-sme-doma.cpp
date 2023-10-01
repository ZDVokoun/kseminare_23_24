#include <bits/stdc++.h>
#define endl '\n'
#define nl '\n'

using namespace std;
typedef long long ll;
typedef vector<long long> vll;
typedef vector<int> vint;

signed main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  ll z = 0, k = 0, p = 0;
  cin >> z >> k >> p;
  vll a(p + 2);
  a[0] = z - 1;
  a[p + 1] = k + 1;
  for (ll i = 0; i < p; i++)
    cin >> a[i + 1];
  sort(a.begin(), a.end());
  ll m = 0;
  for (ll i = 0; i < p + 1; i++)
    m = max(m, abs(a[i + 1] - a[i] - 1));
  cout << m << nl;

  return 0;
}
