#include <algorithm>
#include <bits/stdc++.h>
#define endl '\n'
#define nl '\n'
#define int ll

using namespace std;
typedef long long ll;
typedef vector<long long> vll;
typedef vector<int> vint;
typedef vector<bool> vbool;
typedef pair<ll, ll> pint;

ll maxInAllIntervals(const vector<pint> &heights) {
  set<int> used = {-1};
  used.insert(heights.size());
  ll res = 0;
  for (int i = 0; i < heights.size(); i++) {
    auto itt = used.upper_bound(heights[i].second);
    ll k = (*(itt)-heights[i].second) * (heights[i].second - *(--itt));
    res += k * heights[i].first;
    if (k > 1)
      used.insert(++itt, heights[i].second);
  }
  return res;
}

signed main(signed argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  int n;
  cin >> n;
  vector<pint> heights(n);
  for (int i = 0; i < n; i++) {
    cin >> heights[i].first;
    heights[i].second = i;
  }
  sort(heights.begin(), heights.end());
  ll mins = maxInAllIntervals(heights);
  reverse(heights.begin(), heights.end());
  ll maxs = maxInAllIntervals(heights);
  cout << maxs - mins << endl;
  return 0;
}
