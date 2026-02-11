import xml.etree.ElementTree as ET
import os
import argparse

def parse_model(model_path):
    tree = ET.parse(model_path)
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
            if src in entities and tgt in entities:
                relations.append((src, tgt, label))
    
    return entities, relations

def generate_java(entities, relations, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for eid, name in entities.items():
        filename = os.path.join(output_dir, f"{name}.java")
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
    print(f"Generated Java code in {output_dir}")

def generate_python(entities, relations, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for eid, name in entities.items():
        filename = os.path.join(output_dir, f"{name}.py")
        with open(filename, "w") as f:
            f.write(f"class {name}:\n")
            f.write("    def __init__(self):\n")
            
            has_relations = False
            for src, tgt, label in relations:
                if src == eid and tgt in entities:
                    has_relations = True
                    target_name = entities[tgt]
                    if "(N)" in label:
                        rel_name = label.split()[0]
                        f.write(f"        self.{rel_name} = []\n")
                    else:
                        rel_name = label.split()[0] if label else target_name.lower()
                        f.write(f"        self.{rel_name} = None\n")
            
            if not has_relations:
                f.write("        pass\n")
    print(f"Generated Python code in {output_dir}")

def main():
    parser = argparse.ArgumentParser(description="Generate code from XML model")
    parser.add_argument("--model", required=True, help="Path to the XML model file")
    parser.add_argument("--output", required=True, help="Base path for output")
    args = parser.parse_args()

    entities, relations = parse_model(args.model)
    
    java_out = os.path.join(args.output, "java")
    python_out = os.path.join(args.output, "python")
    
    generate_java(entities, relations, java_out)
    generate_python(entities, relations, python_out)

if __name__ == "__main__":
    main()