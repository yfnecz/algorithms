#include "timings.h"
#include "matrices.hpp"
#include <iostream>
#include<vector>

void myMatrix::init(int x, int y) {
  _sizex = x;
  _sizey = y;
  m.resize(_sizex);
  for (int i = 0; i < _sizex; ++i) {
    m[i].resize(_sizey);
    for( int j = 0; j< _sizey; ++j ) {
      m[i][j] = 0;
    }
  }
}

myMatrix::myMatrix(int x, int y) {
  init(x,y);
}

myMatrix::myMatrix(int n) {
  init(n,n);
}

myMatrix::myMatrix(const myMatrix& copy) {
  init(copy.sizex(), copy.sizey());
  for(int i=0; i<_sizex; ++i)
    for(int j=0; j<_sizey; ++j)
      m[i][j] = copy.get(i,j);
}

myMatrix& myMatrix::operator=(myMatrix& copy) {
  if (this == &copy) {
    return *this;
  }
  init(copy.sizex(), copy.sizey());
  for(int i=0; i<_sizex; ++i)
    for(int j=0; j<_sizey; ++j)
      m[i][j] = copy[i][j];
  return *this;
}

myMatrix::~myMatrix() {
}

int myMatrix::sizex() const{
  return _sizex;
}

int myMatrix::sizey() const{
  return _sizey;
}

int myMatrix::get(int x, int y) const {
  return m[x][y];
}

void myMatrix::shrink(int x, int y) {
  if(_sizex <= x && _sizey <= y ) return;

  if(_sizex > x) {
    for(int i = 0; i < (_sizex - x); ++i)
      m.pop_back();
    _sizex = x;
  }
  
  if(_sizey > y) {
    for(int i=0; i<_sizex; ++i)
      for(int j = 0; j < (_sizey-y); ++j)
        m[i].pop_back();
    _sizey = y;
  }
}

void myMatrix::addSize(int x, int y) {
  if( _sizex >= x && _sizey >=y ) return;

  if (_sizey < y) {
    for(int i=0; i<_sizex; ++i) {
      m[i].resize(y);
      m[i][y-1] = 0;
    }
    _sizey = y;
  }
  
  if( _sizex < x ) {
    int newrows = x-_sizex;
    m.resize(x);
    for( int i = 0; i < newrows; ++i ) {
      m[_sizex+i].resize(_sizey);
      for(int j=0; j<_sizey; ++j ) {
        m[_sizex+i][j] = 0;
      }
    }
    _sizex = x;
  }
}

vector<int>& myMatrix::operator[](int index) {
  if( index >=0 && index < _sizex ) {
    return m[index];
  } else {
    cout << "Access violaton" << endl;
    throw "Access violation";
  }
}

myMatrix myMatrix::operator+(myMatrix& b) {
  if( _sizex != b.sizex() || _sizey != b.sizey() ) {
    cout << "Size error" << endl;
    throw "Size error";
  }
  myMatrix res(_sizex, _sizey);
  for(int i=0; i<_sizex; ++i)
    for(int j=0; j<_sizey; ++j)
      res[i][j] = m[i][j] + b[i][j];

  return res;
}

myMatrix myMatrix::operator*(int num) {
  myMatrix result(_sizex, _sizey);
  for(int i=0; i<_sizex; ++i)
    for(int j=0; j<_sizey; ++j)
      result[i][j] = m[i][j]*num;

  return result;
}

void myMatrix::print() {
  cout << "Printing matrix by address " << this << endl;
  for( int i = 0; i < _sizex; ++i ) {
    for( int j = 0; j< _sizey; ++j ) {
      cout << m[i][j] << " ";
    }
    cout << endl;    
  }
  cout << endl;
}

myMatrix myMatrix::takePart(int xst, int x, int yst, int y) const {
  if( (xst+x) > _sizex || (yst+y) > _sizey ) {
    cout << "Size violation takePart" << endl;
    throw "Size violation takePart";
  }
  myMatrix part(x, y);
  for(int i=xst; i<xst+x; ++i)
    for(int j=yst; j<yst+y; ++j) {
      part[i-xst][j-yst] = m[i][j];
    }
  return part;
}

