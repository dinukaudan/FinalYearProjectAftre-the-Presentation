from ui import MainApp
from utils import utils

########################################
# entry point of the program
########################################

utils.create_folder_if_not_exist('./outputs')
utils.create_folder_if_not_exist('./repos')
utils.create_folder_if_not_exist('./settings')

app = MainApp()
app.mainloop()
