#include <iostream>
#include <string>
#include "RSA.hpp"


extern string private_key, p_bin, q_bin, r_bin, a_bin;
using namespace std;
int main(){
    RSA rsa(p_bin, q_bin, a_bin);
    rsa.test();
    return 0;
}