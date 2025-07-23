import ROOT
import csv
import numpy as np
import os
import subprocess


# data now looks like this:

# data
# data
# position
# data
# ... ~ 300     we want
# data
# position
# data
# ... ~ 10      junk 
# data
# position
# data
# ... ~ 300     we want
# etc

# reads in data for 1 given file
def cleanFile(directory, fname):

    pa_channel = 3

    pos = []
    data = []

    # opens and reads in data files (few thousand lines each)
    with open("{0}/{1}".format(directory, fname), "r") as f:
        reader = csv.reader(f)
        i = 0
        data_position = []
        newPos = False
        for row in reader:
            if row == "/n":
                continue
            if row[0].startswith("X +"): # position row
                pos.append(row)
                newPos = True
            elif newPos:
                data.append(data_position)
                data_position = []
                data_position.append(row)
                newPos = False
            else:
                data_position.append(row)
            i+=1
    # data taken in between starting pa loop and first position is not useful
    del data[0]

    # dont want data taken between y movements
    data_out = []
    for i in range(len(pos)):
        if i % 2 == 0:
            data_out.append(data[i])

    return pos, data_out

# position data is of form 
# ['X +0000000', ' Y +0000000']
def stripPos(rawPos):
    positions = np.empty_like(rawPos)
    for i in range(len(rawPos)):
        for j in range(len(rawPos[i])):
            rawPos[i][j] = rawPos[i][j].replace(" ", "")
            positions[i][j] = rawPos[i][j][2:]

    positions = np.array(positions).astype(int)
    return positions


def generate_plot(directory, fname):
    ROOT.gROOT.SetBatch(ROOT.kTRUE)
    ROOT.gErrorIgnoreLevel = ROOT.kWarning

    pos, data = cleanFile(directory, fname)
    pos = stripPos(pos)/2000 # convert from motor units to cm

    pos_hist = ROOT.TH2D("pos_hist", "", 51, 0, 51, 51, 0, 51)
    current_hist = ROOT.TH1D("current_hist", "1d current hist", 50, -1.3, 0)

    bins = np.zeros(100*100)

    for i, row in enumerate(data):
        position_y = pos[2*i][1]
        x_0 = pos[2*i][0]
        x_1 = pos[2*i + 1][0]
        position_x = x_0 
        dx = (x_1 - x_0) / len(row)
        for j, point in enumerate(row):
            position_x += dx
            if -1 * float(point[3]) < 1.0 and -1 * float(point[3]) > 0:
                bin_number = pos_hist.Fill(position_x, position_y, -1*float(point[3]))
                bins[bin_number - 1] += 1
            current_hist.Fill(float(point[3]))

    for i, n in enumerate(bins):
        if n > 0:
            pos_hist.SetBinContent(i+1, pos_hist.GetBinContent(i+1) / n)


    l, r, t, b = 0.05, 0.05, 0.05, 0.05

    canvas = ROOT.TCanvas("c1", "c1", 500, 500)

    pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1.0, 1.0)
    pad2 = ROOT.TPad("pad2", "pad2", 0, 0.0, 1.0, 0.3)
    pad1.Draw()
    pad1.SetLeftMargin(l)
    pad1.SetRightMargin(r+0.05)
    pad1.SetTopMargin(t)
    pad1.SetBottomMargin(b)
    pad1.cd()
    pos_hist.SetStats(0)
    pos_hist.Draw("COLZ")
    canvas.cd()

    pad2.Draw()
    pad2.SetLeftMargin(l)
    pad2.SetRightMargin(r)
    pad2.SetTopMargin(t)
    pad2.SetBottomMargin(b)
    pad2.cd()
    current_hist.Draw()

    canvas.SaveAs(".tmp/SBU14_July1.gif")

if __name__ == "__main__":

    generate_plot("/home/mollergem/MOLLER_xray_gui/scans/SBU14", "combined")