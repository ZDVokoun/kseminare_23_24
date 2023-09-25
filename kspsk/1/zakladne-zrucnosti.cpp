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

  int n;
  cin >> n;
  if (n < 3) {
    cout << 0 << endl;
    return 0;
  }
  vint a(n);
  int m = 0, m2nd = 0;
  int cur = 0;
  for (int i = 0; i < n; i++) {
    cin >> cur;
    if (cur >= m) {
      m2nd = m;
      m = cur;
    } else if (cur > m2nd)
      m2nd = cur;
  }
  cout << min(m2nd - 1, n - 2) << endl;

  return 0;
}
