#include <iostream>
#include <chrono>
#include "timings.h"
using namespace std::chrono;

int Timer::stop() {
  t2 = high_resolution_clock::now();
  return std::chrono::duration_cast<std::chrono::microseconds>( t2 - t1 ).count();
}
