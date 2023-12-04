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

signed main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  ll N, M;
  cin >> N >> M;
  vll items(N);
  for (ll i = 0; i < N; i++)
    cin >> items[i];
  vector<pair<ll, vll>> recipes(M);
  for (ll i = 0; i < M; i++) {
    ll count;
    cin >> recipes[i].first >> count;
    recipes[i].second = vll(count);
    for (ll j = 0; j < count; j++)
      cin >> recipes[i].second[j];
  }
  sort(recipes.begin(), recipes.end());
  reverse(recipes.begin(), recipes.end());
  for (auto recipe : recipes) {
    ll cost = 0;
    for (ll ing : recipe.second)
      cost += items[ing];
    items[recipe.first] = min(cost, items[recipe.first]);
  }

  cout << items[0] << endl;

  return 0;
}
