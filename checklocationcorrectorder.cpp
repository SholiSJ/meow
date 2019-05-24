#include<iostream>
#include<fstream>
#include<string>
using namespace std;
int main(){
   std::ios::sync_with_stdio(false); // to speed up reading
    ifstream testfile;
    string line,name;
    uint_fast16_t n,i=0;
    float lat1,lat2,lng1,lng2;
    testfile.open("testfile.txt");
    if (!testfile) {
        cout << "Unable to open file";
        exit(1); // terminate with error
    }
    /*testfile.seekg(19,ios::beg);//skip to last of first line
    testfile>>n;
    testfile.seekg(21,ios::beg);*/ //for counting
    getline(testfile,line);//read next line;
    getline(testfile,line);
 
  while ( testfile >> name >> lat1 >> lng1 >> lat2 >> lng2 )
  {i++;
if((lat1>=lat2)&&(lng2>=lng1)) {if((lat1==lat2)&&(lng2==lng1)) { cout<<"co-ordinates same at "<<i<<endl;} ;}
else {cout<<"wrong co-ordinates of location "<<i<<endl;};

        }
        testfile.close(); // Step 5: Closing file


return 0;
}
