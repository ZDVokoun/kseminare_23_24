#include <bits/stdc++.h>
#define endl '\n'
#define nl '\n'

using namespace std;
typedef long long ll;
typedef vector<long long> vll;
typedef vector<int> vint;

int getLog(ll n) {
  int res = 0;
  while ((n >> res) > 1)
    res++;
  return res;
}

signed main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  int n;
  vint moc(64);
  cin >> n;
  ll cur = 0;
  for (int i = 0; i < n; i++) {
    cin >> cur;
    moc[getLog(cur)]++;
  }
  ll res = 0;
  for (int i : moc)
    res += i * (i - 1) / 2;
  cout << res << endl;

  return 0;
}
