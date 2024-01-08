#include <bits/stdc++.h>
#define endl '\n'
#define nl '\n'

using namespace std;
typedef long long ll;
typedef vector<long long> vll;
typedef vector<int> vint;
typedef vector<bool> vbool;
typedef pair<int, int> pint;

double dist(int a, int b, int c, int x, int y) {
  return abs(a * x + b * y + c) / sqrt(pow(a, 2) + pow(b, 2));
}

int mod(int a, int b) {
  if (a < 0)
    return b + (a % b);
  return a % b;
}

signed main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  int N;
  cin >> N;
  vector<pint> vertices(N);
  for (int i = 0; i < N; i++)
    cin >> vertices[i].first >> vertices[i].second;
  double max = 0;
  int res = 0;
  int cur = 0;
  for (int i = 0; i < N; i++) {
    pint point_vec = {vertices[i + 1 % N].first - vertices[i].first,
                      vertices[i + 1 % N].second - vertices[i].second};
    ll a = point_vec.second;
    ll b = -point_vec.first;
    ll c = -a * vertices[i].first - b * vertices[i].second;
    double prev = dist(a, b, c, vertices[cur].first, vertices[cur].second);
    while (true) {
      double d = dist(a, b, c, vertices[cur].first, vertices[cur].second);
      if (d < prev) {
        cur = mod(cur - 1, N);
        break;
      }
      prev = d;
      cur = mod(cur + 1, N);
      if (d > max) {
        max = d;
        res = i;
      }
    }
  }
  cout << res + 1 << endl;

  return 0;
}
