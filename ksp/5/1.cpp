#include <bits/stdc++.h>
#define endl '\n'
#define nl '\n'

using namespace std;
typedef long long ll;
typedef vector<long long> vll;
typedef vector<int> vint;
typedef vector<bool> vbool;
typedef pair<int, int> pint;

bool isPossible(ll arr[], ll n, ll m, ll curr_min) {
  ll studentsRequired = 1;
  ll curr_sum = 0;

  for (ll i = 0; i < n; i++) {
    if (arr[i] > curr_min)
      return false;

    if (curr_sum + arr[i] > curr_min) {
      studentsRequired++;

      curr_sum = arr[i];

      if (studentsRequired > m)
        return false;
    }

    else
      curr_sum += arr[i];
  }
  return true;
}

ll findPages(ll arr[], ll n, ll m) {
  ll sum = 0;

  if (n < m)
    return -1;
  ll mx = INT64_MIN;

  for (ll i = 0; i < n; i++) {
    sum += arr[i];
    mx = max(mx, arr[i]);
  }

  ll start = mx, end = sum;
  ll result = INT64_MAX;

  while (start <= end) {
    ll mid = (start + end) / 2;
    if (isPossible(arr, n, m, mid)) {
      result = mid;

      end = mid - 1;
    }

    else
      start = mid + 1;
  }

  return result;
}

signed main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  ll N, K;
  cin >> N >> K;
  ll a[N];
  for (ll i = 0; i < N; i++)
    cin >> a[i];
  ll mx = findPages(a, N, K);
  ll last = 0;
  ll sum = a[0];
  for (ll i = 0; i < N - 1; i++) {
    if (sum + a[i + 1] > mx) {
      cout << last + 1 << " " << i + 1 << endl;
      last = i + 1;
      sum = 0;
    }
    sum += a[i + 1];
  }
  cout << last + 1 << " " << N << endl;

  return 0;
}
