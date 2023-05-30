#include <iostream>
#include "nanobench.h"
#include <unordered_map>

typedef long long int ll;

ll fib(ll n)
{
    if (n == 0)
        return 0;
    if (n == 1)
        return 1;
    return fib(n - 1) + fib(n - 2);
}

ll memofib(ll n, std::unordered_map<ll, ll> &table)
{
    if (n == 0)
        return 0;
    if (n == 1)
        return 1;
    if (table.find(n) != table.end())
    {
        return table[n];
    }
    ll res = memofib(n - 1, table) + memofib(n - 2, table);
    table[n] = res;
    return res;
}
typedef std::unordered_map<ll, ll> mm;
int main()
{
    ll d;
    ankerl::nanobench::Bench().run("Fibonacii 1", [&]
                                   { d = fib(1); });
    ankerl::nanobench::Bench().run("Fibonacii 10", [&]
                                   { d = fib(10); });
    ankerl::nanobench::Bench().run("Fibonacii 20", [&]
                                   { d = fib(20); });
    ankerl::nanobench::Bench().run("Fibonacii 30", [&]
                                   { d = fib(30); });
    /*
    ankerl::nanobench::Bench().run("Fibonacii 40", [&]
                                   { d = fib(40); });
    std::cout << d << std::endl;
    */

    ankerl::nanobench::Bench().run("MFibonacii 1", [&]
                                   { mm a; d = memofib(1, a); });
    ankerl::nanobench::Bench().run("MFibonacii 10", [&]
                                   { mm a; d = memofib(10, a); });
    ankerl::nanobench::Bench().run("MFibonacii 20", [&]
                                   { mm a; d = memofib(20, a); });
    ankerl::nanobench::Bench().run("MFibonacii 30", [&]
                                   { mm a; d = memofib(30, a); });
    ankerl::nanobench::Bench().run("MFibonacii 40", [&]
                                   { mm a; d = memofib(40, a); });
    ankerl::nanobench::Bench().run("MFibonacii 400", [&]
                                   { mm a; d = memofib(400, a); });
    std::cout << d << std::endl;
    return 0;
}