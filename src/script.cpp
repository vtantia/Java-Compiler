#include <bits/stdc++.h>
#include <ext/pb_ds/assoc_container.hpp>
#include <ext/pb_ds/tree_policy.hpp>

// using namespace __gnu_pbds;
using namespace std;
// template <typename T>
// using ordered_set = tree<T, null_type, less<T>, rb_tree_tag,
//  tree_order_statistics_node_update>;

const long long Mod = 1e9 + 7;
const long long Inf = 1e18;
const long long Lim = 1e5 + 1e3;
const double eps = 1e-10;

typedef long long ll;
typedef vector <int> vi;
typedef vector <vi> vvi;
typedef vector <ll> vl;
typedef pair <int, int> pii;
typedef pair <ll, ll> pll;

#define F first
#define S second
#define mp make_pair
#define pb push_back
#define pi 2*acos(0.0)
#define rep2(i,b,a) for(ll i = (ll)b, _a = (ll)a; i >= _a; i--)
#define rep1(i,a,b) for(ll i = (ll)a, _b = (ll)b; i <= _b; i++)
#define rep(i,n) for(ll i = 0, _n = (ll)n ; i < _n ; i++)
#define mem(a,val) memset(a,val,sizeof(a))
#define all(v) v.begin(), v.end()
#define fast ios_base::sync_with_stdio(false),cin.tie(0),cout.tie(0);

string str[3000];
string cand = "    def p_";

bool CheckFunc(int ind) {
    int i = 0, j = str[ind].size();
    for ( ; i < min(str[ind].size(), cand.size()); ++i)
        if (str[ind][i] != cand[i]) break;

    if (i == cand.size())
        for(j = i; j < str[ind].size(); ++j)
            if (str[ind][j] == '(') 
                break;

    return (j == str[ind].size())?false:true;
}

bool CheckSoFunc(int ind) {
    int state=0, i;
    for(i = 0; i < str[ind].size() && state < 3; ++i) {
        if (str[ind][i] == '\'')
            state++;
        else 
            state = 0;
    }

    return (state == 3 && i < str[ind].size())?true:false;
}

bool CheckEoFunc(int ind) {
    int len=str[ind].size();
    if (len >= 3) {
        if (str[ind][len-1] == '\'' &&
            str[ind][len-2] == '\'' &&
            str[ind][len-3] == '\'')
            return true;
    }
    return false;
}

void pFname(int index) {
    int i;
    for(int i = cand.size(); i < str[index].size(); ++i) {
        if (str[index][i] != '(') 
            cout << str[index][i];
        else
            break;
    }
}

int main() {
    fast;
    // FILE *fin = freopen("parser.py","r",stdin);
    int index = -1, ptr, flag=1;
    while(flag) {
        flag = (bool)getline(cin, str[++index]);
        if (CheckFunc(index))
            break;
        else
            cout << str[index] << '\n';
    }
    while (flag) {
/*        if (CheckFunc(index))
            cout << "****** Function Begins ********\n";

        cout << str[index] << '\n';
        if (CheckEoFunc(index)) {
            cout << "****** Function Ends *******\n";
        }
*/
        flag=1;
        while (flag) {
            if (CheckFunc(index)) {
                flag = (bool) getline(cin, str[++index]);
                if (flag && CheckSoFunc(index)) {
                    cout << str[index-1] << '\n';
                    break;
                }
            }
            flag = (bool) getline(cin, str[++index]);
        }
        if (!flag) break;

        ptr = index-1;
        cout << str[index] << '\n';

        while (!CheckEoFunc(index)) {
            
            if (!getline(cin, str[++index]))
                break;

            cout << str[index] << '\n';
        }

        cout << "        " << "genPTree(\"";

        pFname(ptr);

        cout << "\", p)\n\n";

    }
    return 0;
}