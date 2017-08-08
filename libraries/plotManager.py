import matplotlib as mpl;
import matplotlib.pyplot as plt
class plotRenderingController():
    def renderHsig(self, arrUnDat):
        for arr in arrUnDat[1:]:
            plt.figure(1, figsize=(5, 5))
            #plt.subplots_adjust(left=0.1, bottom=0.1, wspace=0.8, hspace=0.5)
            plt.plot(arrUnDat[0][3], arr[3], 'ro', ms=2)
            plt.xlim(0, 7)
            plt.ylim(0, 7)
            plt.show()


    def renderHsig1(self, arrUnDat):
        plt.figure(1, figsize=(5, 5))
        #plt.subplots_adjust(left=0.1, bottom=0.1, wspace=0.8, hspace=0.5)
        plt.plot(arrUnDat[1][3],arrUnDat[0][3],'ro', arrUnDat[2][3],arrUnDat[0][3],'ro', arrUnDat[3][3],arrUnDat[0][3], 'ro',arrUnDat[4][3],arrUnDat[0][3],'ro',arrUnDat[5][3],arrUnDat[0][3],'ro', ms=2,)
        plt.xlim(0, 7)
        plt.ylim(0, 7)
        plt.show()