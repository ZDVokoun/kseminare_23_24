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

int waitTime(int arr, int dep) {
  if (dep - arr < 0)
    return dep - arr + 86400;
  return dep - arr;
}

struct DirectionParse {
  string connection;
  int departure;
  string next;
  int nextArrival = -1;
};

struct Direction {
  int connection;
  int departure;
  int next;
  int nextArrival = -1;
  int visited = 500;
};

struct QItem {
  int waitTime;
  int arrival;
  int town;
  vector<pint> hist;
  bool operator<(const QItem &a) const { return waitTime < a.waitTime; }
};

signed main(int argc, char *argv[]) {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  string start, dest;
  int begin, nOfCon;
  cin >> start >> begin >> dest >> nOfCon;
  if (start == dest)
    return 0;
  map<string, vector<DirectionParse>> stationsParse;
  set<string> connectionsParse;
  for (int i = 0; i < nOfCon; i++) {
    string connection;
    int nOfStations;
    cin >> connection >> nOfStations;
    connectionsParse.insert(connection);
    string prevStation;
    int prevDeparture;
    cin >> prevStation >> prevDeparture;
    for (int j = 1; j < nOfStations; j++) {
      string station;
      int departure;
      cin >> station >> departure;
      stationsParse[prevStation].push_back(
          {connection, prevDeparture, station, departure});
      prevStation = station;
      prevDeparture = departure;
    }
  }

  vector<string> connections(connectionsParse.begin(), connectionsParse.end());
  vector<string> stations(stationsParse.size());
  vector<vector<Direction>> graph(stationsParse.size());
  int i = 0;
  for (auto p : stationsParse) {
    stations[i] = p.first;
    vector<Direction> node(p.second.size());
    for (int j = 0; j < p.second.size(); j++) {
      node[j].connection =
          distance(connectionsParse.begin(),
                   connectionsParse.find(p.second[j].connection));
      node[j].next =
          distance(stationsParse.begin(), stationsParse.find(p.second[j].next));
      node[j].departure = p.second[j].departure;
      node[j].nextArrival = p.second[j].nextArrival;
    }
    graph[i] = node;
    i++;
  }
  int startI = distance(stationsParse.begin(), stationsParse.find(start));
  int destI = distance(stationsParse.begin(), stationsParse.find(dest));
  //
  // for (auto s : stations)
  //   cout << s << endl;

  priority_queue<QItem> q;
  q.push({0, begin, startI, {}});
  vector<pint> departures;
  while (!q.empty()) {
    QItem cur = q.top();
    q.pop();
    // cout << stations[cur.town] << endl;
    if (cur.town == destI) {
      departures = cur.hist;
      break;
    }
    for (int i = 0; i < graph[cur.town].size(); i++) {
      if (graph[cur.town][i].visited <= 0)
        continue;
      graph[cur.town][i].visited--;
      int dWaitTime = waitTime(cur.arrival, graph[cur.town][i].departure);
      if (dWaitTime != 0) {
        vector<pint> newHist = cur.hist;
        newHist.push_back({graph[cur.town][i].connection, cur.town});
        cur.waitTime += dWaitTime;
        q.push({cur.waitTime, graph[cur.town][i].nextArrival,
                graph[cur.town][i].next, newHist});
      }
      q.push({cur.waitTime, graph[cur.town][i].nextArrival,
              graph[cur.town][i].next, cur.hist});
    }
  }

  // cout << departures.size() << endl;
  // int j = 1;
  // string curStation = start;
  // string curConn = "";
  // for (auto d : stations[start])
  //   if (d.departure == departures[0].second) {
  //     curConn = d.connection;
  //     curStation = d.next;
  //   }
  // while (j < departures.size()) {
  //   bool isTrasfer = false;
  //   for (auto d : stations[curStation]) {
  //     if (d.departure == departures[j].first) {
  //       isTrasfer = true;
  //       for (auto dd : stations[curStation])
  //         if (dd.departure == departures[j].second) {
  //           cout << dd.next << " " << dd.connection << endl;
  //           curStation = dd.next;
  //           curConn = dd.connection;
  //           j++;
  //           break;
  //         }
  //       break;
  //     }
  //   }
  //   if (!isTrasfer) {
  //     for (auto d : stations[curStation]) {
  //       if (d.connection == curConn) {
  //         curStation = d.next;
  //         break;
  //       }
  //     }
  //   }
  // }
  departures.push_back({0, destI});
  for (int i = 0; i < departures.size() - 1; i++)
    cout << connections[departures[i].first] << " "
         << stations[departures[i + 1].second] << endl;

  return 0;
}
