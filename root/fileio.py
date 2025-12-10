import json
import os
from typing import Iterable, Union

import ROOT


def write_metadata(
    metadata: dict,
    fout: Union[ROOT.TFile, str],
    directory: str = "",
    close_file: bool = True
):
    if isinstance(fout, str):
        if os.path.exists(fout):
            fout = ROOT.TFile(fout, "update")
        else:
            fout = ROOT.TFile(fout, "recreate")

    metadata_name = metadata.get("name", "metadata")
    json_str = json.dumps(metadata)
    root_str = ROOT.TObjString(json_str)

    if directory:
        current_dir = fout.GetDirectory(directory)
        if not current_dir:
            current_dir = fout.mkdir(directory)
    else:
        current_dir = fout

    current_dir.cd()
    root_str.Write(metadata_name)
    if close_file:
        fout.Close()




def save_to_root(
    *objects,
    fout: Union[ROOT.TFile, str],
    directory: str = "",
    print_filename: bool = True,
    nested: bool = False,
    overwrite: bool = False,
    metadata: Union[dict, None] = None
):
    if isinstance(fout, str):
        if overwrite:
            fout = ROOT.TFile(fout, "recreate")
        else:
            if os.path.exists(fout):
                fout = ROOT.TFile(fout, "update")
            else:
                fout = ROOT.TFile(fout, "recreate")

    if metadata is not None:
        write_metadata(metadata, fout, directory, close_file=False)


    def recursive_save(obj, current_dir, path=""):
        if isinstance(obj, ROOT.TObject):
            current_dir.cd()
            obj.Write()

        elif isinstance(obj, dict):
            for sub_key, sub_obj in obj.items():
                if not nested:
                    recursive_save(sub_obj, current_dir, path)
                else:
                    sub_key_str = str(sub_key)
                    sub_dir_path = f"{path}/{sub_key_str}" if path else sub_key_str

                    if not current_dir.GetDirectory(sub_key_str):
                        current_dir.mkdir(sub_key_str)

                    sub_dir = current_dir.GetDirectory(sub_key_str)
                    recursive_save(sub_obj, sub_dir, sub_dir_path)

        elif isinstance(obj, Iterable) and not isinstance(obj, (str, bytes)):
            for sub_obj in obj:
                recursive_save(sub_obj, current_dir, path)

        else:
            raise ValueError(f"Unsupported object type: {type(obj)}")

    if not fout.GetDirectory(directory) and directory:
        fout.mkdir(directory)

    current_dir = fout.GetDirectory(directory) if directory else fout
    for obj in objects:
        recursive_save(obj, current_dir)

    if print_filename:
        print(f"Output file: {fout.GetName()}")

    fout.cd()
