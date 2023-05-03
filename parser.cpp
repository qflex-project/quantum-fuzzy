#include <iostream>
#include <string>
#include <vector>

using namespace std;

void replaceAll(string &s, string sub1, string sub2){
	size_t f = 0;

	while (true){
		f = s.find(sub1, f);
    	if (f == string::npos) break;
    	s.replace(f, sub1.size(), sub2);
    	f++;
	}
}

int main(){
	char line[300];
	string s, s2;
	int i,j;

	vector <vector<string> > vet;

	vector <string> ex;

	size_t f, f2;

	int pos = 0;

	vet.push_back(vector<string>());

	while (cin.getline(line, 300)){
		s = line;

		if (s == "########" && vet[pos].size() != 0){
			vet.push_back(vector<string>());
			pos++;
		}
		else if (s[0] == 'M'){
			while (s != "########"){ 
				cin.getline(line, 200);
				s = line;
			}
		}
		else if (s != ""){
			f = s.find(" ");

			if (f!=string::npos){
				if(pos == 0){
					s2 = s.substr(f+1);
					replaceAll(s2, "*", "");
					//replaceAll(s2, "x", "x_");
					//replaceAll(s2, "y", "y_");
					replaceAll(s2, " ", "");
					ex.push_back(s2);
				}
				s = s.substr(0, f);
			}

			if (s[0] == '0' || s[0] == '1') vet[pos].push_back(s);
		}
	}

	int qb = vet[0][0].size();
	int cl;

	if (vet[pos].size() == 0) vet.pop_back();

	cout << "\\begin{footnotesize}" << endl;
	cout << "\\begin{table*}[ht]" << endl;
	cout << "\\centering" << endl;
	cout << "\\footnotesize" << endl;
	cout << "\\caption{Evolution of superposition quantum registers in modelling quantum circuit: $A_I \\cap B_I$}" << endl;
	cout << "\\label{tab:x}" << endl;

	cout << "\\begin{tabular}{l";
	for (i =0; i < vet.size(); i++) cout << "|c";
	cout << "}" << endl;
	cout << "\\hline\\noalign{\\smallskip}" << endl;

	cout << "non-void amplitudes";
	for (i =0; i < vet.size(); i++)
		//cout << " & $|s_" << i << "\\rangle$";
		cout << " & $T" << i << "$";
	cout << "\n \\\\" << endl;

	cout << "\\noalign{\\smallskip}\\hline\\noalign{\\smallskip}\\hline" << endl;
	cout << "\\noalign{\\smallskip}" << endl;


	for (i =0; i < vet[0].size(); i++){
		cout << "$" << ex[i] << "$ & $" << vet[0][i];
		for (j = 1; j < vet.size(); j++){
			if (vet[j][i] != vet[j-1][i]){
				cout << "$ & $";
				for (int k = 0; k < vet[j][i].size(); k++){
					if (vet[j][i][k] == vet[j-1][i][k])
						cout << vet[j][i][k];
					else
						cout << "\\red{" << vet[j][i][k] << "}";
				}
			}
			else{
				cout << "$ & $" << vet[j][i];
			}
		}
		cout << "$ \\\\" << endl;
		/*
		cout << "$ & $";

		cl = 0;
		if (vet[j][i][qb-2] == '1') {
			cout << "\\underline{";
			cl++;
		}
		if (vet[j][i][qb-1] == '1') {
			cout << "\\overline{";
			cl++;
		}

		cout << vet[j][i];
		for (j = 0; j < cl; j++) cout << "}";


		cout << "$ \\\\\\hline" << endl;
		*/
	}

	cout << "\\noalign{\\smallskip}\\hline" << endl;
	cout << "\\noalign{\\smallskip}" << endl;

	cout << "\\end{tabular}" << endl;
	cout << "\\end{table*}" << endl;
	cout << "\\end{footnotesize}" << endl;
}

