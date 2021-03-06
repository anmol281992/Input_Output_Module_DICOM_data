import dicom
import os
import sys
import numpy as np
from tkinter import *
from tkinter import filedialog

# Inorder to run the module "pydicom" module is required.

def import_dicom_folder(folder):
    '''
    Imports all the Dicom Images in a folder and arranges the images along the z-axis based on the INSTANCE NUMBER of the image.
        Argument:
             folder: The name of folder  containing a Dicom Images.
        returns:
             Image_list: A 3D numpy array which stores the  pixel data of dicom images arranged in the ascending order of its INSTANCE NUMBER .
             dicom_data_list: When we import dicom images from "folder" they are stored in a dicom_data_list in its original format. The dicom data_list is arranged based on image's INSTANCE NUMBER .
    '''
    try:
        file_list = [file for file in os.listdir(folder) if file.endswith('.dcm') and os.path.isfile(os.path.join(folder,file))]
    except FileNotFoundError:
        print("Folder Does Not exist, Load correct folder")
        return 0
    else:
        if len(file_list) == 0:
            print('No .dcm files in the folder')
            return 0
        else:
            Instance_index = []
            Image_list = {}
            dicom_data_list = {}
            for count, file in enumerate(file_list):
                    try:
                        a = dicom.read_file(os.path.join(folder, file))
                    except:
                        print("Error loading the dcm file" + folder + ": skipping to next file")
                    else:
                        Instance_index.append(int(a.InstanceNumber))
                        dicom_data_list[int(a.InstanceNumber)] = a
                        Image_list[int(a.InstanceNumber)] = a.pixel_array

            Instance_index.sort()
            dicom_data_list = [dicom_data_list[instance] for instance in Instance_index]
            Image_list = np.array([Image_list[instance] for instance in Instance_index])
            return Image_list.transpose(1, 2, 0), dicom_data_list

def export_dicom_folder(folder_name, mask_matrix, dicom_data_list):
    '''

    :param folder_name: Defines the path of the folder in which we will store the masks of the Proximal Femur
    :param mask_matrix: It is numpy array which stores the mask corresponding to each dicom image arranged based on the INSTANCE NUMBER of the Image
    :param dicom_data_list: Same as defined in import_dicom_folder
    :return:
    '''

    for count, k in enumerate(dicom_data_list):
        name_file = folder_name.split('/')[-1] + '_' + str(k.SOPInstanceUID) + str(k.InstanceNumber) + 'mask.dcm'
        Out = dicom.dataset.Dataset(k)
        Out = dicom.dataset.FileDataset(name_file, Out)
        Out.pixel_array = mask_matrix[:, :, count]
        Out.file_meta = k.file_meta
        dicom.write_file(os.path.join(folder_name, name_file), Out)
    return

class GUI(Frame):
    '''
     Generates the GUI for import_export_module.
    '''

    def __init__(self,master = None):
        Frame.__init__(self, master)
        self.GUI_frame = master
        self.image_list = np.array([])
        self.dicom_data_list = []
        self.frame_Buttons = Frame(master,)
        self.Upper_dialog(self.frame_Buttons)
        self.Segmentation_dialog(self.frame_Buttons)
        self.Lower_dialog(self.frame_Buttons)
        self.frame_info_box = Frame(master)
        self.info_box(self.frame_info_box)
        self.frame_Buttons.pack(side=TOP, ipady=3)
        self.frame_info_box.pack(side=TOP, ipady=3)
        self.GUI_frame.mainloop()


    def info_box(self, master):
        self.var = StringVar()
        self.text_box = Entry(master, textvariable=self.var, width = 25)
        self.text_box.pack(side= LEFT, ipady=3)


    def segmentation(self):
        try:
            self.var.set("Segmenting ......")
            self.mask_matrix = self.image_list  # Replace this line with tensorflow graph to generate the masks.
            self.var.set("Segmentation complete")
        except:
            self.var.set("Unable to segment")

    def Segmentation_dialog(self,master):
        sub_frame = master
        self.seg_button = Button(sub_frame, text="Segment", command=self.segmentation)
        self.seg_button.pack(side= LEFT, ipady=3)

        return

    def Upper_dialog(self,master):
        sub_frame = master
        self.folder = "C:/"
        self.Entry_button_left = Button(sub_frame, text="Import Dicom", command=self.button_pressed_load_data)
        self.Entry_button_left.pack(side=LEFT, ipady=3)

        return

    def Lower_dialog(self,master):
        sub_frame = master
        self.Entry_button_right = Button(sub_frame, text="Export Dicom", command=self.button_pressed_export_mask)
        self.Entry_button_right.pack(side=LEFT, ipady=3)
        return

    def button_pressed_load_data(self):
        self.var.set("Importing ..... ")
        self.folder = filedialog.askdirectory(initialdir="/", title="Select Folder")
        try:
            self.image_list, self.dicom_data_list = import_dicom_folder(self.folder)
            self.var.set("Import Successfull")
        except:
            self.var.set("Unable to import from folder")

        if not self.image_list.any():
            self.var.set("Empty image list")
        return

    def button_pressed_export_mask(self):
        if not self.image_list.any():
            self.var.set("Empty Image List")
        else:
            self.var.set("Exporting .....")
            parent_path = os.path.split(self.folder)[0]
            self.folder_export = filedialog.askdirectory(initialdir= parent_path, title="Export Dicom Folder")
            try:
                if self.folder_export == parent_path:
                    self.var.set("Please select folder")
                else:
                    export_dicom_folder(self.folder_export, self.mask_matrix, self.dicom_data_list)
                    self.var.set("Export Successfull")
            except:
                self.var.set("Export Unsucessfull")
        return


if __name__ == '__main__':
    root = Tk()
    gui = GUI(master= root)
    root.mainloop()

    #string = generating_GUI()
    #print(string)




