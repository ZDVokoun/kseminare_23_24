#include <bits/stdc++.h>

#define endl '\n'
#define nl '\n'

using namespace std;

typedef long long ll;

void DFSUtil(vector<vector<int>> &g, vector<bool> &vis, int &lastV, int v) {
  lastV = v;
  for (int ch : g[v])
    if (!vis[ch]) {
      vis[ch] = true;
      DFSUtil(g, vis, lastV, ch);
    }
}

int main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  int n, k, p;
  cin >> n >> k >> p;

  vector<vector<int>> g(n);
  for (int i = 0; i < p; i++) {
    int x, y;
    cin >> x >> y;
    g[x].push_back(y);
    g[y].push_back(x);
  }
  vector<bool> vis(n);
  vis[0] = true;
  int lastV = 0;
  DFSUtil(g, vis, lastV, 0);
  vector<pair<int, int>> res;
  for (int v = 1; v < n; v++) {
    if (!vis[v] && g[v].size() < k && g[lastV].size() < k) {
      vis[v] = true;
      res.push_back({lastV, v});
      DFSUtil(g, vis, lastV, v);
    }
  }
  if (any_of(vis.begin(), vis.end(), [](bool b) { return !b; })) {
    cout << -1 << endl;
    return 0;
  }
  cout << res.size() << endl;
  for (auto e : res)
    cout << e.first << " " << e.second << endl;

  return 0;
}