myMatrix multiply( myMatrix a, myMatrix b, int reclvl = 0 ) {

  /* Matrix size is the same */
  if(a.sizex() != b.sizex() || a.sizey() != b.sizey()) {
    cout << "Size mismatch!" << endl;
    throw "Size mismatch!";
  }
  int x = a.sizex(), y = a.sizey();
  
  /* recursion break case*/
  if (x == 1 && y == 1) {
    myMatrix res(1, 1);
    res[0][0] = a[0][0] * b[0][0];
    return res;
  }

  /* common case */
  int newx = x/2, newy = y/2, bigx = x-x/2, bigy = y-y/2;
  myMatrix A = a.takePart(0, newx, 0, newy),
    B = a.takePart(0, newx, newy, y - newy),
    C = a.takePart(newx, x - newx, 0, newy),
    D = a.takePart(newx, x - newx, newy, y - newy),
    E = b.takePart(0, newx, 0, newy),
    F = b.takePart(0, newx, newy, y-newy),
    G = b.takePart(newx, x - newx, 0, newy),
    H = b.takePart(newx, x - newx, newy, y - newy);
  
  /* make all matrices big */
  A.addSize(bigx,bigy);
  B.addSize(bigx,bigy);
  C.addSize(bigx,bigy);
  E.addSize(bigx,bigy);
  F.addSize(bigx,bigy);
  G.addSize(bigx,bigy);

  myMatrix H_1 = H*-1,
    E_1 = E*-1,
    D_1 = D*-1,
    C_1 = C*-1;

  myMatrix P1 = multiply(A, F+H_1, reclvl+1),
    P2 = multiply(A+B, H, reclvl+1),
    P3 = multiply(C+D, E, reclvl+1),
    P4 = multiply(D, G+E_1, reclvl+1),
    P5 = multiply(A+D, E+H, reclvl+1),
    P6 = multiply(B+D_1, G+H, reclvl+1),
    P7_1 = multiply(A+C_1, E+F, reclvl+1)*-1;
  myMatrix P2_1 = P2*-1,
    P3_1 = P3*-1;

  myMatrix part1 = P5 + P4 + P2_1 + P6,
    part2 = P1 + P2,
    part3 = P3 + P4,
    part4 = P1 + P5 + P3_1 + P7_1;

  part1.shrink(newx,newy);
  part2.shrink(newx, y-newy);
  part3.shrink(x-newx, newy);

  myMatrix res2(construct(part1, part2, part3, part4));
  return res2;
  
}

myMatrix construct(myMatrix a, myMatrix b, myMatrix c, myMatrix d) {
  int ax = a.sizex(), ay = a.sizey(), dx = d.sizex(), dy=d.sizey();
  myMatrix res(ax+dx, ay+dy);
  /* stupid code here */
  for(int i=0; i<ax; ++i) {
    for(int j=0; j<ay; ++j)
      res[i][j] = a[i][j];
    for(int j=0; j<dy; ++j)
      res[i][ay+j] = b[i][j];
  }
  for(int i=0; i<dx; ++i) {
    for(int j=0; j<ay; ++j)
      res[ax+i][j] = c[i][j];
    for(int j=0; j<dy; ++j)
      res[ax+i][ay+j] = d[i][j];
  }
  return res;
}

int main(int, char **) {

  /*** Input data generated***/
  Timer t1;

  int n, m;
  do {
    srand(t1.stop());
    n = rand() % 12;
  } while (n < 5);

  myMatrix a(n), b(n);

  for(int i=0; i<n; ++i)
    for(int j=0; j<n; ++j) {
      srand(t1.stop());
      a[i][j] = rand() % 10;
      b[j][i] = rand() % 9;
    }

  a.print();
  b.print();
  
  Timer t;
  /*** Algorithm starts ***/
  myMatrix res = multiply(a,b);

  cout << "Time elapsed: " << t.stop() << endl;
  
  /*** Print output ***/
  res.print();
  
  return 0;
}
