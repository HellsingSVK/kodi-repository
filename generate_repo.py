import os
import hashlib
import zipfile
import xml.etree.ElementTree as ET

ADDONS_DIR = "addons"
OUTPUT_DIR = "zips"

def build_repository():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    addons_xml = ET.Element("addons")

    for addon_name in os.listdir(ADDONS_DIR):
        addon_path = os.path.join(ADDONS_DIR, addon_name)
        xml_file = os.path.join(addon_path, "addon.xml")

        if not os.path.isdir(addon_path) or not os.path.exists(xml_file):
            continue

        tree = ET.parse(xml_file)
        root = tree.getroot()
        addons_xml.append(root)

        addon_id = root.attrib.get("id")
        version = root.attrib.get("version")

        addon_zip_dir = os.path.join(OUTPUT_DIR, addon_id)
        if not os.path.exists(addon_zip_dir):
            os.makedirs(addon_zip_dir)

        zip_filename = f"{addon_id}-{version}.zip"
        zip_filepath = os.path.join(addon_zip_dir, zip_filename)

        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root_folder, _, files in os.walk(addon_path):
                for file in files:
                    full_path = os.path.join(root_folder, file)
                    rel_path = os.path.relpath(full_path, ADDONS_DIR)
                    zip_file.write(full_path, rel_path)

    addons_xml_path = os.path.join(OUTPUT_DIR, "addons.xml")
    tree = ET.ElementTree(addons_xml)
    tree.write(addons_xml_path, encoding="utf-8", xml_declaration=True)

    with open(addons_xml_path, "rb") as f:
        md5_hash = hashlib.md5(f.read()).hexdigest()

    with open(os.path.join(OUTPUT_DIR, "addons.xml.md5"), "w") as f:
        f.write(md5_hash)

if __name__ == "__main__":
    build_repository()