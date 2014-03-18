#include <iostream>
using namespace std;

int main() {
	string args;
	cin >> args;

	size_t pos = 0;
	bool progress = true;
	while (progress) {
		int array = 0;
		while ( 1 )
			if (args[pos] == '[') { array++; args.erase(pos, 1); }
			else break;

		if      (args[pos] == 'Z') { args.replace(pos, 1, "boolean,"); pos += 8; }
		else if (args[pos] == 'B') { args.replace(pos, 1, "byte,"); pos += 5; }
		else if (args[pos] == 'C') { args.replace(pos, 1, "char,"); pos += 5; }
		else if (args[pos] == 'D') { args.replace(pos, 1, "double,"); pos += 7; }
		else if (args[pos] == 'F') { args.replace(pos, 1, "float,"); pos += 6; }
		else if (args[pos] == 'I') { args.replace(pos, 1, "int,"); pos += 4; }
		else if (args[pos] == 'J') { args.replace(pos, 1, "long,"); pos += 5; }
		else if (args[pos] == 'S') { args.replace(pos, 1, "short,"); pos += 6; }
		else if (args[pos] == 'L') {
			args.erase(pos, 1);
			pos = args.find(";", pos);
			args.replace(pos, 1, ",");
			pos++;
		}
		else progress = false;

		while ( array-- ) {
			args.replace(pos-1, 1, "[],");
			pos += 2;
		}
	}

	pos = 0;
	while ((pos = args.find("/", pos)) != std::string::npos) args[pos] = '.';

	if (args[args.size() - 1] == ',') args.erase(args.size() - 1, 1);

	cout << args << endl;
}
