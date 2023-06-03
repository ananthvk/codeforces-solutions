#include <algorithm>
#include <deque>
#include <iostream>
#include <map>
#include <limits>
#include <cmath>
#include <string>
#include <tuple>
#include <vector>
#include <stdint.h>
using namespace std;

// clang-format off
typedef uint64_t ull;
typedef int64_t ll;
typedef struct {ll x; ll y;} pointi;
#ifdef ONLINE_JUDGE
#define FAST_IO ios_base::sync_with_stdio(false); cin.tie(NULL);
#else
#define FAST_IO ;
#endif
#define mp make_pair
#define mt make_tuple
// Looping construct macros
#define FORN(i, stop) for (ll(i) = 0; (i) < (stop); (i)++)
#define FORR(i, stop, step) for (ll(i) = 0; (i) < (stop); (i) += (step))
#define FORS(i, start, stop, step) for (ll(i) = (start); (i) < (stop); (i) += (step))
#define DONOTUSECONC(a, b) a##b
#define DONOTUSECON(a,b) DONOTUSECONC(a, b)
#define DONOTUSEENUMERATE(i, val, container, body, ite) ll i = 0; auto ite = container.begin(); decltype(container)::value_type val; for (; ite != container.end(); ite++, i++){ val = *ite; body }
// A macro for python-style enumerate, though it is not very neat
#define ENUMERATE(i, val, container, body) {DONOTUSEENUMERATE(i, val, container, body, DONOTUSECON(DONOTUSECON(container,iterator), __COUNTER__))}
//#define abs(x) (x < 0 ? (-x) : x)
#define vi vector<int>
#define vl vector<ll>
#define vu vector<ull>
#define vc vector<char>
#define pb push_back
#define pf push_front
#define all(x) (x).begin(), (x).end()
// Maximum and minimum value of a datatype
// use it as MAXVAL(ll) - useful for finding minimum/maximum element, etc
#define MAXVAL(dt) std::numeric_limits<dt>::max()
#define MINVAL(dt) std::numeric_limits<dt>::min()
// Read a single value such as int, string, etc
#define readn() input<ll>()
#define reads() input<string>()
// Read a list of values after reading n, number of elements
// 'i' - integer, 'c' - character
#define readvi() readv<ll>()
#define readvc() readv<char>()
// Same as above, but when the number of elements is known
#define readvin(n) readv<ll>(n)
#define readvcn(n) readv<char>(n)
// Templated functions for input and output
template <typename T> ostream &operator<<(ostream &os, const deque<T> &v) { FORN(i, v.size()) { os << v[i]; if (i != (v.size() - 1)) os << " "; } return os; } template <typename T> ostream &operator<<(ostream &os, const vector<T> &v) { FORN(i, v.size()) { os << v[i]; if (i != (v.size() - 1)) os << " "; } return os; } template <typename T> T input() { T t; cin >> t; return t; } template <typename T> vector<T> readv() { std::vector<T> t; ll n; cin >> n; t.reserve(n); FORN(i, n) { t.push_back(input<T>()); } return t; } template <typename T> vector<T> readv(ll n) { std::vector<T> t; t.reserve(n); FORN(i, n) { t.push_back(input<T>()); } return t; } template <typename T> void print(T v1) { cout << v1; } template <typename T> void println(T v1) { cout << v1; cout << "\n"; } template <typename T, typename... Args> void print(T v1, Args... v2) { cout << v1; print(v2...); } template <typename T, typename... Args> void println(T v1, Args... v2) { cout << v1; print(v2...); cout << "\n"; }
// Printing functions for debugging
#ifndef ONLINE_JUDGE
template <typename T> void dprint(T v1) { cerr << v1; } template <typename T> void dprintln(T v1) { cerr << v1; cerr << "\n"; } template <typename T, typename... Args> void dprint(T v1, Args... v2) { cerr << v1; dprint(v2...); } template <typename T, typename... Args> void dprintln(T v1, Args... v2) { cerr << v1; dprint(v2...); cerr << "\n"; }
#else
template <typename T> void dprint(T v1) { } template <typename T> void dprintln(T v1) {} template <typename T, typename... Args> void dprint(T v1, Args... v2) {} template <typename T, typename... Args> void dprintln(T v1, Args... v2) {}
#endif
// clang-format on
// Solution from here
// *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
int main()
{
    FAST_IO
    ll ntests = readn();
    FORN(i, ntests)
    {
        ll n = readn();
        // Get all divisors of n <= sqrt(n)
        vi divs;
        divs.reserve(100);
        ll sq = std::sqrt(n);
        // Running time for this operation is O(sqrt(n))
        FORS(i, 2, n+1, 1)
        {
            if (n % i == 0)
            {
                divs.push_back(i);
            }
        }
        //println(sq);
        //println(divs);
        if (divs.size() < 3)
        {
            println("NO");
        }
        else
        {
            ll n_divisors = divs.size();
            // Running time of this operation is O(sqrt(n) * 2n)
            ll flag = 0;
            FORN(i, n_divisors)
            {
                flag = 0;
                ll num = n / divs[i];
                // Check if there are 2 numbers a and b such that their product is num
                map<ll, ll> prodmap; // Contains a map where prodmap[num/ele] = ele
                // So this actually checks if there is a number num/ele
                for (const auto &a : divs)
                {
                    ll complement = num / a;
                    if (prodmap.find(a) != prodmap.end())
                    {
                        ll b = prodmap[a];
                        if (a != divs[i] && b != divs[i])
                        {
                            flag = 1;
                            println("YES");
                            println(divs[i], " ", a, " ", b);
                            break;
                        }
                    }
                    prodmap[complement] = a;
                }
                if (flag)
                    break;
            }
            if (!flag)
            {
                println("NO");
            }
        }
    }
    return 0;
}
// This is the solution for the problem from codeforces
// https://codeforces.com/contest/1294/problem/C
