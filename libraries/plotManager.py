import matplotlib as mpl;
import matplotlib.pyplot as plt
class plotRenderingController():
    def renderHsig(self, arrUnDat):
        for arr in arrUnDat[1:]:
            plt.figure(1, figsize=(5, 5))
            #plt.subplots_adjust(left=0.1, bottom=0.1, wspace=0.8, hspace=0.5)
            plt.plot(arrUnDat[0][3], arr[3], 'ro', ms=2)
            plt.xlim(0, 1.5)
            plt.ylim(0, 1.5)
            plt.show()