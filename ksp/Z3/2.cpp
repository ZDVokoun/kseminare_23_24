#include <algorithm>
#include <bits/stdc++.h>
#include <cstdint>
#define endl '\n'
#define nl '\n'

using namespace std;
typedef long long ll;
typedef vector<long long> vll;
typedef vector<int> vint;
typedef vector<bool> vbool;
typedef pair<int, int> pint;
typedef pair<ll, ll> pll;

int toSkip(int start, int end, vint &voluntaryStart, vint &voluntaryEnd) {
  int i = start, j = start;
  int m = INT32_MAX;
  while (j <= end) {
    if (voluntaryStart[j] - voluntaryEnd[i] >= 40) {
      m = min(m, j - i - 1);
      i++;
    } else
      j++;
  }
  return m;
}

signed main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  ll P, V;
  cin >> P >> V;

  vector<pint> transfers;
  char building = '\0', curBuilding;
  pint prev, cur;
  for (ll i = 0; i < P; i++) {
    cin >> cur.first >> cur.second >> curBuilding;
    if (building != '\0' && curBuilding != building)
      transfers.push_back({prev.second, cur.first});
    prev = cur;
    building = curBuilding;
  }
  vint voluntaryStart(V), voluntaryEnd(V);
  for (ll i = 0; i < V; i++)
    cin >> voluntaryStart[i] >> voluntaryEnd[i];
  ll res = V;
  for (pint transfer : transfers) {
    int start = lower_bound(voluntaryStart.begin(), voluntaryStart.end(),
                            transfer.first) -
                voluntaryStart.begin();
    int end =
        lower_bound(voluntaryEnd.begin(), voluntaryEnd.end(), transfer.second) -
        voluntaryEnd.begin();
    end--;
    int fromStart = lower_bound(voluntaryStart.begin(), voluntaryStart.end(),
                                transfer.first + 40) -
                    voluntaryStart.begin() - start;
    int fromEnd = end -
                  (upper_bound(voluntaryEnd.begin(), voluntaryEnd.end(),
                               transfer.second - 40) -
                   voluntaryEnd.begin()) +
                  1;
    // cout << start << " " << end << " " << fromStart << " " << fromEnd << nl;
    if (start > end)
      continue;
    res -= min(min(fromStart, fromEnd),
               toSkip(start, end, voluntaryStart, voluntaryEnd));
  }

  cout << res << endl;

  return 0;
}
