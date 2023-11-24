#include <bits/stdc++.h>
#include <string>
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

  int m, n;
  cin >> n >> m;
  vector<string> map(n);
  if (m < 2 || n < 2) {
    cout << 0 << endl;
    return 0;
  }

  for (int i = 0; i < n; i++)
    cin >> map[i];
  // for (int i = 0; i < n; i++)
  //   cout << map[i] << endl;

  ll res = 0;
  for (int y = 0; y < n - 1; y++)
    for (int x = 0; x < m - 1; x++)
      if (map[y][x] == '/' && map[y][x + 1] == '\\' && map[y + 1][x] == '\\' &&
          map[y + 1][x + 1] == '/') {
        res++;
      }
  cout << res << endl;

  return 0;
}
