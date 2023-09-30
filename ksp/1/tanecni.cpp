#include <algorithm>
#include <bits/stdc++.h>
#define endl '\n'
#define nl '\n'

using namespace std;
typedef long long ll;
typedef vector<long long> vll;
typedef vector<int> vint;

std::vector<int> findLIS(const std::vector<int> &X) {
  int N = X.size();
  vint P(N), M(N + 1);
  M[0] = -1;

  int L = 0;
  for (int i = 0; i < N; ++i) {
    auto it = lower_bound(M.begin() + 1, M.begin() + L + 1, i,
                          [&X](int a, int b) { return X[a] < X[b]; });

    int newL = distance(M.begin(), it);
    P[i] = M[newL - 1];
    M[newL] = i;

    if (newL > L) {
      L = newL;
    }
  }

  vint S(L);
  int k = M[L];
  for (int j = L - 1; j >= 0; --j) {
    S[j] = X[k];
    k = P[k];
  }

  return S;
}

signed main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  int N;
  cin >> N;
  vint pairs(N);
  for (int i = 0; i < N; i++)
    cin >> pairs[i];
  vint res = findLIS(pairs);
  vint print(res.size());
  int j = 0;
  for (int i = 0; i < pairs.size(); i++) {
    if (pairs[i] == res[j]) {
      print[j] = i + 1;
      j++;
    }
  }
  cout << print.size() << nl;
  for (int num : print)
    cout << num << endl;

  return 0;
}
