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

  ll M, N;
  cin >> M >> N;
  vll arr(N);
  for (ll i = 0; i < N; i++)
    cin >> arr[i];
  ll res = 1;
  ll cur = arr[0];
  for (ll i = 1; i < N; i++) {
    if (arr[i] - cur + 1 > M) {
      cur = arr[i];
      res++;
    }
  }
  cout << res << endl;

  return 0;
}
