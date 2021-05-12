// "config.py" guide and creator, by tory#3784

#include <iostream>
#include <fstream>
#include <string>
#include <conio.h>

using namespace std;

void createCFG() {
//    declare output file
    ofstream cfg("psnconfig.ini");
//    grab psnid & npsso
    string psnid, npsso;
    cout << "\tInsert your PSN id =";
    cin >> psnid;
    cout << "\tPaste the npsso given =";
    cin >> npsso;
//    create the config.py
    cfg << "[main]" << endl;
    cfg << "npsso = " << npsso << endl;
    cfg << "PSNID = " << psnid;
}

void getNPSSO() {
    cout << "Login into your My PlayStation account. To open press ENTER" << endl;
    getch();
    system("start https://my.playstation.com/");
    cout << "To get to the next step press ENTER" << endl;
    getch();
    system("start https://ca.account.sony.com/api/v1/ssocookie");
    cout << "Copy the NPSSO given by the browser without quotation mark. Press ENTER to continue" << endl;
    getch();
}

int main() {
    int option;
    cout << "1. Get NPSSO (used in config.py)" << endl;
    cout << "2. Create 'config.py' in this directory" << endl;
    do {
        cout << "Enter the menu number 1 or 2, then press ENTER" << endl;
        cin >> option;
        switch (option) {
            case 1:
                getNPSSO();
                break;
            case 2:
                createCFG();
                break;
            default:
                cout << "No option from the menu selected" << endl;
                break;
        }
    } while (option != 0);

}
