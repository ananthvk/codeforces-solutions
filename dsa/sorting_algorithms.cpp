#include <iostream>
#include "nanobench.h"

typedef long long int ll;

bool verify(std::vector<ll> &v)
{
    // Returns true if v is in non-decreasing order
    ll N = v.size();
    for (ll i = 1; i < N; i++)
    {
        if (v[i] < v[i - 1])
            return false;
    }
    return true;
}

void bubble_sort(std::vector<ll> &v)
{
    ll N = v.size();
    for (ll i = 0; i < N; i++)
    {
        for (ll j = 0; j < N - 1 - i; j++)
        {
            if (v[j] > v[j + 1])
                std::swap(v[j], v[j + 1]);
        }
    }
}

int main()
{
    // NOT an exact benchmark --- Fix it later ... This was just to see if the library links correctly
    std::vector<ll> v = {1, 8, 11, 9, 6, 12, 24, 32, 15, 20, 9, 100, 50};
    ankerl::nanobench::Bench().run("Bubble sort 10", [&]
                                   { bubble_sort(v); });
    std::cout << verify(v)<<"\n";
    for(const auto& e: v){
        std::cout<<e<<" ";
    }
    std::cout<<"\n";
}