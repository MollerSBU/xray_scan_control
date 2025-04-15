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

    # when reading in files real time, we dont want points that havent finished taking data
    # only way to do this is to count lines, and break if we get too close 
    # faster to just run wc than to read file, count lines, then read it again
    lc = subprocess.run("wc -l {}/{}".format(directory, fname), 
                      shell=True, stdout = subprocess.PIPE)
    
    # example output is b'656 2024-11-05_20:45\n'
    n_lines = int(str(lc.stdout).strip("\'b\\n").split()[0])

    # opens and reads in data files (few thousand lines each)
    with open("{0}/{1}".format(directory, fname), "r+") as f:
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

    # # splits data into 
    # split_data = np.array([data[x:x+nPoints] for x in range(0, len(data), nPoints)]).astype(float)
    # averaged = np.empty(len(split_data))
    # sigma = np.empty(len(split_data))

    # for i in range(len(split_data)):
    #     averaged[i] = np.median(split_data[i], axis=0)[pa_channel]
    #     dat = np.array(split_data[i]).T[pa_channel]
    #     sigma[i] = np.std(dat[np.abs(dat - averaged[i]) < 3])

    # return pos, averaged, sigma

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

    #print(pos)

    pos_hist = ROOT.TH2D("pos_hist", "", 51, 0, 51, 51, 0, 51)
    current_hist = ROOT.TH1D("current_hist", "1d current hist", 50, -1.3, 0)

    # [['X +0000000', ' Y +0000000'], ['X +0101000', ' Y +0000000'], ['X +0101000', ' Y +0005000'], ['X +0000004', ' Y +0005000'], ['X +0000004', ' Y +0010000'], ['X +0101000', ' Y +0010000'], ['X +0101000', ' Y +0015000'], ['X +0001655', ' Y +0015000'], ['X +0001655', ' Y +0020000'], ['X +0098902', ' Y +0020000']]

    #print(pos)

    bins = np.zeros(100*100)

    for i, row in enumerate(data):
        position_y = pos[2*i][1]
        x_0 = pos[2*i][0]
        x_1 = pos[2*i + 1][0]
        position_x = x_0 
        dx = (x_1 - x_0) / len(row)
        for j, point in enumerate(row):
            position_x += dx

            # if x_1 > x_0:
            # else:
            #     position_x -= dx
            #binx, biny = pos_hist.GetXaxis().FindBin(position_x), pos_hist.GetYaxis().FindBin(position_y)
            #bin = pos_hist.GetBin(binx, biny, 0)
            #if -1 * float(point[3]) > 0:
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

    # circle1 = ROOT.TEllipse(1, 10.16, 1, 1)
    # circle2 = ROOT.TEllipse(3, 19.05, 1, 1)
    # circle3 = ROOT.TEllipse(5, 27.94, 1, 1)
    # circle4 = ROOT.TEllipse(9.5, 46.36, 1, 1)

    # circle5 = ROOT.TEllipse(49.5, 10.16, 1, 1)
    # circle6 = ROOT.TEllipse(47.5, 19.05, 1, 1)
    # circle7 = ROOT.TEllipse(45.5, 27.94, 1, 1)
    # circle8 = ROOT.TEllipse(41, 46.36, 1, 1)

    pad1.Draw()
    pad1.SetLeftMargin(l)
    pad1.SetRightMargin(r+0.05)
    pad1.SetTopMargin(t)
    pad1.SetBottomMargin(b)
    pad1.cd()
    #pad1.SetLogz()
    pos_hist.SetStats(0)
    pos_hist.Draw("COLZ")


    # circle1.SetLineColor(ROOT.kRed)
    # circle1.SetLineWidth(3)
    # circle1.SetFillColorAlpha(ROOT.kRed, 0)
    # circle1.Draw("same")

    # circle2.SetLineColor(ROOT.kRed)
    # circle2.SetLineWidth(3)
    # circle2.SetFillColorAlpha(ROOT.kRed, 0)
    # circle2.Draw("same")

    # circle3.SetLineColor(ROOT.kRed)
    # circle3.SetLineWidth(3)
    # circle3.SetFillColorAlpha(ROOT.kRed, 0)
    # circle3.Draw("same")

    # circle4.SetLineColor(ROOT.kRed)
    # circle4.SetLineWidth(3)
    # circle4.SetFillColorAlpha(ROOT.kRed, 0)
    # circle4.Draw("same")

    # circle5.SetLineColor(ROOT.kBlue)
    # circle5.SetLineWidth(3)
    # circle5.SetFillColorAlpha(ROOT.kRed, 0)
    # circle5.Draw("same")

    # circle6.SetLineColor(ROOT.kBlue)
    # circle6.SetLineWidth(3)
    # circle6.SetFillColorAlpha(ROOT.kRed, 0)
    # circle6.Draw("same")

    # circle7.SetLineColor(ROOT.kBlue)
    # circle7.SetLineWidth(3)
    # circle7.SetFillColorAlpha(ROOT.kRed, 0)
    # circle7.Draw("same")

    # circle8.SetLineColor(ROOT.kBlue)
    # circle8.SetLineWidth(3)
    # circle8.SetFillColorAlpha(ROOT.kRed, 0)
    # circle8.Draw("same")
    canvas.cd()

    pad2.Draw()
    pad2.SetLeftMargin(l)
    pad2.SetRightMargin(r)
    pad2.SetTopMargin(t)
    pad2.SetBottomMargin(b)
    pad2.cd()
    current_hist.Draw()

    canvas.SaveAs("/home/mollergem/MOLLER_xray_gui/scan_control/.tmp/test.gif")

if __name__ == "__main__":
    #dir = sys.argv[1]

    #generate_plot("/home/mollergem/MOLLER_xray_gui/scans/SBU04", "2025-03-11_16:14")

    generate_plot("/home/mollergem/MOLLER_xray_gui/scans/prototype2", "prototype2_2025-04-10-1602")
    #generate_plot("/home/mollergem/MOLLER_xray_gui/scans/test", "test_continuous.txt")

    pass