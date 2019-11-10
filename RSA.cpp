#include "RSA.hpp"
RSA::RSA(string p_bin, string q_bin, string a) {
    this->p = bitset<2048>(p_bin);
    this->q = bitset<2048>(q_bin);
    this->a = bitset<2048>(a);

    // bitset_mul(p, q, this->n);
    // bitset_mul(p, q, this->phi_n);
    // extended_euclid(this->phi_n, this->a, this->b);
}
void RSA::bitset_add(const bitset<2048> &a, const bitset<2048> &b, bitset<2048> &sum) {
    bool carry_bit = 0;
    for(int i = 0;i < 2048;i++){
        sum[i] = (a[i] + b[i] + carry_bit) % 2;
        carry_bit = (a[i] + b[i] + carry_bit) / 2;
    }
}
