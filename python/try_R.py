# references:
# graphics http://rpy.sourceforge.net/rpy2/doc-dev/html/graphics.html
# bupaR using SVG animations.https://github.com/bupaverse/processanimateR
# Unleash the value of PROCESS MINING https://towardsdatascience.com/unleash-the-value-of-process-mining-4e3b5af4e9d8
# https://www.win.tue.nl/bpi/dorky.php?id=2012:challenge
# https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0207806

import rpy2.robjects.packages as rpackages
utils = rpackages.importr('utils')
utils.chooseCRANmirror(ind=1) # select the first mirror in the list

packnames = ('bupaR', 'eventdataR','edeaR','processmapR','processmonitR','xesreadR','petrinetR')
from rpy2.robjects.vectors import StrVector
utils.install_packages(StrVector(packnames))


from rpy2.robjects.packages import importr, data
eventdataR = importr('eventdataR')
patients = data(eventdataR).fetch('patients')['patients'] #fetch dataset from library

process_map = importr("processmapR")
pm = process_map.process_map(patients)


# from rpy2.interactive import process_revents
# process_revents.start()
# grdevices = importr('grDevices')
# grdevices.png(file="file.png", width=512, height=512)
# rpy2.rinterface.NULL
# pm

import os

os.path.dirname(os.path.abspath('file.png'))
#'C:\\Windows\\system32'


from rpy2 import robjects
rprint = robjects.globalenv.get("print")
rprint(pm)


# grdevices.png(file="file.png", width=512, height=512)
# rprint(pm)
# grdevices.dev_off()



# from rpy2.robjects.lib import grid
# process_revents.start()
# grdevices.png(file="file.png", width=512, height=512)
# grid.activate()
# pmm = pm
# rprint(pmm)
# grdevices.dev_off()
