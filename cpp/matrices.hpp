#include<vector>

using namespace std;

class myMatrix {
public:
  myMatrix(int);
  myMatrix(const myMatrix&);
  myMatrix(int, int);
  ~myMatrix();
  myMatrix& operator=(myMatrix&);
  vector<int>& operator[](int);
  int get(int,int) const;
  int sizex() const;
  int sizey() const;
  void print();
  void shrink(int, int);
  myMatrix operator+(myMatrix&);
  myMatrix operator*(int);
  void addSize(int, int);
  myMatrix takePart(int,int,int,int) const;
  friend myMatrix multiply(myMatrix, myMatrix, int a);
  friend myMatrix construct(myMatrix a, myMatrix b, myMatrix c, myMatrix d);
  
private:
  void init(int, int);
  int _sizex, _sizey;
  vector<vector<int> > m;
};

