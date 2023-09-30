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

void findPeaks(vector<vint> &tab, vector<vbool> &visited, vector<pint> &res,
               int x, int y) {
  visited[y][x] = true;
  bool isPeak = true;
  for (pint n : neigh(x, y, tab.size(), tab[0].size())) {
    if (!visited[n.second][n.first] && tab[n.second][n.first] > tab[y][x]) {
      isPeak = false;
      findPeaks(tab, visited, res, n.first, n.second);
    }
  }
  if (isPeak)
    res.push_back({x, y});
}

void topologicalSortUp(vector<vint> &tab, vector<vbool> &visited,
                       stack<pint> &sorted, int x, int y) {
  visited[y][x] = true;
  for (pint n : neigh(x, y, tab.size(), tab[0].size())) {
    if (tab[n.second][n.first] > tab[y][x] && !visited[n.second][n.first]) {
      topologicalSortUp(tab, visited, sorted, n.first, n.second);
    }
  }
  sorted.push({x, y});
};

void longestPathsUp(vector<vint> &tab, vector<vint> &len, stack<pint> &sorted) {
  pint cur;
  while (!sorted.empty()) {
    cur = sorted.top();
    sorted.pop();
    for (pint n : neigh(cur.first, cur.second, tab.size(), tab[0].size())) {
      if (tab[n.second][n.first] > tab[cur.second][cur.first] &&
          len[n.second][n.first] <= len[cur.second][cur.first] + 1) {
        len[n.second][n.first] = len[cur.second][cur.first] + 1;
      }
    }
  }
}

vector<pint> getPath(vector<vint> &len, pint start, pint dest) {
  pint cur = start;
  vector<pint> res;
  bool run = true;
  while (run) {
    res.push_back(cur);
    if (cur == dest)
      break;
    for (pint n : neigh(cur.first, cur.second, len.size(), len[0].size())) {
      if (len[n.second][n.first] + 1 == len[cur.second][cur.first]) {
        cur = n;
        break;
      }
    }
  }
  return res;
}

signed main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  int R, S;
  cin >> R >> S;
  vector<vint> tab(R, vint(S));
  pint St, C;
  cin >> St.first >> St.second >> C.first >> C.second;
  for (int y = 0; y < R; y++)
    for (int x = 0; x < S; x++)
      cin >> tab[y][x];

  vector<vbool> visitedSt(R, vbool(S)), visitedC(R, vbool(S));
  stack<pint> sortedSt, sortedC;
  topologicalSortUp(tab, visitedSt, sortedSt, St.first, St.second);
  topologicalSortUp(tab, visitedC, sortedC, C.first, C.second);

  vector<vint> lenSt(R, vint(S, -1)), lenC(R, vint(S, -1));
  lenSt[St.second][St.first] = 0;
  lenC[C.second][C.first] = 0;
  longestPathsUp(tab, lenSt, sortedSt);
  longestPathsUp(tab, lenC, sortedC);

  vector<pint> peaks;
  vector<vbool> visitedP(R, vbool(S));
  findPeaks(tab, visitedP, peaks, St.first, St.second);

  int maxlen = 0;
  pint bestp;
  for (pint p : peaks) {
    if (lenSt[p.second][p.first] + lenC[p.second][p.first] > maxlen) {
      maxlen = lenSt[p.second][p.first] + lenC[p.second][p.first];
      bestp = p;
    }
  }
  cout << maxlen + 1 << endl;

  vector<pint> pathUp = getPath(lenSt, bestp, St);
  vector<pint> pathDown = getPath(lenC, bestp, C);
  for (int i = pathUp.size() - 1; i > 0; i--)
    cout << pathUp[i].first << " " << pathUp[i].second << nl;
  for (pint p : pathDown)
    cout << p.first << " " << p.second << nl;

  return 0;
}
