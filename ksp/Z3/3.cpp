#include <bits/stdc++.h>
#include <queue>
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

  int W, H;
  cin >> W >> H;
  vector<string> map(H);
  for (int i = 0; i < H; i++)
    cin >> map[i];
  vector<vint> visited(H, vint(W, -1));
  queue<pint> q;
  for (int i = 0; i < W; i++)
    q.push({i, 0});
  pint cur;
  int end = -1;
  while (!q.empty()) {
    cur = q.front();
    q.pop();
    if (cur.second == H - 1) {
      end = cur.first;
      break;
    }
    for (int d : vector<int>({-1, 0, 1})) {
      int x = cur.first + d;
      int y = cur.second + 1;
      if (visited[y][x] == -1 && map[y][x] == '.') {
        q.push({x, y});
        visited[y][x] = cur.first;
      }
    }
  }
  // for (int y = 0; y < H; y++) {
  //   cout << endl;
  //   for (int x = 0; x < W; x++)
  //     cout << visited[y][x] << " ";
  // }

  if (end == -1)
    cout << "NEEXISTUJE" << endl;
  else {
    int x = end, y = H - 1;
    vint track;
    while (y >= 0) {
      track.push_back(x);
      x = visited[y][x];
      y--;
    }
    for (int i = track.size() - 1; i >= 0; i--)
      cout << track[i] << endl;
  }

  return 0;
}
