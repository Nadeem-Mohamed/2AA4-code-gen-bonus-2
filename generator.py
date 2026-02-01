#https://stackoverflow.com/questions/3106480/really-simple-way-to-deal-with-xml-in-python reference used
#to process xml files


import xml.etree.ElementTree as ET
import os

MODEL_PATH = "model/diagram.xml"
OUT_PATH = "src-gen"

tree = ET.parse(MODEL_PATH)
root = tree.getroot()

entities = {}
relations = []

for cell in root.iter("mxCell"):
    if cell.get("vertex") == "1" and cell.get("value"):
        parent = cell.get("parent", "")
        if parent != "1":
            continue
        entities[cell.get("id")] = cell.get("value")

for cell in root.iter("mxCell"):
    if cell.get("edge") == "1":
        src = cell.get("source")
        tgt = cell.get("target")
        label = cell.get("value", "")
        relations.append((src, tgt, label))

os.makedirs(OUT_PATH, exist_ok=True)

for eid, name in entities.items():
    filename = os.path.join(OUT_PATH, f"{name}.java")
    with open(filename, "w") as f:
        f.write(f"public class {name} {{\n")

        for src, tgt, label in relations:
            if src == eid and tgt in entities:
                target_name = entities[tgt]

                if "(N)" in label:
                    rel_name = label.split()[0]
                    f.write(f"    private java.util.List<{target_name}> {rel_name};\n")
                else:
                    rel_name = label.split()[0] if label else target_name.lower()
                    f.write(f"    private {target_name} {rel_name};\n")

        f.write("}\n")

print("Generation complete.")