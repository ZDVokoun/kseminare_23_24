#include <bits/stdc++.h>
#define ll long long

using namespace std;

int main(int argc, char *argv[]) {
  int K, P, D;
  cin >> K >> P >> D;
  vector<pair<ll, ll>> res(D + K + P);
  res[K - 1] = {1, 0};
  ll result = 0;
  // first - udalost vylihnuti, second - udalost sneseni
  for (int i = 0; i < D; i++) {
    res[i + P].second += res[i].first;

    res[i + P].second += res[i].second;
    res[i + K].first += res[i].second;

    result += res[i].first;
  }
  if (result)
    cout << result << endl;

  return 0;
}
