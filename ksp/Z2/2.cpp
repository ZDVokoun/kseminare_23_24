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

  ll R, S, x, y;
  cin >> R >> S >> x >> y;
  vector<string> map(R);
  for (int m = 0; m < R; m++)
    cin >> map[m];
  while (true) {
    if (map[y][x] == '>') {
      if (x == S - 1)
        break;
      x++;
    }
    if (map[y][x] == '^') {
      if (y == 0)
        break;
      y--;
    }
    if (map[y][x] == '<') {
      if (x == 0)
        break;
      x--;
    }
    if (map[y][x] == 'v') {
      if (y == R - 1)
        break;
      y++;
    }
  }
  cout << x << " " << y << endl;

  return 0;
}
