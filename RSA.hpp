#include <bitset>
#include <iostream>

using namespace std;
extern string private_key, p_bin, q_bin, r_bin;
class RSA {
   public:
    // p,q,private_key
    bitset<2048> p, q, private_key, r, a, b, n, phi_n;
    // 计算n的函数
    // 计算fai(n)的函数
    // 计算根据fai(n)与加密指数b计算解密指数a的函数
    RSA(string p_bin, string q_bin, string a);

    //以下所有的运算都不会溢出
    void bitset_add(const bitset<2048> &a, const bitset<2048> &b,
                     bitset<2048> &sum);
    void bitset_sub(const bitset<2048> &a, const bitset<2048> &b,
                     bitset<2048> &diff);
    void bitset_mul(const bitset<2048> &a, const bitset<2048> &b,
                     bitset<2048> &prod);
    void bitset_div(const bitset<2048> &a, const bitset<2048> &b,
                     bitset<2038> &quot);
    bool bitset_div(const bitset<2048> &a, const bitset<2048> &b);
    void extended_euclid(const bitset<2048> &phi_n, const bitset<2048> &a,
                         const bitset<2048> &b);
    void test();

    // 加密指数b
    // 填充函数,接受一个1024位的消息与一个1024位的随机数，返回一个2048位的消息
    void padding(bitset<1024> M, bitset<1024> r);
    bitset<1024> H(const bitset<1024> &a);

    // 加密函数接受一个2048位的大整数，与一个加密指数，使用平方乘算法
    bitset<2048> encrypt(bitset<1024> message);
    void do_encrypt(const bitset<1024> &message, bitset<2048> &result);
};