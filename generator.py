import xml.etree.ElementTree as ET
import os
import argparse
import re

def parse_model(model_path):
    tree = ET.parse(model_path)
    root = tree.getroot()

    entities = {}
    inheritance_map = {} 
    relations = []
    edge_labels = {}
    
    for cell in root.iter("mxCell"):
        if cell.get("vertex") == "1" and cell.get("value"):
            parent = cell.get("parent", "")
            if parent == "1" or parent == "0": 
                val = cell.get("value", "").strip()
                if val:
                    val = val.replace("&nbsp;", " ").replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
                    val = re.sub(r'<[^>]+>', '', val)
                    val = re.sub(r'<<[^>]+>>', '', val)
                    val = re.sub(r'[^a-zA-Z0-9_]', '', val)
                    
                    if val:
                        entities[cell.get("id")] = val
        
        parent = cell.get("parent", "")
        if parent and parent != "1" and parent != "0":
             val = cell.get("value", "").strip()
             if val:
                 if parent not in edge_labels:
                     edge_labels[parent] = val

    for cell in root.iter("mxCell"):
        if cell.get("edge") == "1":
            edge_id = cell.get("id")
            src = cell.get("source")
            tgt = cell.get("target")
            
            label = cell.get("value", "").strip()
            if not label and edge_id in edge_labels:
                label = edge_labels[edge_id]
            
            style = cell.get("style", "")
            
            if not src or not tgt:
                if label:
                    print(f"WARNING: Edge with label '{label}' is not connected to a source or target. Check your diagram.")
                continue
                
            if src not in entities or tgt not in entities:
                if label:
                     print(f"WARNING: Edge with label '{label}' connects to unknown entities (ids: {src} -> {tgt}).")
                continue

            is_inheritance = False
            if "endArrow=block" in style and "endFill=0" in style:
                is_inheritance = True
            
            if is_inheritance:
                parent_id = tgt
                child_id = src
                if parent_id not in inheritance_map:
                    inheritance_map[parent_id] = []
                inheritance_map[parent_id].append(child_id)
            else:
                is_list = False
                field_name = label
                
                if "(N)" in label:
                    is_list = True
                    field_name = label.replace("(N)", "").strip()
                elif "(1)" in label:
                    is_list = False
                    field_name = label.replace("(1)", "").strip()
                
                if not field_name or field_name.lower() in ["has", "contains", "receives", "stocks", "manages", "offers", "teaches", "enrolls", "submits", "requires", "results_in", "joins", "hosts", "employs"]:
                    target_cls = entities[tgt]
                    base_name = target_cls[0].lower() + target_cls[1:]
                    
                    if field_name:
                         field_name = field_name + target_cls
                    else:
                        field_name = base_name

                field_name = re.sub(r'[^a-zA-Z0-9_]', '', field_name)
                
                relations.append({
                    "source": src,
                    "target": tgt,
                    "name": field_name,
                    "is_list": is_list
                })
    
    return entities, inheritance_map, relations

def generate_java(entities, inheritance_map, relations, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    child_to_parent = {}
    for p_id, children in inheritance_map.items():
        for c_id in children:
            child_to_parent[c_id] = p_id

    class_fields = {}
    
    for r in relations:
        src = r["source"]
        if src not in class_fields:
            class_fields[src] = []
        
        existing_names = [f["name"] for f in class_fields[src]]
        original_name = r["name"]
        final_name = original_name
        
        if final_name in existing_names:
            target_cls = entities[r["target"]]
            if not final_name.endswith(target_cls):
                final_name = final_name + target_cls
        
        idx = 2
        while final_name in existing_names:
            final_name = f"{original_name}{idx}"
            idx += 1
            
        r["name"] = final_name
        class_fields[src].append(r)

    for eid, name in entities.items():
        filename = os.path.join(output_dir, f"{name}.java")
        with open(filename, "w") as f:
            has_list = False
            if eid in class_fields:
                for field in class_fields[eid]:
                    if field["is_list"]:
                        has_list = True
                        break
            
            if has_list:
                f.write("import java.util.List;\n\n")

            extends_clause = ""
            if eid in child_to_parent:
                parent_id = child_to_parent[eid]
                if parent_id in entities:
                    extends_clause = f" extends {entities[parent_id]}"
            
            f.write(f"public class {name}{extends_clause} {{\n")
            
            if eid in class_fields:
                for field in class_fields[eid]:
                    tgt_id = field["target"]
                    if tgt_id in entities:
                        target_name = entities[tgt_id]
                        field_name = field["name"]
                        if field["is_list"]:
                            f.write(f"    private List<{target_name}> {field_name};\n")
                        else:
                            f.write(f"    private {target_name} {field_name};\n")
            
            f.write("}\n")
    print(f"Generated Java code in {output_dir}")

def main():
    parser = argparse.ArgumentParser(description="Generate Java code from XML model")
    parser.add_argument("--model", required=True, help="Path to the XML model file")
    parser.add_argument("--output", required=True, help="Base path for output")
    args = parser.parse_args()

    entities, inheritance_map, relations = parse_model(args.model)
    
    java_out = os.path.join(args.output, "java")
    
    generate_java(entities, inheritance_map, relations, java_out)

if __name__ == "__main__":
    main()