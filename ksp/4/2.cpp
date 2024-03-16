#include <bits/stdc++.h>
#define endl '\n'
#define nl '\n'
#define MOD 1000000007

using namespace std;
typedef long long ll;
typedef vector<long long> vll;
typedef vector<int> vint;
typedef vector<bool> vbool;
typedef pair<int, int> pint;

signed main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  int N, K;
  cin >> N >> K;
  map<ll, ll> cnt;

  ll cur;
  for (int i = 0; i < N; i++) {
    cin >> cur;
    cnt[cur]++;
  }

  vector<vector<ll>> table(cnt.size(), vector<ll>(K + 1));

  int i = 0;
  for (auto p : cnt) {
    table[i][0] = p.second;
    i++;
  }

  ll start = 1;
  for (int k = 1; k <= K; k++) {
    table[k - 1][k] = start * table[k - 1][0] % MOD;
    start = table[k - 1][k];
  }

  for (int i = 1; i < cnt.size(); i++)
    table[i][1] = (table[i - 1][1] + table[i][0]) % MOD;

  for (int k = 2; k <= K; k++) {
    for (int i = k; i < cnt.size(); i++) {
      table[i][k] =
          (table[i - 1][k] + (table[i][0] * table[i - 1][k - 1]) % MOD) % MOD;
    }
  }
  cout << table[cnt.size() - 1][K] << endl;

  return 0;
}
