import os

walk_dir = os.getcwd()

color_type = "Color"
image_type = "Image"
other_type = "other"


def enum_var_def(asset_type):
    if asset_type == color_type:
        return "color:UIColor"
    elif asset_type == image_type:
        return "image:UIImage"
    else:
        return ""


def enum_var_return(asset_ype):
    if asset_ype == color_type:
        return "UIColor(named:self.rawValue)"
    elif asset_ype == image_type:
        return "UIImage(named:self.rawValue)"
    else:
        return ""


def walk_directory(directory):
    subdirs = next(os.walk(directory))[1]
    for subdir in subdirs:
        if subdir[0] != ".":
            new_dir = directory + '/' + subdir
            if subdir.endswith('.xcassets'):
                create_assets_enum(new_dir)
            else:

                walk_directory(new_dir)


def write_case(asset_name, write_file):
    if ' ' in asset_name:
        original_asset_name = asset_name
        asset_name = asset_name.replace(" ", "_")
        write_file.write("\tcase " + asset_name + " = \"" + original_asset_name + "\"\n")
    else:
        write_file.write("\tcase " + asset_name + "\n")


def write_new_color_variable(asset_name, extension_file):
    original_asset_name = asset_name
    asset_name = asset_name.replace(" ", "_")
    extension_file.write("\tstatic var " + asset_name + " = UIColor(named:\"" + original_asset_name + "\")!\n")


def create_new_asset_enum_file(assets_name, asset_type, save_path):

    asset_folder_name = assets_name[:-9]

    enum_file_name = asset_type + asset_folder_name + ".swift"

    new_file = open(save_path + "/" + enum_file_name, 'w')
    new_file.write("//Enums for assets inside of " + assets_name + " directory\n")
    new_file.write("//Created by AssetEnumCreator.py\n")
    new_file.write("\n")
    new_file.write("import UIKit\n")
    new_file.write("\n")
    new_file.write("enum " + asset_type + asset_folder_name + ":String{\n")

    return new_file, enum_file_name


def create_new_color_extension(assets_name, save_path):
    asset_folder_name = assets_name[:-9]

    enum_file_name = asset_folder_name + "UIColorExtension.swift"

    new_file = open(save_path + "/" + enum_file_name, 'w')
    new_file.write("//UIColor Extension for colors inside of " + assets_name + " directory\n")
    new_file.write("//Created by AssetEnumCreator.py\n")
    new_file.write("\n")
    new_file.write("import UIKit\n")
    new_file.write("\n")
    new_file.write("extension UIColor{\n")

    return new_file, enum_file_name


def close_enum_file(file, filename, file_path, save_path, asset_type="other"):

    if asset_type != other_type:
        file.write("\n")
        file.write("\t var " + enum_var_def(asset_type) + "{\n")
        file.write("\t\tget{\n")
        file.write("\t\t\treturn " + enum_var_return(asset_type) + "!\n")
        file.write("\t\t}\n")
        file.write("\t}\n")
        file.write("}\n")
        file.close()
    else:
        file.write("}\n")
        file.close()

    os.rename(file_path + "/" + filename, save_path + "/" + filename)


def create_assets_enum(assets_dir):

    subdirs = next(os.walk(assets_dir))[1]
    save_path, assets_name = os.path.split(assets_dir)
    temp_path = "/tmp/"
    image_asset_file, image_asset_filename = create_new_asset_enum_file(assets_name, image_type, temp_path)
    color_asset_file, color_asset_filename = create_new_asset_enum_file(assets_name, color_type, temp_path)
    color_extension_file, extension_filename = create_new_color_extension(assets_name, temp_path)

    for subdir in subdirs:
        if subdir.endswith(".imageset"):
            image_asset_name = subdir[:-9]
            write_case(image_asset_name, image_asset_file)
        if subdir.endswith(".colorset"):
            color_asset_name = subdir[:-9]
            write_case(color_asset_name, color_asset_file)
            write_new_color_variable(color_asset_name, color_extension_file)

    close_enum_file(image_asset_file, image_asset_filename, temp_path, save_path, image_type)
    close_enum_file(color_asset_file, color_asset_filename, temp_path, save_path, color_type)
    close_enum_file(color_extension_file, extension_filename, temp_path, save_path)


walk_directory(walk_dir)
