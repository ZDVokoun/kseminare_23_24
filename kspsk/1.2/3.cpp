#include <bits/stdc++.h>
#define endl '\n'
#define nl '\n'

using namespace std;
typedef long long ll;
typedef vector<long long> vll;
typedef vector<int> vint;
typedef vector<bool> vbool;
typedef pair<int, int> pint;

void DFS(vector<string> &map, vector<vbool> &visited, vector<vint> &comp, int x,
         int y, int cur) {
  comp[y][x] = cur;
  int mx = 2 * x + 1;
  int my = 2 * y + 1;
  vector<pair<int, int>> neigh = {{1, 0}, {0, 1}, {-1, 0}, {0, -1}};
  for (auto n : neigh) {
    int dx = n.first, dy = n.second;
    if (map[my + dy][mx + dx] == '.' && !visited[y + dy][x + dx]) {
      visited[y + dy][x + dx] = true;
      DFS(map, visited, comp, x + dx, y + dy, cur);
    }
  }
}

signed main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  int n, m;
  cin >> n >> m;
  vector<string> map(2 * n + 1);
  getline(cin, map[0]);
  for (int i = 0; i < 2 * n + 1; i++)
    getline(cin, map[i]);
  vector<vbool> visited(n, vbool(m));
  vector<vint> comp(n, vint(m));
  int compName = 0;
  for (int y = 0; y < n; y++) {
    // cout << y << endl;
    for (int x = 0; x < m; x++)
      if (!visited[y][x]) {
        DFS(map, visited, comp, x, y, compName);
        compName++;
      }
  }
  if (compName == 1) {
    cout << n * m << endl;
    return 0;
  }
  vector<int> count(compName);
  for (int y = 0; y < n; y++)
    for (int x = 0; x < m; x++)
      count[comp[y][x]]++;
  vector<set<int>> graph(compName);
  for (int y = 0; y < n; y++)
    for (int x = 0; x < m; x++) {
      if (x - 1 >= 0 && comp[y][x - 1] != comp[y][x])
        graph[comp[y][x]].insert(comp[y][x - 1]);
      if (y - 1 >= 0 && comp[y - 1][x] != comp[y][x])
        graph[comp[y][x]].insert(comp[y - 1][x]);
      if (x + 1 < m && comp[y][x + 1] != comp[y][x])
        graph[comp[y][x]].insert(comp[y][x + 1]);
      if (y + 1 < n && comp[y + 1][x] != comp[y][x])
        graph[comp[y][x]].insert(comp[y + 1][x]);
    }
  ll res = 0;
  for (int u = 0; u < compName; u++) {
    for (int v : graph[u])
      if (count[u] + count[v] > res)
        res = count[u] + count[v];
  }
  cout << res << endl;

  return 0;
}
