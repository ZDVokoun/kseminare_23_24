#include <algorithm>
#include <bits/stdc++.h>
#define endl '\n'
#define nl '\n'

using namespace std;
typedef long long ll;
typedef vector<long long> vll;
typedef vector<int> vint;
typedef vector<bool> vbool;
typedef pair<int, int> pint;

int DFS(vector<vll> &map, vector<vint> &result, int n, int m, int x, int y,
        int curN) {
  if (result[y][x] != 0)
    return result[y][x];
  ll min = map[y][x];
  int fx = -1, fy = -1;
  if (y - 1 >= 0 && min > map[y - 1][x]) {
    fx = x;
    fy = y - 1;
    min = map[fy][fx];
  }
  if (x - 1 >= 0 && min > map[y][x - 1]) {
    fx = x - 1;
    fy = y;
    min = map[fy][fx];
  }
  if (y + 1 < n && min > map[y + 1][x]) {
    fx = x;
    fy = y + 1;
    min = map[fy][fx];
  }
  if (x + 1 < m && min > map[y][x + 1]) {
    fx = x + 1;
    fy = y;
    min = map[fy][fx];
  }
  if (fx != -1) {
    int name = DFS(map, result, n, m, fx, fy, curN);
    result[y][x] = name;
    return name;
  } else {
    result[y][x] = curN;
    return curN;
  }
}

signed main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  int n, m;
  cin >> n >> m;
  vector<vll> map(n, vll(m));
  for (int y = 0; y < n; y++)
    for (int x = 0; x < m; x++) {
      ll cur;
      cin >> cur;
      map[y][x] = cur;
    }

  vector<vint> result(n, vint(m));
  int curN = 1;
  for (int y = 0; y < n; y++)
    for (int x = 0; x < m; x++) {
      int name = DFS(map, result, n, m, x, y, curN);
      if (name == curN)
        curN++;
    }
  for (int y = 0; y < n; y++) {
    for (int x = 0; x < m; x++) {
      cout << result[y][x];
      if (x < m - 1)
        cout << " ";
    }
    cout << endl;
  }

  return 0;
}
