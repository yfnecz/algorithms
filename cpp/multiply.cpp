#include<iostream>
#include<math.h>
#include<sstream>
#include "timings.h"

using namespace std;

int multiply( string x, string y, int iter = 0 ) {
  if( y.size() == 1 && x.size() == 1) {
    return( stoi(x) * stoi(y) );
  }

  if(x.size() > y.size()) x.swap(y);
  for(int i = x.size(); i < y.size()+y.size()%2; ++i) {
    x = "0" + x;
  }
  if( y.size() %2 ) {
    y = "0" + y;
  }

  int n = y.size();
  string a = x.substr(0, n/2), b = x.substr(n/2), c = y.substr(0,n/2), d = y.substr(n/2);
  int a_b = stoi(a) + stoi(b), c_d = stoi(c) + stoi(d);
  ostringstream s_a_b, s_c_d;
  s_a_b << a_b; s_c_d << c_d;
  int ac = multiply(a, c, iter+1), bd = multiply(b, d, iter+1), abcd = multiply( s_a_b.str(), s_c_d.str(), iter+1 );
  return (
      pow(10,n)*ac
      + pow(10,(n/2))*(abcd - ac - bd)
      + bd
  );
}


void test(int number) {
  int time = 0;
  for(int i = 0; i< number; ++i) {
    int x = rand() %10000, y = rand() %10000;
    int res = x*y;
    Timer t;
    int my_res = multiply(to_string(x),to_string(y));
    time += t.stop();
    if( res != my_res ) {
      cout << "ERROR!! x = " << x << ", y = " << y << endl;
      exit(5);
    }
  }
  cout << "Time elapsed in multiply: " << time*0.000001 << endl;  
}

int main( int argc, char **argv ) {
  Timer t;
  test(10000000);
  cout << "Time elapsed full: " << t.stop()*0.000001 << endl;
  return 0;
}
