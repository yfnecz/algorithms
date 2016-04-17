#include <iostream>
#include <chrono>
using namespace std::chrono;

class Timer {
public:
  Timer() : t1(high_resolution_clock::now()), t2(high_resolution_clock::now()) {}
  int stop();
private:
  high_resolution_clock::time_point t1, t2;  
};
