#include <bits/stdc++.h>
#define endl '\n'
#define nl '\n'

using namespace std;
typedef long long ll;
typedef vector<long long> vll;
typedef vector<int> vint;
typedef vector<bool> vbool;
typedef pair<int, int> pint;

vector<pint> neigh(int x, int y, int R, int S) {
  vector<pint> res;
  vector<pint> rneigh = {{1, 0}, {0, 1}, {-1, 0}, {0, -1}};
  for (pint d : rneigh) {
    if (0 > x + d.first || S <= x + d.first || 0 > y + d.second ||
        R <= y + d.second)
      continue;
    else
      res.push_back({x + d.first, y + d.second});
  }
  return res;
}

int BFSCount(vector<string> &tab, pint start) {
  if (tab[start.second][start.first] == '#')
    return 0;
  int count = 0;
  queue<pint> q;
  vector<vbool> visited(tab.size(), vbool(tab[0].size()));
  q.push(start);
  visited[start.second][start.first] = true;
  pint cur;
  while (!q.empty()) {
    cur = q.front();
    q.pop();
    visited[cur.second][cur.first] = true;
    if (tab[cur.second][cur.first] == 'M')
      count++;
    for (pint n : neigh(cur.first, cur.second, tab.size(), tab[0].size())) {
      if (!visited[n.second][n.first] && tab[n.second][n.first] != '#') {
        visited[n.second][n.first] = true;
        q.push(n);
      }
    }
  }
  return count;
}

signed main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  int n, m;
  cin >> n >> m;
  vector<string> tab(n);
  for (int y = 0; y < n; y++)
    cin >> tab[y];

  for (int y = 0; y < n; y++)
    for (int x = 0; x < m; x++)
      if (tab[y][x] == 'F') {
        for (pint n : neigh(x, y, n, m))
          if (tab[n.second][n.first] == 'M') {
            cout << "Neda sa" << endl;
            return 0;
          } else if (tab[n.second][n.first] == 'F')
            continue;
          else {
            tab[n.second][n.first] = '#';
          }
      }

  int matfyz = 0;
  for (int y = 0; y < n; y++)
    for (int x = 0; x < m; x++)
      if (tab[y][x] == 'M')
        matfyz++;
  int availableMatfyz = BFSCount(tab, {m - 1, n - 1});
  if (matfyz != availableMatfyz) {
    cout << "Neda sa" << endl;
    return 0;
  }

  cout << "Plan uspesny" << nl;
  for (string row : tab)
    cout << row << nl;

  return 0;
}
