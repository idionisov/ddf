from ROOT import TObject, TH1, TH2, TFile
from collections.abc import Iterable



def save_to_root(*objects,
    tfile:          TFile | str = "",
    tdir_path:      str         = "",
    print_filename: bool        = True
):
    """
    Recursively save all TObject derived objects in a nested dictionary to a specific TDirectory in a TFile.

    Parameters:
    - objects: Dictionary (possibly nested) of objects that inherit from TObject or the TObjects themselves.
    - tfile (ROOT.TFile or /path/to/new_root_file.root): ROOT file where objects will be saved.
    - tdir_path (str): Path of the TDirectory in the TFile where objects will be saved.
    """

    if not tfile:
        tfile = TFile(tfile, "recreate")

    if not tfile.GetDirectory(tdir_path):
        tfile.mkdir(tdir_path)

    for obj in objects:
        if isinstance(obj, TObject):
            tfile.cd(tdir_path)
            obj.Write()

        elif isinstance(obj, dict):
            for i_obj in obj.values():
                save_to_root(i_obj, tfile=tfile, tdir_path=tdir_path, print_filename=False)
        
        elif isinstance(obj, Iterable):
            for i_obj in obj:
                save_to_root(i_obj, tfile=tfile, tdir_path=tdir_path, print_filename=False)

        else:
            raise ValueError(f"{type(obj)} is neither a TObject nor a viable container.")
    
    if print_filename:
        print(f"Output file: {tfile.GetName()}")

    tfile.cd()



def save_dict_to_root(*obj_dicts,
    tfile:      TFile,
    tdir_path:  str = ""
):
    """
    Recursively save all TObject derived objects in a nested dictionary to a specific TDirectory in a TFile.

    Parameters:
    - obj_dict (dict): Dictionary (possibly nested) with objects that inherit from TObject.
    - tfile (ROOT.TFile): ROOT file where objects will be saved.
    - tdir_path (str): Path of the TDirectory in the TFile where objects will be saved.
    """
    
    def save_recursively(current_dict, current_dir):
        """
        Helper function to recursively save objects in the dictionary to the current directory.
        """
        for key, value in current_dict.items():
            if isinstance(value, TObject):
                current_dir.cd()
                value.Write()
            elif isinstance(value, dict):
                save_recursively(value, current_dir)
            

    for obj_dict in obj_dicts:
        if not isinstance(obj_dict, dict):
            raise ValueError("Cannot save objects that are not stored in a dictionary!")
        
        if not tfile.GetDirectory(tdir_path):
            tfile.mkdir(tdir_path)

        dir = tfile.GetDirectory(tdir_path)
        save_recursively(obj_dict, dir)
        tfile.cd()


def print_dict_all(obj):
    
    msg: str = obj.GetName()
    if isinstance(obj, TH1) or isinstance(obj, TH2):
        msg = f"{msg}   Entries: {int(obj.GetEntries())}   Integral: {obj.Integral():.03f}"
    
    elif isinstance(obj, dict):
        for obj_i in obj.values():
            print_dict_all(obj_i)
    
    elif isinstance(obj, Iterable):
        for obj_i in obj:
            print_dict_all(obj_i)
    
    else: raise ValueError(f"{type(obj)} is neither a histogram nor a dict nor a tuple.")

    msg = f"{msg}   {type(obj)}"
    print(msg)