/// \file
/// This macro plot all graphs for BL Lac object on a TGraph
/// with data read from a text file containing the UMRAO.
///
/// \macro_image
/// \macro_code
///
/// \authors Samuel Bueno Soltau
/// \date 2019-05-11

#include "TString.h"
#include "TGraph.h"
#include "TAxis.h"
#include "TCanvas.h"
#include "TF1.h"
#include "TGraphQQ.h"
#include "TStyle.h"
#include "TMath.h"

// Uncomment this number accord to graph that you wish plot

//#define RADIO 48
//#define RADIO 80
//#define RADIO 145

// Constants
#if RADIO == 48
// For BL Lac 4.8 GHz
#define DIR_FILE "data/BLL2200+420-048GHz-TS.csv"
#define DESTINY "graphics/bllac-048GHz-K_S-scatter.pdf"
#define COLOR_P kRed

#elif RADIO == 80
// For BL Lac 8.0 GHz
#define DIR_FILE data/BLL2200+420-080GHz-TS.csv"
#define DESTINY "graphics/bllac-080GHz-K_S-scatter.pdf"
#define COLOR_P kBlue

#else // RADIO == 145
// For BL Lac 14.5 GHz
#define DIR_FILE "data/BLL2200+420-145GHz-TS.csv"
#define DESTINY "graphics/bllac-145GHz-K_S-scatter.pdf"
#define COLOR_P kGreen+3

#endif

#define TITLE ";Measured Flux Density (Jy);Calculated  Density (Jy)"
#define MAX 20000
#define NUM_COL 6
#define COLOR_L 12
#define MARK_STYLE kOpenCircle


void GraphBLLacKSFromCSVscatter()
{
    // Open the data file. This csv contains the columns:
    // MJD      - Modified Julian Date
    // Date     - Gregorian date format YYYY-MM-DD
    // Sorig    - Original Flux density in jansky
    // sigSorig - Original sigma flux density error
    // Scalc    - Calculated Flux density in jansky
    // sigScalc - Calculated sigma flux density error
    // First line is a header.
    
    gROOT->Reset();
    
    FILE *fstream = fopen(DIR_FILE, "r");
    
    char line[MAX];
    
    double mjd[MAX];
    char dt[MAX][11];
    double So[MAX];
    double SoErr[MAX];
    double Sc[MAX];
    double ScErr[MAX];
    Double_t x[MAX];
   
    // Skip the first line: header 
    fgets(line, sizeof(line), fstream);
    //std::cout << line << std::endl;
    
    int lineno = -1;
    int count = 0;
    while (fgets(line, sizeof(line), fstream) != NULL) {
        lineno++;
        if (sscanf(line, "%lg, %10[^,], %lg, %lg, %lg, %lg", &mjd[lineno], dt[lineno], &So[lineno], &SoErr[lineno], &Sc[lineno], &ScErr[lineno]) != NUM_COL) {
            fprintf(stderr, "Invalid data in line %d:\n%s\n", lineno, line);
            return;
        }
    }
    fclose(fstream);
    
//     for(int i = 0; i <= lineno; i++) {
//         std::cout << i << " : " << line << std::endl;
//         std::cout << "      MJD : " << mjd[i] << std::endl;
//         std::cout << "     Date : " << dt[i] << std::endl;
//         std::cout << "   S orig : " << So[i] << std::endl;
//         std::cout << "sigS orig : " << SoErr[i] << std::endl;
//         std::cout << "   S calc : " << Sc[i] << std::endl;
//         std::cout << "sigS calc : " << ScErr[i] << std::endl;
//     }
//     
//     std::cout << " First line: " << mjd[0] << " " << dt[0] << " " << " " << So[0] << " " << SoErr[0] << " " << Sc[0] << " " << ScErr[0] << std::endl;
//     std::cout << "  Last line: " << mjd[lineno] << " " << dt[lineno] << " " << So[lineno] << " " << SoErr[lineno] << " " << Sc[lineno] << " " << ScErr[lineno] << std::endl;
//     std::cout << "Total Lines: " << lineno + 1<< std::endl;
    
    gStyle->SetOptTitle(kFALSE);  //this will disable the title for all coming graphs
    
    // Draw the graph
    auto canv = new TCanvas("c", "c", 950, 500);
    canv->Clear();
    
    canv->SetFillColor(kWhite);
    canv->GetFrame()->SetFillColor(kWhite);
    canv->GetFrame()->SetBorderSize(12);
    canv->SetLeftMargin(0.07);
    canv->SetRightMargin(0.04);
    canv->SetGrid();

    // Create the graph without title

    // Quantile-Quantile plot the original values versus calculate value
    auto g2 = new TGraphQQ(lineno, So, lineno, Sc);
    g2->SetTitle(TITLE);
    g2->GetYaxis()->CenterTitle();
    g2->GetXaxis()->CenterTitle();
    
    g2->SetLineColor(COLOR_L);
    g2->SetLineStyle(9); // need fix
    g2->SetLineWidth(10);
    g2->SetMarkerStyle(10);
    g2->SetMarkerColor(COLOR_P);
    g2->SetMarkerSize(1);
    g2->DrawClone("APE");
    
    canv->Print(DESTINY);

    gSystem->Exit(kTRUE);
}
